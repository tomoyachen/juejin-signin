from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
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
    browser.implicitly_wait(3)
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

    # 访问签到页
    browser.get(f'{DOMAIN}/user/center/signin?from=main_page')
    time.sleep(3)

    # 签到
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

    # 访问抽奖页
    browser.get(f'{DOMAIN}/user/center/lottery?from=sign_in_success')
    if '/lottery' not in browser.current_url:
        lottery_links = browser.find_elements_by_xpath("//*[contains(text(),' 幸运抽奖')]")
        lottery_links[-1].click()
    time.sleep(3)

    # 沾喜气
    if is_element_present('#stick-txt-0'):
        print("开始沾喜气")
        lucky_btn = browser.find_element_by_css_selector('#stick-txt-0')
        close_footer_banner(browser)
        lucky_btn.click()
        if is_element_present('.wrapper > .footer > button'):
            try:
                modal_confirm_btn = browser.find_element_by_css_selector('.wrapper > .footer > button')
                modal_confirm_btn.click()
            except Exception as e:
                print("关闭沾喜气弹层失败", e)
                browser.refresh()
        else:
            browser.refresh()
    else:
        print("沾喜气异常")

    # 抽奖
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
                modal_title_list = browser.find_elements_by_css_selector('div.byte-modal__body > div > div.title')
                job_result.prize = modal_title_list[-1].text if modal_title_list else "未知奖励"
                print(job_result.prize)

        else:
            print("无需抽奖")
    else:
        print("抽奖异常")
        job_result.status = SigninStatus.ERROR
        job_result.msg += "抽奖异常"

    # 浏览几篇帖子
    try:
        view_articles_from_home_page(browser, 3)
    except:
        pass

    browser.close()

    return job_result

def check_cookies_expires() -> int:
    """
    获取距离过期时间还有几天
    :return:
    """
    for cookie in get_cookies():
        if cookie.get("name") == "sessionid":
            expiration_date = int(cookie.get("expirationDate") or 0)

            from datetime import datetime, timedelta
            now:datetime = datetime.utcnow() + timedelta(hours=8)
            expires:datetime = datetime.utcfromtimestamp(expiration_date) + timedelta(hours=8)

            return (expires - now).days

def close_footer_banner(browser: WebDriver):
    """
    关闭底部的广告位
    :return:
    """
    elements = browser.find_elements_by_css_selector('.ion-close')
    for element in elements:
        if element.is_displayed():
            element.click()

# TODO 显性等待太多..
def view_articles_from_home_page(browser: WebDriver, limit: None):
    """
    在首页浏览几篇文章
    :return:
    """
    browser.get(DOMAIN)
    time.sleep(5)
    articles = browser.find_elements_by_css_selector('.title-row > .title')
    first_tab = browser.current_window_handle
    for acticle in articles[0:limit]:
        browser.switch_to.window(first_tab)
        browser.execute_script('window.scrollBy(0, 30)')
        if acticle.is_displayed():
            close_footer_banner(browser)
            acticle.click()
            time.sleep(2)
            browser.switch_to.window(browser.window_handles[-1])
            print(f'浏览了 {browser.title}')
            browser.execute_script('window.scrollBy(0, 200)')
            time.sleep(1)
            browser.execute_script('window.scrollBy(0, 300)')
            time.sleep(1)
        else:
            break


if __name__ == '__main__':
    run()
