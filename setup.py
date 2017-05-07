import os
from messenger import *
from victim_node import *
from attack_server import *
from time import sleep
from threading import Thread

PORT = 3838
VICTIM_PORT = 4848


def main():
    # Static IP
    Server_ip = "10.195.243.246"
    msg = "JOIN," + Server_ip
    vict = Victim()
    vict.process_new_victim("JOIN")

    listen_for_attacks = Thread(None, vict.processing_thread,)
    listen_for_attacks.start()
    listen_for_attacks.join()


if __name__ == '__main__':
    main()
