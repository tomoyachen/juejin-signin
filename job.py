import time
import schedule
from robot import Robot
import juejin

def juejin_signin_job(*args):

    result = juejin.run()
    status = result["status"]
    points = result["data"]["points"]
    prize = result["data"]["prize"]

    if status == juejin.SigninStatus.SIGNINED_AND_LOTTERY_DREW:
        Robot().send_markdown("成功", f"签到成功（{points}）、抽奖成功（{prize}）")
    elif status == juejin.SigninStatus.SIGNINED:
        Robot().send_markdown("成功", f"签到成功（{points}）、无需抽奖")
    elif status == juejin.SigninStatus.LOTTERY_DREW:
        Robot().send_markdown("成功", f"无需签到、抽奖成功（{prize}）")
    elif status == juejin.SigninStatus.NORMAL:
        Robot().send_markdown("成功", "无需签到、无需签到")
    elif status == juejin.SigninStatus.ERROR:
        Robot().send_markdown("失败", "系统异常")
    else:
        Robot().send_markdown("失败", "未知错误")



# 每隔 3600秒 执行一次 job
# schedule.every(3600).seconds.do(juejin_signin_job)

# 每天 10:00 执行 job
schedule.every().day.at('10:00').do(juejin_signin_job)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
