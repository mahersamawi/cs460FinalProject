import socket
from messenger import *
from time import sleep

PORT = 8888

def add_new_victim():
    print "Adding New Victim"


def main():
    while True:
        victim, data = Messenger.listen(PORT)
        print "Victim IP is %s" % (victim)
        MSG_TYPES.get(data)

MSG_TYPES = {}
MSG_TYPES['JOIN'] = add_new_victim()
if __name__ == '__main__':
    main()
