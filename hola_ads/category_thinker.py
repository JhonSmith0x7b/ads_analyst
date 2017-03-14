# -*- coding:utf-8 -*-

import urllib, urllib2, json, sqlite3
import utils
import threading
class thinker:
	def __init__(self, pkg):
		self.pkg = pkg
		pass

	def think(self):
		db = sqlite3.connect(utils.DATABASE_CATEGORAY)
		cur = db.cursor()
		cur.execute('select * from category_pkg_table where pkg = "%s"' % self.pkg)
		data = cur.fetchall()
		db.close()
		if len(data) > 0:
			return data
		else:
			data = self.recognize()
			try:
				thread = threading.Thread(target = self.sediment, args = (data,))
				thread.start()
			except Exception, e:
				print 'open sediment thread fail. %s' % str(e)
			return data
		pass

	def recognize(self):
		try:
			url = utils.CATEGORY_API
			request_data = {'pkg': self.pkg}
			request_data = urllib.urlencode(request_data)
			request = urllib2.Request(url = url, data = request_data)
			response = urllib2.urlopen(request)
			json_object = json.loads(response.read())
			return json_object
		except Exception, e:
			print 'recongnize error %s' %str(e)
			return False
		pass

	def sediment(self, data):
		db = sqlite3.connect(utils.DATABASE_CATEGORAY)
		if data:
			cur = db.cursor()
			sql = """
			insert into category_pkg_table
			values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", 
			"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")
			""" % (data['pkg'], data['downloadCounts'], data['score'], data['catchAt'], 
				data['cover'], data['category'], data['android_ver'], data['one'], data['two'], 
				data['three'], data['four'], data['five'], data['plus'], data['desc'],
				data['version'], data['fullName'], data['size'])
			insert_result = cur.execute(sql)
			db.commit()
			db.close()
		pass