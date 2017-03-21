# -*- coding:utf-8 -*-
import hashlib

def get_s3_url(url):
	return 'http://imgcn.dataverse.cn/%s' % get_s3_uri
	pass

def get_s3_uri(url):
	md5 = get_md5(url)
	return 'cad/%s/%s.jpg' % (md5[0: 3], md5)
	pass

def get_md5(url):
	md5 = hashlib.md5()
	md5.update(url)
	return md5.hexdigest()
	pass