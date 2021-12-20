import time
import schedule
from robot import Robot
import juejin

def juejin_signin_job(*args):

    try:
        job_result = juejin.run()
    except Exception as e:
        Robot().send('失败', f'脚本出错 {e}')

    status = job_result.status
    points = job_result.points
    prize = job_result.prize
    msg = job_result.msg

    if status == juejin.SigninStatus.SIGNINED_AND_LOTTERY_DREW:
        noty_title, noty_msg = "成功", f"签到成功（{points}）、抽奖成功（{prize}）"
    elif status == juejin.SigninStatus.SIGNINED:
        noty_title, noty_msg = "成功", f"签到成功（{points}）、无需抽奖"
    elif status == juejin.SigninStatus.LOTTERY_DREW:
        noty_title, noty_msg = "成功", f"无需签到、抽奖成功（{prize}）"
    elif status == juejin.SigninStatus.NORMAL:
        noty_title, noty_msg = "成功", "无需签到、无需抽奖"
    elif status == juejin.SigninStatus.ERROR:
        noty_title, noty_msg = "失败", f"{msg}"
    else:
        noty_title, noty_msg = "失败", "未知错误"

    noty_result = Robot().send(noty_title, noty_msg)

    if noty_result['errcode'] == 0:
        print('通知成功')
    else:
        print('通知失败', noty_result['errmsg'])

# 每隔 3600秒 执行一次 job
# schedule.every(3600).seconds.do(juejin_signin_job)

# 每天 10:00 执行 job
schedule.every().day.at('10:00').do(juejin_signin_job)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
