import socket
from contextlib import closing

from line import callBoxLine
from lineNotifyMessage import lineNotifyMessage


def main():
    erp_uat_server = check_server_factory('ERP UAT Server', '10.77.9.101', '80')
    erp_uat_server.check()
    bpm_uat_server = check_server_factory('BPM UAT Server', '10.77.9.103', '8086')
    bpm_uat_server.check()
    crt_uat_server = check_server_factory('Crystal Report UAT Server', '10.77.9.105', '80')
    crt_uat_server.check()


def send_line_message(server, host, port):
    # callBoxLine("BPM Server can not be used now!!")

    # 修改為你要傳送的訊息內容
    message = server + '(' + host + ') Port ' + port + ' 無法Ping通!'
    # 修改為你的權杖內容
    token = 'UslqqsBVGwcn0RJcI9R9vyx5TeWX66wYP6AlZtnHU9v'

    lineNotifyMessage(token, message)


class check_server_factory():

    def __init__(self, server, host, port_list):
        self.server = server
        self.host = host
        self.port_list = port_list

    def check(self):
        port_list = self.port_list.split(':')
        for port in port_list:
            if not check_socket(self.host, int(port)):
                send_line_message(self.server, self.host, port)


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