#-*- coding:utf-8 -*-
from flask import Blueprint, request, render_template
import urllib, urllib2, json, sqlite3, datetime
from hola_ads import utils

sdk_mapper = Blueprint('sdk_mapper' , __name__, template_folder = './')

@sdk_mapper.route('/sdk_mapper/test', methods = ['POST', 'GET'])
def test():
	banner_list = Db_queryer(Query_banner_db()).query()
	interstitial_list = Db_queryer(Query_interstitial_db()).query()
	reward_list = Db_queryer(Query_reward_db()).query()
	games_list = Db_queryer(Query_games_db()).query()
	trace_list = Db_queryer(Query_trace_db()).query()
	csta_list = Db_queryer(Query_csta_db()).query()
	accountkit_list = Db_queryer(Query_accountkit_db()).query()
	ssl08_list = Db_queryer(Query_ssl08_db()).query()
	tappsflyer_list = Db_queryer(Query_tappsflyer_db()).query()
	eventappsflyer_list = Db_queryer(Query_eventappsflyer_db()).query()
	json_data = json.dumps({'banner': banner_list, 
		'interstitial': interstitial_list,
		'reward': reward_list,
		'games': games_list,
		'trace': trace_list,
		'csta': csta_list,
		'accountkit': accountkit_list,
		'ssl08': ssl08_list,
		'tappsflyer': tappsflyer_list,
		'eventappsflyer': eventappsflyer_list
		})

	return render_template('sdk_mapper/index.htm', banner_data = json_data), 200

@sdk_mapper.route('/sdk_mapper/index', methods = ['POST', 'GET'])
def index():
	banner_list = Db_queryer(Query_banner_db()).query()
	interstitial_list = Db_queryer(Query_interstitial_db()).query()
	reward_list = Db_queryer(Query_reward_db()).query()
	games_list = Db_queryer(Query_games_db()).query()
	trace_list = Db_queryer(Query_trace_db()).query()
	csta_list = Db_queryer(Query_csta_db()).query()
	accountkit_list = Db_queryer(Query_accountkit_db()).query()
	ssl08_list = Db_queryer(Query_ssl08_db()).query()
	tappsflyer_list = Db_queryer(Query_tappsflyer_db()).query()
	eventappsflyer_list = Db_queryer(Query_eventappsflyer_db()).query()
	json_data = json.dumps({'banner': banner_list, 
		'interstitial': interstitial_list,
		'reward': reward_list,
		'games': games_list,
		'trace': trace_list,
		'csta': csta_list,
		'accountkit': accountkit_list,
		'ssl08': ssl08_list,
		'tappsflyer': tappsflyer_list,
		'eventappsflyer': eventappsflyer_list
		})

	return render_template('sdk_mapper/index.htm', banner_data = json_data), 200

@sdk_mapper.route('/sdk_mapper/t_appsflyer', methods = ['POST', 'GET'])
def t_appsflyer():
	try:
		if request.method == 'POST':
			url = 'https://t.appsflyer.com/api/v4/androidevent'
			resp = Url_opener(Post_json_urlopen()).open_via_request(url, request)
			resp_data = resp.read()
			resp_code = resp.getcode()
			Db_inserter(Insert_tappsflyer_db()).insert(request, resp_code, resp_data)
			return resp_data, resp_code
		return '', 200
	except Exception, e:
		print str(e)
		return 'error: %s' % str(e), 500

@sdk_mapper.route('/sdk_mapper/event_appsflyer', methods = ['POST', 'GET'])
def event_appsflyer():
	try:
		if request.method == 'POST':
			url = 'https://events.appsflyer.com/api/v4/androidevent'
			resp = Url_opener(Post_json_urlopen()).open_via_request(url, request)
			resp_data = resp.read()
			resp_code = resp.getcode()
			Db_inserter(Insert_eventappsflyer_db()).insert(request, resp_code, resp_data)
			return resp_data, resp_code
		return '', 200
	except Exception, e:
		print str(e)
		return 'error: %s' % str(e), 500

