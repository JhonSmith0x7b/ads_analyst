# -*- coding:utf-8 -*-
from flask import Flask, url_for, render_template, g, request, json
import sqlite3
import sys;reload(sys);sys.setdefaultencoding('utf-8')
from  hola_ads import ads_analyst, common_db, common, utils, category_thinker
import time
app = Flask(__name__)
app.debug = True
#g attr list
#_db_tool  common db tool
#

#ERROR DIC

@app.route('/pyanalyst', methods = ['get'])
def ads_analysis():
	if not check_ip():
		return 'IP Forbidd'
	doquery = request.args.get('doquery', '')
	if doquery != '':
		ads = get_ads()
		pre_time = time.time()
		query_data = ads.query_via_parameter(typical = 'ads_list', package_name = request.args.get('package_name', ''), 
			adtype = request.args.get('adtype', ''), geo = request.args.get('geo', ''), 
			dt_start = request.args.get('dt_start', ''), dt_end = request.args.get('dt_end', ''), 
			page = request.args.get('page', ''), 
			offset = request.args.get('offset', ''), image = request.args.get('image', ''))
		query_time = time.time() - pre_time
		return render_template('hola_ads/ads_analyst.htm', data = query_data.encode('utf-8'),
			adtype = request.args.get('adtype', ''), geo = request.args.get('geo', ''), 
			dt_start = request.args.get('dt_start', ''), dt_end = request.args.get('dt_end', ''), 
			page = request.args.get('page', ''), package_name = request.args.get('package_name', ''),
			query_time = query_time), 
		200 , {'Content-Type':'text/html;charset=utf-8'}
	return render_template('hola_ads/ads_analyst.htm', data = 1, adtype = '', geo = '', 
		dt_start = '', dt_end = '', page = '', package_name = '')
	pass

@app.route('/pyanalyst/pyquery', methods = ['post'])
def query_route():
	if not check_ip():
		return 'IP Forbidd'
	ads = get_ads()
	json_data = ads.query_via_parameter(typical = request.form.get('typical', ''), 
		adtype = request.form.get('adtype', ''), geo = request.form.get('geo', ''),
		dt_start = request.form.get('dt_start', ''), dt_end = request.form.get('dt_end', ''), 
		package_name = request.form.get('package_name', ''),
		page = request.form.get('page', ''), offset = request.form.get('offset', ''))
	return json_data, 200, {'Content-Type':'text/json;charset=utf-8'}

@app.route('/pyanalyst/ad_detail')
def ad_detail():
	if not check_ip():
		return 'IP Forbidd'
	image = request.args.get('image', '')
	if image != '':
		ads = get_ads()
		query_data = ads.query_via_parameter(typical = 'groupby_date_count', image = image)
		return render_template('hola_ads/ad_detail.htm', data = query_data.encode('utf-8')), 
		200, {'Content-Type':'text/html;charset=utf-8'}
	return render_template('hola_ads/ad_detail.htm', data = '')


def get_ads():
	ads = getattr(g, 'ads', None)
	if ads is None:
		ads = ads_analyst.ads_analyst()
		g.ads = ads
	return ads

def check_ip():
	remote_ip = request.remote_addr
	if remote_ip in utils.ALLOW_IP_LIST:
		return True

if __name__ == '__main__':
	app.run(host = '0.0.0.0')
