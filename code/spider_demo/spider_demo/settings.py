import sys
from pathlib import Path

from dict_to_db import DictToDb

db = DictToDb("Data.db")
project_dir = Path(sys.argv[0]).parent
# 这里使用的是HTML 链接地址【可不带cookie】请求获取数据，网页里面也有XHR请求可以请求数据，但是XHR请求更麻烦，并且更容易封ip
# 封ip后带不带cookie都将返回状态码302 可能登录后可以访问 但是一般来说抓取数据能不登录就不登录 故未测试
word_page_url = "https://www.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText={word}" \
                "&ltype=wholesale&SortType=default&page=1"
start_url_list = []
table_name = "data"


def load_crawl_data_by_excel():  # 从Excel导入关键词，生成初始请求链接
    input_word_data = db.excel_to_dict_list(project_dir.joinpath('导入抓取关键词列表.xlsx'), export_sheet=['Sheet1'])
    for data in input_word_data:
        data['url'] = word_page_url.format(word=data['word'])
        start_url_list.append(data)


load_crawl_data_by_excel()

BOT_NAME = 'spider_demo'

SPIDER_MODULES = ['spider_demo.spiders']
NEWSPIDER_MODULE = 'spider_demo.spiders'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 5  # 未使用代理ip 放慢速度用避免封禁ip
CONCURRENT_REQUESTS_PER_DOMAIN = 2
CONCURRENT_REQUESTS_PER_IP = 2
ITEM_PIPELINES = {
    'spider_demo.pipelines.SpiderDemoPipeline': 300,
}
# 定义需要抓取的关键词列表
CRAWL_WORDS = ['hat', 'sock']

DEFAULT_REQUEST_HEADERS = {  # 设置默认的请求头，以一定程度防止反爬
    "Host": "www.aliexpress.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "DNT": "1",
    "Sec-GPC": "1",
}
