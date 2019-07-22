import socket
from contextlib import closing

from line import callBoxLine
from lineNotifyMessage import lineNotifyMessage


def main():

    host = '10.77.9.103'
    port = 8086

    check_socket(host, port)

def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            print
            "Port is open"
        else:
            print
            "Port is not open"
            # callBoxLine("BPM Server can not be used now!!")

            # 修改為你要傳送的訊息內容
            message = 'BPM Server 10.77.9.103 Port 8086 無法Ping通!'
            # 修改為你的權杖內容
            token = 'UslqqsBVGwcn0RJcI9R9vyx5TeWX66wYP6AlZtnHU9v'

            lineNotifyMessage(token, message)
if __name__ == '__main__':
    main()