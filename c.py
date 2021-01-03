import socket
import base64

PORT = 9999
SERVER = socket.gethostname()
DC = "close"
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((SERVER,PORT))


def welcome():
    server_msg = client_socket.recv(1024)
    print(server_msg.decode("utf-8"))

def send():
    message_input = input(" -> ")
    while message_input.lower().strip() != DC:
        message = message_input.encode('utf-8')
        msg_len = len(message)
        send_len = str(msg_len).encode('utf-8')
        send_len += b' ' *(1024 - len(send_len))
        client_socket.send(send_len)
        client_socket.send(message)
        server_msg = client_socket.recv(1024)
        print(server_msg.decode("utf-8"))
        message_input = input(" -> ")
    client_socket.close()

welcome()
send()

