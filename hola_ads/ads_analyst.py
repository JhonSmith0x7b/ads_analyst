# -*- coding:utf-8 -*-
from flask import Flask, url_for, render_template, g, request, json
import sqlite3
import ads_analysis, common_db, common, utils
DATABASE_ADS = utils.DATABASE_ADS
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
			
	def query_via_parameter(self, typical, request_id = '', icon = '', image = '', package_name = '', adtype = '', geo = '', dt_start = '', dt_end = '', page = '', offset = ''):
		db_tool = getattr(g, '_db_tool', None)
		if db_tool is None:
			db_tool = common_db.Common_db(DATABASE_ADS)
			g._db_tool = db_tool
		sql_page = page if page != '' else '1'
		sql_offset = offset if offset != '' else '10'
		try:
			sql_page = (int(sql_page) -1) * int(sql_offset)
		except:
			sql_page = '1'
		if typical == 'ads_list':
			sql = """
			SELECT *, count( DISTINCT dt) AS cd, 
			count(DISTINCT geo) AS cg, count(*) AS cc 
			FROM ads
			WHERE 1=1
			"""
			if package_name != '':
				sql += ' AND package_name = "%s" ' % package_name
			if dt_start != '':
				sql += ' AND dt >=  "%s" ' % dt_start
			if dt_end != '':
				sql += ' AND dt <= "%s" ' % dt_end
			if geo != '':
				sql += ' AND geo = "%s" ' % geo
			if adtype != '':
				sql += ' AND adtype = "%s" ' % adtype
			sql += ' GROUP BY image, adtype'
			sql += ' ORDER BY cc DESC LIMIT %s, %s' % (sql_page, sql_offset)
			print sql
			return  json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False)
			pass
		if typical == 'groupby_date_count':
			sql = """
			SELECT
			count(*),
			REPLACE(substr(event_time, 1, 6), '/', '-') d
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
		if typical == 'query_page_via_type_geo_date':
			sql = """
			select count(distinct image) from ads where 1=1
			"""
			if package_name != '':
				sql += ' AND package_name = "%s"' % package_name
			if adtype != '':
				sql += ' AND adtype = "%s"' % adtype
			if geo != '':
				sql += ' AND geo = "%s"' % geo
			if dt_start != '':
				sql += ' AND dt >= "%s"' % (dt_start)
			if dt_end != '':
				sql += ' AND dt <= "%s"' % (dt_end)
			print sql
			return json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False)
		#deprecate
		if typical == 'count_county_type_day':
			#select type, count(type) as c from ads GROUP BY type order by c desc;
			#select geo, count(geo) as c from ads GROUP BY geo order by c DESC;
			#select substr(event_time, 0, 12), count(substr(event_time, 0, 12)) as c from ads group by substr(event_time, 0, 12) order by c desc;
			type_result = json.dumps(db_tool.query_by_sql('select adtype, count(adtype) as c from ads GROUP BY adtype order by c desc'), ensure_ascii = False)
			geo_reuslt = json.dumps(db_tool.query_by_sql('select geo, count(geo) as c from ads GROUP BY geo order by c DESC'), ensure_ascii = False)
			date_result = json.dumps(db_tool.query_by_sql('select dt as d, count(dt) as c from ads group by dt order by d desc'), ensure_ascii = False)
			count = count = db_tool.query_by_sql('select count(*) from ads')
			result_list = [type_result, geo_reuslt, date_result, count]
			return json.dumps(result_list, ensure_ascii = False)
		
		pass
