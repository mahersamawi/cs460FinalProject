import os
from messenger import *
from victim_node import *
from attack_server import *
from time import sleep
from threading import Thread

PORT = 3838
VICTIM_PORT = 4848


def main():
    test = "127.0.0.1"
    msg = "JOIN," + test
    vict = Victim()

    vict.process_new_victim("JOIN")

    listen_for_attacks = Thread(None, vict.processing_thread,)

    listen_for_attacks.start()

    while True:
        if raw_input() == "EXIT":
            os.system('kill -9 %d' % os.getpid())
    listen_for_attacks.join()


if __name__ == '__main__':
    main()