@sdk_mapper.route('/sdk_mapper/i_haloapps_banner', methods = ['POST', 'GET'])
def i_haloapps_banner():
	try:
		if request.method == 'GET':
			url = 'http://i.haloapps.com/single_game/banner.php/ad_unit_id'
			resp = Url_opener(Get_urlopen()).open_via_request(url, request)
			resp_data = resp.read()
			resp_code = resp.getcode()
			Db_inserter(Insert_banner_db()).insert(request, resp_code, resp_data)
			return resp_data, resp_code
		return '', 200
	except Exception, e:
		return 'error: %s' % str(e), 500
	pass

@sdk_mapper.route('/sdk_mapper/i_haloapps_interstitial', methods = ['POST', 'GET'])
def i_haloapps_interstitial():
	try:
		if request.method == 'GET':
			url = 'http://i.haloapps.com/single_game/interstitial.php/ad_unit_id'
			resp = Url_opener(Get_urlopen()).open_via_request(url, request)
			resp_data = resp.read()
			resp_code = resp.getcode()
			Db_inserter(Insert_interstital_db()).insert(request, resp_code, resp_data)
			return resp_data, resp_code
		return '', 200
	except Exception, e:
		return 'error: %s' % str(e), 500
	pass

@sdk_mapper.route('/sdk_mapper/i_haloapps_games', methods = ['POST', 'GET'])
def i_haloapps_games():
	try:
		if request.method == 'GET':
			url = 'http://i.haloapps.com/games/api/adConfig'
			resp = Url_opener(Get_urlopen()).open_via_request(url, request)
			resp_data = resp.read()
			resp_code = resp.getcode()
			Db_inserter(Insert_games_db()).insert(request, resp_code, resp_data)
			return resp_data, resp_code
		return '', 200
	except Exception, e:
		return 'error: %s' % str(e), 500
	pass

@sdk_mapper.route('/sdk_mapper/i_haloapps_trace', methods = ['POST', 'GET'])
def i_haloapps_trace():
	try:
		if request.method == 'GET':
			url = 'http://i.haloapps.com/tracking_sdk_conf.lua'
			resp = Url_opener(Get_urlopen()).open_via_request(url, request)
			resp_data = resp.read()
			resp_code = resp.getcode()
			Db_inserter(Insert_trace_db()).insert(request, resp_code, resp_data)
			return resp_data, resp_code
		return '', 200
	except Exception, e:
		return 'error: %s' % str(e), 500
	pass

@sdk_mapper.route('/sdk_mapper/rewarded_video', methods = ['POST', 'GET'])
def rewarded_video():
	try:
		if request.method == 'GET':
			url = 'http://rewarded-video-api.avidly.com/index.php'
			resp = Url_opener(Get_urlopen()).open_via_request(url, request)
			resp_data = resp.read()
			resp_code = resp.getcode()
			Db_inserter(Insert_reward_db()).insert(request, resp_code, resp_data)
			return resp_data, resp_code
		return '', 200
	except Exception, e:
		print str(e)
		return 'error: %s' % str(e), 500
	pass

@sdk_mapper.route('/sdk_mapper/c_sta_log', methods = ['POST', 'GET'])
def c_sta_log():
	try:
		if request.method == 'POST':
			url = 'http://c.sta.haloapps.com/log'
			resp = Url_opener(Post_str_urlopen()).open_via_request(url, request)
			resp_data = resp.read()
			resp_code = resp.getcode()
			Db_inserter(Insert_csta_db()).insert(request, resp_code, resp_data)
			return resp_data, resp_code
		return '', 200
	except Exception, e:
		print str(e)
		return 'error: %s' % str(e), 500
	pass

@sdk_mapper.route('/sdk_mapper/accountkit', methods = ['POST', 'GET'])
def accountkit():
	try:
		if request.method == 'POST':
			url = 'https://accountkit.avidly.com/v1.0/account/log'
			resp = Url_opener(Post_form_urlopen()).open_via_request(url, request)
			resp_data = resp.read()
			resp_code = resp.getcode()
			Db_inserter(Insert_accountkit_db()).insert(request, resp_code, resp_data)
			return resp_data, resp_code
		return '', 200
	except Exception, e:
		print str(e)
		return 'error: %s' % str(e), 500
	pass

