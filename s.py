import socket
import os.path
import base64
import random
from security import *

PORT = 9999
SERVER = "127.0.0.1"
DC = "close"
WRITE = 'write'
VIEW = 'view'
PROTOCOL_VERSION = 'SFTMP/1.0'
WELCOME_TEXT = 'STFMP supports three operations:\n- write: write content to the file : type write##filename##content to activate this\n- view: view content to the file : type view##filename##key_number to activate this\n- close: close the connection : type close to activate this'
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind((SERVER,PORT))
um_key = random.randint(0,9)

def hand_clinet(conn,addr):
    print(f"New connection {addr} connected")

    while True:
        msg_len = conn.recv(1024).decode('utf-8')
        print("before loop start")
        if not msg_len:
            break
        msg_len = int(msg_len)
        msg = conn.recv(msg_len).decode('utf-8')
        print("if loop start")
        if msg == DC: 
            print("case 1")
            connected = False
            print("Disconnected")
            conn.send(bytes("connection closed","utf-8"))
        elif msg.split("##")[0] == VIEW:
            print("case 3")
            filename = msg.split("##")[1]
            key = msg.split("##")[2] 
            if os.path.isfile(filename):
                f = open(filename, "r")
                de = cipher_decrypt(f.read(),int(key))
                print(de)
                conn.send(bytes(PROTOCOL_VERSION+"##ok##"+de,"utf-8"))            
                f.close()
            else:
                conn.send(bytes(PROTOCOL_VERSION+"##not_found##File not found.","utf-8"))   
        elif msg.split("##")[0] == WRITE:
            print("case 2")
            
            filename = msg.split("##")[1]
            filecontent = msg.split("##")[2]
            num_key = random.randint(0,9)
            en = cipher_encrypt(filecontent,num_key)
            print(repr(en))
            f = open(filename, "w")
            f.write(en)
            # conn.send(bytes(f.read(),"utf-8"))
            # print(f.read())
            f.close()
            conn.send(bytes(PROTOCOL_VERSION+"##ok##The file has been written.here is your Security key: "+str(num_key),"utf-8"))


        else:
            conn.send(bytes(PROTOCOL_VERSION+"##invalid##Invalid request.","utf-8"))
        print("end if loop")
        # print(msg.split("##"))
        en = cipher_encrypt(msg,int(um_key))
        print(f"{addr}: {en}")
            # print("end of loop")
            
    print("out of loop")
    
    conn.close()
    print("close conn")

def start():
    server_socket.listen()
    
    conn,addr = server_socket.accept()
    conn.send(bytes(WELCOME_TEXT + "\n"+ "Your key is :"+str(um_key),"utf-8"))
    hand_clinet(conn,addr)
    
    print("end")


print("SERVER IS UP AND RUNNING")
start()
# server_socket.listen()
