from flask import Flask, request
from functools import wraps
import hashlib
import json
import datetime

app = Flask(__name__)

def auth_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        sign = request.args.get('sign')
        key = 'juejin' + datetime.datetime.now().strftime('%Y%m%d')
        key_md5 = hashlib.md5(bytes(key, encoding='utf-8')).hexdigest()
        if sign in [key_md5, ]:
            return func(*args, **kwargs)
        else:
            return '无权访问！'
    return decorated_function

@app.route('/', methods=['GET','POST'])
@auth_required
def index():
    if request.method == 'POST':
        cookies = request.form.get('cookies')
        if not cookies:
            return '😩 invalid params!'
        try:
            if not isinstance(json.loads(cookies), list):
                return '😩 invalid params!'
        except Exception:
            return '😩 invalid params!'

        with open('cookies.txt', "w") as f:
            f.write(cookies)
            return '😆 success!'

        return "🤯 system error!"

    return '😥 ???'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)