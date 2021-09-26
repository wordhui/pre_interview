"""
TODO 此文件并不是标准的测试文件，只是简单快速的测试下
"""
import random
import traceback
from decimal import Decimal

import requests

domain = 'http://127.0.0.1:5000'


def test_add():
    try:
        add_list = [random.randint(10000000000000000, 10000000000000000000000000000000000) / 10 for i in
                    range(random.randint(50000, 100000))]
        post_json = {'value_array': [{'value': _} for _ in add_list]}
        response = requests.post(domain + '/add', json=post_json)
        response.raise_for_status()
        if response.json().get('result') == float(sum((Decimal(str(_))) for _ in add_list)):
            print(f'测试成功:\n{post_json}\n{response.json()}')
        else:
            print(f'测试失败:\n{post_json}\n{response.json()}')
    except:
        print(f'测试失败 error:{traceback.format_exc()}')


def test_get_system_date():
    response = requests.get(domain + '/get_date')
    print(response.text)


def test_chat():
    text = 'adsfa\nm再见adsf' * 100000 + 'asdasf您好asdfasdf'
    # text = 'asdfasd您好asdfasd'
    response = requests.post(domain + '/chat', json={'msg': text})
    response.raise_for_status()
    print(response.text)


if __name__ == '__main__':
    test_add()
    test_get_system_date()
    # test_chat()
