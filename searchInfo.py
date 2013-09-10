import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin
try:
	from pysqlite2 import dbapi2 as sqlite
except ImportError:
	import sqlite3

class crawler:
	def __init__(self, dbname):
		self.con = sqlite.connect(dbname)

	def __del__(self):
		self.con.close()
	
	def dbcommit(self):
		self.con.commit()

	def createtables(self):
		self.con.execute(
				'create table os_version(id integer primary key autoincrement, \
						majorversion varchar(8))')
		self.con.execute(
				'create table site(id integer primary key autoincrement,\
						sitename varchar(256), majorversionid integer)')
		self.con.execute(
				'create table packages(id integer primary key autoincrement,\
						package varchar(256), sitenameid integer,\
						majorversionid integer)')
		self.dbcommit()

	def getentryid(self, table, field, value, createnew=True):
		cur = self.con.execute(
				"select id from %s where %s='%s'" % (table, field, value))
		res = cur.fetchone()
		if res == None:
			cur = self.con.execute(
					"insert into %s (%s) values ('%s')" % (table, field, value))
			self.dbcommit()
			return cur.lastrowid
		else:
			return res[0]

	def addtosite(self, site, version):
		vid = self.getentryid('os_version', 'majorversion', version)
		cur = self.con.execute(
				"select * from site where sitename='%s' and majorversionid=%s" \
						% (site, vid))
		res = cur.fetchone()
		if res == None:
			cur = self.con.execute(
					"insert into site (sitename, majorversionid) values ('%s', %s)"\
							% (site, vid))
			self.dbcommit()
		
	def addtopackages(self, results, site, version):
		vid = self.getentryid('os_version', 'majorversion', version)
		print '----- vid = {0} -------'.format(vid)
		res = self.con.execute(
				"select id from site where sitename='%s' and majorversionid=%s" \
						% (site, vid)).fetchone()[0]
		for i in results:
			cur = self.con.execute(
				"select * from packages where package='%s'" % i)
			if cur.fetchone() == None:
				print 'Adding %s ' % i
				cur = self.con.execute(
						"insert into packages (package, sitenameid, majorversionid) \
								values ('%s', %s, %s)" % (i, res, vid))
		self.dbcommit()

	def crawl(self, site, version):
		try:
			c = urllib2.urlopen(site)
		except:
			print "Could not open %s" % site
			return 
		self.addtosite(site, version)
		soup = BeautifulSoup(c.read())
		links = soup('a')
		results = []
		for link in links:
			if ('href' in dict(link.attrs)):
				if 'rpm'  in link['href']:
					results.append(link['href'])

		self.addtopackages(results, site, version)

class searcher:
	def __init__(self, dbname):
		self.con = sqlite.connect(dbname)

	def __del__(self):
		self.con.close()

	def query(self, q):
		res = self.con.execute(
				"select site.sitename, packages.package from packages, site \
						where site.majorversionid=packages.majorversionid \
						and packages.sitenameid=site.id and\
						packages.package LIKE '%{0}%' and\
						packages.majorversionid=(select id from os_version \
						where majorversion='{1}')".format(q[0], q[1]))
		for i in res.fetchall():
			print i[0]+i[1]
