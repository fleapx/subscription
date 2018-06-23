# subscription
定期抓取指定网站上的内容（微博，公众号），将更新的数据保存到数据库，并发送邮件

## 如何使用

- 在setting.py中配置好mongodb，mysql，邮箱以及打码平台的相关参数
- 所爬取到的微博和公众号都会保存到mongodb中，再也不担心被删帖了：）
- weibo_subscription表中填写需要订阅的微博用户相关信息，主要为uid和status字段，status为0表示正常订阅，为1表示暂停
  - 打开`m.weibo.com`进入用户主页，url中的`profile/`之后的数字即为用户uid。如：`https://m.weibo.cn/profile/1823630913` uid为：`1823630913`
- weixin_subscription表中填写需要订阅的公众号的相关信息
- 在run.py中设置爬虫抓取频率以及邮件发送频率
  - 公众号更新没那么频繁，而且抓多了会有验证码，不建议频繁抓取，一天两三次就可以
  - 邮件发送频率也不可太过于频繁，否则会被当做垃圾邮件发不出去
- 需要调整邮件的显示样式请修改TemplateUtil.py文件，该文件会拼接出html页面，并作为邮件正文发送
- 邮件服务商都会被邮件中的html进行处理，因此页面在某些邮箱下显示会有问题，亲测qq邮箱客户端可以正常显示
- 启动时运行run.py文件即可



![image](https://github.com/williamzhanggg/subscription/blob/master/other/screenshot/Screenshot_20180623-104654.jpg?raw=true)



![image](https://github.com/williamzhanggg/subscription/blob/master/other/screenshot/Screenshot_20180623-104800.jpg?raw=true)
