from messenger import *
from victim_node import *
from attack_server import *
from time import sleep


PORT = 3838


def main():
    vict = Victim()
    vict.processing_thread("DOS, 127.0.0.1, 20")
    return


if __name__ == '__main__':
    main()
