from functionlist import *

baseurl = 'http://blog.alyac.co.kr'
removetag = ['알약','이스트 시큐리티']
def alyac_crwrscript(url):

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

		bodytext = bodyhtml.get_text('\n').strip()
		
		bodyhtml = str(bodyhtml)


		testdict['title'] = title
		testdict['date'] = filter_date
		testdict['imglist'] = imglist
		testdict['pdflist'] = returnpdf(str(bodyhtml),baseurl)
		testdict['txtlist'] = returntxt(bodyhtml)
		testdict['html'] = bodyhtml
		testdict['text'] = bodytext
		testdict['relatedurl'] = returnrelatedurl(bodyhtml,baseurl)
		testdict['movie'] = returnyoutube(bodyhtml)
		testdict['tag'] = taglist

		return testdict

	except Exceptiond as e:
		error_link(e,url)

if __name__ == '__main__':
	testurl = 'http://blog.alyac.co.kr/748?category=750247'

	print(alyac_crwrscript(testurl)['relatedurl'])
