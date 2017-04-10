# -*- coding:utf-8 -*-
from flask import Flask, url_for, render_template, g, request, json
import sqlite3, time, hashlib
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
			
	def query_via_parameter(self, typical, request_id = '', icon = '', image = '', 
		package_name = '', adtype = '', geo = '', dt_start = '', 
		dt_end = '', page = '', offset = '', rival_list = '', sourceapp = ''):
		db_tool = self.get_db()
		sql_page = page if page != '' else '1'
		sql_offset = offset if offset != '' else '10'
		try:
			sql_page = (int(sql_page) - 1) * int(sql_offset)
		except:
			sql_page = '1'
		if typical == 'ads_list':
			sql = """
			SELECT ads.*, count( DISTINCT dt) AS cd, 
			count(*) AS cc
			FROM ads ads
			WHERE 1=1
			"""
			if package_name != '':
				sql += ' AND package_name = "%s" ' % package_name
			elif adtype != '':
				sql += 'AND package_name in %s ' % self.query_package_list_by_adtype(adtype)
			if dt_start != '':
				sql += ' AND dt >=  "%s" ' % dt_start
			if dt_end != '':
				sql += ' AND dt <= "%s" ' % dt_end
			if geo != '':
				sql += ' AND geo = "%s" ' % geo
			if rival_list != '':
				sql += ' AND package_name in %s' % rival_list
			if sourceapp != '':
				sql += ' AND app_name = "%s" ' % sourceapp
			sql += ' GROUP BY image, geo '
			sql += ' ORDER BY cd DESC LIMIT %s, %s' % (sql_page, sql_offset)
			print sql
			data = db_tool.query_by_sql(sql)
			data_category = []
			for row in data:
				result = self.query_adtype_via_package(row[14])
				if len(result) > 0:
					category = (result[0][0],)
					row += category
					data_category.append(row)
				else:
					category = ('', '')
					row += category
					data_category.append(row)
			data_s3 = []
			for row in data_category:
				s3_url = common.get_s3_url(row[6])
				row += (s3_url,)
				data_s3.append(row)
			return  json.dumps(data_s3, ensure_ascii = False)
			pass
		if typical == 'query_page_via_type_geo_date':
			sql = """
			select count(distinct concat(image, geo)) from ads where 1=1
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
			if rival_list != '':
				sql += ' AND package_name in %s' % rival_list
			if sourceapp != '':
				sql += ' AND app_name = "%s"' % sourceapp
			print sql
			return json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False)
		if typical == 'get_selector':
			type_result = json.dumps(db_tool.query_sqlite_by_sql('select category from category_pkg_table group by category order by count(category) DESC'), 
				ensure_ascii = False)
			geo_reuslt = json.dumps(db_tool.query_by_sql('select geo from ads GROUP BY geo order by count(geo) DESC'), 
				ensure_ascii = False)
			sourceapp_result = json.dumps(db_tool.query_by_sql('select app_name from ads group by app_name order by count(app_name) DESC'))
			result_list = [type_result, geo_reuslt, sourceapp_result]
			return json.dumps(result_list, ensure_ascii = False)
		if typical == 'get_rival_list':
			rival_type = ["tasty_treats", "slots"]
			sql = """
			select * from rival_table where rival in ("%s", "%s") order by rival
			""" % (rival_type[0], rival_type[1])
			rival_list = db_tool.query_sqlite_by_sql(sql)
			return_list = []
			for r in rival_type:
				return_list.append([])
			for rival in rival_list:
				for t in rival_type:
					if rival[2] == t:
						return_list[rival_type.index(t)].append(rival)
			return json.dumps(return_list, ensure_ascii = False)
			pass
		if typical == 'associate_package':
			sql = """
			select distinct package_name from ads
			"""
			print sql
			return json.dumps(db_tool.query_by_sql(sql), ensure_ascii = False)
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
		package_list = db_tool.query_sqlite_by_sql(sub_sql)
		package_list_str = '('
		for package in package_list:
			package_list_str += ' "%s", ' % package[0]
		package_list_str += '"nanimo") '
		return package_list_str
	def query_adtype_via_package(self, package):
		db_tool = self.get_db()
		sql = """
		select category from category_pkg_table where pkg = '%s'
		""" % package
		return db_tool.query_sqlite_by_sql(sql)
