# Discord RPC Client for Network-Enabled Yamaha Receivers
# By Patrog Azadfekr (8bit_coder)
#
# TODO: Add functionality for detecting when a song is on repeat (eg. "@SERVER:REPEAT=?") ((ALSO make sure to only count repeats past the first play, this is done
# via a check that interprets the @?SERVER:SONG= command that executes every time a new song plays
# TODO: Add full mute detection functionality (eg. "@MAIN:MUTE=?")
# TODO: Add functionality for displaying album art??
# TODO: Add playcount tracking
# TODO: Add a configuration file for customizability(similar in style to wxllow/applemusicRP)
# TODO: Add optional "By" string in the second field (remember Pandora does things differently)
# TODO: Add funtionality for detecting advanced input names via @SYS:INPNAMEHDMI1=? and etc
# TODO: Add funtionality for detecting when receiver is turned off(to prevent socket errors and to quit the program0
# TODO: Get rid of initSource requirement and just detect the source at program startup

from pypresence import Presence
import socket
import time

receiverIP = open("config.txt", "r")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

curSong = ""
currentSource = ""
prevSource = ""
prevSong = ""
defaultText = " - "
idleText = "Playback Stopped"
initSource = "Server"

class YamahaAPI:
    def __init__(self, ip, source):
        clientSocket.connect((ip,50000))
        self.data = [""]
        self.cacheSong = idleText
        self.cacheArtist = defaultText
        self.cacheAlbum = defaultText
        self.cacheModel = defaultText
        self.mode = source
        self.cacheVolume = -40.0
        self.cacheSoundProgram = defaultText
        self.cacheSource = defaultText
        self.cachePlaybackStatus = "Play"
        
    def UpdateData(self):
        if self.mode == "PANDORA":
            data = "@" + self.mode + ":TRACK=?"+"\r\n"
            clientSocket.send(data.encode())
        else:
            data = "@" + self.mode + ":SONG=?"+"\r\n"
            clientSocket.send(data.encode())
        data = "@" + self.mode + ":ARTIST=?"+"\r\n"
        clientSocket.send(data.encode())
        data = "@" + self.mode + ":ALBUM=?"+"\r\n"
        clientSocket.send(data.encode())
        data = "@" + self.mode + ":PLAYBACKINFO=?"+"\r\n"
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
        receiveData = clientSocket.recv(1024)
        returnedStrings = receiveData.decode().replace("\r","").split("\n")
        self.data = returnedStrings
        # return returnedStrings

    def GetCurSong(self):
        curData = self.data
        for i in range(len(curData)):
            if self.mode == "PANDORA" or self.mode == "SPOTIFY":
                if curData[i].startswith("@" + self.mode + ":TRACK="):
                    if curData[i] == "@" + self.mode + ":TRACK=":
                        return(self.cacheSong)
                    else:
                        self.cacheSong = curData[i].replace("@" + self.mode + ":TRACK=","")
                        return(curData[i].replace("@" + self.mode + ":TRACK=",""))
            else:
                if curData[i].startswith("@" + self.mode + ":SONG="):
                    if curData[i] == "@" + self.mode + ":SONG=":
                        return(self.cacheSong)
                    else:
                        self.cacheSong = curData[i].replace("@" + self.mode + ":SONG=","")
                        return(curData[i].replace("@" + self.mode + ":SONG=",""))
        return(self.cacheSong)

    def GetCurArtist(self):
        curData = self.data
        for i in range(len(curData)):
            if curData[i].startswith("@" + self.mode + ":ARTIST="):
                if curData[i] == "@" + self.mode + ":ARTIST=":
                    return(self.cacheArtist)
                else:
                    self.cacheArtist = curData[i].replace("@" + self.mode + ":ARTIST=","")
                    return(curData[i].replace("@" + self.mode + ":ARTIST=",""))
        return(self.cacheArtist)

    def GetCurAlbum(self):
        curData = self.data
        for i in range(len(curData)):
            if curData[i].startswith("@" + self.mode + ":ALBUM="):
                if curData[i] == "@" + self.mode + ":ALBUM=":
                    return(self.cacheAlbum)
                else:
                    self.cacheAlbum = curData[i].replace("@" + self.mode + ":ALBUM=","")
                    return(curData[i].replace("@" + self.mode + ":ALBUM=",""))
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

    def GetPlaybackStatus(self):
        curData = self.data
        for i in range(len(curData)):
            if curData[i] == ("@" + self.mode + ":PLAYBACKINFO=Play"):
                return True
            if curData[i] == ("@" + self.mode + ":PLAYBACKINFO=Stop"):
                return False

    def SourceDetect(self):
        curData = self.data
        for i in range(len(curData)):
            if str(curData[i]).replace("\r\n","").startswith("@MAIN:INP="):
                currentSource = str(curData[i]).replace("\r\n","").replace("@MAIN:INP=","")
                self.mode = currentSource.upper()
                return currentSource
        return(self.cacheSource)

    def GetVolume(self):
        curData = self.data
        for i in range(len(curData)):
            if curData[i].startswith("@MAIN:VOL="):
                if curData[i] == "@MAIN:VOL=":
                    return(self.cacheVolume)
                else:
                    if curData[i].replace("@MAIN:VOL=","") == "-80.5":
                        self.cacheVolume = "Mute"
                        return("Mute")
                    else:
                        self.cacheVolume = curData[i].replace("@MAIN:VOL=","") + "dB"
                        return(curData[i].replace("@MAIN:VOL=","") + "dB")
        return(self.cacheVolume)

    def ResetPlaybackCache(self):
        self.cacheSong = idleText
        self.cacheArtist = defaultText
        self.cacheAlbum = defaultText

    def GetSoundProgram(self):
        curData = self.data
        for i in range(len(curData)):
            if curData[i].startswith("@MAIN:STRAIGHT=On"):
                self.cacheSoundProgram = "Straight"    
                return("Straight")
            if curData[i].startswith("@MAIN:SOUNDPRG="):
                if curData[i] == "@MAIN:SOUNDPRG=":
                    return(self.cacheSoundProgram)
                else:
                    self.cacheSoundProgram = curData[i].replace("@MAIN:SOUNDPRG=","")    
                    return(curData[i].replace("@MAIN:SOUNDPRG=",""))
            
        return(self.cacheSoundProgram)

