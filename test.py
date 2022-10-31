from Log import Logger

# log = Logger("./log")
# log.writeAccesslog("success")
#

#定时 do
import datetime
import time
def time_printer():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func time :', ts)
def loop_monitor():
    while True:
        time_printer()
        time.sleep(5)  # 暂停5秒
if __name__ == "__main__":
    loop_monitor()