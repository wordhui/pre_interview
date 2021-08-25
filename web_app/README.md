# 前端web app开发面试题

我们希望你能独立的在10小时内完成题目任务。结束后给 hr@simplylab.xyz 发送题目的解答，邮件主题请用如下的命名规则：投递的简历平台+面试岗位+姓名+微信+电话。

完成题目的过程中请注意代码、命名规范以及合理的代码注释。

## 该题目的解答提交形式

- 注册GitHub账号，把代码上传到GitHub，直接发送GitHub项目链接给我们
- GitHub上需要有说明文档，写明详细步骤说明，让我们可以本地运行测试你的web app各项功能
- 链接可发送至上述邮箱（hr@simplylab.xyz）

## 本题目要求使用的技术和packages

- [ReactJS](https://www.react.org/) 
  - [create-react-app](https://reactjs.org/docs/create-a-new-react-app.html)
  - 全部使用[Function Components](https://reactjs.org/docs/components-and-props.html) ([Hooks](https://reactjs.org/docs/hooks-intro.html))，避免使用Class Components
- [React Router](https://reactrouter.com/web/guides/quick-start)
- [React Redux](https://react-redux.js.org/)
- [Material UI](https://material-ui.com/)


## 题目内容具体要求说明

需要搭建的web app一共有两个页面（首页、搜索页），包含三种不同的状态：
1. 首页
2. 搜索页loading状态
3. 搜索页结果显示

其中以下的每个页面顶部都有一个导航栏，位置一直在网页最顶端，不随页面其他内容部分滑动。最左端显示一个网页Logo，名字为BestSearch，其中Best部分字体是加粗的。在任何一个网页点击这个BestSearch都会回到首页。

需要实现的整个web app的demo可以点击这个链接观看：[web app demo](https://preinterview.s3.us-west-2.amazonaws.com/Lark20210825-170441.gif)

每个页面的具体细节描述如下：

#### 首页

###### 网页的本地URL：
http://localhost:3000/

###### 功能描述：
此页面为网页首页，全网页一共只有两个部分：

1. 一条"Search Trends"的标语，在页面水平居中的位置；
2. 一个搜索框，搜索框的placeholder为“Search for new products in 961K stores”，搜索框右方有一个搜索按钮。

用户可以通过（1）按回车键或者（2）点击右方搜索按钮这两种不同的方式触发搜索功能，从而跳转至搜索页 http://localhost:3000/search/{keyword} 进行搜索并显示搜索结果。

同时，在首页中，整个导航栏里只有左端名为“BestSearch”的Logo这一个元素。

###### UI如下图所示：

![home page](https://preinterview.s3.us-west-2.amazonaws.com/Lark20210825-170437.png?raw=true)


#### 搜索页loading状态

###### 网页的本地URL：
http://localhost:3000/search/{keyword}

其中`{keyword}`是当前用户用来搜索的搜索词。

比如用户希望搜索`Hat`这个词，那么当前的路径应该为 http://localhost:3000/search/Hat

请注意，路径中的`{keyword}`如果包含空格符号，需要转化为 `+` 显示在路径中。

比如如果用户希望搜索`Best cat toys`这个词，那么路径应为 http://localhost:3000/search/Best+cat+toys

###### 功能描述：
由于前端网页向后台发送搜索请求并最终拿到返回的搜索结果是一个异步的过程，在用户点击回车键（或者右方搜索按钮）之后、前端网页拿到返回的搜索结果之前这个时间段内，会显示一个loading的状态，具体UI如下图所示。

同时，在搜索页的导航栏中，除了“BestSearch”的Logo以外，导航栏的水平居中位置会显示一个搜索框，搜索框中会显示目前正在搜索的关键词。

用户可以通过三种不同的方式进入这个搜索页面进行搜索：
1. 在首页中输入搜索词，点击回车键（或者右方搜索按钮），会跳转至此搜索页面进行搜索；
2. 已经在搜索页的时候，在搜索框里输入一个与当前不同的搜索词，点击回车键（或者搜索按钮），会进行对于新搜索词的搜索；
3. 在浏览器中直接输入一个带有搜索词的搜索页URL。比如用户直接在浏览器的地址栏输入 http://localhost:3000/search/Hat ，就可以进入此搜索页面搜索Hat相关的内容并最终看到搜索结果。

###### UI如下图所示：

![search loading page](https://preinterview.s3.us-west-2.amazonaws.com/Lark20210825-170433.png?raw=true)

#### 搜索页结果显示

###### 网页的本地URL：
http://localhost:3000/search/{keyword}

此部分与上述“搜索页loading状态”的URL相同。

###### 功能描述：
当前端网页得到后台返回的结果之后，会将搜索结果展现在此搜索页上。

搜索结果内容分为三个板块：
1. Recent product launches：用柱状图显示后台返回的信息；
2. Related product trends：用堆叠面积图显示后台返回的信息；
3. Related new products published in the last 7 days：用responsive layout grid显示后台返回的产品列表。
同时，与上述“搜索页loading状态”相同，在搜索页的导航栏中，除了“BestSearch”的Logo以外，导航栏的水平居中位置会显示一个搜索框，搜索框中会显示目前正在搜索的关键词。

###### UI如下图所示：

![search results page](https://preinterview.s3.us-west-2.amazonaws.com/Lark20210825-170429.png?raw=true)

## Web app开发要求说明

如上图所示，本题需要制作一个web app来完成一个简单的搜索动作。页面需要美观、流畅，但是不需复杂，只需要最基本的框架和元素就可以。

- 调用接口：API: http://3.141.23.218:5000/interview/keyword_search
  
  Parameters（输入参数）: 
```
  
  {
    "login_token":"INTERVIEW_SIMPLY2021",  # required(str): login token
    "search_phrase": "hat",                # required(str):
  }
```
其中`search_phrase`的值是用户输入的搜索keyword（string），比如"hat"、"best shoes"等。
- 调用方法：POST
- 参数格式：JSON

输出：为JSON格式的数据，具体需要用到的JSON中的fields如下例所示：

```
{
  product_launch_data: [
    { key_as_string: "2021-08-01T00:00:00.000Z", doc_count: 7 },
    { key_as_string: "2021-08-02T00:00:00.000Z", doc_count: 1252 },
    ...
    { key_as_string: "2021-08-30T00:00:00.000Z", doc_count: 997 },
    { key_as_string: "2021-08-31T00:00:00.000Z", doc_count: 1194 },
  ],
  product_trends: [ 
  {
      name: "hat",
      search_msv: [
        { date: "2015-9", sv: 161700 },
        { date: "2015-10", sv: 169950 },
        ......
        { date: "2021-6", sv: 353280 },
        { date: "2015-7", sv: 450000 },
      ],
    },
    ...
  ],
  products: [
    {
      published_at: "2021-08-21T12:38:07-07:00",
      title: "hat on hat dad hat",
      price: "23.00",
      store_domain: "recruiternest.com",
      image: "https://images.lululemon.com/is/image/lululemon/LM9AA2S_047992_1"
    },
    ...
    {
      published_at: "2021-08-19T00:26:21+02:00",
      title: "hat soft",
      price: "129.95",
      store_domain: "wheat.no",
      image: "https://images.lululemon.com/is/image/lululemon/LM9AA3S_051348_1"
    },
  ],
}
```

其中:
- `product_launch_data`对应的是搜索结果里的Recently product launches柱状图，`key_as_string`对应横轴，`doc_count`对应纵轴；
- `product_trends`对应的是搜索结果里的Related product trends面积图，date对应横轴，sv对应纵轴；
- `products`对应的是搜索结果里的Related products published in the last 7 days。

在开发、参考或模仿的过程中，需要满足以下条件：
- 项目名称为“BestSearch”
- 整个项目能在本地服务器直接运行
- 页面需要美观、流畅，但是不需复杂，只需要最基本的框架和元素就可以
- 尽量和上图中的UI做得像
- 提交的web app需要为自适应（响应式设计、responsive design）
