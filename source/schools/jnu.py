import sqlConnect
from sqlConnect import sqlConnect
from myHTMLParser import myHTMLParser
import urllib2
import re
import sys
import traceback

srcprefix = "http://news.jnu.edu.cn"
allImgUrl = []

class titleParser(myHTMLParser):
	"""docstring for titleParser"""
	def __init__(self):
		super(titleParser, self).__init__()

	def handle_starttag(self, tag, attrs):
		if(tag == 'a'):
			for i, j in enumerate(attrs):
				if(j[0]== 'href'):
					self._url.append(srcprefix + j[1])
		elif(tag == 'img'):
			for i, j in enumerate(attrs):
				if(j[0] == "src"):
					self._imgUrl = srcprefix + j[1]

	def handle_data(self, data):
		self._context += data
		str1,number=re.subn(r"[0-9]{4}-[0-9]{2}-[0-9]{2}","",data)
		str2,number=re.subn(r"\r","",str1)
		str3,number=re.subn(r"\n","",str2)
		str4,number=re.subn(r' ','',str3)
		if(str4!=''):
			self._title.append(str4)
		if(self.lasttag == 'p'):
			self._context += '\n'


def getContext(c_url):
	ret = []
	for i, url in enumerate(c_url):
		try :
			print("handling %dth context from jnu" %(i + 1))
			link = urllib2.urlopen(url)
			srcCode = link.read()
			newsPattern = '<div class="conTxt">[\s\S]+?</div>'
			newsblock = re.compile(newsPattern).findall(srcCode)[0]
			newsblock,number=re.subn(r'<p style="text-align: center; text-indent: 2em">.*?</p>','',newsblock)
			parser = titleParser()
			stri = parser.unescape(newsblock)
			parser.feed(stri)
			allImgUrl.append(parser.imgUrl)
			stri = parser.context
			stri=re.sub(r'\\r\\n',' ',stri)
			stri=stri[58:]
			parser.close()
			ret.append(stri)
		except :
			ret.append('error')
			print("error when handling %dth context from jnu" %(i + 1))
			print(traceback.print_exc())
	return ret


def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	test = sqlConnect("jnu", 10)
	tParser = titleParser()
	link = urllib2.urlopen("http://news.jnu.edu.cn/jnyw/List/List_149.html")
	srcCode = link.read()
	srcCode = re.compile(r'<ul class="newsList infoList infoListA">[\s\S]+?</ul>').findall(srcCode)
	srcCode = srcCode[0]
	tParser.feed(srcCode)
	pattern = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
	allDate = re.compile(pattern).findall(srcCode)
	test.date = allDate
	test.title = tParser.title
	test.contextUrl = tParser.url
	test.context = getContext(test.contextUrl)
	test.imgUrl = allImgUrl
	test.updateSql()
	test.mysqlToJson()