@sdk_mapper.route('/sdk_mapper/ssl08', methods = ['POST', 'GET'])
def ssl08():
	try:
		if request.method == 'POST':
			url = 'https://ssl08.haloapps.com/pay/ggdirectpay'
			resp = Url_opener(Post_form_urlopen()).open_via_request(url, request)
			resp_data = resp.read()
			resp_code = resp.getcode()
			Db_inserter(Insert_ssl08_db()).insert(request, resp_code, resp_data)
			return resp_data, resp_code
		return '', 200
	except Exception, e:
		print str(e)
		return 'error: %s' % str(e), 500
	pass

class Super_urlopen_method:
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 
'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
	def open(self):
		pass

class Get_urlopen(Super_urlopen_method):
	def open(self, url, request):
		req = urllib2.Request(url, None, headers = self.headers)
		resp = urllib2.urlopen(req)
		return resp
		pass
class Post_str_urlopen(Super_urlopen_method):
	def open(self, url, request):
		data = request.data
		req = urllib2.Request(url, data = data, headers = self.headers)
		resp = urllib2.urlopen(req)
		return resp
		pass
class Post_json_urlopen(Super_urlopen_method):
	def open(self, url, request):
		data = request.data
		req = urllib2.Request(url, data = data, headers = self.headers)
		req.add_header('Content-Type', 'application/json')
		resp = urllib2.urlopen(req)
		return resp
		pass
class Post_form_urlopen(Super_urlopen_method):
	def open(self, url, request):
		data = Param_converter(Form_2_data()).convert(request.form)
		req = urllib2.Request(url, data = data, headers = self.headers)
		resp = urllib2.urlopen(req)
		return resp
		pass
class Url_opener:
	def __init__(self, method):
		self.m = method
	def open_via_request(self, url, request):
		args = Param_converter(Args_2_str()).convert(request.args)
		url = '%s?%s' % (url, args)
		return self.m.open(url, request)




class Super_converter_mehod:
	def convert(self):
		pass

class Args_2_str(Super_converter_mehod):
	def convert(self, args):
		try:
			re_str = ''
			for key in args:
				args[key].encode('utf-8')
			re_str = urllib.urlencode(args)
			return re_str
		except Exception, e:
			return ''
		pass
class Form_2_data(Super_converter_mehod):
	def convert(self, form):
		try:
			re_data = ''
			for key in form:
				form[key].encode('utf-8')
			re_data = urllib.urlencode(form)
			return re_data
		except Exception, e:
			return ''

class Param_converter:
	def __init__(self, method):
		self.m = method
		pass
	def convert(self, sth):
		return self.m.convert(sth)

class Super_db_mehod:
	db = ''
	def get_db(self):
		if self.db == '':
			self.db = sqlite3.connect(utils.SDK_MAPPER_DB)
			return self.db
		else:
			return self.db
	def insert(self):
		pass
	def check_table(self, table):
		db = self.get_db()
		cursor = db.cursor()
		exist_sql = """
		select count(*) from sqlite_master where type = "table" and name = "%s"
		""" % table
		cursor.execute(exist_sql)
		result = cursor.fetchall()
		if int(result[0][0]) == 0:
			return False
		else:
			return True
	def get_db_time(self):
		return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

	def query(self):
		pass


class Query_banner_db(Super_db_mehod):
	def query(self):
		table = 'banner_table'
		db = self.get_db()
		cursor = db.cursor()
		sql = """
		select * from %s order by time desc limit 6
		""" % table
		cursor.execute(sql)
		result = cursor.fetchall()
		_list = []
		for _object in result:
			try:
				_dict = {}
				request = json.loads(_object[1].encode('utf-8'))
				response_code = _object[2]
				response_data = json.loads(_object[3].encode('utf-8'))
				time = _object[4].encode('utf-8')
				_dict['time'] = time
				_dict['code'] = response_code
				_dict['pkg'] = request['args']['__pkg']
				_dict['sdk_ver'] = request['args']['__sdk_ver']
				_dict['response'] = response_data
				_list.append(_dict)
			except Exception, e:
				print str(e)
				pass
		return _list
		pass
