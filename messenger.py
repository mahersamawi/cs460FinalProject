import socket
from time import sleep


class Messenger():

    @staticmethod
    def send_message(url, port, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = (url, int(port))
        client_socket.sendto(message, addr)
        client_socket.close()
        return True

    @staticmethod
    def set_up_listening_socket(port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.settimeout(10)
        listen_addr = ("", int(port))
        server_socket.bind(listen_addr)
        return server_socket

    @staticmethod
    def get_msg_type(msg):
        return msg.split(",")[0]

    @staticmethod
    def strip_msg(msg):
        return msg.split(",")[1:]
