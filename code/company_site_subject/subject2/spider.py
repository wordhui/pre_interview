import json
import re
import sys
import os
import random
import string
import hashlib
import time
import traceback

import urllib3
from pathlib import Path
from urllib.parse import unquote

import filetype
import httpx
import requests
from requests_toolbelt import MultipartEncoder
from tenacity import retry, wait_random, stop_after_attempt

from logger import log

urllib3.disable_warnings()
upload_image_headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    # 'content-type': 'multipart/form-data; boundary=----WebKitFormBoundarygF74eU4ZSXom0QY9',
    'origin': 'https://www.aliseeks.com',
    'pragma': 'no-cache',
    'referer': 'https://www.aliseeks.com/',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/93.0.4577.82 Safari/537.36',
    'x-ali-ref': '',
    'x-ali-uui': '3WalmH6s+XgmY8jZ1YtmqIqBxfnPMPCQq/SqjhCd1C8=',
    'x-app-vi': 'Aliseeks.com@783849c',
}
get_real_url_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
              '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/93.0.4577.82 Safari/537.36',
}
upload_image_url = 'https://api.aliseeks.com/upload/image?r=httpx'
search_img_url = "https://api.aliseeks.com/search/image?signature={sign}&time={time}"
search_data = {"fsKey": "WryDRPArKOhBEWPAY9gp", "currency": "USD", "language": "en_US", "category": None,
               "locale": "en_US", "provider": "ali", "shipToCountry": "en_US"}
client = httpx.Client(http2=True, verify=False, proxies='http://127.0.0.1:8888')
img_dir = Path(sys.argv[0]).parent.joinpath('img_dir')
data_dir = Path(sys.argv[0]).parent.joinpath('json_data_dir')
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def get_sign(t):
    """
    生成接口请求的签名
    :return: 生成的签名
    """
    key = "hdwnjnabzowkdla:"
    msg = f"{key}{t}"
    sign = hashlib.md5(msg.encode('utf8')).hexdigest()
    return sign


@retry(reraise=True, wait=wait_random(min=3, max=5), stop=stop_after_attempt(3))
def upload_image(file_path):
    """
    上传图片到aliseeks 并且获取这个图片的files_key
    :param file_path:需要上传的文件路径
    :return: files_key
    """
    fields = {'file': (os.path.basename(file_path), open(file_path, 'rb'), filetype.guess(file_path).MIME)}
    boundary = f'----WebKitFormBoundary{"".join(random.sample(string.ascii_letters + string.digits, 16))}'
    data_multipart = MultipartEncoder(fields=fields, boundary=boundary)
    upload_image_headers['content-type'] = data_multipart.content_type
    log.info(f"upload file :{file_path}")
    response = requests.post(upload_image_url, data=data_multipart, headers=upload_image_headers, verify=False)
    result = response.json()
    return result['key']


@retry(reraise=True, wait=wait_random(min=3, max=5), stop=stop_after_attempt(3))
def search_product_by_file_key(files_key):
    """
    根据file_key查询商品  # TODO 这个查询结果还涉及翻页操作，时间有限，暂只实现核心逻辑，翻页这种重复工作暂未实现
    :param files_key: 文件 key
    :return: 商品列表
    """
    search_data['fsKey'] = files_key
    upload_image_headers['content-type'] = "application/json"
    log.info(f"search_product_by_file_key:{files_key}")
    t = int(time.time() * 1000)
    sign = get_sign(t)
    url = search_img_url.format(sign=sign, time=t)
    response = requests.post(url, json=search_data, headers=upload_image_headers, verify=False)
    result = response.json()
    product_list = result.get('items', [])
    result_list = []
    for p in product_list:
        try:
            detail_url = p.get('detailUrl')
            real_product_id = get_product_real_id(detail_url)
            p['real_product_id'] = real_product_id
            result_list.append(p)
        except:
            p['real_product_id'] = None
            result_list.append(p)
            log.error(f"error：{traceback.format_exc()} product_info:{p}")
    with open(data_dir.joinpath(f"{files_key}_{int(time.time())}.json"), 'w', encoding='utf8') as f:
        f.write(json.dumps(result_list))
    return result_list


@retry(reraise=True, wait=wait_random(min=3, max=5), stop=stop_after_attempt(3))
def get_product_real_id(detail_url, delay=3):
    """
    根据detail_url 获取商品系统内部id
    """
    time.sleep(delay)
    response = requests.get(detail_url, headers=get_real_url_headers, allow_redirects=False)
    if response.status_code == 307:
        location_url = unquote(response.headers['location'])
        real_product_id = "".join(re.findall(r'/(\d+?)\.html', location_url))
        log.info(f"get_product_real_id {real_product_id} by:{detail_url}")
        return real_product_id
    else:
        log.warning(f"get_product_real_id 错误 ：error status：{response.status_code} url:{detail_url}")


def search_product_by_img(img_path):
    """根据传入的图片路径，自动上传到 aliseeks 网站查询，并将查询返回的类加密url 访问服务器解析出最终的 product id 将数据保存在json文件中"""
    file_key = upload_image(img_path)
    search_product_by_file_key(file_key)


if __name__ == '__main__':
    search_product_by_img(img_dir.joinpath('1.jpg'))
