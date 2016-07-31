#!/usr/local/bin/python

"""
Just the workings of some sort of data gatherer.
Looks like Bobby has already completed something like this, so just committed for record keeping purposes.
"""

import csv
from collections import Counter
import json
import geojson

# stuff to run always here such as class/def
def main():
    pass

if __name__ == "__main__":
	# stuff only to run when not called via 'import' here
	main()

# This class exists in case we have extra info about each feature.
# The extra info in the csv might contain information about where it is, what it's called, etc.
class Feature:
	def __init__(self, name, feature_id, lat, lon):
		self.name = name
		self.feature_id = feature_id
		self.lat = lat
		self.lon = lon

	def getDict(self):
		return {"name": self.name, "feature_id": self.feature_id, "lat": self.lat, "lon": self.lon}

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name


class Postcode:
	def __init__(self, postcode, name, state):
		self.postcode = int(postcode)
		self.name = name
		self.state = state

		# A list of Feature references.
		self.features = []

		# This is a counter of how many of each feature this postcode has
		self.featureQuantity = Counter()

		# Other characteristics e.g. crime, census data.
		self.characteristics = {}

	def addFeature(self, feature):
		self.features.append(feature)
		self.featureQuantity.update([feature.name])

	def addCharacteristic(self, key, value):
		self.characteristics[key] = value

	def getDict(self, includeFeatures=False):
		data = {}
		data["name"] = self.name
		data["state"] = self.state
		data["postcode"] = self.postcode

		if includeFeatures:
			feats = []
			for f in self.features:
				feats.append(f.getDict())
			data["features"] = feats

		data["characteristics"] = self.characteristics

		return data

	def createGeoJSON(self):
		# Some example geoJSON: http://openlayers.org/en/v3.17.1/examples/data/geojson/switzerland.geojson

		postcodeDict = self.getDict(includeFeatures=True)
		features = []

		# Getting the polygon boundary.
		target = str(self.postcode)
		# This data is form here: http://ec2-52-62-36-123.ap-southeast-2.compute.amazonaws.com/geoserver/wfs?service=wfs&version=1.0.0&request=getFeature&typeName=datavic:vmadmin_pc_centroid&outputFormat=JSON
		with open("postcodeMultipoint.geojson", "r") as f:
			data = json.load(f)
			for p in data["features"]:
				if p["properties"]["postcode"] == target:
					print(type(p['geometry']['coordinates'][0][0]))
					postcodePolygon = geojson.Feature(id="suburb", geometry=geojson.Polygon(p['geometry']['coordinates'][0][0]))

		features.append(postcodePolygon)

		# Getting FOIs.
		for feat in postcodeDict["features"]:
			point = geojson.Point((feat["lat"], feat["lon"]))
			# With the properties part we can specify more fields of each feature to include.
			geoFeature = geojson.Feature(geometry=point, id=feat["feature_id"], properties = {k: feat[k] for k in (['name'])})
			features.append(geoFeature)

		return geojson.FeatureCollection(features)

	# This includes geojson for the features and postcode boundaries as well as characteristics/basic info.
	def createFullDict(self):
		data = {}
		# Get geoJSON for the features (points) and suburb outline (polygon).
		data = self.createGeoJSON()
		# Get additional facts (census data, crime, name of suburb, etc.).
		data["facts"] = self.getDict(includeFeatures=False)

		return data

	def __str__(self):
		return "{} - {}\nFeatures\n    {}\nCharacteristics\n    {}".format(self.postcode, self.name, self.features, self.characteristics)

	def __repr__(self):
		return "{} - {}\nFeatures\n    {}\nCharacteristics\n    {}".format(self.postcode, self.name, self.features, self.characteristics)


