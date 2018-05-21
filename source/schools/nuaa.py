import sqlConnect
from sqlConnect import sqlConnect
import myHTMLParser
from myHTMLParser import myHTMLParser
import urllib2
import re
import sys
import urllib

srcprefix = "http://newsweb.nuaa.edu.cn"
allImgUrl = []

class titleParser(myHTMLParser):
	"""docstring for titleParser"""
	def __init__(self):
		super(titleParser, self).__init__()

	def handle_starttag(self, tag, attrs):
		if(tag == 'a'):
			for i, j in enumerate(attrs):
				if(j[0] == "href"):
					self._url.append(srcprefix + j[1])
				elif(j[0] == "title"):
					self._title.append(j[1])
		elif(tag == 'img'):
			for i, j in enumerate(attrs):
				if(j[0] == "src"):
					self._imgUrl = srcprefix + j[1]

	def handle_data(self, data):
		self._context += data
		if(self.lasttag == 'p'):
			self._context += '\n'


def getContext(c_url):
	ret = []
	for i, url in enumerate(c_url):
		try :
			print("handling %dth context from nuaa" %(i + 1))
			link = urllib2.urlopen(url)
			
			srcCode = link.read()
			newsPattern = r'<div class=\'wp_articlecontent\'>[\s\S]+?</div>'
			newsblock = re.compile(newsPattern).findall(srcCode)[0]
			parser = titleParser()
			stri = parser.unescape(newsblock)
			parser.feed(stri)
			allImgUrl.append(parser.imgUrl)
			stri = parser.context
			parser.close()
			ret.append(stri)
		except :
			ret.append('error')
			print("error when handling %dth context from nuaa" %(i + 1))
	return ret


def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	test = sqlConnect("nuaa", 10)
	tParser = titleParser()
	link = urllib2.urlopen("http://newsweb.nuaa.edu.cn/zhyw1/list.htm")
	srcCode = link.read()
	srcCode = re.compile(r'<ul class="wp_article_list">[\s\S]+?</ul>').findall(srcCode)
	srcCode = srcCode[0]
	tParser.feed(srcCode)
	pattern = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
	allDate = re.compile(pattern).findall(srcCode)
	test.date = allDate
	test.title = tParser.title
	test.contextUrl = tParser.url
	#temContext = getContext(test.contextUrl)
	test.context = getContext(test.contextUrl)
	test.imgUrl = allImgUrl
	test.updateSql()
	test.mysqlToJson()
	
	