Receiver = YamahaAPI(receiverIP.read(), initSource.upper())

client_id = "1035741925468291134"
RPC = Presence(client_id)
RPC.connect()

while True:
    time.sleep(0.25)

    Receiver.UpdateData()
    playbackStatus = Receiver.GetPlaybackStatus()
    
    prevSong = curSong
    prevSource = currentSource
    curSong,modelInfo,currentSource,currentVolume,currentSoundProgram = Receiver.GetCurSong(),Receiver.GetModel(), Receiver.SourceDetect(), Receiver.GetVolume(), Receiver.GetSoundProgram()

    if currentSource == "Pandora":
        curArtist = Receiver.GetCurAlbum()
    else:
        curArtist = Receiver.GetCurArtist()
        
    if curSong != prevSong or playbackStatus == False or currentSource != prevSource:
        start_time=time.time()
        Receiver.ResetPlaybackCache()

    if currentSource == "Pandora" or currentSource == "Rhapsody" or currentSource == "SiriusXM" or currentSource == "Pandora" or currentSource == "Spotify" or currentSource == "AirPlay" or currentSource == "SERVER" or currentSource == "USB":
        RPC.update(large_image="yamaha-logo-light", large_text=modelInfo + ": " + currentSource + " " + str(currentVolume), details=curSong, state=curArtist, start=start_time)
    else:
        RPC.update(large_image="yamaha-logo-light", large_text=modelInfo + ": " + str(currentVolume), details=currentSource, state=currentSoundProgram, start=start_time)
