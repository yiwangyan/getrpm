#!/usr/bin/env python2.7
import getopt
import sys
import searchInfo

def doquery(query=None, version=None, fromfile=None, tofile=None):
	s = searchInfo.searcher('rpm.db')
	s.query((query, version))

def updatedb():
	print 'Updating the rpm.db'

def parseopt(argv):
	version = '6'
	querystr = ''
	FLAG = False
	tofile = None
	try:
		opts, args = getopt.getopt(argv, "hv:eq:f:t:u:", ["version=", "exact"])
	except getopt.GetoptError:
		print '%s -v <version, default 6> -e [-q <package>|-f <filename>\
				-t <filename>' % sys.argv[0]
		sys.exit(1)

	for opt, arg in opts:
		if opt == '-h':
			print "Usage: getRPM.py -v version -e"
			print "\t-v version: search the version of CentOS"
			print "\t\t--version=version"
			print "\t-e: exact match, default not"
			print "\t\t--exact"
			print "\t-q query str: package name"
			print "\t-f filename: the file which store package name"
			print "\t-t filename: write result to filename"
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
		elif opt == '-u':
			update()
	return (querystr, version, FLAG, tofile)

if __name__ == '__main__':
	q, v, f, t= parseopt(sys.argv[1:])
	doquery(query=q, version=v, fromfile=f, tofile=t)