class Query_interstitial_db(Super_db_mehod):
	def query(self):
		table = 'interstitial_table'
		db = self.get_db()
		cursor = db.cursor()
		sql = """
		select * from %s order by time desc limit 6
		""" % table
		cursor.execute(sql)
		result = cursor.fetchall()
		_list = []
		for _object in result:
			try:
				_dict = {}
				request = json.loads(_object[1].encode('utf-8'))
				response_code = _object[2]
				response_data = json.loads(_object[3].encode('utf-8'))
				time = _object[4].encode('utf-8')
				_dict['time'] = time
				_dict['code'] = response_code
				_dict['pkg'] = request['args']['__pkg']
				_dict['sdk_ver'] = request['args']['__sdk_ver']
				_dict['response'] = response_data
				_list.append(_dict)
			except Exception, e:
				print str(e)
				pass
		return _list
class Query_reward_db(Super_db_mehod):
	def query(self):
		table = 'reward_table'
		db = self.get_db()
		cursor = db.cursor()
		sql = """
		select * from %s order by time desc limit 6
		""" % table
		cursor.execute(sql)
		result = cursor.fetchall()
		_list = []
		for _object in result:
			try:
				_dict = {}
				request = json.loads(_object[1].encode('utf-8'))
				response_code = _object[2]
				response_data = json.loads(_object[3].encode('utf-8'))
				time = _object[4].encode('utf-8')
				_dict['time'] = time
				_dict['code'] = response_code
				_dict['packageName'] = request['args']['packageName']
				_dict['platform'] = request['args']['platform']
				_dict['response'] = response_data
				_list.append(_dict)
			except Exception, e:
				print str(e)
				pass
		return _list

class Query_games_db(Super_db_mehod):
	def query(self):
		table = 'games_table'
		db = self.get_db()
		cursor = db.cursor()
		sql = """
		select * from %s order by time desc limit 6
		""" % table
		cursor.execute(sql)
		result = cursor.fetchall()
		_list = []
		for _object in result:
			try:
				_dict = {}
				request = json.loads(_object[1].encode('utf-8'))
				response_code = _object[2]
				response_data = json.loads(_object[3].encode('utf-8'))
				time = _object[4].encode('utf-8')
				_dict['time'] = time
				_dict['code'] = response_code
				_dict['packageName'] = request['args']['packageName']
				_dict['platform'] = request['args']['platform']
				_dict['staToken'] = request['args']['staToken']
				_dict['response'] = response_data
				_list.append(_dict)
			except Exception, e:
				print str(e)
				pass
		return _list

class Query_trace_db(Super_db_mehod):
	def query(self):
		table = 'trace_table'
		db = self.get_db()
		cursor = db.cursor()
		sql = """
		select * from %s order by time desc limit 6
		""" % table
		cursor.execute(sql)
		result = cursor.fetchall()
		_list = []
		for _object in result:
			try:
				_dict = {}
				request = json.loads(_object[1].encode('utf-8'))
				response_code = _object[2]
				response_data = json.loads(_object[3].encode('utf-8'))
				time = _object[4].encode('utf-8')
				_dict['time'] = time
				_dict['code'] = response_code
				_dict['pid'] = request['args']['pid']
				_dict['ch'] = request['args']['ch']
				_dict['sdk_ver'] = request['args']['sdk_ver']
				_dict['response'] = response_data
				_list.append(_dict)
			except Exception, e:
				print str(e)
				pass
		return _list

