import socket
from messenger import *
from time import sleep

PORT = 8888


def add_new_victim():
    print "Adding New Victim"


MSG_DICT = {
    'JOIN': add_new_victim
}


def main():
    while True:
        victim, data = Messenger.listen(PORT)
        print "Victim IP is %s" % (victim)
        print data
        MSG_DICT.get(data)()


if __name__ == '__main__':
    main()
