# 本项目所用时间统计

* #### 项目开始时间 2021-9-25 16:31
* #### 项目结束时间 2012-9-25 18:50
* #### 部署所需时间 约60分钟 从服务器重装到部署运行 上面未统计部署时间

# 项目简介

* #### 项目采用fastapi(类flask)开发,gunicorn + uvicorn 部署 未使用Nginx
* #### 项目API很小 未根据模块进行分割，全在一个app文件里面
* #### API接口对测试的请求大小进行了限制，超过5M的请求将会拦截
* #### API未限制ip访问频率,未对接口进行签名
*  #### 云服务器API地址: [地址](http://81.68.226.215:5000) http://81.68.226.215:5000
*  #### 云服务器API文档地址:[地址](http://81.68.226.215:5000/docs) http://81.68.226.215:5000/docs