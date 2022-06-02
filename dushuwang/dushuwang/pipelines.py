# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


class DushuwangPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.Connect(host='192.168.101.6', port=3306, user='root', password='paris2030@ROOT',
                                    database='dushuwang',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into book(name,author,imgUrl,info) values("%s","%s","%s","%s")' % (
            item['name'], item['author'], item['imgUrl'], item['info'])
        self.cursor.execute(sql)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
