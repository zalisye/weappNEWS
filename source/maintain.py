import pymysql
from bosonnlp import BosonNLP

def maintain() :
	apitoken = "ZUKLt9tO.24611.KI1wUPXknGRP"
	nlp = BosonNLP(apitoken)
	conn = pymysql.connect(
		host='123.206.68.192',
		port=3306,
		user='root',
		passwd='',
		db='news',
		charset='utf8'
	)
	cur = conn.cursor()
	cur.execute("DELETE FROM `data` WHERE context = 'error'")
	conn.commit()

	cur.execute("SELECT * FROM `data` WHERE	abstract = 'error'")
	data = cur.fetchall()
	for entry in data :
		result = nlp.summary('', entry[3], 50).replace('\n', '')
		if(result == 'error') :
			print '[Deleted]wrong entry: ' + entry
			cur.execute("DELETE FROM `data` WHERE ID = %s", (entry[0]))
		else :
			cur.execute("UPDATE `data` SET abstract = %s WHERE ID = %s", (result, entry[0]))

	cur.close()
	conn.commit()
	conn.close()


if __name__ == '__main__':
	maintain()