class Query_csta_db(Super_db_mehod):
	def query(self):
		table = 'csta_table'
		db = self.get_db()
		cursor = db.cursor()
		sql = """
		select * from %s order by time desc limit 6
		""" % table
		cursor.execute(sql)
		result = cursor.fetchall()
		_list = []
		for _object in result:
			try:
				_dict = {}
				request = json.loads(_object[1].encode('utf-8'))
				response_code = _object[2]
				response_data = json.loads(_object[3].encode('utf-8'))
				time = _object[4].encode('utf-8')
				_dict['time'] = time
				_dict['code'] = response_code
				_dict['pid'] = request['args']['pid']
				_dict['cid'] = request['args']['cid']
				_dict['ver'] = request['args']['ver']
				_dict['userId'] = request['args']['userId']
				_dict['response'] = response_data
				_list.append(_dict)
			except Exception, e:
				print str(e)
				pass
		return _list

class Query_accountkit_db(Super_db_mehod):
	def query(self):
		table = 'accountkit_table'
		db = self.get_db()
		cursor = db.cursor()
		sql = """
		select * from %s order by time desc limit 6
		""" % table
		cursor.execute(sql)
		result = cursor.fetchall()
		_list = []
		for _object in result:
			try:
				_dict = {}
				request = json.loads(_object[1].encode('utf-8'))
				response_code = _object[2]
				response_data = json.loads(_object[3].encode('utf-8'))
				time = _object[4].encode('utf-8')
				_dict['time'] = time
				_dict['code'] = response_code
				_dict['packageName'] = request['form']['packageName']
				_dict['thirdPartyName'] = request['form']['thirdPartyName']
				_dict['platform'] = request['form']['platform']
				_dict['gameAccountId'] = request['form']['gameAccountId']
				_dict['androidId'] = request['form']['androidId']
				_dict['response'] = response_data
				_list.append(_dict)
			except Exception, e:
				print str(e)
				pass
		return _list

class Query_ssl08_db(Super_db_mehod):
	def query(self):
		table = 'ssl08_table'
		db = self.get_db()
		cursor = db.cursor()
		sql = """
		select * from %s order by time desc limit 6
		""" % table
		cursor.execute(sql)
		result = cursor.fetchall()
		_list = []
		for _object in result:
			try:
				_dict = {}
				request = json.loads(_object[1].encode('utf-8'))
				response_code = _object[2]
				response_data = json.loads(_object[3].encode('utf-8'))
				time = _object[4].encode('utf-8')
				_dict['time'] = time
				_dict['code'] = response_code
				_dict['package_name'] = request['form']['package_name']
				_dict['product_id'] = request['form']['product_id']
				_dict['cp_player_id'] = request['form']['cp_player_id']
				_dict['androidid'] = request['form']['androidid']
				_dict['response'] = response_data
				_list.append(_dict)
			except Exception, e:
				print str(e)
				pass
		return _list

class Query_tappsflyer_db(Super_db_mehod):
	def query(self):
		table = 'tappsflyer_table'
		db = self.get_db()
		cursor = db.cursor()
		sql = """
		select * from %s order by time desc limit 6
		""" % table
		cursor.execute(sql)
		result = cursor.fetchall()
		_list = []
		for _object in result:
			try:
				_dict = {}
				request = json.loads(_object[1].encode('utf-8'))
				response_code = _object[2]
				response_data = json.loads(_object[3].encode('utf-8'))
				time = _object[4].encode('utf-8')
				_dict['time'] = time
				_dict['code'] = response_code
				_dict['app_id'] = request['args']['app_id']
				_data = json.loads(request['data'].encode('utf-8'))
				_install_data =  json.loads(_data['installAttribution'].encode('utf-8'))
				_dict['appsflyerKey'] = _data['appsflyerKey']
				_dict['android_id'] = _data['android_id']
				_dict['af_message'] = _install_data['af_message']
				_dict['response'] = response_data
				_list.append(_dict)
			except Exception, e:
				print str(e)
				pass
		return _list

