import time
import hmac
import hashlib
import base64
import urllib.parse
import json
import requests
import yaml

def get_config(key: str) -> str:
    NEW_YAML_FILE_TEMPLATE = '''# Dingtalk robot token & secret
DINGTALK_ACCESS_TOKEN: "你的机器人 access token 字段"
DINGTALK_SECRET: "你的机器人 secret 字段"

# Feishu robot token & secret (optional)
FEISHU_ACCESS_TOKEN: "你的机器人 access token 字段"
FEISHU_SECRET: "你的机器人 secret 字段（机器人开启了签名校验才需要）"

# Which one do you want to use? "FEISHU" or "DINGTALK"
ROBOT_TYPE: "FEISHU"
'''

    config = {}
    try:
        with open("config.yaml", "r", encoding='utf8') as f:
            text = f.read()
        config = yaml.load(text, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        print("文件不存在，已自动创建", e)
        new_file = open('config.yaml', 'w', encoding='utf8')
        new_file.write(NEW_YAML_FILE_TEMPLATE)
        new_file.close()
    if key and key in config:
        return config[key]
    return ""

class DingTalkRobot():

    def __init__(self):
        self.url = 'https://oapi.dingtalk.com/robot/send'
        self.access_token = get_config('DINGTALK_ACCESS_TOKEN')
        self.secret = get_config('DINGTALK_SECRET')

    def get_sign(self, timestamp) -> str:
        secret = self.secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def send_markdown(self, title, msg, at_mobiles=[]) -> dict:
        headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        timestamp = str(round(time.time() * 1000))
        params = {
                "access_token": self.access_token,
                "timestamp": timestamp,
                "sign": self.get_sign(timestamp)
        }
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": msg
            },
            "at": {
                "atMobiles": at_mobiles,
                "isAtAll": False
            },
        }
        # print(params)
        r = requests.post(self.url, params=params, data=json.dumps(data), headers=headers)
        return r.json()

class FeishuRobot():

    def __init__(self):
        self.access_token = get_config("FEISHU_ACCESS_TOKEN")
        self.secret = get_config("FEISHU_SECRET")
        self.url = f'https://open.feishu.cn/open-apis/bot/v2/hook/{self.access_token}'

    def get_sign(self, timestamp) -> str:
        secret = self.secret
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign

    def send_text(self, title, msg) -> dict:
        headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        timestamp = str(round(time.time()))
        params = {}
        data = {
            "timestamp": timestamp,
            "sign": self.get_sign(timestamp),
            "msg_type": "text",
            "content": {
                    "text": f'{title}\r\n{msg}'
            }
        }
        # print(params)
        r = requests.post(self.url, params=params, data=json.dumps(data), headers=headers)
        if r.status_code == 200:
            return r.json()

class Robot():
    def send(self, title, msg):
        robot_type = get_config('ROBOT_TYPE')
        if robot_type == 'DINGTALK':
            result = DingTalkRobot().send_markdown(title, msg)
            return result
        elif robot_type == 'FEISHU':
            result = FeishuRobot().send_text(title, msg)
            if 'StatusCode' in result:
                result["errcode"] = result['StatusCode']
                result["errmsg"] =  result['StatusMessage']
            elif 'code' in result:
                result["errcode"] = result['code']
                result["errmsg"] =  result['msg']
            return result

if __name__ == '__main__':
    res = Robot().send("标题", "内容")
    print(res)
