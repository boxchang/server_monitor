import socket
from contextlib import closing

from line import callBoxLine
from lineNotifyMessage import lineNotifyMessage


def main():
    # TIPTOP
    erp_server = check_server_factory('ERP Server', '10.77.9.1', '80', 'ERP八○')
    erp_server.check()
    # result = erp_server.check()

    # erp_server = check_server_factory('ERP Server', '122.55.40.243', '18081')
    # result = erp_server.check()
    # if not result:
    erp_server = check_server_factory('ERP Server', '210.4.114.243', '18081', 'ERP(外)一八○八一')
    erp_server.check()

    # BPM
    bpm_server = check_server_factory('BPM Server', '10.77.9.3', '8086', 'BPM八○八六')
    bpm_server.check()
    # result = bpm_server.check()

    # bpm_server = check_server_factory('BPM Server', '122.55.40.243', '18083')
    # bpm_server.check()
    # result = bpm_server.check()
    # if not result:
    bpm_server = check_server_factory('BPM Server', '210.4.114.243', '18083', 'BPM(外)一八○八三')
    bpm_server.check()

    # Crystal Report
    crt_server = check_server_factory('Crystal Report Server', '10.77.9.2', '80', 'CRT八○')
    crt_server.check()
    # result = crt_server.check()

    # crt_server = check_server_factory('Crystal Report Server', '122.55.40.243', '80')
    # crt_server.check()
    # result = crt_server.check()
    # if not result:
    crt_server = check_server_factory('Crystal Report Server', '210.4.114.243', '80', 'CRT(外)八○')
    crt_server.check()


def send_line_message(server, host, port, msg):
    # callBoxLine("BPM Server can not be used now!!")

    # 修改為你要傳送的訊息內容
    message = msg + ' 無法用!'
    # 修改為你的權杖內容
    token = 'UslqqsBVGwcn0RJcI9R9vyx5TeWX66wYP6AlZtnHU9v'

    lineNotifyMessage(token, message)


class check_server_factory():

    def __init__(self, server, host, port_list, msg):
        self.server = server
        self.host = host
        self.port_list = port_list
        self.msg = msg

    def check(self):
        port_list = self.port_list.split(':')
        for port in port_list:
            if not check_socket(self.host, int(port)):
                send_line_message(self.server, self.host, port, self.msg)
                return False
            else:
                return True


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