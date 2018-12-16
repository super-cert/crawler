#-*- coding: utf-8 -*-
import urllib.request
import requests
import re
import hashlib
from pymongo import MongoClient
from pymongo import errors
from bs4 import BeautifulSoup
import inspect
import time
import sys
#import traceback
import json

##help 2.0 verision

def convert_date_number(datestring):

	temp = datestring.lower().replace(' ','')

	if temp == 'january' or temp == 'jan':
		return '01' 
	elif temp == 'february' or temp == 'feb':
		return '02'
	elif temp == 'march' or temp =='mar':
		return '03'

	elif temp == 'april' or temp =='apr':
		return '04' 
	elif temp == 'may' :
		return '05'
	elif temp == 'june' or temp == 'jun':
		return '06'
	elif temp == 'july' or temp == 'jul':
		return '07'
	elif temp == 'august' or temp == 'aug':
		return '08'
	elif temp == 'september' or temp == 'sep':
		return '09'
	elif temp == 'october' or temp == 'oct':
		return '10'
	elif temp == 'november' or temp == 'nov' :
		return '11'
	elif temp == 'december' or temp == 'dec':
		return '12'
	else:
		return None

def requestsurl(link):
	Custom_Header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

	return requests.get(link,Custom_Header)


def mongohelp2(**kargs): #defname = ahnlab_crwscript mongohelp  ahnlab_crwscript json 
	try:
		testdict = {}
		testdict['link'] = kargs['link']
		sample = kargs['script'](**kargs)
		if sample is None:
			return
		
		testdict.update(sample)
		mongodbinsert(kargs['collection'],testdict)
	except Exceptiond as e:
		error_link(e,kargs['link'])

def mongohelp(collection,defname,url,**kargs): #defname = ahnlab_crwscript mongohelp  ahnlab_crwscript json
	try:
		testdict = {}
		testdict['link'] = url
		for key,value in kargs.items():
			testdict[key] = value
		
		sample = defname(collection,url)
		
		if sample is None:
			return
		
		testdict.update(sample)
		mongodbinsert(collection,testdict)
	except Exception as e:
		error_link(e,url)

def mongodbinsert(collection,testdic): # 실제 insert 하는 부분
	testdic['_id']  = hashfunc(testdic['link']+str(testdic['text'])) # 기본키 역할을 하는 '_id' 는 link+date로 이루어진 해쉬로 중복 충돌을 위한 기능

	try:
		collection.insert_one(testdic)
	except errors.DuplicateKeyError: #중복 시 넘어감
		pass
#404 에러 
def hashfunc(data):

	return hashlib.md5(data.encode()).hexdigest()


def error_link(e,url):
	#/home/Project/crwr/error_link
	with open('error_link','a') as files:
			files.write(inspect.stack()[1][3]+" : ")
			files.write(str(e)+' ')
			files.write(str(url)+' ')
			files.write(time.asctime()+' \n')

