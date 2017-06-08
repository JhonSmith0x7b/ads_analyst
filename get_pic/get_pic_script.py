#-*- coding:utf-8 -*-

import urllib, urllib2, zlib, re, sys, sqlite3
import pandas as pd
from pandas import DataFrame, Series


def get_pkgs2list():
	df = pd.read_csv('longtxt.txt', sep = '\t')
	return list(df['package_name'])

def get_pic():
	pakcage_list = get_pkgs2list()
	headers = {
			    'X-Ad-Id': 'fc728fdc-9aa4-4c00-afec-1090ba53b5a4',
			    'X-DFE-Device-Id': '38ada555195e230f',
			    'Authorization': 'GoogleLogin auth=xATESS19Zgl-OLiv5OR0afWacxSkg61O5Se3ZbYgkMAtfkavg0Iotv7-9rbKg6wjwTcOEw.',
			    'Host': 'android.clients.google.com',
			    'User-Agent': 'curl/7.51.0',
			    'Accept': ' */*',
			    'Accept-Encoding': 'deflate, gzip'
			}
	db = getdb_checktable()
	cursor = db.cursor()
	table_name = 'gp_res_table'
	counter = 0
	current_pkgs = []
	sql = """
	select distinct package_name from %s
	""" % table_name
	t = cursor.execute(sql).fetchall()
	for _ in t:
		current_pkgs.append(_[0])
	for package_name in pakcage_list:
		if package_name in current_pkgs:
			continue
		try:
			url = 'https://android.clients.google.com/fdfe/details?doc=%s' % package_name
			req = urllib2.Request(url = url, headers = headers)
			resp = urllib2.urlopen(req)
			decompressed_data=zlib.decompress(resp.read(), 16 + zlib.MAX_WBITS)
			pic_list = re.findall(r'https://lh3.googleusercontent.com[\w, \., /, -]*', decompressed_data)
			for p in pic_list:
				if p[-1] == 'H':
					try:
						req = urllib2.Request(url = p)
						resp = urllib2.urlopen(req, timeout = 10)
						print 'H'
					except Exception, e:
						print 'no H %s' % str(e)
						pic_list[pic_list.index(p)] = p[:-1]
			video_list = re.findall(r'https://www.youtube.com[\w, \., /, -, ?, =]*', decompressed_data)
			sql = """
			insert into %s (package_name, pic_list, video_list) values(?, ?, ?)
			""" % table_name
			cursor.execute(sql, (package_name, str(pic_list), str(video_list)))
			db.commit()
			counter += 1
			print counter
		except Exception, e:
			print package_name
			print 'E %s' % str(e)
			pass
	cursor.close()
	db.close()
	pass

def getdb_checktable():
	db = sqlite3.connect('gp_res_db.db')
	cursor = db.cursor()
	table_name = 'gp_res_table'
	sql = """
	select count(*) from sqlite_master where type = "table" and name = "%s"
	""" % table_name
	cursor.execute(sql)
	if cursor.fetchall()[0][0] == 0:
		sql = """
		create table gp_res_table(package_name text, pic_list text, video_list text, banner text)
		"""
		cursor.execute(sql)
		db.commit()
	cursor.close()
	return db
	pass


if __name__ == '__main__':
	sys.exit(get_pic())