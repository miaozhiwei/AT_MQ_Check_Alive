import threading
import socket
import datetime
from send_email_alive import send_email

##################################################
# MQ 地址
mq_ip = 'localhost'
# MQ 端口
mq_port = 5672
##################################################
# 检查频率（秒）
check_alive_loop = 60
# 连续失败次数
check_alive_times = 0
##################################################


# 检查MQ队列是否连接
def check_alive(ip, port):
    global check_alive_times
    print('Check Alive Loop:', datetime.datetime.now())
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(3)
    try:
        # 连接服务器
        s = sk.connect((ip, port))
        # 如果连接成功，计数器清零。如果连接失败，不会执行。
        check_alive_times = 0
    except:
        check_alive_times = check_alive_times + 1
        print('连接RabbitMQ服务器失败 %d 次' % check_alive_times)
        if check_alive_times >= 3:
            # 发邮件,发邮件频率由调用方法自己控制。
            send_email()
            check_alive_times = 0
    sk.close()
    # 因为定时器构造后只执行1次，必须循环调用。
    global check_alive_timer
    timer = threading.Timer(check_alive_loop, check_alive, args=(mq_ip, mq_port))
    timer.start()

# 首次启动时用：
check_alive_timer = threading.Timer(check_alive_loop, check_alive, args=(mq_ip, mq_port))
check_alive_timer.start()
