from functionlist import *

target_list = ['http://blog.alyac.co.kr/category/%EA%B5%AD%EB%82%B4%EC%99%B8%20%EB%B3%B4%EC%95%88%EB%8F%99%ED%96%A5','http://blog.alyac.co.kr/category/%EC%95%85%EC%84%B1%EC%BD%94%EB%93%9C%20%EB%B6%84%EC%84%9D%20%EB%A6%AC%ED%8F%AC%ED%8A%B8']
removetag = ['알약','이스트 시큐리티']
baseurl = 'http://blog.alyac.co.kr'

def get_pagenum(targeturl):

	html = requesturl(targeturl).read().decode()
	soup = BeautifulSoup(html,'html.parser')
	return soup.select('#paging > span > a > span')[-1].text,html,soup

def pagelinksearch(targeturl,num):
	html = requesturl(targeturl+'?page={}'.format(num)).read().decode()
	soup = BeautifulSoup(html,'html.parser')
	linklist = list(map(lambda x:x['href'],soup.select('#searchList > div > ol > li > a')))
	return (linklist)

def alyac_crwrscript(collection,url):

	try:
		html = requesturl(url).read().decode()
		soup = BeautifulSoup(html,'html.parser')
		title = (soup.select('#container > div.content_wrap > div > div.post.sub_con > div.post_main > div.post_top > strong')[0].text)
		date = (soup.select('#container > div.content_wrap > div > div.post.sub_con > div.post_main > div.post_top > div > span')[0].text)
		date_split = (date.split()[0].split('.'))
		filter_date = date_split[1]+'.'+date_split[2]+'.'+date_split[0]
		taglist = [x for x in list(map(lambda x:x.text,soup.select('#container > div.content_wrap > div > div.post.sub_con > div.post_main > div.tagTrail > a'))) if not x in removetag]
		testdict={}
		texthtml = (html.split('<div class="container_postbtn">')[0])
		rawhtml = BeautifulSoup(texthtml,'html.parser')
	
		imgtag, imglist, bodyhtml = returnimg(rawhtml,url)
		bodyhtml = rawhtml.select('#container > div.content_wrap > div > div.post.sub_con > div.post_main > div.post_content')[0]
		bodyhtml = str(bodyhtml)
		#if dupcheck(collection,url,bodytext):
#			return None
		testdict['title'] = title
		testdict['date'] = filter_date
		testdict['imglist'] = imglist
		testdict['pdflist'] = returnpdf(bodyhtml,baseurl)
		testdict['txtlist'] = returntxt(bodyhtml)
		testdict['html'] = bodyhtml
		testdict['text'] = bodyhtml.get_text('\n').strip()
		testdict['relatedurl'] = returnrelatedurl(bodyhtml,baseurl)
		testdict['movie'] = returnyoutube(bodyhtml)
		testdict['tag'] = taglist

		return testdict

	except Exceptiond as e:
		error_link(e,url)



	
if __name__ == "__main__":

	client = MongoClient('127.0.0.1', 27017) # ip, port
	test1_db = client.pymongotest
	collection = test1_db.alyac ##mcafree collection

	for targeturl in target_list:

		try:
			pagenum, html, soup = get_pagenum(targeturl)
		
			for i in range(1,int(pagenum)+1):

				for link in pagelinksearch(targeturl,i):
					if 'http:' in link:
						
						mongohelp(collection,alyac_crwrscript,link)
					else:
						
						mongohelp(collection,alyac_crwrscript,baseurl+link)

		except Exception as e:
			print(e)
			client.close()	

	print("done")
	client.close()