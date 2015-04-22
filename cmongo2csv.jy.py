#!/usr/bin/env jython
"""
cmongo2csv
Utility to convert a MongoDB JSON dump to a CSV file.

Copyright 2015 Sam Saint-Pettersen.
Licensed under the MIT/X11 License.

Tweaked for Jython compatibility.
Uses Java implemented JSON module
and getopt instead of argparse.

"""
import sys
import os
import re
import com.xhaus.jyson.JysonCodec as json
import getopt

signature = 'cmongo2csv 1.0 [Jython] (https://github.com/stpettersens/cmongo2csv)'

def displayVersion():
	print('\n' + signature)

def displayInfo():
	print(__doc__)

def cmongo2csv(file, out, separator, verbose, version, info):

	if len(sys.argv) == 1: 
		displayInfo()
		sys.exit(0)

	if file == None and out == None:
		if verbose == False and version == True and info == False:
			displayVersion()

		elif verbose == False and version == False and info == True:
			displayInfo()

		sys.exit(0)

	if out == None: out = re.sub('.json', '.csv', file)

	if file.endswith('.json') == False:
		print('Input file is not a MongoDB dump.')
		sys.exit(1)

	if out.endswith('.csv') == False and out.endswith('.tsv') == False:
		print('Output file is not a CSV or TSV file.')
		sys.exit(1)

	if separator == None: separator = ','

	if out.endswith('.tsv'): separator = '\t'

	head, tail = os.path.split(file)
	collection = re.sub('.json', '', tail)

	f = open(file, 'r')
	lines = f.readlines()
	f.close()

	fields = []
	inserts = []
	headers = True
	for line in lines:
		ii = ''
		inputJson = json.loads(line)
		for key, value in inputJson.iteritems():

			fvalue = re.sub('\{|\}|\'', '', str(value))

			pattern = re.compile('\$oid')
			if pattern.match(str(fvalue)):
				if headers: fields.append(str(key))
				v = re.split(':', str(fvalue), 1)
				v = re.sub('\s', '', v[1], 1)
				v = re.sub('\u', '', v)
				ii += 'ObjectId(%s)%s' % (v, separator)
				continue

			pattern = re.compile('\$date')
			if pattern.match(str(fvalue)):
				if headers: fields.append(str(key))
				v = re.split(':', str(fvalue), 1)
				v = re.sub('\s', '', v[1], 1)
				v = re.sub('\u', '', v)
				v = ''.join(v)
				ii += '%s%s' % (v, separator)
				continue

			pattern = re.compile('[\w\s]+')
			if pattern.match(str(fvalue)):
				if headers: fields.append(str(key))
				ii += '%s%s' % (fvalue, separator)
			

		ii = ii[:-1]
		inserts.append(ii)
		ii = ''
		headers = False

	if verbose:
		print('\nGenerating CSV file: \'%s\' from\nMongoDB JSON dump file: \'%s\''
		% (out, file))

	f = open(out, 'w')
	f.write(separator.join(fields) + '\n')
	for insert in inserts:
		f.write(insert + '\n')

	f.close()


# Handle any command line arguments.
try:
	opts, args = getopt.getopt(sys.argv[1:], "f:o:s:lvi")
except:
	print('Invalid option or argument.')
	displayInfo()
	sys.exit(2)

file = None
out = None
separator = None
comments = None
verbose = False
version = False
info = False
for o, a in opts:
	if o == '-f':
		file = a
	elif o == '-o':
		out = a
	elif o == '-s':
		separator = a
	elif o == '-n':
		comments = False
	elif o == '-l':
		verbose = True
	elif o == '-v':
		version = True
	elif o == '-i':
		info = True
	else:
		assert False, 'unhandled option'

cmongo2csv(file, out, separator, verbose, version, info)
