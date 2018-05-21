filelist = ['segw/pages/context/context.js', 'segw/pages/context/context.wxml', 'segw/pages/index/index.js', 'segw/pages/index/index.wxml', 'segw/pages/news/news.js', 'segw/pages/news/news.wxml']
with open('variable.ini', 'r') as df:
    for kv in [d.strip().split('=') for d in df]:
        if(kv[0] == 'userprefix'):
            for curfile in filelist:
                try:
                    temfile = open(curfile, 'r')
                    alltext = temfile.read()
                    alltext = alltext.replace('http://cn.bing.com', kv[1])
                    print (kv[1])
                finally:
                    if temfile:
                        temfile.close()
                        try:
                            temfile = open(curfile, 'w')
                            temfile.write(alltext)
                        finally:
                            if temfile:
                                temfile.close()
print "done"
