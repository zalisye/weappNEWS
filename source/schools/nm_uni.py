import sqlConnect
from sqlConnect import sqlConnect
import myHTMLParser
from myHTMLParser import myHTMLParser
import urllib2
import re
import sys
import urllib

srcprefix = "http://news.imu.edu.cn"
allImgUrl = []

class titleParser(myHTMLParser):
	"""docstring for titleParser"""
	def __init__(self):
		super(titleParser, self).__init__()

	def handle_starttag(self, tag, attrs):
		if(tag == 'a'):
			for i, j in enumerate(attrs):
				str=j[1]
				str=str[2:]
				self._url.append(srcprefix + str)
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
			print("handling %dth context from imu" %(i + 1))
			link = urllib2.urlopen(url)
			srcCode = link.read()
			newsPattern = '<div id="vsb_content">[\s\S]+?</div>'
			newsblock = re.compile(newsPattern).findall(srcCode)[0]
			newsblock,number=re.subn(r',Microsoft YaHei; font-size: 12px;">.*?</span></p>','/>',newsblock)
			parser = titleParser()
			stri = parser.unescape(newsblock)
			parser.feed(stri)
			allImgUrl.append(parser.imgUrl)
			stri = parser.context
			parser.close()
			ret.append(stri)
		except :
			ret.append('error')
			print("error when handling %dth context from imu" %(i + 1))

	return ret


def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	test = sqlConnect("imu", 10)
	tParser = titleParser()
	link = urllib2.urlopen("http://news.imu.edu.cn/xwyl/ndyw.htm")
	srcCode = link.read()
	srcCode = re.compile(r'</span></h4>[\s\S]+?</ul>').findall(srcCode)
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
