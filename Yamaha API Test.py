import socket
import time
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
defaultText = " - "

class YamahaAPI:
    def __init__(self, ip):
        clientSocket.connect((ip,50000))

Receiver = YamahaAPI("192.168.1.131")

input = AIRPLAY

while 1:
    data = "@" + input + ":SONG=?"+"\r\n"
    clientSocket.send(data.encode())
    data = "@" + input + ":ARTIST=?"+"\r\n"
    clientSocket.send(data.encode())
    data = "@" + input + ":ALBUM=?"+"\r\n"
    clientSocket.send(data.encode())
    data = "@SYS:MODELNAME=?"+"\r\n"
    clientSocket.send(data.encode())
    data = "@MAIN:INP=?"+"\r\n"
    clientSocket.send(data.encode())
    data = "@MAIN:VOL=?"+"\r\n"
    clientSocket.send(data.encode())
    data = "@MAIN:STRAIGHT=?"+"\r\n"
    clientSocket.send(data.encode())
    data = "@MAIN:SOUNDPRG=?"+"\r\n"
    clientSocket.send(data.encode())
    time.sleep(0.1)
    receiveData = clientSocket.recv(1024)
    print(receiveData)