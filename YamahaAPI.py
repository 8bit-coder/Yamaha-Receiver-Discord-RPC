import socket
import time
import re

#this formats the requests to be in the form of "@SERVER:SONG=?\r\n", mainly to reduce clutter
def RequestFormer(requestType, request, inputName = "SERVER", zone = "MAIN"): 
    endData = "\r\n"
    
    match requestType:
        case "zone":
            return str("@" + zone + ":" + request + "=?").upper() + endData
        case "system":
            return str("@SYS:" + request + "=?").upper() + endData
        case "source":
            return str("@" + inputName + ":" + request + "=?").upper() + endData

#this takes a string in the form of "1:03" and converts it to integer 63
def TimeStringToInt(timeString):
    time = 0
    
    try:
        timeList = timeString.split(":")
        time = (int(timeList[0]) * 60) + int(timeList[1])
        
        return(time)
    except Exception:
        return(time)

class YamahaAPI:
    """
    This API allows for requesting information from a network-enabled Yamaha receiver.
    
    Usage Instructions:
        YamahaAPI(IP, zone)
            IP:
                IP Address of the Yamaha receiver
            zone:
                zone to get data from, defaults to 1 (main)
        
        UpdateData(refreshInterval)
            refreshInterval:
                delay between requesting and reading data, defaults to 0.1 seconds (has hard cap at 0.025 to prevent errors)
        
        GetData(request, defaultString)
            request:
                string specifying data being requested (see list of requestable data)
            defaultString:
                string to return if data isn't found, defaults to empty string ("")
        
        LastChangeTimestamp(): returns timestamp of whenever last song or input was changed
        
    List of requestable data (case insensitive):
        Any zone:
            INP:
                Current input
            INPNAME:
                Current input name
                
            ZONENAME:
                Current zone name
            
            PWR:
                Power state of zone - returns "On" or "Off"
            SLEEP:
                Sleep timer - returns "Off", "120", "90", "60", or "30" in minutes
            VOL:
                Current zone volume - returns in dB from -80.5 to 16.5
            MUTE:
                Mute status - returns "On" or "Off"
            
        Main zone:
            SONG:
                Song Name
            ARTIST:
                Artist Name
            ALBUM:
                Album Name
            STATION:
                Net Radio Station
            BAND:
                Tuner band - returns "FM" or "AM"
            FMFREQ:
                FM Radio Frequency - returns in the format of "104.70" in MHz
            AMFREQ:
                AM Radio Frequency - returns in the format of "1130" in kHz
            PLAYBACKINFO:
                Playback status - returns "Play" or "Stop"
        
            MODELNAME:
                The model number - eg. "TSR-7790" or "RX-A820"
            
            SOUNDPRG:
                Sound program - returns the current sound program, eg. 7ch Stereo
            STRAIGHT:
                Sound program bypass toggle - returns "On" or "Off"
            PUREDIRMODE:
                Pure direct mode - returns "On" or "Off"
            
            PARTY:
                Party mode toggle - returns "On" or "Off"
            ENHANCER:
                Audio upscaler toggle - returns "On" or "Off"
            SWFRTRIM:
                Subwoofer volume trim - returns anywhere from "-6.0" to "6.0" in 0.5 dB increments
            TONEBASS:
                Bass tone control adjustment - returns anywhere from "-6.0" to "6.0" in 0.5 dB increments
            TONETREBLE:
                Treble tone control adjustment - returns anywhere from "-6.0" to "6.0" in 0.5 dB increments
            
            YPAOVOL:
                YPAO Volume toggle - returns "Auto" or "Off"
            EXBASS:
                Extra bass toggle - returns "Auto" or "Off"
            3DCINEMA:
                3D Cinema toggle - returns "Auto" or "Off"
            ADAPTIVEDRC:
                Adaptive Dynamic Range Control toggle - returns "Auto" or "Off"
            DIALOGUELVL:
                Dialogue Boost Level - returns 0 - 4
            
            HDMIOUT1:
                HDMI 1 enable state - returns "On" or "Off"
            HDMIOUT2:
                HDMI 2 enable state - returns "On" or "Off" (or UNAVAILABLE if the receiver doesn't have a second HDMI output)
    """
    defaultInput = "SERVER"
        
    def __init__(self, ip, zone = 1):
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a TCP socket
        self.tcpSocket.connect((ip,50000)) #connect to it
        
        self.volatileDataDictionary = {} #this dictionary will keep being cleared
        self.dataDictionary = {'INP': YamahaAPI.defaultInput} #this dictionary will only be cleared under new actions (eg. playing a new song, changing inputs, etc)
        
        self.lastChangeTimestamp = time.time() #this is the timestamp for when the last new action was performed
        
        match zone: #this is for multizone receivers and getting data from other zones
            case 1:
                self.zone = "MAIN"
            case 2:
                self.zone = "ZONE2"
            case 3:
                self.zone = "ZONE3"
            case 4:
                self.zone = "ZONE4"
            case _:
                self.zone = "MAIN"
        
    def UpdateData(self, refreshInterval = 0.1):
        match self.dataDictionary.get('INP'): #this resolves the receiver's returned input name to some internal names required for data requests
            case "Rhapsody":
                curInput = "RHAP"
            case "TUNER":
                curInput = "TUN"
            case "NET RADIO":
                curInput = "NETRADIO"
            case "Bluetooth":
                curInput = "BT"
            case _:
                curInput = self.dataDictionary.get('INP').upper()
        
        if refreshInterval <= 0.025: #sets the cap on refresh rate
            requestDelay = 0.025
        else:
            requestDelay = refreshInterval
        
        if self.zone == "MAIN":
            if curInput == "PANDORA" or curInput == "SPOTIFY":
                sendData = RequestFormer("source", "track", curInput) #spotify and pandora use track instead of song
            elif curInput == "TUN":
                sendData = RequestFormer("source", "band", curInput)
                sendData += RequestFormer("source", "fmfreq", curInput)
                sendData += RequestFormer("source", "amfreq", curInput)
            elif curInput == "NETRADIO":
                sendData = RequestFormer("source", "song", curInput)
                sendData += RequestFormer("source", "station", curInput)
            else:
                sendData = RequestFormer("source", "song", curInput)
            sendData += RequestFormer("source", "artist", curInput)
            sendData += RequestFormer("source", "album", curInput)
            sendData += RequestFormer("source", "soundprg", curInput)
            sendData += RequestFormer("source", "playbackinfo", curInput)
            
            sendData += RequestFormer("system", "modelname")
            sendData += RequestFormer("system", "party")
            
            sendData += RequestFormer("zone", "basic") #this gives a lot of fairly useless but nice data
            sendData += RequestFormer("zone", "zonename")
            if re.match(r'^(HDMI|AV|PHONO|AUDIO|VAUX|AUDIO|USB)', curInput): #eg. if the input is HDMI 1, request the full input name (Apple TV, Switch, etc.)
                sendData += RequestFormer("system", str("inpname" + curInput))
                
            self.tcpSocket.send(sendData.encode()) #send the full request
            
            time.sleep(requestDelay) #wait for the request to process and be sent back
            
            receivedData = self.tcpSocket.recv(8192).decode() #read the data
        else:
            sendData = RequestFormer("zone", "basic", zone = self.zone) #get zone data
            sendData += RequestFormer("zone", "zonename", zone = self.zone)
            if re.match(r'^(HDMI|AV|PHONO|AUDIO|VAUX|AUDIO|USB)', curInput):
                sendData += RequestFormer("system", str("inpname" + curInput))

            self.tcpSocket.send(sendData.encode())
            
            time.sleep(requestDelay)
            
            receivedData = self.tcpSocket.recv(8192).decode()
        
        #this dictionary is things that need to be stripped out of the final strings
        stringFixes = {
            "\r": "",
            "MAIN:": "",
            "SYS:": "",
            str(curInput + ":"): "",
            str(self.zone + ":"): ""
        }
        
        #perform the replacing using the stringFixes dictionary
        for old, new in stringFixes.items():
            receivedData = receivedData.replace(old, new)
        
        #split on newlines, remove last item as it's always empty
        splitData = receivedData.split("\n")[0:-1]
        
        #clear the working dictionary
        self.volatileDataDictionary.clear()
        
        for item in splitData: #for each item in the split data
            if item.startswith("@"): #if it starts with @ (to prevent corrupt data from being added to the dictionary)
                if item.count("=") >= 1: #if it has an = (to prevent corrupt data from being added to the dictionary)
                    #strip the '@', split on the first '=', make it into a tuple (x,y), put that tuple in a list, convert that to a dictionary, ie {x:y}
                    #and then finally put that into the working dictionary
                    self.volatileDataDictionary.update(dict([tuple(item.replace("@", "", 1).split("=", 1))])) 
        
        #this gathers all possible values that should be watched for whether to mark a new action
        curSong = self.volatileDataDictionary.get("SONG")
        prevSong = self.dataDictionary.get("SONG")
        curPlaybackStatus = self.volatileDataDictionary.get("PLAYBACKINFO")
        prevPlaybackStatus = self.dataDictionary.get("PLAYBACKINFO")
        curInput = self.volatileDataDictionary.get("INP")
        prevInput = self.dataDictionary.get("INP")
        curElapsedTime = TimeStringToInt(self.volatileDataDictionary.get("ELAPSEDTIME"))
        prevElapsedTime = TimeStringToInt(self.dataDictionary.get("ELAPSEDTIME"))
        
        #the curElapsedTime being greater than 0 but less than previous elapsed time is to ensure that time has actually passed
        if curSong != prevSong or curPlaybackStatus != prevPlaybackStatus or curInput != prevInput or (curElapsedTime > 0 and curElapsedTime < prevElapsedTime):
            self.dataDictionary.clear() #clear the cache dictionary
            self.lastChangeTimestamp = time.time() #update the timestamp
        
        for item in self.volatileDataDictionary: #for every item in the live dictionary
            if len(self.volatileDataDictionary.get(item)) > 0: #if the item is longer than 0 (to prevent empty values from being added)
                self.dataDictionary.update({item: self.volatileDataDictionary.get(item)}) #add the item to the cache dictionary
        
    def GetData(self, request, defaultString = ""):
        curInput = self.dataDictionary.get("INP", "") #get the current input
        curInputName = self.dataDictionary.get(str("INPNAME" + self.dataDictionary.get("INP")), "") #get the advanced input name (if possible)
        
        if request.lower() == "song":
            if curInput == "PANDORA" or curInput == "SPOTIFY": #compensate for pandora and spotify being quirky and unique
                return self.dataDictionary.get("TRACK", defaultString)
            else:
                return self.dataDictionary.get("SONG", defaultString)
        
        elif request.lower() == "inpname": #if requesting the input name...
            if curInputName == "": #and there is no special input name...
                return curInput #return the default input name
            else:
                return curInputName #otherwise, return the custom name
        
        else:
            return self.dataDictionary.get(request.upper(), defaultString) #otherwise, return the normal value requested
    
    def LastChangeTimestamp(self):
        return self.lastChangeTimestamp