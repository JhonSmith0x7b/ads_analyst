#-*- coding:utf-8 -*-
import sqlite3, MySQLdb, sys, datetime
sys.path.append('/home/wangxin/www/ads_analyst/')
sys.path.append('/Users/jhonsmith/develop/git/ads_analyst')
from hola_ads import utils, common

db = ''
db_s = ''
log = ''
def get_db():
	global db
	if db == '':
		db = MySQLdb.connect(host = utils.MYSQL_HOST,
							user = utils.MYSQL_USER,
							passwd = utils.MYSQL_PASSWD,
							db = utils.MYSQL_DB)
	return db

def get_db_s():
	global db_s
	if db_s == '':
		db_s = sqlite3.connect(utils.DATABASE_CATEGORAY)
	return db_s

def get_30000(all = False):
	global log
	if all:
		sql = """
			SELECT
				ads.*, count(DISTINCT dt) AS cd ,
				count(*) AS cc
			FROM
				ads ads
			WHERE
				1 = 1
			AND geo = 'US'
			GROUP BY
				image ,
				geo
			ORDER BY
				cd DESC
			limit 0, 10000
		"""
		cursor = get_db().cursor()
		cursor.execute(sql)
		result = cursor.fetchall()
		log += 'from all get %s ' % len(result)
		return result
	else:
		current_date = datetime.datetime.today().strftime('%Y%m%d')
		sql_date_range = common.delta_date(current_date, 30)
		sql = """
			SELECT
				ads.*, count(DISTINCT dt) AS cd ,
				count(*) AS cc
			FROM
				ads ads
			WHERE
				1 = 1
			AND dt > "%s"
			AND geo = 'US'
			GROUP BY
				image ,
				geo
			ORDER BY
				cd DESC
			limit 0, 10000
		""" % sql_date_range
		cursor = get_db().cursor()
		cursor.execute(sql)
		result = cursor.fetchall()
		log += 'from month get %s ' % len(result)
		return result
	pass

def set_30000(date, all = False):
	global log
	if len(date) > 5000 and all:
		cursor = get_db_s().cursor()
		exist_sql = """
		select count(*) from sqlite_master where type = "table" and name = "thirty_alldate_us_ad"
		"""
		cursor.execute(exist_sql)
		if int(cursor.fetchall()[0][0]) == 0:
			create_sql = """
			CREATE TABLE thirty_alldate_us_ad(request_id text, uid text, 
			pid text, cad_ver text, app_name text, icon text, image text, 
			sub_title text, title text, social_context text, call_to_action text, 
			body text, adtype text, dt text, package_name text, event_time text, geo text, cd text, cc text)
			"""
			cursor.execute(create_sql)
			get_db_s().commit()
			log += 'create all table '
		delete_sql = """
		delete from thirty_alldate_us_ad
		"""
		cursor.execute(delete_sql)
		get_db_s().commit()
		log += 'remove all table '
		for index in xrange(len(date)):
			insert_sql = """
			insert into thirty_alldate_us_ad(request_id, uid, pid, cad_ver, app_name, 
			icon, image, sub_title, title, social_context, call_to_action, body, adtype,
			dt, package_name, event_time, geo, cd, cc) values("%s", "%s", "%s", "%s", "%s", 
			"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")
			""" % (date[index][0], date[index][1], date[index][2], date[index][3], date[index][4], 
				date[index][5], date[index][6], date[index][7], date[index][8], date[index][9], 
				date[index][10], date[index][11], date[index][12], date[index][13], date[index][14], 
				date[index][15], date[index][16], date[index][17], date[index][18])
			cursor.execute(insert_sql)
		get_db_s().commit()
		log += 'insert to all table '
	elif len(date) > 5000:
		cursor = get_db_s().cursor()
		exist_sql = """
		select count(*) from sqlite_master where type = "table" and name = "thirty_monthdate_us_ad"
		"""
		cursor.execute(exist_sql)
		if int(cursor.fetchall()[0][0]) == 0:
			create_sql = """
			CREATE TABLE thirty_monthdate_us_ad(request_id text, uid text, 
			pid text, cad_ver text, app_name text, icon text, image text, 
			sub_title text, title text, social_context text, call_to_action text, 
			body text, adtype text, dt text, package_name text, event_time text, geo text, cd text, cc text)
			"""
			cursor.execute(create_sql)
			get_db_s().commit()
			log += 'create month table '
		delete_sql = """
		delete from thirty_monthdate_us_ad
		"""
		cursor.execute(delete_sql)
		get_db_s().commit()
		log += 'remove month table '
		for index in xrange(len(date)):
			insert_sql = """
			insert into thirty_monthdate_us_ad(request_id, uid, pid, cad_ver, app_name, 
			icon, image, sub_title, title, social_context, call_to_action, body, adtype,
			dt, package_name, event_time, geo, cd, cc) values("%s", "%s", "%s", "%s", "%s", 
			"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")
			""" % (date[index][0], date[index][1], date[index][2], date[index][3], date[index][4], 
				date[index][5], date[index][6], date[index][7], date[index][8], date[index][9], 
				date[index][10], date[index][11], date[index][12], date[index][13], date[index][14], 
				date[index][15], date[index][16], date[index][17], date[index][18])
			cursor.execute(insert_sql)
		get_db_s().commit()
		log += 'insert to month table '
	pass


def start():
	global log
	set_30000(get_30000(True), all = True)
	set_30000(get_30000(False), all = False)
	with open('catch.log', 'a') as f:
		f.write(log)
		f.close()
	pass

start()