def readPostcodeData():
	""" Returns a dict of postcode -> Postcode object entries """

	postcodes = {}

	# Create a Postcode object for each postcode.
	with open('suburbnames.csv','r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			postcode = int(row["POA_CODE_2011"])
			name = row["SSC_NAME_2011"] # Name of suburb
			# Getting rid of the (Vic.) at the end of some suburb names.
			if name.split()[-1] == "(Vic.)":
				name = " ".join(name.split()[:-1])
			state = row["STATE_NAME_2011"]

			postcodes[postcode] = Postcode(postcode, name, state)

	# Read crime data.
	with open('crime.csv', 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			postcode = int(row["Postcode"])
			crimeData = int(row["Apr 2015 - Mar 2016"])
			if postcode in postcodes:
				postcodes[postcode].addCharacteristic("Crime", crimeData)


	# Read census data.
	with open('census.csv', 'r') as f:
		reader = csv.reader(f)
		reader.next()
		for row in reader:
			postcode = int(row[0][3:])
			if postcode in postcodes:
				postcodes[postcode].addCharacteristic("medianAge", int(row[1]))
				postcodes[postcode].addCharacteristic("medianMortgage", int(row[2]))
				postcodes[postcode].addCharacteristic("medianSalary", int(row[3]))
				postcodes[postcode].addCharacteristic("medianRent", float(row[4]))
				postcodes[postcode].addCharacteristic("familySalary", int(row[5]))
				postcodes[postcode].addCharacteristic("averagePersons", float(row[7]))


	# Read FOI data.
	with open("foi2.csv", "r") as f:
		reader = csv.DictReader(f)

		for foi in reader:
			name = foi["feature_subtype"]
			postcode = int(foi["postcode"])
			feature_id = foi["feature_id"]
			coords = foi["geom_text"].split(",")[-1][11:-1].split()
			try:
				lat, lon = map(float, coords)
			except ValueError:
				# Some values don't have both coords.
				lat, lon = None, None

			# Could read additional fields for each feature. Location info?

			feature = Feature(name, feature_id, lat, lon)

			if postcode in postcodes:
				postcodes[postcode].addFeature(feature)

	# Read house price data.
	with open("houses-by-suburb-Dec-qtr.csv", "r") as f:
		reader = csv.DictReader(f)

		# Suburb name -> Data for that suburb.
		houseData = {}

		for row in reader:
			suburb = row["SUBURB"].lower()
			data = {"Oct - Dec 14": row["Oct - Dec 14"], "Jan - Mar 15": row["Jan - Mar 15"], "Apr - Jun 15": row["Apr - Jun 15"], "Jul - Sep 15": row["Jul - Sep 15"], "Oct - Dec 15": row["Oct - Dec 15"]}
			houseData[suburb] = data

		# Iterate through each postcode and check if we have that postcode name in our postcodes dict.
		for p in postcodes:
			postcodeName = postcodes[p].name.lower()
			if postcodeName in houseData:
				postcodes[p].addCharacteristic("House Data - Single Family / Semi Detached", houseData[postcodeName])

	return postcodes



"""
for i in postcodes:
	try:
		print(i, postcodes[i].characteristics["House Data - Single Family / Semi Detached"])
	except KeyError:
		pass
"""
"""
for i in postcodes:
	print(postcodes[i])
	print
"""

"""
def getData(targetFile):

	postcodeFeatures = {}

	with open(targetFile, "r") as f:
		reader = csv.DictReader(f)

		# Building the "database".
		# This is a dict of entries like: postcode -> Counter
		# The Counter for each postcode maintains a list of how many of a feature there are there.

		for foi in reader:
			feature = foi["feature_subtype"]
			postcode = int(foi["postcode"])
			# If this postcode already exists, update the counter of FOIs.
			try:
				postcodeFeatures[postcode].update([feature])
			# Otherwise make a new entry in the dict with the key as the postcode.
			# Initialise a new Counter for this entry with the feature in question.
			except:
				postcodeFeatures[postcode] = Counter([feature])

	return postcodeFeatures

blah = getData(target)


print(blah[3072])
"""