class Query_eventappsflyer_db(Super_db_mehod):
	def query(self):
		table = 'eventappsflyer_table'
		db = self.get_db()
		cursor = db.cursor()
		sql = """
		select * from %s order by time desc limit 6
		""" % table
		cursor.execute(sql)
		result = cursor.fetchall()
		_list = []
		for _object in result:
			try:
				_dict = {}
				request = json.loads(_object[1].encode('utf-8'))
				response_code = _object[2]
				response_data = json.loads(_object[3].encode('utf-8'))
				time = _object[4].encode('utf-8')
				_dict['time'] = time
				_dict['code'] = response_code
				_dict['app_id'] = request['args']['app_id']
				_data = json.loads(request['data'].encode('utf-8'))
				_eventValue_data =  json.loads(_data['eventValue'].encode('utf-8'))
				_af_param_2_data = json.loads(_eventValue_data['af_param_2'].encode('utf-8'))
				_dict['appsflyerKey'] = _data['appsflyerKey']
				_dict['android_id'] = _data['android_id']
				_dict['eventName'] = _data['eventName']
				_dict['productId'] = _af_param_2_data['productId']
				_dict['af_revenue'] = _eventValue_data['af_revenue']
				_dict['af_currency'] = _eventValue_data['af_currency']
				_dict['af_validated'] = _eventValue_data['af_validated']
				_dict['response'] = response_data
				_list.append(_dict)
			except Exception, e:
				print str(e)
				pass
		return _list

class Db_queryer:
	def __init__(self, method):
		self.m = method
		pass
	def query(self):
		return self.m.query()
		pass

class Insert_banner_db(Super_db_mehod):
	def insert(self, insert_dict):
		table = 'banner_table'
		db = self.get_db()
		cursor = db.cursor()
		if not self.check_table(table):
			sql = """
			create table %s(_id integer primary key autoincrement, 
			request text, response_code, response_data, time text)
			""" % table
			cursor.execute(sql)
			db.commit()
		sql = """
		insert into %s(request, response_code, response_data, time) 
		values(?, ?, ?, ?)
		""" % table
		cursor.execute(sql, (insert_dict['request'], insert_dict['response_code'],
			insert_dict['response_data'], self.get_db_time()))
		db.commit()
		pass


class Insert_interstital_db(Super_db_mehod):
	def insert(self, insert_dict):
		table = 'interstitial_table'
		db = self.get_db()
		cursor = db.cursor()
		if not self.check_table(table):
			sql = """
			create table %s(_id integer primary key autoincrement, 
			request text, response_code, response_data, time text)
			""" % table
			cursor.execute(sql)
			db.commit()
		sql = """
		insert into %s(request, response_code, response_data, time) 
		values(?, ?, ?, ?)
		""" % table
		cursor.execute(sql, (insert_dict['request'], insert_dict['response_code'],
			insert_dict['response_data'], self.get_db_time()))
		db.commit()
		pass

class Insert_reward_db(Super_db_mehod):
	def insert(self, insert_dict):
		table = 'reward_table'
		db = self.get_db()
		cursor = db.cursor()
		if not self.check_table(table):
			sql = """
			create table %s(_id integer primary key autoincrement, 
			request text, response_code, response_data, time text)
			""" % table
			cursor.execute(sql)
			db.commit()
		sql = """
		insert into %s(request, response_code, response_data, time) 
		values(?, ?, ?, ?)
		""" % table
		cursor.execute(sql, (insert_dict['request'], insert_dict['response_code'],
			insert_dict['response_data'], self.get_db_time()))
		db.commit()
		pass

class Insert_games_db(Super_db_mehod):
	def insert(self, insert_dict):
		table = 'games_table'
		db = self.get_db()
		cursor = db.cursor()
		if not self.check_table(table):
			sql = """
			create table %s(_id integer primary key autoincrement, 
			request text, response_code, response_data, time text)
			""" % table
			cursor.execute(sql)
			db.commit()
		sql = """
		insert into %s(request, response_code, response_data, time) 
		values(?, ?, ?, ?)
		""" % table
		cursor.execute(sql, (insert_dict['request'], insert_dict['response_code'],
			insert_dict['response_data'], self.get_db_time()))
		db.commit()
		pass

