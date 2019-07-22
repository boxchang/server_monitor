import socket
from contextlib import closing

from line import callBoxLine


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
            callBoxLine("BPM Server can not be used now!!")
if __name__ == '__main__':
    main()