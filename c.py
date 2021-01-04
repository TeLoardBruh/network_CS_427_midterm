import socket
import base64
from security import *

PORT = 9999
SERVER = "127.0.0.1"
DC = "close"
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((SERVER,PORT))

 
# def welcome():
global key
server_msg = client_socket.recv(1024)
print(server_msg.decode("utf-8"))
key = server_msg.decode("utf-8").split("key is :")[1]
print(key)

def send():
    message_input = input(" -> ")
    # print("some key :" + str(key))
    while message_input.lower().strip() != DC:
        en = cipher_encrypt(message_input,int(key))
        print(type(key))
        print("key ->" + key )
        print("encrypy ->"+en)
        message = message_input.encode('utf-8')
        msg_len = len(message)
        send_len = str(msg_len).encode('utf-8')
        send_len += b' ' *(1024 - len(send_len))
        client_socket.send(send_len)
        print(type(message))
        client_socket.send((message))
        server_msg = client_socket.recv(1024)
        print(server_msg.decode("utf-8"))
        message_input = input(" -> ")
    client_socket.close()
print(type(key))
# welcome()
send()

