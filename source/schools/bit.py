from sqlConnect import sqlConnect
from myHTMLParser import myHTMLParser
import urllib2
import re
import sys
import traceback

srcprefix = "http://www.bit.edu.cn/xww"
imgprefix = "http://www.bit.edu.cn"
allImgUrl = []

class titleParser(myHTMLParser):
	"""docstring for titleParser"""
	def __init__(self):
		super(titleParser, self).__init__()

	def handle_starttag(self, tag, attrs):
		if(tag == 'a'):
			for i, j in enumerate(attrs):
				if(j[0] == "href"):
					self._url.append(srcprefix + j[1][2:])
		elif(tag == 'img'):
			for i, j in enumerate(attrs):
				if(j[0] == "src"):
					self._imgUrl = imgprefix + j[1][5:]

	def handle_data(self, data):
		self._context += data
		if(self.lasttag == 'p'):
			self._context += '\n'


def getContext(c_url):
	ret = []
	for i, url in enumerate(c_url):
		try :
			print("handling %dth context from bit" %(i + 1))
			link = urllib2.urlopen(url)
			srcCode = link.read()
			newsPattern = '<div class="article_con">[\s\S]+?</div>'
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
			print("error when handling %dth context from bit" %(i + 1))
			print(traceback.print_exc())

	return ret


def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	test = sqlConnect("bit", 10)
	tParser = titleParser()
	link = urllib2.urlopen("http://www.bit.edu.cn/xww/xwtt/index.htm")
	srcCode = link.read()
	srcCode = re.compile(r'<div class="new_con">[\S\s]+?</div>').findall(srcCode)
	srcCode = srcCode[0]
	tParser.feed(srcCode)
	pattern = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
	allDate = re.compile(pattern).findall(srcCode)
	pattern = r'<a.+?>[\S\s]+?</a>'
	allTitle = re.compile(pattern).findall(srcCode)
	for i in range(len(allTitle)) :
		flag = True
		ss = ""
		for x in allTitle[i] :
			if(x == '<') :
				flag = False
			if (flag == True):
				ss += x
			if(x == '>') :
				flag = True
		allTitle[i] = ss
	test.date = allDate
	test.title = allTitle
	test.contextUrl = tParser.url
	test.context = getContext(test.contextUrl)
	test.imgUrl = allImgUrl
	test.updateSql()
	test.mysqlToJson()
