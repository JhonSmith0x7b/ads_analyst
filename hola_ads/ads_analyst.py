# -*- coding:utf-8 -*-
from flask import Flask, url_for, render_template, g, request, json
import sqlite3
import ads_analysis, common_db, common, utils
DATABASE_ADS = 'static/db/fbad.db'
#g attr list
#_db_tool  common db tool
#

#ERROR DIC

class ads_analyst:
	def __init__(self):
		pass
		
	def query(self, typical):
		db_tool = getattr(g, '_db_tool', None)
		if db_tool is None:
			db_tool = common_db.Common_db(DATABASE_ADS)
			g._db_tool = db_tool
		db_tool.init_db()
		if typical == 'page':
			return json.dumps(db_tool.query_by_sql('select * from ads limit %s, %s' % (request.form['start'], request.form['offset'])), ensure_ascii = False), 200, {'Content-Type':'text/json;charset=utf-8'}
		if typical== 'get_date_list':
			return json.dumps(db_tool.query_by_sql('select distinct substr(event_time, 0, 12) from ads order by event_time'), ensure_ascii = False), 200, {'Content-Type':'text/json;charset=utf-8'}
		if typical == 'date':
			return json.dumps(db_tool.query_by_sql('select * from ads where event_time like "%s"limit %s, %s' % (request.form['date'] + '%', request.form['start'], request.form['offset'])), ensure_ascii = False), 200, {'Content-Type':'text/json;charset=utf-8'}
		if typical == 'count_county_type_day':
			#select type, count(type) as c from ads GROUP BY type order by c desc;
			#select geo, count(geo) as c from ads GROUP BY geo order by c DESC;
			#select substr(event_time, 0, 12), count(substr(event_time, 0, 12)) as c from ads group by substr(event_time, 0, 12) order by c desc;
			type_result = json.dumps(db_tool.query_by_sql('select type, count(type) as c from ads GROUP BY type order by c desc'), ensure_ascii = False)
			geo_reuslt = json.dumps(db_tool.query_by_sql('select geo, count(geo) as c from ads GROUP BY geo order by c DESC'), ensure_ascii = False)
			date_result = json.dumps(db_tool.query_by_sql('select substr(event_time, 0, 12) as d, count(substr(event_time, 0, 12)) as c from ads group by substr(event_time, 0, 12) order by d desc'), ensure_ascii = False)
			count = count = db_tool.query_by_sql('select count(*) from ads')
			result_list = [type_result, geo_reuslt, date_result, count]
			return json.dumps(result_list, ensure_ascii = False), 200, {'Content-Type':'text/json;charset=utf-8'}
		if typical == 'query_via_type_country_id':
			sql = 'select * from ads where type = "%s" and geo = "%s" and event_time like "%s" limit %s, %s' % ((request.form['type'] if request.form['type'] != '' else 'type'), (request.form['country'] if request.form['country'] != '' else 'geo'), (request.form['date'] + '%' if request.form['date'] != '' else '%'), ((int(request.form['page']) - 1) * int(request.form['offset']) if request.form['page'] != '' else '0'), (request.form['offset'] if request.form['offset'] != '' else '10'))
			print sql
			return json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False), 200, {'Content-Type':'text/json;charset=utf-8'}
		if typical == 'query_page_via_type_country_date':
			sql = 'select count(*) from ads where type = "%s" and geo = "%s" and event_time like "%s"' % ((request.form['type'] if request.form['type'] != '' else 'type'), (request.form['country'] if request.form['country'] != '' else 'geo'), (request.form['date'] + '%' if request.form['date'] != '' else '%'))
			print sql
			return json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False), 200, {'Content-Type':'text/json;charset=utf-8'}
		if typical == 'query_top10':
			sql = 'select count() as c, * from ads GROUP BY image order by c desc limit 10'
			return json.dumps(db_tool.query_by_sql(sql), ensure_ascii =False), 200, {'Content-Type':'text/json;charset=utf-8'}
		if typical == 'query_ad_analysis_via_date':
			sql = 'select count(), substr(event_time, 0, 12) as d from ads where image = "%s" group by d order by d' % (request.form['date'])
			return json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False), 200, {'Content-Type':'text/json;charset=utf-8'}

	def query_via_parameter(self, typical, request_id = '', icon = '', image = '', package_name = '', type1 = '', geo = '', event_time = '', page = '', offset = ''):
		db_tool = getattr(g, '_db_tool', None)
		if db_tool is None:
			db_tool = common_db.Common_db(DATABASE_ADS)
			g._db_tool = db_tool
		db_tool.init_db()
		sql_page = page if page != '' else '1'
		sql_offset = offset if offset != '' else '10'
		sql_page = (int(sql_page) -1) * int(sql_offset)
		if typical == 'ads_list':
			sql = """
			SELECT a.*, c.cd, c.cg, c.cc FROM ads a, 
			(SELECT image, count( DISTINCT substr(event_time, 0, 12)) AS cd, 
			count(DISTINCT geo) AS cg, count() AS cc 
			FROM ads GROUP BY image || type) c 
			WHERE a.image = c.image 
			"""
			if package_name != '':
				sql += ' AND a.package_name = "%s" ' % package_name
			if event_time != '':
				sql += ' AND substr(a.event_time, 0, 12) =  "%s" ' % event_time
			if geo != '':
				sql += ' AND a.geo = "%s" ' % geo
			if type1 != '':
				sql += ' AND a.type = "%s" ' % type1
			sql += ' GROUP BY a.image || a.type ORDER BY c.cc DESC LIMIT %s, %s' % (sql_page, sql_offset)
			print sql
			return  json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False)
			pass
		if typical == 'groupby_date_count':
			sql = """
			SELECT
			count(*),
			REPLACE(substr(event_time, 0, 7), '/', '-') d
			FROM
				ads
			WHERE
				image like '%s'
			GROUP BY
				d
			ORDER BY
				d
			""" % (image + '%')
			print sql
			return json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False)
		#deprecate
		if typical == 'count_county_type_day':
			#select type, count(type) as c from ads GROUP BY type order by c desc;
			#select geo, count(geo) as c from ads GROUP BY geo order by c DESC;
			#select substr(event_time, 0, 12), count(substr(event_time, 0, 12)) as c from ads group by substr(event_time, 0, 12) order by c desc;
			type_result = json.dumps(db_tool.query_by_sql('select type, count(type) as c from ads GROUP BY type order by c desc'), ensure_ascii = False)
			geo_reuslt = json.dumps(db_tool.query_by_sql('select geo, count(geo) as c from ads GROUP BY geo order by c DESC'), ensure_ascii = False)
			date_result = json.dumps(db_tool.query_by_sql('select substr(event_time, 0, 12) as d, count(substr(event_time, 0, 12)) as c from ads group by substr(event_time, 0, 12) order by d desc'), ensure_ascii = False)
			count = count = db_tool.query_by_sql('select count(*) from ads')
			result_list = [type_result, geo_reuslt, date_result, count]
			return json.dumps(result_list, ensure_ascii = False)
		if typical == 'query_page_via_type_country_date':
			sql = 'select count(distinct image), image from ads where type = "%s" and geo = "%s" and event_time like "%s"' % ((request.form['type'] if request.form['type'] != '' else 'type'), (request.form['country'] if request.form['country'] != '' else 'geo'), (request.form['date'] + '%' if request.form['date'] != '' else '%'))
			print sql
			return json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False)
		
		pass
