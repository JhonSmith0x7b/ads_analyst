# -*- coding:utf-8 -*-

import sqlite3, os, MySQLdb, sys, urllib, urllib2, json, time
sys.path.append('../../')
sys.path.append('/home/wangxin/www/ads_analyst/')
from hola_ads import utils 

counter = 0
counter_category = 0

def get_mysql_db():
	db = MySQLdb.connect(host = utils.MYSQL_HOST,
								user = utils.MYSQL_USER,
								passwd = utils.MYSQL_PASSWD,
								db = utils.MYSQL_DB,
								connect_timeout = 20)
	return db

def get_sqlite_db():
	db = sqlite3.connect('ads_db.db')
	return db

def get_all_from_mysql():
	cur = get_mysql_db().cursor()
	cur.execute('select * from ads where dt > %s', (str(int(time.strftime('%Y%m%d')) - 7), ))
	result = cur.fetchall()
	return result

def catch_circle():
	global counter
	global counter_category
	ads = get_all_from_mysql()
	for ad in ads:
		try:
			sediment(ad)
			print 'process %s' % ads.index(ad)
		except Exception, e:
			print 'circle error %s' % str(e)
	check_new()
	log =  """


	%s done.

	ads add : %s

	category add : %s

	""" % (time.strftime('%Y%m%d'), counter, counter_category)
	with open('catch.log', 'a') as f:
		f.write(log)
		f.close()

def sediment(data):
	global counter
	global counter_category
	try:
		if data:
				db = get_sqlite_db()
				cur = db.cursor()
				sql = """
				insert into ads_table
				values(?, ?, ?, ?, ?, ?, ?, ?, ?, 
				?, ?, ?, ?, ?, ?, ?, ?)
				"""
				insert_result = cur.execute(sql, [data[0], data[1], 
					data[2], data[3], 
					data[4], data[5], data[6], data[7], data[8], 
					data[9], data[10], data[11], data[12], data[13],
					data[14], data[15], data[16]])
				db.commit()
				db.close()
				counter += 1
	except Exception, e:
		print 'sediment error %s' % str(e)

def check_new():
	db = get_sqlite_db()
	cur = db.cursor()
	cur.execute('select distinct package_name from ads_table')
	packages = cur.fetchall()
	for package in packages:
		cur.execute('select 1 from category_pkg_table where pkg = ?', [package[0],])
		data = cur.fetchall()
		if len(data) < 1:
			try:
				sediment_category(recognize(package[0]))
			except Exception, e:
				print 'check new error %s' % str(e)

def sediment_category(data):
	global counter
	global counter_category
	db = get_sqlite_db()
	if data:
		cur = db.cursor()
		sql = """
			insert into category_pkg_table
			values(?, ?, ?, ?, ?, ?, ?, ?, ?, 
			?, ?, ?, ?, ?, ?, ?, ?)
			"""
		insert_result = cur.execute(sql, [data['pkg'], data['downloadCounts'], 
			data['score'], data['catchAt'], 
			data['cover'], data['category'], data['android_ver'], data['one'], data['two'], 
			data['three'], data['four'], data['five'], data['plus'], data['desc'],
			data['version'], data['fullName'], data['size']])
		db.commit()
		db.close()
		counter_category += 1

def recognize(pkg):
	try:
		url = utils.CATEGORY_API
		request_data = {'pkg': pkg}
		request_data = urllib.urlencode(request_data)
		url += '?%s' % request_data
		request = urllib2.Request(url = url)
		response = urllib2.urlopen(request)
		json_object = json.loads(response.read())
		return json_object
	except Exception, e:
		print 'recongnize error %s %s' % (str(e), pkg)
		return {'category':'error'}
	pass

catch_circle()
