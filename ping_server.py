import socket
import time
from contextlib import closing

from line import callBoxLine
from lineNotifyMessage import lineNotifyMessage


def main():
    erp_server1 = check_server_factory('ERP Server', '10.77.9.1', '80', 'ERP八○')
    erp_server2 = check_server_factory('ERP Server', '210.4.114.243', '18081', 'ERP(外)一八○八一')
    bpm_server1 = check_server_factory('BPM Server', '10.77.9.3', '8086', 'BPM八○八六')
    bpm_server2 = check_server_factory('BPM Server', '210.4.114.243', '18083', 'BPM(外)一八○八三')
    crt_server1 = check_server_factory('Crystal Report Server', '10.77.9.2', '80', 'CRT八○')
    crt_server2 = check_server_factory('Crystal Report Server', '210.4.114.243', '80', 'CRT(外)八○')

    print("Start Monitor")
    while(True):
        print("Start Check")
        # TIPTOP
        result = erp_server1.check()
        if not result:
            erp_server1.count()
        else:
            erp_server1.reset_count()

        if erp_server1.getCount() > 3:
            send_line_message(erp_server1.server, erp_server1.host, erp_server1, erp_server1.msg)

        result = erp_server2.check()
        if not result:
            erp_server2.count()
        else:
            erp_server2.reset_count()

        if erp_server2.getCount() > 3:
            send_line_message(erp_server2.msg)


        # BPM
        result = bpm_server1.check()
        if not result:
            bpm_server1.count()
        else:
            bpm_server1.reset_count()

        if bpm_server1.getCount() > 3:
            send_line_message(bpm_server1.msg)

        result = bpm_server2.check()
        if not result:
            bpm_server2.count()
        else:
            bpm_server2.reset_count()

        if bpm_server2.getCount() > 3:
            send_line_message(bpm_server2.msg)


        # Crystal Report
        result = crt_server1.check()
        if not result:
            crt_server1.count()
        else:
            crt_server1.reset_count()

        if crt_server1.getCount() > 3:
            send_line_message(crt_server1.msg)

        result = crt_server2.check()
        if not result:
            crt_server2.count()
        else:
            crt_server2.reset_count()

        if crt_server2.getCount() > 3:
            send_line_message(crt_server2.msg)

        print("Stop Check")
        time.sleep(60)

def send_line_message(msg):
    # callBoxLine("BPM Server can not be used now!!")

    # 修改為你要傳送的訊息內容
    message = msg + ' 無法用!'
    # 修改為你的權杖內容
    token = 'UslqqsBVGwcn0RJcI9R9vyx5TeWX66wYP6AlZtnHU9v'

    lineNotifyMessage(token, message)


class check_server_factory():
    count_flag = 0

    def __init__(self, server, host, port_list, msg):
        self.server = server
        self.host = host
        self.port_list = port_list
        self.msg = msg

    def check(self):
        port_list = self.port_list.split(':')
        for port in port_list:
            if not check_socket(self.host, int(port)):
                return False
            else:
                return True

    def count(self):
        self.count_flag += 1

    def reset_count(self):
        self.count_flag = 0

    def getCount(self):
        return self.count_flag


def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            print
            "Port is open"
            return True
        else:
            print
            "Port is not open"
            return False

if __name__ == '__main__':
    main()