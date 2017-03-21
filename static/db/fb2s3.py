#-*- coding:utf-8 -*-

import boto3, hashlib, urllib, urllib2, threading, sys, MySQLdb, time, sqlite3
sys.path.append('/home/wangxin/www/ads_analyst/')
sys.path.append('/Users/jhonsmith/develop/git/ads_analyst')
from hola_ads import utils, common

counter = 0 
divide = 90
sleep_divide = 1
over_counter = 0

def get_url_from_mysql():
	return get_distinct_image_from_mysql()
	pass

def get_mysql_db():
	db = MySQLdb.connect(host = utils.MYSQL_HOST,
								user = utils.MYSQL_USER,
								passwd = utils.MYSQL_PASSWD,
								db = utils.MYSQL_DB,
								connect_timeout = 20)
	return db

def get_sqlite_db():
	db = sqlite3.connect(utils.DATABASE_ADS)
	return db

def get_distinct_image_from_mysql():
	cur = get_mysql_db().cursor()
	cur.execute('select distinct image from ads')
	result = cur.fetchall()
	return result

def print_error_log(e):
	global counter
	print 'thread %s, error %s' % (str(counter), e)

def get_image_via_http(url, do = True):
	global counter
	request = urllib2.Request(url = url)
	try:
		response = urllib2.urlopen(request)
	except urllib2.HTTPError as e:
		print_error_log(e)
		return False
	except urllib2.URLError as e:
		print_error_log(e)
		return False
	except Exception, e:
		print url
		print_error_log(e)
		return False
	else:
		result = response.read()
		if len(result) > 1000:
			return result
		elif do:
			get_image_via_http(url, do = False)
		else:
			print_error_log('to short ' + result)
			return False

def push_to_s3(s3, url):
	global counter
	global over_counter
	counter += 1
	md5 = hashlib.md5()
	md5.update(url)
	original_url = url
	if '&w=' in url:
		url += '&w=1200&h=627'
	data = get_image_via_http(url)
	if data:
		try:
			s3.Bucket('imgcn.dataverse.cn').put_object(
				Key = (common.get_s3_uri(original_url)), 
				Body = data, ACL = 'public-read', ContentType = 'image/jpeg')
			sediment_to_sqlite(original_url, md5.hexdigest())
		except Exception, e:
			print 'push 2 s3 error %s' % str(e)
	over_counter += 1

def check_new():
	db = get_sqlite_db()
	cur = db.cursor()
	sql = """
	select distinct image from ads_table where dt > "%s" 
	and image not in 
		(select image from fb2s3_table)
	""" % (str(int(time.strftime('%Y%m%d')) - 7))
	print sql
	cur.execute(sql)
	images = cur.fetchall()
	if len(images) > 0:
		return images
	else:
		return False

def sediment_to_sqlite(url, md5):
	db = get_sqlite_db()
	cur = db.cursor()
	sql = """
	insert into fb2s3_table values(?, ?)
	"""
	cur.execute(sql, [url, md5])
	db.commit()
	db.close()


def start():
	global counter
	global over_counter
	s3 = boto3.resource('s3',
			aws_access_key_id = 'AKIAO7VYUE4LB7J6FTAA',
			aws_secret_access_key = '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',
			region_name = 'cn-north-1')
	urls = check_new()
	if urls:
		for url in urls:
			try:
				if counter - over_counter > divide:
					print 'ya su mi'
					time.sleep(sleep_divide)
				else:
					thread = threading.Thread(target = push_to_s3, args = (s3,url[0]))
					thread.start()
			except Exception, e:
				print '2 s3 error %s' % str(e)
	log =  """


	%s done.

	image add 2 s3: %s

	added 2 s3 : %s

	""" % (time.strftime('%Y%m%d'), counter, over_counter)
	with open('catch.log', 'a') as f:
		f.write(log)
		f.close()

start()