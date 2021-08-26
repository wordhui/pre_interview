# 「简约思维」后端开发面试题

我们希望你能自觉在5小时完成后端题目任务。结束后给 hr@simplylab.xyz（如果被退回请发送至zt2008@qq.com） 发送题目的解答，邮件主题请用如下的命名规则：投递的简历平台+面试岗位+姓名+电话。

题目的解答提交请附上代码和抓取的数据 - excel或者csv格式
* 将整个工程文件的压缩包作为邮件附件，请注意提供部署服务器的说明文档
* 注册github账号，把代码上传到github，直接发送github项目链接给我们


在本题目中请尽量使用[Scrapy](https://scrapy.org/)框架完成3个基本的数据抓取任务


**三个基本的数据抓取任务:**

##### (1)获取雪球 美国股市涨幅最大的100个股票信息（股票代码，股票名称，当前价，涨跌幅，市值，市盈率）
https://xueqiu.com/hq#exchange=US&firstName=3&secondName=3_0&order=desc&orderby=percent

##### (2)爬取aliexpress的商品搜索页面的产品列表信息（商品名称，售价，评分，销量等）
https://www.aliexpress.com/wholesale
https://www.aliexpress.com/wholesale?SearchText=hat
