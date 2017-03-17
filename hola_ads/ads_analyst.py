# -*- coding:utf-8 -*-
from flask import Flask, url_for, render_template, g, request, json
import sqlite3, time
import common_db, common, utils, category_thinker
DATABASE_ADS = utils.DATABASE_ADS
#g attr list
#_db_tool  common db tool
#

#ERROR DIC

class ads_analyst:
	def __init__(self):
		pass
	
	def get_db(self):
		db_tool = getattr(g, '_db_tool', None)
		if db_tool is None:
			db_tool = common_db.Common_db(DATABASE_ADS)
			g._db_tool = db_tool
		return db_tool
		pass

	def query(self, typical):
		db_tool = self.get_db
			
	def query_via_parameter(self, typical, request_id = '', icon = '', image = '', package_name = '', adtype = '', geo = '', dt_start = '', dt_end = '', page = '', offset = ''):
		db_tool = self.get_db()
		sql_page = page if page != '' else '1'
		sql_offset = offset if offset != '' else '10'
		try:
			sql_page = (int(sql_page) -1) * int(sql_offset)
		except:
			sql_page = '1'
		if typical == 'ads_list':
			sql = """
			SELECT ads.*, count( DISTINCT dt) AS cd, 
			count(*) AS cc , category
			FROM ads_table ads
			left join(
			select pkg, category from category_pkg_table
			) cp on ads.package_name = cp.pkg
			WHERE 1=1
			"""
			if package_name != '':
				sql += ' AND package_name like "%s" ' % ('%' + package_name + '%')
			elif adtype != '':
				sql += 'AND package_name in %s ' % self.query_package_list_by_adtype(adtype)
			if dt_start != '':
				sql += ' AND dt >=  "%s" ' % dt_start
			if dt_end != '':
				sql += ' AND dt <= "%s" ' % dt_end
			if geo != '':
				sql += ' AND geo = "%s" ' % geo
			sql += ' GROUP BY image, geo, category'
			sql += ' ORDER BY cc DESC LIMIT %s, %s' % (sql_page, sql_offset)
			print sql
			data = db_tool.query_by_sql(sql)
			return  json.dumps(data, ensure_ascii = False)
			pass
		if typical == 'query_page_via_type_geo_date':
			sql = """
			select count(distinct image) from ads_table where 1=1
			"""
			if package_name != '':
				sql += ' AND package_name like "%s" ' % ('%' + package_name + '%')
			elif adtype != '':
				sql += 'AND package_name in %s ' % self.query_package_list_by_adtype(adtype)
			if geo != '':
				sql += ' AND geo = "%s"' % geo
			if dt_start != '':
				sql += ' AND dt >= "%s"' % (dt_start)
			if dt_end != '':
				sql += ' AND dt <= "%s"' % (dt_end)
			print sql
			return json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False)
		if typical == 'get_selector':
			type_result = json.dumps(db_tool.query_sqlite_by_sql('select category from category_pkg_table group by category order by count(category) DESC'), 
				ensure_ascii = False)
			geo_reuslt = json.dumps(db_tool.query_by_sql('select geo from ads_table GROUP BY geo order by count(geo) DESC'), 
				ensure_ascii = False)
			result_list = [type_result, geo_reuslt]
			return json.dumps(result_list, ensure_ascii = False)
		if typical == 'category_test':
			sql = """
			select pkg from category_pkg_table where category = '%s'
			""" % adtype
			print sql
			package_list = db_tool.query_sqlite_by_sql(sql)
			package_list_str = '('
			for package in package_list:
				package_list_str += ' "%s", ' % package[0]
			package_list_str += '"nanimo") '
			sql = """
			SELECT *, count( DISTINCT dt) AS cd, 
			count(DISTINCT geo) AS cg, count(*) AS cc 
			FROM ads
			where package_name in %s
			""" % package_list_str
			print sql
			pretime = time.time()
			result = json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False)
			print result, time.time() - pretime
			pass

		#deprecate
		if typical == 'groupby_date_count':
			sql = """
			SELECT
			count(*),
			REPLACE(substr(event_time, 1, 6), '/', '-') d
			FROM
				ads_table
			WHERE
				image like '%s'
			GROUP BY
				d
			ORDER BY
				d
			""" % (image + '%')
			print sql
			return json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False)
		if typical == 'count_county_type_day':
			#select type, count(type) as c from ads GROUP BY type order by c desc;
			#select geo, count(geo) as c from ads GROUP BY geo order by c DESC;
			#select substr(event_time, 0, 12), count(substr(event_time, 0, 12)) as c from ads group by substr(event_time, 0, 12) order by c desc;
			type_result = json.dumps(db_tool.query_sqlite_by_sql('select category, 1 from category_pkg_table group by category order by count(category)'), ensure_ascii = False)
			geo_reuslt = json.dumps(db_tool.query_by_sql('select geo, count(geo) as c from ads_table GROUP BY geo order by c DESC'), ensure_ascii = False)
			date_result = json.dumps(db_tool.query_by_sql('select dt as d, count(dt) as c from ads_table group by dt order by d desc'), ensure_ascii = False)
			count = count = db_tool.query_by_sql('select count(*) from ads_table')
			result_list = [type_result, geo_reuslt, date_result, count]
			return json.dumps(result_list, ensure_ascii = False)
		
		pass
	def query_package_list_by_adtype(self, adtype):
		db_tool = self.get_db()
		sub_sql = """
		select pkg from category_pkg_table where category like '%s'
		""" % ('%' + adtype + '%')
		print sub_sql
		package_list = db_tool.query_sqlite_by_sql(sub_sql)
		package_list_str = '('
		for package in package_list:
			package_list_str += ' "%s", ' % package[0]
		package_list_str += '"nanimo") '
		return package_list_str
