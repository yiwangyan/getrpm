#!/usr/bin/env python2.7
import getopt
import sys
import searchInfo
import os
import re

def doquery(query=None, version=None, flag=None, tofile=None):
	s = searchInfo.searcher('rpm.db')
	r = []
	if isinstance(query, list):
		qfuncs = [s.query(q, version, flag) for q in query]
		for qfunc in qfuncs:
			for obj in qfunc:
				r.append(obj)
	else:
		r = s.query(query, version, flag)
	if tofile == None:
		for i in r:
			print i
	else:
		with open(tofile, 'a') as fd:
			for i in r:
				fd.write(i+'\n')


def updatedb(url):
	p = re.compile(u'/\d+/')
	print 'Updating the rpm.db'
	version = p.findall(url)[0].split('/')[1]
	c = searchInfo.crawler('rpm.db')
	c.crawl(url, version)

def printhelp():
	print "Usage: getRPM.py option ..."
	print "\t-v version: search the version of CentOS"
	print "\t\t--version=version"
	print "\t-e: exact match, default not"
	print "\t\t--exact"
	print "\t-q query str: package name"
	print "\t-f filename: the file which store package name"
	print "\t-t filename: write result to filename"
	print "\t-u packageurl: add or update info of the packageurl's package"

def parseopt(argv):
	version = '6'
	querystr = ''
	FLAG = False
	tofile = None
	try:
		opts, args = getopt.getopt(argv, "hv:eq:f:t:u:", ["version=", "exact"])
	except getopt.GetoptError:
		print '%s -v <version, default 6> -e [-q <package>|-f <filename>\
				-t <filename> -u <packageurl>' % sys.argv[0]
		sys.exit(1)

	for opt, arg in opts:
		if opt == '-h':
			printhelp()
			sys.exit()
		elif opt == '-u':
			updatedb(arg)
			sys.exit()
		elif opt in ("-v", "--version"):
			version = arg
		elif opt in ("-e", "--exact"):
			FLAG = True
		elif opt == '-q':
			querystr = arg
		elif opt == '-f':
			querystr = []
			with open(arg, 'r') as fd:
				querystr = [l.strip() for l  in fd]
		elif opt == '-t':
			tofile = arg
	return (querystr, version, FLAG, tofile)

if __name__ == '__main__':
	q, v, f, t= parseopt(sys.argv[1:])
	doquery(query=q, version=v, flag=f, tofile=t)
