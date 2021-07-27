from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import re
import json
import time
from enum import Enum, unique

DOMAIN = 'https://juejin.cn'

chrome_options = Options()
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')

@unique
class SigninStatus(Enum):
    NORMAL = 0
    SIGNINED_AND_LOTTERY_DREW = 1
    SIGNINED = 2
    LOTTERY_DREW = 3
    ERROR = -1

def get_cookies():
    with open("cookies.txt", "r") as f:
        text = f.read()
    cookies = []
    try:
        text = re.sub('"sameSite": "(.+?)",', '"sameSite": "None",', text)
        cookies = json.loads(text)
    except json.decoder.JSONDecodeError as e:
        print("cookies 格式错误", e)
    except Exception as e:
        print("未知错误", e)

    return cookies

def run() -> dict:
    status = SigninStatus.NORMAL
    points = None
    prize = None

    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(DOMAIN)

    cookies = get_cookies()

    if not cookies:
        print("cookies 异常")
        return SigninStatus.ERROR

    for cookie in cookies:
        browser.add_cookie(cookie)

    def is_element_present(css):
        try:
            browser.find_element_by_css_selector(css)
        except NoSuchElementException:
            return False
        return True

    browser.refresh()
    browser.get(f'{DOMAIN}/user/center/signin?from=main_page')
    time.sleep(3)

    if is_element_present('button.signin'):
        print("开始签到")
        browser.find_element_by_css_selector('button.signin').click()
        status = SigninStatus.SIGNINED
        time.sleep(1) # 等待弹层出现
        points = browser.find_element_by_css_selector('span.header-text > span').text
        print(points)

    elif is_element_present('button.signedin'):
        print("无需签到")
    else:
        print("签到异常")
        return SigninStatus.ERROR

    browser.get(f'{DOMAIN}/user/center/lottery?from=sign_in_success')
    time.sleep(3)

    if is_element_present('div.turntable-item.item.lottery'):
        lottery_text = browser.find_element_by_css_selector('div.turntable-item.item.lottery > div.text')
        lottery_btn = browser.find_element_by_css_selector('div.turntable-item.item.lottery')
        if '免费抽奖：1次' in lottery_text.text:
            print("开始免费抽奖")
            lottery_btn.click()
            if status == SigninStatus.SIGNINED:
                status = SigninStatus.SIGNINED_AND_LOTTERY_DREW
            else:
                status = SigninStatus.LOTTERY_DREW
            time.sleep(10) # 等待转完奖品
            if is_element_present('div.byte-modal__header > span.byte-modal__title'):
                prize = browser.find_element_by_css_selector('div.byte-modal__body > div > div.title').text
                print(prize)

        else:
            print("无需抽奖")
    else:
        print("抽奖异常")
        return SigninStatus.ERROR

    browser.close()

    result = {
        "status": status,
        "data": {
            "points": points,
            "prize": prize
        }
    }

    return result

if __name__ == '__main__':
    run()
