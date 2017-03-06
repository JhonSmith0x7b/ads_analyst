# -*- coding:utf-8 -*-
from datetime import datetime


def coverttime_via_format(time_str, format):
	return datetime.strptime(time_str, format)
	pass