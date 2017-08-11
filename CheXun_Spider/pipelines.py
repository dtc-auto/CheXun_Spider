# -*- coding: utf-8 -*-
from datetime import datetime
import pymssql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ChexunSpiderPipeline(object):
    def __init__(self, server, user, password, database, host, into_sql, star_spider_name):
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.into_sql = into_sql
        self.star_spider_name = star_spider_name
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            server=crawler.settings.get('DATABASE_SERVER_NAME'),
            user=crawler.settings.get('DATABASE_USER_NAME'),
            password=crawler.settings.get('DATABASE_USER_PASSWORD'),
            database=crawler.settings.get('DATABASE_NAME'),
            host=crawler.settings.get('DATABASE_HOST'),
            into_sql=crawler.settings.get('INTO_SQL'),
            star_spider_name=crawler.settings.get('STAR_SPIDER_NAME')
        )

    def open_spider(self, spider):
        self.conn = pymssql.connect(user=self.user, password=self.password, host=self.host, database=self.database)

    def process_item(self, item, spider):
        if self.into_sql == 1:
            if self.star_spider_name == 'URL_Spider':
                self.url_spider_into(item, spider)
            if self.star_spider_name == 'Brand_Spider':
                 self.Brand_Spider_into(item, spider)
            if self.star_spider_name == 'Companies_Spider':
                self.Companies_Spider_into(item, spider)
            if self.star_spider_name == 'Configuration_Spider':
                self.Configuration_Spider_into(item, spider)
        return item


  # 便于理解,根据spider_name，分4次写入sql



    def url_spider_into(self, item, spider):
            cur = self.conn.cursor()
            self.conn.autocommit(True)
            serie_id=item['serie_id'],
            serie_name_cn=item['serie_name_cn'],
            serie_name_en=item['serie_name_en'],
            serie_url=item['serie_url'],
            brand_id=item['brand_id'],
            company_id=item['company_id']
            create_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            last_update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cur.execute("""INSERT INTO BDCI_CHEXUN.stg.CONFIG_SERIES
                            (serie_id, serie_name_cn, serie_name_en, serie_url, brand_id, company_id, create_time, last_update_time)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                        , (serie_id, serie_name_cn, serie_name_en, serie_url, brand_id, company_id, create_time, last_update_time))

            self.conn.autocommit(False)
            self.conn.commit()
        #self.conn.close()


    def Brand_Spider_into(self, item, spider):
            cur = self.conn.cursor()
            self.conn.autocommit(True)
            brand_id=item['brand_id'],
            brand_name_cn=item['brand_name_cn'],
            brand_name_en=item['brand_name_en'],
            create_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            last_update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cur.execute("""INSERT INTO BDCI_CHEXUN.stg.CONFIG_BRANDS
                            (brand_id, brand_name_cn, brand_name_en, create_time, last_update_time)
                        VALUES (%s,%s,%s,%s,%s)"""
                        , (brand_id, brand_name_cn, brand_name_en, create_time, last_update_time))

            self.conn.autocommit(False)
            self.conn.commit()
        #self.conn.close()


    def Companies_Spider_into(self, item, spider):
            cur = self.conn.cursor()
            self.conn.autocommit(True)
            company_id=item['company_id'],
            company_name_cn=item['company_name_cn'],
            company_name_en=item['company_name_en'],
            create_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            last_update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cur.execute("""INSERT INTO BDCI_CHEXUN.stg.CONFIG_COMPANIES
                            (company_id, company_name_cn, company_name_en, create_time, last_update_time)
                        VALUES (%s,%s,%s,%s,%s)"""
                        , (company_id, company_name_cn, company_name_en, create_time, last_update_time))

            self.conn.autocommit(False)
            self.conn.commit()

        #self.conn.close()


    def Configuration_Spider_into(self, item, spider):
            cur = self.conn.cursor()
            self.conn.autocommit(True)
            config_id=item['serie_id'],
            spec_id=item['spec_id'],
            para_name=item['para_name'],
            para_value=item['para_value'],
            create_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            last_update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cur.execute("""INSERT INTO BDCI_CHEXUN.stg.CONFIGURATION_DETAILS
                            (serie_id, spec_id, para_name, para_value, create_time, last_update_time)
                        VALUES (%s,%s,%s,%s,%s,%s)"""
                        , (config_id, spec_id, para_name, para_value, create_time, last_update_time))

            self.conn.autocommit(False)
            self.conn.commit()
        #self.conn.close()
