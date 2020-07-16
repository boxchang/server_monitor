import socket
import time
from contextlib import closing

def main():
    #box = check_server_factory('Box Com', '10.231.220.203', '6400')
    box = check_server_factory('Box Com', '127.0.0.1', '6400')
    while(True):
        box.check()
        time.sleep(2)


class check_server_factory():

    def __init__(self, server, host, port_list):
        self.server = server
        self.host = host
        self.port_list = port_list

    def check(self):
        port_list = self.port_list.split(':')
        for port in port_list:
            if not check_socket(self.host, int(port)):
                print('lost 6400')


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