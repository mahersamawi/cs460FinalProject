import socket
from time import sleep


class Messenger():

    @staticmethod
    def send_message(url, port, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((url, port))
        client_socket.send(message)
        client_socket.close()

    @staticmethod
    def listen(port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_addr = ("", int(port))
        try:
            server_socket.bind(listen_addr)
        except:
            print "Unable to Bind"
        server_socket.listen(1)
        conn, addr = server_socket.accept()
        data = conn.recv(8192)
        if data:
            return (addr[0]), data
        server_socket.close()
