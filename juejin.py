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

class JobResult():
    def __init__(self, status = SigninStatus.NORMAL, msg = ""):
        self.status = status
        self.msg = msg
        self.points = None,
        self.prize = None

def get_cookies() -> list:
    cookies = []
    try:
        with open("cookies.txt", "r", encoding='utf8') as f:
            text = f.read()
        text = re.sub('"sameSite": "(.+?)",', '"sameSite": "None",', text)
        cookies = json.loads(text)
    except FileNotFoundError as e:
        print("文件不存在，已自动创建", e)
        new_file = open('cookies.txt', 'w', encoding='utf8')
        new_file.write('使用 Chrome 插件 `EditThisCookie` 来导出 cookies 列表，粘入此文件')
        new_file.close()
    except json.decoder.JSONDecodeError as e:
        print("cookies 格式错误", e)
    except Exception as e:
        print("未知错误", e)

    return cookies

def run() -> JobResult:
    job_result = JobResult(SigninStatus.NORMAL)

    browser = webdriver.Chrome(options=chrome_options)
    browser.get(DOMAIN)

    cookies = get_cookies()

    if not cookies:
        print("cookies 异常")
        return JobResult(SigninStatus.ERROR, "cookies 异常")

    for cookie in cookies:
        browser.add_cookie(cookie)

    def is_element_present(css):
        try:
            browser.find_element_by_css_selector(css)
        except NoSuchElementException:
            return False
        return True

    browser.refresh()

    if not is_element_present('.nav-item .avatar'):
        print("cookies 失效")
        return JobResult(SigninStatus.ERROR, "cookies 失效")

    browser.get(f'{DOMAIN}/user/center/signin?from=main_page')
    time.sleep(3)

    if is_element_present('button.signin'):
        print("开始签到")
        browser.find_element_by_css_selector('button.signin').click()
        job_result.status = SigninStatus.SIGNINED
        time.sleep(1) # 等待弹层出现
        job_result.points = browser.find_element_by_css_selector('span.header-text > span').text
        print(job_result.points)

    elif is_element_present('button.signedin'):
        print("无需签到")
    else:
        print("签到异常")
        job_result.status = SigninStatus.ERROR
        job_result.msg = "签到异常"

    browser.get(f'{DOMAIN}/user/center/lottery?from=sign_in_success')
    if '/lottery' not in browser.current_url:
        lottery_links = browser.find_elements_by_xpath("//*[contains(text(),' 幸运抽奖')]")
        lottery_links[-1].click()
    time.sleep(3)

    if is_element_present('#turntable-item-0'):
        lottery_btn = browser.find_element_by_css_selector('#turntable-item-0')
        browser.execute_script("arguments[0].scrollIntoView();", lottery_btn)
        if is_element_present("div.text.text-free"):
            print("开始免费抽奖")
            lottery_btn.click()
            if job_result.status == SigninStatus.SIGNINED:
                job_result.status = SigninStatus.SIGNINED_AND_LOTTERY_DREW
            else:
                job_result.status = SigninStatus.LOTTERY_DREW
            time.sleep(10) # 等待转完奖品
            if is_element_present('div.byte-modal__header > span.byte-modal__title'):
                job_result.prize = browser.find_element_by_css_selector('div.byte-modal__body > div > div.title').text
                print(job_result.prize)

        else:
            print("无需抽奖")
    else:
        print("抽奖异常")
        job_result.status = SigninStatus.ERROR
        job_result.msg += "抽奖异常"

    browser.close()

    return job_result

if __name__ == '__main__':
    run()
