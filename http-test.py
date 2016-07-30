import urllib2

url = 'http://139.59.226.51/jsontest'

opener = urllib2.build_opener()
f = opener.open(url)
print f.read()