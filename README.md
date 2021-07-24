# 介绍
掘金签到抽奖 github actions，可以实现定时自动签到抽奖。

juejin.py 
基于 Selenium 的签到、抽奖脚本。使用 cookies 免登陆。可手动执行。

job.py 
基于 schedule 的轻量化定时任务。启动后会按照设定时间定时执行 juejin 脚本。

robot.py
基于 钉钉 webhook 的通知服务。可以在 job 执行后发送通知消息。

app.py 
基于 flask 的 API 服务。可以使用接口来更新过期的 cookies。


# 快速使用

## fork本仓库
fork本仓库


## 配置 cookies

1.获取 cookies
使用 Chrome 插件 `EditThisCookie` 来导出 cookies 列表

2.使用json压缩工具进行json压缩

3.复制到文本暂存，并且最外层包裹一对单引号 ''

```

'[{"domain":".juejin.cn","expirationDate":1634104506,"hostOnly":false,"httpOnly":false,"name":"_tea_utm_cache_2608","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"****","id":1},{"domain":".juejin.cn","expirationDate":1634783500.868403,"hostOnly":false,"httpOnly":false,"name":"MONITOR_WEB_ID","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"****","id":2},{"domain":".juejin.cn","expirationDate":1632306612.470033,"hostOnly":false,"httpOnly":true,"name":"n_mh","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"****","id":3},{"domain":".juejin.cn","expirationDate":1627122573.421149,"hostOnly":false,"httpOnly":false,"name":"passport_csrf_token","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"****","id":4},{"domain":".juejin.cn","expirationDate":1627122573.421113,"hostOnly":false,"httpOnly":false,"name":"passport_csrf_token_default","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"****","id":5},{"domain":".juejin.cn","expirationDate":1627122612.470014,"hostOnly":false,"httpOnly":true,"name":"sessionid","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"****","id":6},{"domain":".juejin.cn","expirationDate":1627122612.470023,"hostOnly":false,"httpOnly":true,"name":"sessionid_ss","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"****","id":7},{"domain":".juejin.cn","expirationDate":1653042612.469971,"hostOnly":false,"httpOnly":true,"name":"sid_guard","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"****","id":8},{"domain":".juejin.cn","expirationDate":1627122612.470004,"hostOnly":false,"httpOnly":true,"name":"sid_tt","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"****","id":9},{"domain":".juejin.cn","expirationDate":1627122612.469983,"hostOnly":false,"httpOnly":true,"name":"uid_tt","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"****","id":10},{"domain":".juejin.cn","expirationDate":1627122612.469993,"hostOnly":false,"httpOnly":true,"name":"uid_tt_ss","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"****","id":11},{"domain":"juejin.cn","expirationDate":1658543501,"hostOnly":true,"httpOnly":false,"name":"tt_scid","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":".****","id":12},{"domain":"juejin.cn","expirationDate":1657155093,"hostOnly":true,"httpOnly":false,"name":"ttcid","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"****","id":13}]'



```



## 配置钉钉推送

https://developers.dingtalk.com/document/app/overview-of-group-robots
按照上面的官方文档进行配置机器人，获取到 access token 和 secrets

## 创建仓库的 Actions secrets

仓库->Setting->Secrets

创建三个：

- COOKIES 使用粘贴板中cookies数据， 注意：最外层需要用单引号包裹住 ''
- DING_ACCESS_TOKEN  钉钉的access token
- DING_SECRET 钉钉的 secrets




## 启用GitHub actions

点击仓库下方的actions 启用workflow


 