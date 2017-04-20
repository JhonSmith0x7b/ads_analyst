# -*- coding:utf-8 -*-
import sqlite3
import os
import sys
import MySQLdb
import utils
from DBUtils.PooledDB import PooledDB
from flask import current_app
def create_mysql_db_pool():
	pool = PooledDB(
                creator=MySQLdb,
                use_unicode=False,
                db = utils.MYSQL_DB,
                host=utils.MYSQL_HOST,
                port=utils.MYSQL_PORT,
                user=utils.MYSQL_USER,
                passwd=utils.MYSQL_PASSWD,
                charset=utils.MYSQL_CHARSET,
                mincached = 6,
                maxcached = 11,
                maxconnections=utils.MYSQL_MAXCONNECTIONS)
	return pool.connection(shareable = True)
class Common_db:
	#self.db_path 	db path
	#self.db db
	# def __init__(self, db_path):
	# 	self.db_path = db_path
	# 	pass

	# def init_db(self):
	# 	if not os.path.isfile(self.db_path):
	# 		return 1230000
	# 	try:
	# 		db = sqlite3.connect(self.db_path)
	# 		db.text_factory = str
	# 	except:
	# 		return 1230001
	# 	self.db = db
	# 	return db

	# def query_by_sql(self, sql):
	# 	cur = self.db.cursor().execute(sql)
	# 	return cur.fetchall()

	def __init__(self, nanimo):
		# db = MySQLdb.connect(host = utils.MYSQL_HOST,
		# 						user = utils.MYSQL_USER,
		# 						passwd = utils.MYSQL_PASSWD,
		# 						db = utils.MYSQL_DB)
		# db = sqlite3.connect(utils.DATABASE_ADS)
		self.db = current_app.db
		db_s = sqlite3.connect(utils.DATABASE_CATEGORAY)
		self.db_s = db_s
		pass

	def init_db(self):
		pass

	def query_by_sql(self, sql):
		cur = self.db.cursor()
		cur.execute(sql)
		return cur.fetchall()
		pass

	def query_sqlite_by_sql(self, sql):
		cur = self.db_s.cursor()
		cur.execute(sql)
		return cur.fetchall()
		pass

	def close_db(self):
		try:
			self.db.close()
			self.db_s.close()
		except Exception, e:
			print 'close db error %s' % str(e)