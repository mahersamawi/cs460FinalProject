from messenger import *
from victim_node import *
from attack_server import *
from time import sleep


PORT = 3838


def main():
    ip = "10.192.89.234"
    test = "127.0.0.1"
    msg = "DOS," + test + ",10" 
    msg2 = "DOS," + ip + ",2" 
    vict = Victim()
    vict.processing_thread(msg)
    return


if __name__ == '__main__':
    main()
