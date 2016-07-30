#!/usr/local/bin/python3

"""
Just the workings of some sort of data gatherer.
Looks like Bobby has already completed something like this, so just committed for record keeping purposes.
"""

import csv
from collections import Counter

target = "data/foi-csv.csv"

class Feature:
	def __init__(self, ):

class Postcode:


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