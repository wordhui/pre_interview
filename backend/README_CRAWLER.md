# 「简约思维」后端爬虫开发面试题

我们希望你能自觉在5小时完成后端题目任务。结束后给 hr@simplylab.xyz（如果被退回请发送至zt2008@qq.com） 发送题目的解答，邮件主题请用如下的命名规则：投递的简历平台+面试岗位+姓名+电话。

题目的解答提交请附上代码和抓取的数据（excel或者csv格式）
* 将整个工程文件的压缩包作为邮件附件，请注意提供部署服务器的说明文档
* 注册github账号，把代码上传到github，直接发送github项目链接给我们


在本题目中请尽量使用[Scrapy](https://scrapy.org/)框架（但是没有任何限制）完成3个基本的数据抓取任务，对于（2）（3）任务中的搜索内容，可以使用例子中的单一搜索词“hat”，或者自行指定几个特定的搜索词，然后代码注释中或者说明文档中可以详细说明如果调整搜索词。（注：为节省沟通成本，我们总结出四个最基本的任务形态，四个测试任务都经过了我们的团队的实际编写测试，难度不高，相信如果你有足够的经验，可以在很短的时间内完成）


**四个基本的数据抓取任务:**

##### (1)获取雪球 美国股市涨幅最大的100个股票信息（股票代码，股票名称，当前价，涨跌幅，市值，市盈率）
https://xueqiu.com/hq#exchange=US&firstName=3&secondName=3_0&order=desc&orderby=percent

##### (2)爬取aliexpress的商品搜索页面的产品列表信息（商品名称，图片url，售价，评分，销量等）
* 搜索hat链接：https://www.aliexpress.com/wholesale?SearchText=hat

##### (3)获取GoogleTrend的详情页的时间序列信息(例如其中的“Interest over time”图标的时间序列数据)
* 搜索hat链接：https://trends.google.com/trends/explore?q=hat&geo=CN

##### (4)获取连续多页的网店的商品列表页的商品信息(由于页面可连续加载，需要完成至少2页的商品信息抓取，并在文档中说明)
* 连续加载页面链接：https://www.fashionnova.com/collections/all?sort_by=best-selling
