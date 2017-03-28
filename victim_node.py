import socket
from messenger import *
from time import sleep

PORT = 8888

def main():
    my_ip = socket.gethostbyname(socket.gethostname())
    msg = "JOIN"
    Messenger.send_message(my_ip, PORT, msg)

def join_msg():
    pass

def listen_receive_command():
    pass


if __name__ == '__main__':
    main()
