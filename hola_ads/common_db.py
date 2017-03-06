# -*- coding:utf-8 -*-
import sqlite3
import os
import sys
class Common_db:
	#self.db_path 	db path
	#self.db db
	def __init__(self, db_path):
		self.db_path = db_path
		pass

	def init_db(self):
		if not os.path.isfile(self.db_path):
			return 1230000
		try:
			db = sqlite3.connect(self.db_path)
			db.text_factory = str
		except:
			return 1230001
		self.db = db
		return db

	def query_by_sql(self, sql):
		cur = self.db.cursor().execute(sql)
		return cur.fetchall()