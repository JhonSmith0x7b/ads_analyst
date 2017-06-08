# -*- coding:utf-8 -*-
from flask import Flask, url_for, render_template, g, request, json, current_app,Blueprint
import urllib, urllib2, zlib, re
import getpic_common as com
get_pic =  Blueprint('get_pic' , __name__, template_folder = com.TEMPLATES_PATH)


@get_pic.route('/gppic', methods = ['get', 'post'])
def hello():
	return render_template('helloworld.htm'), 200, {'Content-Type': 'text/html;charset=utf-8'}

@get_pic.route('/gppic/get', methods = ['get', 'post'])
def get_pic1():
	package_name = request.form.get('package_name', 'com.google.android.apps.plus')
	url = 'https://android.clients.google.com/fdfe/details?doc=%s' % package_name
	print url
	headers = {
	    'X-Ad-Id': 'fc728fdc-9aa4-4c00-afec-1090ba53b5a4',
	    'X-DFE-Device-Id': '38ada555195e230f',
	    'Authorization': com.AUTH,
	    'Host': 'android.clients.google.com',
    	'User-Agent': 'Android-Finsky/7.8.36.P-all%20%5B0%5D%20%5BPR%5D%20156940515 (api=3,versionCode=80783600,sdk=23,device=D5833,hardware=qcom,product=D5833,platformVersionRelease=6.0.1,model=D5833,buildId=23.5.A.0.575,isWideScreen=0)',
	    'Accept': ' */*',
	    'Accept-Encoding': 'deflate, gzip'
	}
	req = urllib2.Request(url = url, headers = headers)
	resp = urllib2.urlopen(req)
	decompressed_data=zlib.decompress(resp.read(), 16 + zlib.MAX_WBITS)
	#pic
	pic_list = re.findall(r'https://lh3.googleusercontent.com[\w, \., /, -]*', 
		decompressed_data)[:10]
	for p in pic_list:
		if p[-1] == 'H':
			try:
				req = urllib2.Request(url = p)
				resp = urllib2.urlopen(req, timeout = 10)
				print 'H'
			except Exception, e:
				print 'no H %s' % str(e)
				pic_list[pic_list.index(p)] = p[:-1]
	#video
	video_list = re.findall(r'https://www.youtube.com/watch[\w\./\-?=]*|https://youtu.be[\w\./\-?=]*', 
		decompressed_data)[:5]
	#briefs
	parttern = re.compile(r'Offered.*Downloads', re.MULTILINE|re.DOTALL)
	brief = parttern.findall(decompressed_data)
	briefs = []
	for _ in re.findall(r'[\x20-\x7e]*', brief[0]):
	    if _ != '' and len(_) > 6:
	        briefs.append(_)
	#permissions
	permissions = re.findall(r'android.permission[a-zA-Z\._]*', decompressed_data)

	re_data = [pic_list, video_list, briefs, permissions]
	return json.dumps(re_data), 200, {'Content-Type': 'text/json;charset=utf-8'}
	pass

















if __name__ == '__main__':
	app.run(host = '0.0.0.0', threaded=False)