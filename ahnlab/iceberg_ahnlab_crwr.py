from iceberglist import *


pageurl = 'http://ahnlabasec.tistory.com'
baseurl = 'http://ahnlabasec.tistory.com/category/%EC%95%85%EC%84%B1%EC%BD%94%EB%93%9C%20%EC%A0%95%EB%B3%B4'
boardurl = 'http://ahnlabasec.tistory.com/category/%EC%95%85%EC%84%B1%EC%BD%94%EB%93%9C%20%EC%A0%95%EB%B3%B4?page={}'
# 악성코드 정보 
#content > div > div.titleWrap > h2 > a
rmurl = ['http://ahnlabasec.tistory.com/943?category=342979','http://ahnlabasec.tistory.com/2?category=342979']
baseurl2 = 'http://ahnlabasec.tistory.com/category/%EC%B7%A8%EC%95%BD%EC%A0%90%20%EC%A0%95%EB%B3%B4'
boardurl2 = 'http://ahnlabasec.tistory.com/category/%EC%B7%A8%EC%95%BD%EC%A0%90%20%EC%A0%95%EB%B3%B4?page={}' 

def ioc_vulnervalitbity():

	basehtml2 = (requesturl(baseurl2).read().decode())
	soup2 = BeautifulSoup(basehtml2,'html.parser')


	pagenum2 = int(soup2.select('#paging > span > a > span')[-1].text)
	print("page : "+str(pagenum2))
	link_list2 = get_link(basehtml2)

	try:
		for i in link_list2:
			
			mongohelp(collection,ahnlab_crwrscript,i)

		#페이지 넘기기
		for i in range(2,pagenum2+1):
			#print(boardurl.format(i))
			pagehtml2 = (requesturl(boardurl2.format(i)).read().decode())
			link_list2 = get_link(pagehtml2)
			#print(len(link_list))
			for i in link_list2:
		
				mongohelp(collection,ahnlab_crwrscript,i)

	except:
		error_link(e,url)
		client.close()

def ioc_malware():
	basehtml = (requesturl(baseurl).read().decode())
	soup = BeautifulSoup(basehtml,'html.parser')
	test= 0
	pagenum = int(soup.select('#paging > span > a > span')[-1].text)
	print("page : "+str(pagenum))
	link_list = get_link(basehtml)
	
	try:
		for i in link_list:
			1+1
			mongohelp(collection,ahnlab_crwrscript,i)

		#페이지 넘기기
		for i in range(2,pagenum+1):
			#print(boardurl.format(i))
			pagehtml = (requesturl(boardurl.format(i)).read().decode())
			link_list = get_link(pagehtml)
			#print(len(link_list))
			for i in link_list:
		
				mongohelp(collection,ahnlab_crwrscript,i)

	except:
		error_link(e)
		client.close()

def ahnlab_crwrscript(collection,url): # 무조건 dic  input = url output = json {key:value}
	try:
		html = (requesturl(url).read().decode())

		headsoup = BeautifulSoup(html,'html.parser').select('#content > div.entry > div.titleWrap')[0]
		testdict = {}
		title = (headsoup.select('h2 > a')[0].text)
		date = (headsoup.select('span.date')[0].text)
		date_split = (date.split()[0].split('.'))
		filter_date = date_split[1]+'.'+date_split[2]+'.'+date_split[0]		

		htmlsoup = BeautifulSoup(html,'html.parser')		
		onefilter = '<div class=\"container_postbtn\">'
		onehtml = html.split(onefilter)

		if len(onehtml) !=2:
			raise NotSplitError

		onehtml = BeautifulSoup(onehtml[0],'html.parser')

		test = (onehtml.select('div.entry > div.article'))

		rawhtml = (onehtml.select('#content > div.entry > div.article')[0])

		testdict.update(returnimg(rawhtml,url,baseurl))
		
		bodytext = BeautifulSoup(testdict['html'],'html.parser').text
		if(dupcheck(collection,url,bodytext)):
			
			return None
		testdict['title'] = title
		testdict['date'] = filter_date
		testdict['text'] = bodytext # 연관분석에 사용할 것(그림이 중간중간 들어가는데 return text + text  )

		return testdict
	except Exception as e: # return None 
		error_link(e,url)
		

def get_link(html):
	''' 
	urllink = list(map(lambda x:x.attrs['href'],(soup.select('#content > div > div.titleWrap > h2 > a'))))
	print(len(urllink))
	urllink = list(map(lambda x:pageurl+x,filter(lambda x : not pageurl in x, urllink)))
	return urllink # type : list
	'''
	onefilter = '<div id=\"searchList\" class=\"nonEntry\">'
	twofilter = '</ol>'

	onehtml = html.split(onefilter)
	twohtml = onehtml[1].split(twofilter)[0]
	rawhtml = BeautifulSoup(twohtml,'html.parser')
	link_list = list(map(lambda x:x.attrs['href'],rawhtml.select('a')))
	for n,i in enumerate(link_list):
		if not pageurl in i:
			link_list[n]=pageurl+i
	
	print(len(link_list))
	return link_list

if __name__ == "__main__":

	client = MongoClient('127.0.0.1', 27017) # ip, port
	test1_db = client.iceberg
	collection = test1_db.ahnlab
	print("malware")
	ioc_malware()
	print("vulnervalitbity")
	ioc_vulnervalitbity()
	
	print("done")
	client.close()

