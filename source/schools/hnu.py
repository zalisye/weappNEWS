from sqlConnect import sqlConnect
from myHTMLParser import myHTMLParser
import urllib2
import re
import sys
import traceback

srcprefix = "http://news.hnu.edu.cn"
dateprefix = '2017-'
allImgUrl = []

class titleParser(myHTMLParser):
	"""docstring for titleParser"""
	def __init__(self):
		super(titleParser, self).__init__()

	def handle_starttag(self, tag, attrs):
		if(tag == 'a'):
			for i, j in enumerate(attrs):
				if(j[0] == 'href'):
					self._url.append(j[1])
				elif(j[0] == 'title'):
					self._title.append(j[1])
		elif(tag == 'img'):
			for i, j in enumerate(attrs):
				if(j[0] == 'src'):
					self._imgUrl = srcprefix + j[1]

	def handle_data(self, data):
		self._context += data
		if(self.lasttag == 'div'):
			self._context += '\n'


def getContext(c_url):
	ret = []
	for i, url in enumerate(c_url):
		try :
			print("handling %dth context from hnu" %(i + 1))
			link = urllib2.urlopen(url)
			srcCode = link.read()
			newsPattern = ' <div class="conterlist_conter">[\s\S]+?<div class="mian_conterlist_btton">'
			newsblock = re.compile(newsPattern).findall(srcCode)[0]
			newsblock = re.sub(r'<span.+?>', '', newsblock)
			newsblock = re.sub(r'</span>', '', newsblock)
			parser = titleParser()
			stri = parser.unescape(newsblock)
			parser.feed(stri)
			allImgUrl.append(parser.imgUrl)
			stri = parser.context
			parser.close()
			ret.append(stri)
		except :
			ret.append('error')
			print("error when handling %dth context from hnu" %(i + 1))
			print(traceback.print_exc())

	return ret


def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	test = sqlConnect("hnu", 10)
	tParser = titleParser()
	link = urllib2.urlopen("http://news.hnu.edu.cn/zhyw/")
	srcCode = link.read()
	srcCode = re.compile(r'<div class="main_conterlist">[\S\s]+?<div class="page">').findall(srcCode)
	srcCode = srcCode[0]
	tParser.feed(srcCode)
	pattern = r'[[0-9]{2}-[0-9]{2}]'
	allDate = re.compile(pattern).findall(srcCode)
	for i in range(len(allDate)) :
		allDate[i] = dateprefix + allDate[i].lstrip('[').rstrip(']')
	allTitle = tParser.title
	allUrl = tParser.url

	temtit = []
	temurl = []
	temdt = []
	for i in range(len(allUrl)):
		if(allUrl[i][0] == '/'):
			temtit.append(allTitle[i])
			temurl.append(srcprefix + allUrl[i])
			temdt.append(allDate[i])

	test.date = temdt
	test.title = temtit
	test.contextUrl = temurl
	test.context = getContext(test.contextUrl)
	test.imgUrl = allImgUrl
	test.updateSql()
	test.mysqlToJson()

