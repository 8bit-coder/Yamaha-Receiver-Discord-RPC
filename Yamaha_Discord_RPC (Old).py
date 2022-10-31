from pypresence import Presence
import socket
import time

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

curSong = ""
prevSong = ""
defaultText = " - "
idleText = "Playback Stopped"
connectedToDiscord = False

class YamahaAPI:
    def __init__(self, ip):
        clientSocket.connect((ip,50000))
        self.data = [""]
        self.cacheSong = idleText
        self.cacheArtist = defaultText
        self.cacheAlbum = defaultText
        self.cacheModel = defaultText
        
    def UpdateData(self):
        data = "@SERVER:SONG=?"+"\r\n"
        clientSocket.send(data.encode())
        data = "@SERVER:ARTIST=?"+"\r\n"
        clientSocket.send(data.encode())
        data = "@SERVER:ALBUM=?"+"\r\n"
        clientSocket.send(data.encode())
        data = "@SYS:MODELNAME=?"+"\r\n"
        clientSocket.send(data.encode())
        receiveData = clientSocket.recv(1024)
        returnedStrings = receiveData.decode().replace("\r","").split("\n")
        self.data = returnedStrings

    def GetCurSong(self):
        curData = self.data
        for i in range(len(curData)):
            if curData[i].startswith("@SERVER:SONG="):
                if curData[i] == "@SERVER:SONG=":
                    return(self.cacheSong)
                else:
                    self.cacheSong = curData[i].replace("@SERVER:SONG=","")
                    return(curData[i].replace("@SERVER:SONG=",""))
        return(self.cacheSong)

    def GetCurArtist(self):
        curData = self.data
        for i in range(len(curData)):
            if curData[i].startswith("@SERVER:ARTIST="):
                if curData[i] == "@SERVER:ARTIST=":
                    return(self.cacheArtist)
                else:
                    self.cacheArtist = curData[i].replace("@SERVER:ARTIST=","")
                    return(curData[i].replace("@SERVER:ARTIST=",""))
        return(self.cacheArtist)

    def GetCurAlbum(self):
        curData = self.data
        for i in range(len(curData)):
            if curData[i].startswith("@SERVER:ALBUM="):
                if curData[i] == "@SERVER:ALBUM=":
                    return(self.cacheAlbum)
                else:
                    self.cacheAlbum = curData[i].replace("@SERVER:ALBUM=","")
                    return(curData[i].replace("@SERVER:ALBUM=",""))
        return(self.cacheAlbum)

    def GetModel(self):
        curData = self.data
        for i in range(len(curData)):
            if curData[i].startswith("@SYS:MODELNAME="):
                if curData[i] == "@SYS.MODELNAME=":
                    return(self.cacheModel)
                else:
                    self.cacheModel = curData[i].replace("@SYS:MODELNAME=","")
                    return(curData[i].replace("@SYS:MODELNAME=",""))
        return(self.cacheModel)

    def playbackStatus(self):
        curData = self.data
        for i in range(len(curData)):
            if curData[i].startswith("@SERVER:PLAYBACKINFO=Play"):
                return True
            if curData[i].startswith("@SERVER:PLAYBACKINFO=Stop"):
                self.cacheSong = idleText
                self.cacheArtist = defaultText
                self.cacheAlbum = defaultText
                return False

Receiver = YamahaAPI("192.168.1.143")

client_id = "1035741925468291134"
RPC = Presence(client_id)
RPC.connect()

while True:
    time.sleep(0.25)

    Receiver.UpdateData()
    
    prevSong = curSong
    curSong,curArtist,modelInfo = Receiver.GetCurSong(),Receiver.GetCurArtist(),Receiver.GetModel()
        
    if curSong != prevSong:
        start_time=time.time()
        
    if Receiver.playbackStatus() == True:
        RPC.update(large_image="yamaha-logo-light", large_text="Yamaha " + modelInfo, details=curSong, state=curArtist, start=start_time)
    else:
        RPC.update(large_image="yamaha-logo-light", large_text="Yamaha " + modelInfo, details=curSong, state=curArtist, start=start_time)
