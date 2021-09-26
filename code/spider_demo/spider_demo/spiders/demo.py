import re
import json
import datetime

import scrapy
from scrapy.signals import spider_closed
from scrapy.utils.log import logger

from spider_demo.items import SpiderDemoItem
from spider_demo.settings import start_url_list, db, project_dir, table_name


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['www.aliexpress.com']

    def start_requests(self):
        for start_url_info in start_url_list:
            yield scrapy.Request(url=start_url_info['url'],
                                 meta={'current_page': 1, 'from_word': start_url_info['word']},
                                 callback=self.parse)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DemoSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=spider_closed)
        return spider

    def spider_closed(self, spider):
        """爬虫退出时的回调，导出数据到Excel中"""
        logger.info("程序即将退出，导出数据")
        sql = f"select title,img_url,price,score,sales,from_word from {table_name};"
        excel_name = f'导出数据_{datetime.datetime.now().strftime("%Y-%m-%d %H时%M点%S分")}.xlsx'
        db.select_and_save_excel(sql, project_dir.joinpath(excel_name))
        logger.info(f"导出数据成功！")

    def parse(self, response):
        html_text = response.text
        page_json_text = "".join(re.findall(r'(?isu)window\.runParams\s+=\s+({".+?});[\s\n\r\t]+window.'
                                            r'runParams.csrfToken', html_text)).strip()
        page_json_data = json.loads(page_json_text)
        key_word = ''.join(re.findall(r'', response.request.url)).strip()
        for data in page_json_data['mods']['itemList']['content']:
            try:
                item = SpiderDemoItem()
                if data['productType'] == 'ad':  # 不保存广告信息
                    continue
                item['product_id'] = data['productId']
                item['title'] = data['title']['displayTitle']
                item['img_url'] = data['image']['imgUrl']
                item['price'] = data['prices']['salePrice']['formattedPrice']
                try:
                    item['score'] = data['evaluation']['starRating']
                except KeyError:
                    item['score'] = 0.0
                try:
                    item['sales'] = data['trade']['tradeDesc']
                except KeyError:
                    item['sales'] = '0 sold'
                item['from_word'] = response.meta['from_word']
                yield item
            except KeyError as e:
                logger.error(f"KeyError url:{response.request.url} data:{data} error:{e}")
        total_result = page_json_data['resultCount']
        total_page = int(int(total_result) / 60) + 1
        if total_page > 60:
            total_page = 60
        current_page = response.meta.get("current_page", 1)
        if total_page > current_page:
            next_page = current_page + 1
            next_url = re.sub(r'(?<=page=)\d+', str(next_page), response.request.url)
            logger.info(f"链接翻页：{next_url}")
            response.meta['current_page'] = next_page
            yield scrapy.Request(url=next_url, meta=response.meta, callback=self.parse)
