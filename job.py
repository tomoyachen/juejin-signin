import time
import schedule
from robot import Robot

def juejin_signin_job(*args):
    import juejin
    result = juejin.run()
    if result == 1:
        Robot().send_markdown("成功", "签到成功、抽奖失败")
    if result == 2:
        Robot().send_markdown("成功", "无需签到、抽奖成功")
    if result == 0:
        Robot().send_markdown("失败", "无需签到、无需抽奖")
    if result < 0:
        Robot().send_markdown("失败", "系统异常")



# 每隔 3600秒 执行一次 job
# schedule.every(3600).seconds.do(juejin_signin_job)

# 每天 10:00 执行 job
schedule.every().day.at('10:00').do(juejin_signin_job)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
