#!/usr/bin/env ipy
"""
cmongo2csv
Utility to convert a MongoDB JSON dump to a CSV file.

Copyright 2015 Sam Saint-Pettersen.
Licensed under the MIT/X11 License.

Tweaked for IronPython.

Use -h switch for usage information.
"""
import sys
import os
import re
import json
import argparse

signature = 'cmongo2csv 1.0 [IPY] (https://github.com/stpettersens/cmongo2csv)'

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
				ii += 'ObjectId({0}){1}'.format(v, separator)
				continue

			pattern = re.compile('\$date')
			if pattern.match(str(fvalue)):
				if headers: fields.append(str(key))
				v = re.split(':', str(fvalue), 1)
				v = re.sub('\s', '', v[1], 1)
				v = ''.join(v)
				ii += '{0}{1}'.format(v, separator)
				continue

			pattern = re.compile('[\w\s]+')
			if pattern.match(str(fvalue)):
				if headers: fields.append(str(key))
				ii += '{0}{1}'.format(fvalue, separator)
			

		ii = ii[:-1]
		inserts.append(ii)
		ii = ''
		headers = False

	if verbose:
		print('\nGenerating CSV file: \'{0}\' from\nMongoDB JSON dump file: \'{1}\''
		.format(out, file))

	f = open(out, 'w')
	f.write(separator.join(fields) + '\n')
	for insert in inserts:
		f.write(insert + '\n')

	f.close()

				
# Handle any command line arguments.
parser = argparse.ArgumentParser(description='Utility to convert a MongoDB JSON dump to a CSV file.')
parser.add_argument('-f', '--file', action='store', dest='file', metavar="FILE")
parser.add_argument('-o', '--out', action='store', dest='out', metavar="OUT")
parser.add_argument('-s', '--separator', action='store', dest='separator', metavar="SEPARATOR")
parser.add_argument('-l', '--verbose', action='store_true', dest='verbose')
parser.add_argument('-v', '--version', action='store_true', dest='version')
parser.add_argument('-i', '--info', action='store_true', dest='info')
argv = parser.parse_args()

cmongo2csv(argv.file, argv.out, argv.separator, argv.verbose, argv.version, argv.info)
