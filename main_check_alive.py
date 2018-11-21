import threading
import socket
import datetime
from send_email_alive import send_email

##################################################
# MQ 地址
mq_ip = 'localhost'
# MQ 端口
mq_port = 15671
##################################################
# 检查频率（秒）
check_alive_loop = 60
##################################################


# 检查MQ队列是否连接
def check_alive(ip, port):
    print('Check Loop:', datetime.datetime.now())
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        # 连接服务器
        sk.connect((ip, port))
    except:
        print('连接RabbitMQ服务器失败，请检查网络。')
        # 发邮件,发邮件频率由调用方法自己控制。
        send_email()
    sk.close()
    # 因为定时器构造后只执行1次，必须循环调用。
    global check_alive_timer
    timer = threading.Timer(check_alive_loop, check_alive, args=(mq_ip, mq_port))
    timer.start()

# 首次启动时用：
check_alive_timer = threading.Timer(check_alive_loop, check_alive, args=(mq_ip, mq_port))
check_alive_timer.start()
