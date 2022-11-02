import socket
import time
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
defaultText = " - "

class YamahaAPI:
    def __init__(self, ip):
        clientSocket.connect((ip,50000))

Receiver = YamahaAPI("192.168.1.143")

inputName = "SERVER"

while 1:
    data = "@" + inputName + ":SONG=?"+"\r\n"
    data = data + "@" + inputName + ":ARTIST=?"+"\r\n"
    data = data + "@" + inputName + ":ALBUM=?"+"\r\n"
    data = data + "@SYS:MODELNAME=?"+"\r\n"
    data = data + "@MAIN:INP=?"+"\r\n"
    data = data + "@MAIN:VOL=?"+"\r\n"
    data = data + "@MAIN:STRAIGHT=?"+"\r\n"
    data = data + "@MAIN:SOUNDPRG=?"+"\r\n"
    clientSocket.send(data.encode())
    time.sleep(0.05)
    receiveData = clientSocket.recv(1024)
    dataInfo = str(receiveData.decode()).replace("\r","").split("\n")
    print(dataInfo)
