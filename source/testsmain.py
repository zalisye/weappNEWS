import gevent
from gevent import monkey
monkey.patch_all()
import pymysql
import traceback

from schools import bupt, buaa, tsinghua, ahu, hit, hnu, hust, jlu, jnu, nju, njust, nm_uni, nuaa, pku, seu, sjtu, sysu, zhongnan, zju, bit

def t1():
    try:
        bupt.main()
        buaa.main()
        tsinghua.main()
        ahu.main()
        hit.main()
    except:
        print "error1"
        print traceback.print_exc()


def t2():
    try:
        hust.main()
        jlu.main()
        jnu.main()
        nju.main()
        hnu.main()
    except:
        print "error2"
        print traceback.print_exc()


def t3():
    try:
        njust.main()
        nm_uni.main()
        nuaa.main()
        pku.main()
        seu.main()
    except:
        print "error3"
        print traceback.print_exc()


def t4():
    try:
        sjtu.main()
        sysu.main()
        zhongnan.main()
        zju.main()
        bit.main()
    except:
        print "error4"
        print traceback.print_exc()


def maintain():
    conn = pymysql.connect(
		host='123.206.68.192',
		port=3306,
		user='root',
		passwd='',
		db='news',
		charset='utf8'
	)
    cur = conn.cursor()
    cur.execute("DELETE FROM `data` WHERE context = 'error' OR context = '' OR abstract = 'error'")

    cur.close()
    conn.commit()
    conn.close()



def main():
    try:
        gevent.joinall([
            gevent.spawn(t1),
            gevent.spawn(t2),
            gevent.spawn(t3),
            gevent.spawn(t4)
        ])
    except:
        print "error5"

    try :
        maintain()
    except :
        print "error6"

if __name__ == '__main__':
    main()