def returnimg(rawhtml,url): # text 
	
	#bodyhtml = str(rawhtml).replace('(','\(').replace('\)','\)')
	bodyhtml =str(rawhtml)
	imgtag = list(set(rawhtml.findAll('img', attrs = {'src' : True})))	
	#image encoding filter
	
	for i in imgtag:
		if str(i) in bodyhtml:
			if 'base64' in i['src'][:25]:
				bodyhtml = re.sub(r'(<img.+?src=\").+?base64.+?\"','\g<1>'+'encodingemage\"',str(bodyhtml))
	
	bodyhtml = BeautifulSoup(bodyhtml,'html.parser')
	imgtag = list(set(bodyhtml.findAll('img', attrs = {'src' : True})))
	imglist = list(map(lambda x:x['src'],imgtag))

	for n, link in enumerate(imglist): # 여기서 상대경로를 절대경로로 바꿔줌 
		
		if not 'https:' in link:
			if not 'http' in link:
				imglist[n]=url.split('/')[2]+link
	
	if len(imgtag):
		
		for i in range(0,len(imglist)):
			
			regex = str(imgtag[i]).replace('\\','\\\\').replace('(','\(').replace(')','\)').replace('.','\.').replace('?','\?').replace('[','\[').replace(']','\]').replace('+','\+')

			change = '[image:{}]'.format(str(imglist[i]))
			bodyhtml =re.sub(regex,change,str(bodyhtml))


	testdict = {}
	testdict['imglist'] = imglist
	testdict['movielist'] =  list(set([x.group(2) for x in re.finditer("(<a.+?href=\"(https:\/\/(((www\.)?youtube\.com)|(youtu\.be)).+?)\">|<iframe.+?src=\"(.+?)\".+?>.+?/iframe>)",bodyhtml)]))
	testdict['txtlist'] = list(set(re.findall(r'<a.+?href=\"(.+?\.(txt|doc|docx|ppt|hwp|xslx|csv))\"', bodyhtml)))
	testdict['pdflist'] = []
	tmppdf = list(set([x.group(0) for x in re.finditer(r'<a.+?href=\"(.+?\.pdf)\"', bodyhtml)]))
	for i in tmppdf:
		for j in re.split(r'<a.+?href=\"(.+?)\"',i):
			if j.endswith('.pdf'):
				testdict['pdflist'].append(j)
	testdict['relatedlist'] = [x for x in list(set(re.findall(r'<a.+?href=\"(.+?)\"',bodyhtml))) if not x in list(set(testdict['pdflist']+testdict['movielist']+testdict['txtlist']+testdict['imglist']))]
	testdict['html'] = str(bodyhtml)
	return testdict
'''
if dupcheck(collection,url,date):
			return None
'''			

def dupcheck(collection,url,text): # 중복체크 
	
	target = collection.find_one({"_id":hashfunc(url+str(text))}) 		#1. url+date의 대한 hash값을 검사하고 동일한게 없는상태에서 링크가 있다면 날짜가 바뀌엇다고 간주하고 검증 
	if target is None: 
		
		try:
			if not collection.find_one({"link": url}) is None: #
				print("somethingchanged ", end='') 
				
				with open("update_link",'a') as files:
					files.write(url,'\n')
					files.write(" updated","\n")
					files.write(date,'\n')
				return
			else:
				
				return 0
		except:
			
			pass
	else :
		
		if not collection.find_one({"link": url}) is None:
			return 1

	return

class NotSplitError(Exception):	# Exception을 상속받아서 에러 전달
	def __init__(self):
		super().__init__('not split!!!')
		
def returnyoutube(html):
	
	return list(set([x.group(1) for x in re.finditer("<a.+?href=\"(https:\/\/(((www\.)?youtube\.com)|(youtu\.be)).+?)\">",html)]))
	# return list(set(re.findall(r'<a href="(https:\/\/youtu\.be.+?)">',str(html))))
	# +list(set(re.findall(r'<iframe.+?src=\"(.+?)\".+?>.+?/iframe>',str(html))))
	# +list(set(re.findall(r'<a.+?href="(https:\/\/youtube\.com.+?)">',str(html))))

	
def returnrelatedurl(html,baseurl):
	rmlist = ['jpg','jpeg','bmp','gif','png','pdf','mp4','xml']
	test = list(set(re.findall(r'<a.+?href=\"(.+?)\".+?/a>',html)))
	for n, i in enumerate(test):
		if not 'http' in i and not 'https' in i:
			test[n] = baseurl+i

	return list(filter(lambda x: not x.split('.')[-1] in rmlist, test))
	

def returntxt(html):
	try:
		return list(set(re.findall(r'<a.+?href=\"(.+?\.[txt|doc|docx|ppt|hwp|xslx|csv])\"', html)))
	except IndexError as e:
		if 'list index out of range' in str(e):
			return None
		else:
			print(e)

def returnpdf(html,baseurl):
	try:
		test = list(set(re.findall(r'<a.+?href=\"(.+?\.pdf)\"', html)))
		for n, i in enumerate(test):
			if not 'http' in i and not 'https' in i:
				test[n] = baseurl+i		
		return test
	except IndexError as e:
		if 'list index out of range' in str(e):
			return None
		else:
			print(e)


def requesturl(link):

	req = urllib.request.Request(
		link, 
		data=None, 
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		}
	)
	
	return urllib.request.urlopen(req)

