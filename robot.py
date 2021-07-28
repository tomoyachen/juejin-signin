import time
import hmac
import hashlib
import base64
import urllib.parse
import json
import requests
import yaml

def get_config(key: str) -> str:
    config = {}
    try:
        with open("config.yaml", "r", encoding='utf8') as f:
            text = f.read()
        config = yaml.load(text, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        print("文件不存在，已自动创建", e)
        new_file = open('config.yaml', 'w', encoding='utf8')
        new_file.write('# 钉钉机器人 token & secret\nACCESS_TOKEN: "你的机器人 access token 字段"\nSECRET: "你的机器人 secret 字段"')
        new_file.close()
    if key and key in config:
        return config[key]
    return ""

class Robot():

    def __init__(self):
        self.url = 'https://oapi.dingtalk.com/robot/send'
        self.access_token = get_config('ACCESS_TOKEN')
        self.secret = get_config('SECRET')

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


if __name__ == '__main__':
    print(Robot().send_markdown("标题", "内容"))