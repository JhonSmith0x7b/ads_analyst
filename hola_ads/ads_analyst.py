# -*- coding:utf-8 -*-
from flask import Flask, url_for, render_template, g, request, json
import sqlite3, time, hashlib, datetime
import common_db, common, utils, category_thinker
DATABASE_ADS = utils.DATABASE_ADS
#g attr list
#_db_tool  common db tool
#

#ERROR DIC

#sql拼接
class Super_sql_decorator(object):
    def decorate(self, sql):
        pass

class Select_decorator(Super_sql_decorator):
    def __init__(self, args):
        self.args = ','.join(str(arg) for arg in args)
        pass
    def decorate(self, sql):
        return (sql + ' select ' + self.args) 
        pass

class From_decorator(Super_sql_decorator):
    def __init__(self, args):
        self.args = ','.join(str(arg) for arg in args)
    def decorate(self, sql):
        return (sql + ' from ' + self.args)
        pass

class Where_decorator(Super_sql_decorator):
    def __init__(self, args, in_args):
        self.args = args
        self.in_args = in_args
    def decorate(self, sql):
        a = lambda x, y: 'AND %s \'%s\' ' % (str(x), str(y)) if y != '' else ''
        b = lambda x, y: 'AND %s %s ' % (str(x), str(y)) if y != '' else ''
        return (sql + ' where 1 = 1 ' +  ' '.join(a(key, self.args[key]) for key in self.args)
        + ' '.join(b(key, self.in_args[key]) for key in self.in_args))
        pass

class Groupby_decorator(Super_sql_decorator):
    def __init__(self, args):
        self.args = ','.join(str(arg) for arg in args)
    def decorate(self, sql):
        return (sql + ' group by ' + self.args)
        pass

class Having_decorator(Super_sql_decorator):
    def __init(self, args):
        self.args = ','.join(str(arg) for arg in args)
    def decorate(self, sql):
        return (sql + 'having')
        pass
    
class Orderby_decorator(Super_sql_decorator):
    def __init__(self, args):
        self.args = ','.join(str(arg) for arg in args)
        pass
    def decorate(self, sql):
        return (sql + ' order by ' + self.args)

class Limit_decorator(Super_sql_decorator):
    def __init__(self, args):
        self.args = ','.join(str(arg) for arg in args)
        pass
    def decorate(self, sql):
        return (sql + ' limit ' + self.args)

class Sql_queryer(object):
    def __init__(self):
        self.sql = ''
        pass
    def query(self):
        pass
    def decorate(self, decorator):
        self.sql = decorator.decorate(self.sql)
        pass
###

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
			
	def query_via_parameter(self, typical, request_id = '', icon = '', image = '', 
		package_name = '', adtype = '', geo = '', dt_start = '', 
		dt_end = '', page = '', offset = '', rival_list = '', sourceapp = '', date_range = ''):
		db_tool = self.get_db()
		sql_page = page if page != '' else '1'
		sql_offset = offset if offset != '' else '10'
		try:
			sql_page = (int(sql_page) - 1) * int(sql_offset)
		except:
			sql_page = '1'
		sql_date_range = date_range
		if date_range != '':
			current_date = datetime.datetime.today().strftime('%Y%m%d')
			if date_range == '30':
				sql_date_range = common.delta_date(current_date, date_range)
			elif date_range == '7':
				sql_date_range = common.delta_date(current_date, date_range)
			else:
				sql_date_range = ''
		if typical == 'ads_list':
			data = ''
			if geo == 'US' and package_name == '' and rival_list == '' and adtype == '' and dt_start == '' and dt_end == '' and sourceapp == '' and int(sql_page) < 9980 and date_range != '7':
				query_table = 'thirty_monthdate_us_ad' if date_range == '30' else 'thirty_alldate_us_ad'
				q = Sql_queryer()
				q.decorate(Select_decorator(['*']))
				q.decorate(From_decorator([query_table]))
				q.decorate(Limit_decorator([sql_page, sql_offset]))
				print q.sql
				data = db_tool.query_sqlite_by_sql(q.sql)
			else:
				q = Sql_queryer()
				q.decorate(Select_decorator([
					' ads.*', 
					'  count(DISTINCT dt) AS cd', 
					'   count(*) as cc']))
				q.decorate(From_decorator(['ads ads']))
				q.decorate(Where_decorator({
					' package_name = ': package_name,
					'  dt >= ': dt_start,
					'   dt <= ': dt_end,
					'    dt > ': sql_date_range,
					'     geo = ': geo,
					'      app_name = ': sourceapp
					}, {
					' package_name in ': self.query_package_list_by_adtype(adtype),
					'  package_name in ': rival_list,
					}))
				q.decorate(Groupby_decorator([
					' image',
					'  geo'
					]))
				q.decorate(Orderby_decorator([
					' cd desc'
					]))
				q.decorate(Limit_decorator([
					sql_page,
					sql_offset
					]))
				print q.sql
				data = db_tool.query_by_sql(q.sql)
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
			q = Sql_queryer()
			q.decorate(Select_decorator([
				'count(distinct concat(image, geo))'
				]))
			q.decorate(From_decorator([
				'ads'
				]))
			q.decorate(Where_decorator({
				'package_name = ': package_name,
				'  dt >= ': dt_start,
				'   dt <= ': dt_end,
				'    dt > ': sql_date_range,
				'     geo = ': geo,
				'       app_name = ': sourceapp
				}, {
				'package_name in ': self.query_package_list_by_adtype(adtype),
				' package_name in ': rival_list
				}))
			print q.sql
			return json.dumps(db_tool.query_by_sql(q.sql), ensure_ascii = False)
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
			type_result = json.dumps(db_tool.query_sqlite_by_sql('select category, 1 from category_pkg_table group by category order by count(category)'), ensure_ascii = False)
			geo_reuslt = json.dumps(db_tool.query_by_sql('select geo, count(geo) as c from ads_table GROUP BY geo order by c DESC'), ensure_ascii = False)
			date_result = json.dumps(db_tool.query_by_sql('select dt as d, count(dt) as c from ads_table group by dt order by d desc'), ensure_ascii = False)
			count = count = db_tool.query_by_sql('select count(*) from ads_table')
			result_list = [type_result, geo_reuslt, date_result, count]
			return json.dumps(result_list, ensure_ascii = False)
		
		pass
	def query_package_list_by_adtype(self, adtype):
		if adtype == '':
			return ''
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