class Insert_trace_db(Super_db_mehod):
	def insert(self, insert_dict):
		table = 'trace_table'
		db = self.get_db()
		cursor = db.cursor()
		if not self.check_table(table):
			sql = """
			create table %s(_id integer primary key autoincrement, 
			request text, response_code, response_data, time text)
			""" % table
			cursor.execute(sql)
			db.commit()
		sql = """
		insert into %s(request, response_code, response_data, time) 
		values(?, ?, ?, ?)
		""" % table
		cursor.execute(sql, (insert_dict['request'], insert_dict['response_code'],
			insert_dict['response_data'], self.get_db_time()))
		db.commit()
		pass

class Insert_csta_db(Super_db_mehod):
	def insert(self, insert_dict):
		table = 'csta_table'
		db = self.get_db()
		cursor = db.cursor()
		if not self.check_table(table):
			sql = """
			create table %s(_id integer primary key autoincrement, 
			request text, response_code, response_data, time text)
			""" % table
			cursor.execute(sql)
			db.commit()
		sql = """
		insert into %s(request, response_code, response_data, time) 
		values(?, ?, ?, ?)
		""" % table
		cursor.execute(sql, (insert_dict['request'], insert_dict['response_code'],
			insert_dict['response_data'], self.get_db_time()))
		db.commit()
		pass

class Insert_accountkit_db(Super_db_mehod):
	def insert(self, insert_dict):
		table = 'accountkit_table'
		db = self.get_db()
		cursor = db.cursor()
		if not self.check_table(table):
			sql = """
			create table %s(_id integer primary key autoincrement, 
			request text, response_code, response_data, time text)
			""" % table
			cursor.execute(sql)
			db.commit()
		sql = """
		insert into %s(request, response_code, response_data, time) 
		values(?, ?, ?, ?)
		""" % table
		cursor.execute(sql, (insert_dict['request'], insert_dict['response_code'],
			insert_dict['response_data'], self.get_db_time()))
		db.commit()
		pass

class Insert_ssl08_db(Super_db_mehod):
	def insert(self, insert_dict):
		table = 'ssl08_table'
		db = self.get_db()
		cursor = db.cursor()
		if not self.check_table(table):
			sql = """
			create table %s(_id integer primary key autoincrement, 
			request text, response_code, response_data, time text)
			""" % table
			cursor.execute(sql)
			db.commit()
		sql = """
		insert into %s(request, response_code, response_data, time) 
		values(?, ?, ?, ?)
		""" % table
		cursor.execute(sql, (insert_dict['request'], insert_dict['response_code'],
			insert_dict['response_data'], self.get_db_time()))
		db.commit()
		pass

class Insert_tappsflyer_db(Super_db_mehod):
	def insert(self, insert_dict):
		table = 'tappsflyer_table'
		db = self.get_db()
		cursor = db.cursor()
		if not self.check_table(table):
			sql = """
			create table %s(_id integer primary key autoincrement, 
			request text, response_code, response_data, time text)
			""" % table
			cursor.execute(sql)
			db.commit()
		sql = """
		insert into %s(request, response_code, response_data, time) 
		values(?, ?, ?, ?)
		""" % table
		cursor.execute(sql, (insert_dict['request'], insert_dict['response_code'],
			insert_dict['response_data'], self.get_db_time()))
		db.commit()
		pass

class Insert_eventappsflyer_db(Super_db_mehod):
	def insert(self, insert_dict):
		table = 'eventappsflyer_table'
		db = self.get_db()
		cursor = db.cursor()
		if not self.check_table(table):
			sql = """
			create table %s(_id integer primary key autoincrement, 
			request text, response_code, response_data, time text)
			""" % table
			cursor.execute(sql)
			db.commit()
		sql = """
		insert into %s(request, response_code, response_data, time) 
		values(?, ?, ?, ?)
		""" % table
		cursor.execute(sql, (insert_dict['request'], insert_dict['response_code'],
			insert_dict['response_data'], self.get_db_time()))
		db.commit()
		pass

class Db_inserter:
	def __init__(self, method):
		self.m = method
		pass
	def insert(self, request, response_code, response_data):
		request_dict = {
		'args': request.args,
		'form': request.form,
		'data': request.data}
		insert_dict = {
		'request': json.dumps(request_dict),
		'response_code': response_code,
		'response_data': response_data
		}
		self.m.insert(insert_dict)
		pass
