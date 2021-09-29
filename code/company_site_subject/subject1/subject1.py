import os
import sys
import time
import json
import pprint
import traceback
from typing import List
from pathlib import Path

import httpx
from dict_to_db import DictToDb
from tenacity import retry, wait_random, stop_after_attempt

from logger import log

db = DictToDb()
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-length': '80',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'country=CN; _yq_bid=G-E4F9737BDFDE0E69; v5_Culture=zh-cn; _ga=GA1.2.1794659089.1632810808; _gid=GA1.2.428363574.1632810808; v5_TranslateLang=zh-Hans; Last-Event-ID=657572742f6665332f64323334373462326337312f306463623132363138353a313430353037373934333a65736c61663a6e74622d756e656d2d656c69626f6d2d71792064657370616c6c6f632065736f6c632d7265677275626d6168207265677275626d616820656c67676f742d72616276616e113495fd1f9005a4315',
    'origin': 'https://t.17track.net',
    'pragma': 'no-cache',
    'referer': 'https://t.17track.net/zh-cn',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/93.0.4577.82 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}
data_dir = Path(sys.argv[0]).parent.joinpath('json_data_dir')
upload_dir = Path(sys.argv[0]).parent.joinpath('upload_data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

client = httpx.Client(http2=True, verify=False, headers=headers)
post_data = """{"data":[{"num":"LX679316884US","fc":0,"sc":0}],"guid":"","timeZoneOffset":-480}"""
get_logistics_url = "https://t.17track.net/restapi/track"


@retry(reraise=True, wait=wait_random(min=3, max=5), stop=stop_after_attempt(3))
def get_logistics_by_code(code: str, delay: float = 0):
    """
    :param code: 需要查询的code
    :param delay: 查询间隔的时间
    """
    try:
        data = post_data.replace("LX679316884US", code)
        time.sleep(delay)
        response = client.post(get_logistics_url, content=f"""{data}""")
        result = response.json()
        if result.get('ret', 0) == 1:
            log.info(f"code {code}  查询成功:\n{pprint.pformat(result)}")
        else:
            log.warning(f"code{code}查询失败,msg:{result.get('msg')}  请检查cookies是否失效，或者ip是否被封禁,等其它可能的问题！")
            return
        file_name = data_dir.joinpath(f"{code}_{int(time.time())}.json")
        with open(file_name, 'w', encoding='utf8') as f:
            f.write(json.dumps(result))
            log.info(f"保存文件：{file_name}")
    except Exception as e:
        log.error(f"查询code 出错：{code} error:{traceback.format_exc()}")
        raise e


def load_excel_data(excel: str):
    """
    根据传入的Excel文件路径 读取Excel中的物流code信息并返回 【注意只会读取Sheet1中的信息，在其他Sheet中的数据概不读取】
    :param excel: 需要加载数据的Excel文件路径
    :return: Excel中的 物流code 列表
    """
    result_list = db.excel_to_dict_list(excel, export_sheet=['Sheet1'])
    return [r['code'] for r in result_list if 'code' in r.keys() and r['code']]  # 过滤掉没有code key的以及code值为空的


def crawl_data_by_excel():
    all_file = os.listdir(upload_dir)
    excel_file = [f for f in all_file if f.endswith('.xlsx')]
    if not excel_file:
        log.error("upload_data 文件夹中没有Excel文件,请填写Excel文件并保存到 upload_data文件夹中后重新运行程序，程序将在5秒后退出运行！")
        time.sleep(5)
        sys.exit()
    print("请输入序号选择需要导入搜索的Excel文件名：")
    for c, f in enumerate(excel_file):
        print(f"{c} ) {f}")
    for i in range(3):
        count = input("")
        count = count.strip()
        if count and count.isdigit() and int(count) < len(excel_file):
            crawl_data_list = load_excel_data(upload_dir.joinpath(excel_file[int(count)]))
            crawl_manager(crawl_data_list)
            break
        else:
            print(f"输入错误 您还可以在下面重新输入 剩余重试次数：{2 - i}")


def crawl_manager(crawl_data_list: List[str]):
    """根据传入的code list 抓取相关物信息
    :param crawl_data_list 需要抓取的code_data_list
    """
    for code in crawl_data_list:
        try:
            log.info(f"正在抓取：{code}")
            get_logistics_by_code(code, delay=5)  # 未使用代理ip cookie池 下载延迟设置为5秒
        except:
            log.error(f"出错code:{code} error:{traceback.format_exc()}")


def main():
    mode = input("请输入程序运行模式  1/从Excel中导入code进行查询  2从console 中输入code进行查询 \n")
    if mode.strip() == "1":
        crawl_data_by_excel()
    elif mode.strip() == '2':
        code = ''
        while code != 'exit':
            code = input("请输入需要抓取的code (注：输入 exit 退出程序！)\n")
            code = code.strip()
            if code != "exit":
                get_logistics_by_code(code, delay=0.5)
    else:
        log.info(f"输入参数错误 程序将在3秒后结束运行！")
        sys.exit()


if __name__ == '__main__':
    main()
