> 2022 年 2 月 21 日起，掘金官方将正式**禁止脚本签到**行为，违者可能会被**封号**，请珍惜自己的账号。

> 本脚本仅用于学习，请勿用于扰乱社区秩序。

# 介绍
每个部件都是相互独立的，可以按需使用。
值得一提的是，由于是自己使用。所以 cookies 和钉钉/ 飞书机器人 token 使用比较随意。
建议使用者自己在优化一下，提高安全性。

juejin.py 
基于 Selenium 的签到、抽奖脚本。使用 cookies 免登陆。可手动执行。

job.py 
基于 schedule 的轻量化定时任务。启动后会按照设定时间定时执行 juejin 脚本。

robot.py
基于 钉钉/ 飞书 webhook 的通知服务。可以在 job 执行后发送通知消息。

app.py 
基于 flask 的 API 服务。可以使用接口来更新过期的 cookies。

# 安装部署
## 安装依赖
在项目根目录使用 poetry 安装依赖，包括 Selenium、schedule、flask 等库。
```bash
poetry install
```

## 配置 chromedriver （或其他浏览器驱动）

1.下载 chromedriver

淘宝镜像资源地址：http://npm.taobao.org/mirrors/chromedriver/

根据你的 Chrome 版本下载对应的 chromedriver

2.配置到环境变量

windows 放在 Python 安装地址根目录下

mac 与 linux 放在 /usr/local/bin

* 记得关闭 Chrome 的自动更新，否则一段时间后会出现与chromedriver版本不匹配的问题

# 配置 cookies
> cookies 信息很重要，注意不要泄露。

1.获取 cookies
使用 Chrome 插件 `EditThisCookie` 来导出 cookies 列表

* juejin 的 cookies 大概 60 天左右失效

2.存放 cookies

手动创建方式：

在项目根目录创建 `cookies.txt` 文件来存放 cookies 列表信息

接口创建方式：

启动 flask 服务后，通过接口更新 cookies 信息
    
# 配置 钉钉机器人/ 飞书机器人（默认）
> token & secret 信息很重要，注意不要泄露。

1.在项目根目录创建 `config.yaml` 文件来存放机器人认证信息

```yaml
# Dingtalk robot token & secret
DINGTALK_ACCESS_TOKEN: "你的机器人 access token 字段"
DINGTALK_SECRET: "你的机器人 secret 字段"

# Feishu robot token & secret (optional)
FEISHU_ACCESS_TOKEN: "你的机器人 access token 字段"
FEISHU_SECRET: "你的机器人 secret 字段（机器人开启了签名校验才需要）"

# Which one do you want to use? "FEISHU" or "DINGTALK"
ROBOT_TYPE: "FEISHU"
```

请参考官网文档配置后把上述信息填入
https://developers.dingtalk.com/document/app/overview-of-group-robots
https://www.feishu.cn/hc/zh-CN/articles/360024984973

修改 job.py 中你要使用的机器人
    
# 使用
1.手动执行一次
    
```bash
poetry run python juejin.py
```

2.启动定时执行服务

```bash
poetry run python job.py
```

3.启动接口服务
        
```bash
poetry run puthon app.py
```
