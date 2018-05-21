# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

def dbHandle():
    conn=pymysql.connect(
        host="123.206.68.192",
        user="myuser",
        passwd="mypassword",
        db="news",
        charset='utf8',
        use_unicode = False
    )
    return conn

class NewsPipeline(object):
    def process_item(self,item,spider):
        dbObject=dbHandle()
        try:
            cursor=dbObject.cursor()
            s=""
            for a in item['content']:
                s=s+str(a)
            cursor.execute("""INSERT INTO `article`(title,content,time) values(%s,%s,%s)""",(item['title'],s,item['time']))
            cursor.connection.commit()
        except BaseException as e:
            print(e)
            dbObject.rollback()
        return item
