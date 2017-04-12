# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

class Test2Pipeline(object):

    def __init__(self):
        self.file = codecs.open('test2.json',mode='wb',encoding='utf-8')

    def process_item(self, item, spider):
        print "............................"
        line =json.dumps(dict(item),ensure_ascii=False) + '\r\n'
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class MySQLStoreTest2Pipeline(object):

    def __init__(self, dbpool):
		self.dbpool = dbpool

    @classmethod  #是一个函数修饰符，它表示接下来的是一个类方法
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
	        cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    #pipeline默认调用
    def process_item(self, item, spider):
		d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
		d.addErrback(self._handle_error, item, spider)
		d.addBoth(lambda _: item)
		return d

    #将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
		linkmd5id = self._get_linkmd5id(item)
	    #print linkmd5id
		#now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
		conn.execute("""
		select 1 from test2info where linkmd5id = %s
	    """, (linkmd5id, ))
		ret = conn.fetchone()

		if ret:
			conn.execute("""
	    	update test2info set title = %s, link = %s, updated = %s, author = %s where linkmd5id = %s
	    	""", (item['title'], item['link'], item['updated'], item['author'], linkmd5id))

		else:
			conn.execute("""
			insert into test2info(linkmd5id, title, link, updated, author)
			values(%s, %s, %s, %s, %s)
	    	""", (linkmd5id, item['title'], item['link'], item['updated'], item['author']))

    #获取url的md5编码
    def _get_linkmd5id(self, item):
		#url进行md5处理，为避免重复采集设计
		return md5(item['link']).hexdigest()
    	#异常处理
    def _handle_error(self, failue, item, spider):
		log.err(failure)
