import socket
from messenger import *
from time import sleep

LISTEN_PORT = 3838


def add_new_victim():
    print "Adding New Victim"


def main():
    while True:
        victim, data = Messenger.listen(PORT)
        print "Victim IP is %s" % (victim)
        print data


if __name__ == '__main__':
    main()
