# -*- coding:utf-8 -*-
from flask import Flask, url_for, render_template, g, request, json
import sqlite3
import sys;reload(sys);sys.setdefaultencoding('utf-8')
from  hola_ads import ads_analyst, common_db, common, utils
app = Flask(__name__)
app.debug = True
#g attr list
#_db_tool  common db tool
#

#ERROR DIC

@app.route('/pyanalysis', methods = ['get'])
def ads_analysis():
	doquery = request.args.get('doquery', '')
	if doquery != '':
		ads = get_ads()
		query_data = ads.query_via_parameter(typical = 'ads_list', package_name = request.args.get('package_name', ''), 
			type1 = request.args.get('type', ''), geo = request.args.get('geo', ''), 
			event_time = request.args.get('event_time', ''), page = request.args.get('page', ''), 
			offset = request.args.get('offset', ''), image = request.args.get('image', ''))
		return render_template('hola_ads/ads_analysis.htm', data = query_data.encode('utf-8')), 200 , {'Content-Type':'text/html;charset=utf-8'}
	return render_template('hola_ads/ads_analysis.htm', data = 1)
	pass

@app.route('/pyanalysis/pyquery', methods = ['post'])
def query_route():
	ads = get_ads()
	json_data = ads.query_via_parameter(typical = request.form.get('typical', ''), type1 = request.form.get('type', ''), geo = request.form.get('country', ''),
		event_time = request.form.get('date', ''), page = request.form.get('page', ''), offset = request.form.get('offset', ''))
	return json_data, 200, {'Content-Type':'text/json;charset=utf-8'}

@app.route('/pyanalysis/ad_detail')
def ad_detail():
	image = request.args.get('image', '')
	if image != '':
		ads = get_ads()
		query_data = ads.query_via_parameter(typical = 'groupby_date_count', image = image)
		return render_template('hola_ads/ad_detail.htm', data = query_data.encode('utf-8')), 200, {'Content-Type':'text/html;charset=utf-8'}
	return render_template('hola_ads/ad_detail.htm', data = '')

def get_ads():
	ads = getattr(g, 'ads', None)
	if ads is None:
		ads = ads_analyst.ads_analyst()
		g.ads = ads
	return ads

if __name__ == '__main__':
	app.run(host = '0.0.0.0')
