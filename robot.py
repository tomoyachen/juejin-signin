import time
import hmac
import hashlib
import base64
import urllib.parse
import json
import requests

class Robot():

    def __init__(self,access_token,secret):
        self.url = 'https://oapi.dingtalk.com/robot/send'
        self.access_token = access_token
        self.secret = secret

    def get_sign(self, timestamp):
        secret = self.secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def send_markdown(self, title, msg, at_mobiles=[]):
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
        print(params)
        r = requests.post(self.url, params=params, data=json.dumps(data), headers=headers)
        return r.text


if __name__ == '__main__':
    print(Robot(access_token='18a2121b45615926ffac4f813e7434e01adca99f52ba9d640fabfcacea26023b',secret='SEC1d5964abe24c4d39f295f33fad9cff9babf25fe10131639f44c7dae1668c375f').send_markdown("标题", "内容"))