# 本项目所用时间统计

* #### 本项目做的过程中不连续,大约用了4-5个小时 主要是scrapy框架差不多2年没有使用了(一般用requests和httpx)，做起来生疏了起来

# 项目使用说明

* #### 1.编辑导入抓取关键词列表.xlsx文件（编辑后请一定要保存），填写需要抓取的关键词，注意只修改需要抓取的关键词，不要修改Excel首行title和sheet名
* #### 2.安装相关依赖 运行 spider_main.py文件
* #### 3.程序有运行结束的回调，程序运行结束后会自动导出 抓取的数据到Excel中(Excel位置同scrapy.cfg目录) 导出文件名格式如：导出数据_2021-09-26 14时46点42分.xlsx

# 其他说明

* #### 程序未添加cookies 未使用代理ip 抓取速度控制的非常慢
* #### 程序数据库使用的是sqlite,程序未做断点重爬的相关控制，当然scrapy带这个功能
* #### 数据保存采用product-id作为主键，不会出现重复数据