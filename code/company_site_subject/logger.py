import json
import os
import logging
import sys

DEBUG = True


def close_root_log_output():
    """关闭root log的日志输出"""
    root_log = logging.getLogger()
    root_log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.FATAL)
    root_log.addHandler(handler)


def log_file_manager():
    log_size = 41943040  # 默认大小为40M
    if os.path.exists(os.path.join(BASE_DIR, 'log_config.json')):
        with open(os.path.join(BASE_DIR, 'log_config.json'), 'r') as f:
            config = json.load(f)
        log_size = config.get("log_size", 41943040) * 1024 * 1024
        print(f"修改新的log_size为：{log_size}")
    log_file = os.path.join(BASE_DIR, 'log/log.log')
    log_bak_file = os.path.join(BASE_DIR, 'log/log_bak.log')
    if os.path.exists(log_file) and os.path.getsize(log_file) > log_size:
        print("当前log 文件超过设定大小，将备份到log_bak.log")
        if os.path.exists(log_bak_file):
            os.remove(log_bak_file)
        os.rename(log_file, log_bak_file)


BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
if not os.path.exists(os.path.join(BASE_DIR, 'log')):
    os.makedirs(os.path.join(BASE_DIR, 'log'))
close_root_log_output()
log_file_manager()
log = logging.getLogger("all_log")
console_log = logging.getLogger("console_log")
file_log = logging.getLogger("file_log")
log.propagate = False
file_log.propagate = False
console_log.propagate = False
file_formatter = logging.Formatter('%(asctime)s %(levelname)-5s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_formatter = logging.Formatter('%(asctime)s %(levelname)-5s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler(filename=os.path.join(BASE_DIR, 'log/log.log'),
                                   encoding='utf-8')
file_handler.setFormatter(file_formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(console_formatter)
log.addHandler(file_handler)
log.addHandler(console_handler)
file_log.addHandler(file_handler)
console_log.addHandler(console_handler)

file_log.propagate = False  # 设置日志向上级传递，避免在控制台输出 参考：https://www.v2ex.com/t/480247
log.propagate = False
console_log.propagate = False
if DEBUG:  # 调试状态下也会将信息输出到控制台
    file_log.addHandler(console_handler)

file_log.setLevel(logging.INFO)
console_log.setLevel(logging.INFO)
log.setLevel(logging.INFO)

log.c_info = lambda x: console_log.info(x)
log.c_error = lambda x: console_log.error(x)
log.c_warning = lambda x: console_log.warning(x)
log.c_debug = lambda x: console_log.debug(x)
log.f_info = lambda x: file_log.info(x)
log.f_error = lambda x: file_log.error(x)
log.f_warning = lambda x: file_log.warning(x)
log.f_debug = lambda x: file_log.debug(x)
setattr(log, 'fflog', lambda x: file_log.debug(x))

__all__ = ['log', 'file_log', 'console_log']

if __name__ == '__main__':
    log.f_info('')
