import time
# import schedule
from robot import Robot
import juejin
import argparse

cookies = ''
dingtalk_access_token = ''
dingtalk_secret = ''


def juejin_signin_job():

    result = juejin.run(cookies=cookies)
    if result == juejin.SigninStatus.SIGNINED_AND_LOTTERY_DREW:
        Robot(dingtalk_access_token,dingtalk_secret).send_markdown("成功", "签到成功、抽奖成功")
    elif result == juejin.SigninStatus.SIGNINED:
        Robot(dingtalk_access_token,dingtalk_secret).send_markdown("成功", "签到成功、无需抽奖")
    elif result == juejin.SigninStatus.LOTTERY_DREW:
        Robot(dingtalk_access_token,dingtalk_secret).send_markdown("成功", "无需签到、抽奖成功")
    elif result == juejin.SigninStatus.NORMAL:
        Robot(dingtalk_access_token,dingtalk_secret).send_markdown("成功", "无需签到、无需签到")
    elif result == juejin.SigninStatus.ERROR:
        Robot(dingtalk_access_token,dingtalk_secret).send_markdown("失败", "系统异常")
    else:
        Robot(dingtalk_access_token,dingtalk_secret).send_markdown("失败", "未知错误")



# 每隔 3600秒 执行一次 job
# schedule.every(3600).seconds.do(juejin_signin_job)

# 每天 10:00 执行 job
# schedule.every().day.at('10:00').do(juejin_signin_job)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description='please enter two parameters a and b ...'
    parser.add_argument("-a", "--inputA", help="this is parameter a", dest="argA", type=str)
    parser.add_argument("-b", "--inputB", help="this is parameter b", dest="argB", type=str)
    parser.add_argument("-c", "--inputC", help="this is parameter c", dest="argC", type=str)
    args = parser.parse_args()
    print(args)
    cookies = args.argA
    dingtalk_access_token = args.argB
    dingtalk_secret = args.argC  
    juejin_signin_job()
