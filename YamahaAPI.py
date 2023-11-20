import socket
import time
import re

defaultInput = "SERVER"  # Default input source.

# Function to format network requests for the Yamaha receiver.
# requestType: Type of request (e.g., 'zone', 'system', 'source').
# request: Specific request command (e.g., 'SONG', 'ARTIST').
# inputName: Name of the input source, defaults to 'SERVER'.
# zone: The zone of the receiver, defaults to 'MAIN'.
def RequestFormer(requestType, request, inputName = "SERVER", zone = "MAIN"): 
    endData = "\r\n"  # End of line character for network requests.
    
    match requestType:  # Python 3.10+ match-case statement for different request types.
        case "zone":
            return f"@{zone}:{request}=?".upper() + endData
        case "system":
            return f"@SYS:{request}=?".upper() + endData
        case "source":
            return f"@{inputName}:{request}=?".upper() + endData

# Converts a time string (e.g., '1:03') to an integer (total seconds).
# timeString: String representation of time, formatted as 'minutes:seconds'.
def TimeStringToInt(timeString):
    time = 0
    
    try:
        timeList = timeString.split(":")  # Splits the time string into minutes and seconds.
        time = (int(timeList[0]) * 60) + int(timeList[1])  # Converts to total seconds.
        
        return time
    except Exception:  # Catch any conversion error.
        return time

# Class representing the Yamaha API for network communication.
class YamahaAPI:    
    """
    A class to interface with a networked Yamaha Receiver, providing methods to request and process data.

    List of Requestable Data (Case Insensitive):

    Any Zone:
    - INP:
        Description: Current input
    - INPNAME:
        Description: Current input name
    - ZONENAME:
        Description: Current zone name
    - PWR:
        Description: Power state of zone
        Returns: "On" or "Off"
    - SLEEP:
        Description: Sleep timer
        Returns: "Off", "120", "90", "60", or "30" in minutes
    - VOL:
        Description: Current zone volume
        Returns: Volume in dB, ranging from -80.5 to 16.5
    - MUTE:
        Description: Mute status
        Returns: "On" or "Off"

    Main Zone:
    - SONG:
        Description: Song name
    - ARTIST:
        Description: Artist name
    - ALBUM:
        Description: Album name
    - STATION:
        Description: Net Radio Station
    - BAND:
        Description: Tuner band
        Returns: "FM" or "AM"
    - FMFREQ:
        Description: FM Radio Frequency
        Returns: Frequency in MHz, e.g., "104.70"
    - AMFREQ:
        Description: AM Radio Frequency
        Returns: Frequency in kHz, e.g., "1130"
    - PLAYBACKINFO:
        Description: Playback status
        Returns: "Play" or "Stop"
    - MODELNAME:
        Description: The model number, e.g., "TSR-7790" or "RX-A820"
    - SOUNDPRG:
        Description: Sound program
        Returns: Current sound program, e.g., 7ch Stereo
    - STRAIGHT:
        Description: Sound program bypass toggle
        Returns: "On" or "Off"
    - PUREDIRMODE:
        Description: Pure direct mode
        Returns: "On" or "Off"
    - PARTY:
        Description: Party mode toggle
        Returns: "On" or "Off"
    - ENHANCER:
        Description: Audio upscaler toggle
        Returns: "On" or "Off"
    - SWFRTRIM:
        Description: Subwoofer volume trim
        Returns: Value from "-6.0" to "6.0" in 0.5 dB increments
    - TONEBASS:
        Description: Bass tone control adjustment
        Returns: Value from "-6.0" to "6.0" in 0.5 dB increments
    - TONETREBLE:
        Description: Treble tone control adjustment
        Returns: Value from "-6.0" to "6.0" in 0.5 dB increments
    - YPAOVOL:
        Description: YPAO Volume toggle
        Returns: "Auto" or "Off"
    - EXBASS:
        Description: Extra bass toggle
        Returns: "Auto" or "Off"
    - 3DCINEMA:
        Description: 3D Cinema toggle
        Returns: "Auto" or "Off"
    - ADAPTIVEDRC:
        Description: Adaptive Dynamic Range Control toggle
        Returns: "Auto" or "Off"
    - DIALOGUELVL:
        Description: Dialogue Boost Level
        Returns: Value from 0 to 4
    - HDMIOUT1:
        Description: HDMI 1 enable state
        Returns: "On" or "Off"
    - HDMIOUT2:
        Description: HDMI 2 enable state (or UNAVAILABLE if not applicable)
        Returns: "On" or "Off"
    """
    
    def __init__(self, ip, zone = 1):
        """
        Initializes the YamahaAPI object.

        Args:
            ip (str): IP address of the Yamaha receiver.
            zone (int, optional): Zone number of the receiver. Defaults to 1 (MAIN zone).
        """
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket.
        self.tcpSocket.connect((ip, 50000))  # Connect to the Yamaha receiver at the given IP and port 50000.
        
        self.volatileDataDictionary = {}  # Temporary data storage.
        self.dataDictionary = {'INP': defaultInput}  # Persistent data storage.
        
        self.lastChangeTimestamp = time.time()  # Timestamp of the last significant data change.

        # Determine the zone based on the provided zone number.
        match zone:
            case 1:
                self.zone = "MAIN"
            case 2:
                self.zone = "ZONE2"
            case 3:
                self.zone = "ZONE3"
            case 4:
                self.zone = "ZONE4"
            case _:  # Default case.
                self.zone = "MAIN"
    
    def UpdateData(self, refreshInterval = 0.1):
        """
        Updates the data from the receiver based on the current input and zone.

        Args:
            refreshInterval (float, optional): Time interval for refreshing data, in seconds. 
                                               Defaults to 0.1.

        Note:
            This method sends requests to the receiver and processes the responses to update
            internal data dictionaries. It handles different input types and zones.
        """
        # Resolve the receiver's input name to internal names.
        match self.dataDictionary.get('INP'):
            case "Rhapsody":
                curInput = "RHAP"
            case "TUNER":
                curInput = "TUN"
            case "NET RADIO":
                curInput = "NETRADIO"
            case "Bluetooth":
                curInput = "BT"
            case _:  # Default case.
                curInput = self.dataDictionary.get('INP').upper()
        
        # Cap the refresh rate.
        requestDelay = max(0.025, refreshInterval)

        # Building the request data string based on the current input and zone.
        sendData = ""
        if self.zone == "MAIN":
            # Different data requests for different input types.
            if curInput in ["PANDORA", "SPOTIFY"]:
                sendData += RequestFormer("source", "track", curInput)
            elif curInput == "TUN":
                sendData += RequestFormer("source", "band", curInput)
                sendData += RequestFormer("source", "fmfreq", curInput)
                sendData += RequestFormer("source", "amfreq", curInput)
            elif curInput == "NETRADIO":
                sendData += RequestFormer("source", "song", curInput)
                sendData += RequestFormer("source", "station", curInput)
            else:
                sendData += RequestFormer("source", "song", curInput)
            sendData += RequestFormer("source", "artist", curInput)
            sendData += RequestFormer("source", "album", curInput)
            sendData += RequestFormer("source", "soundprg", curInput)
            sendData += RequestFormer("source", "playbackinfo", curInput)
            sendData += RequestFormer("system", "modelname")
            sendData += RequestFormer("system", "party")
            sendData += RequestFormer("zone", "basic")
            sendData += RequestFormer("zone", "zonename")
            if re.match(r'^(HDMI|AV|PHONO|AUDIO|VAUX|AUDIO|USB)', curInput):
                sendData += RequestFormer("system", f"inpname{curInput}")
        else:
            # Request data for other zones.
            sendData += RequestFormer("zone", "basic", zone = self.zone)
            sendData += RequestFormer("zone", "zonename", zone = self.zone)
            if re.match(r'^(HDMI|AV|PHONO|AUDIO|VAUX|AUDIO|USB)', curInput):
                sendData += RequestFormer("system", f"inpname{curInput}")

        # Send the request and wait for the response.
        self.tcpSocket.send(sendData.encode())
        time.sleep(requestDelay)
        receivedData = self.tcpSocket.recv(8192).decode()  # Receive the data (up to 8192 bytes).

        # Dictionary of string replacements for cleaning up the received data.
        stringFixes = {
            "\r": "",
            "MAIN:": "",
            "SYS:": "",
            f"{curInput}:": "",
            f"{self.zone}:": ""
        }
        
        # Apply string replacements.
        for old, new in stringFixes.items():
            receivedData = receivedData.replace(old, new)
        
        # Split the received data by newline characters.
        splitData = receivedData.split("\n")[0:-1]
        
        # Clear the temporary data dictionary.
        self.volatileDataDictionary.clear()
        
        # Process each item in the split data.
        for item in splitData:
            if item.startswith("@") and item.count("=") >= 1:
                # Update the temporary dictionary with the new data.
                key, value = item.replace("@", "", 1).split("=", 1)
                self.volatileDataDictionary[key] = value
        
        # Check for significant changes to update the data dictionary and timestamp.
        curSong = self.volatileDataDictionary.get("SONG")
        prevSong = self.dataDictionary.get("SONG")
        curPlaybackStatus = self.volatileDataDictionary.get("PLAYBACKINFO")
        prevPlaybackStatus = self.dataDictionary.get("PLAYBACKINFO")
        curInput = self.volatileDataDictionary.get("INP")
        prevInput = self.dataDictionary.get("INP")
        curElapsedTime = TimeStringToInt(self.volatileDataDictionary.get("ELAPSEDTIME"))
        prevElapsedTime = TimeStringToInt(self.dataDictionary.get("ELAPSEDTIME"))
        
        if curSong != prevSong or curPlaybackStatus != prevPlaybackStatus or curInput != prevInput or (curElapsedTime > 0 and curElapsedTime < prevElapsedTime):
            self.dataDictionary.clear()
            self.lastChangeTimestamp = time.time()
        
        # Update the permanent data dictionary with new data.
        for item in self.volatileDataDictionary:
            if len(self.volatileDataDictionary.get(item, "")) > 0:
                self.dataDictionary[item] = self.volatileDataDictionary[item]
    
    def GetData(self, request, defaultString = ""):
        """
        Retrieves specific data based on the given request.

        Args:
            request (str): The data item to request (e.g., 'SONG', 'ARTIST'). See main class docstring for possible data.
            defaultString (str, optional): Default return value if the requested data is not found. 
                                           Defaults to an empty string.

        Returns:
            str: The requested data value, or the defaultString if not found.
        """
        curInput = self.dataDictionary.get("INP", "")
        curInputName = self.dataDictionary.get(f"INPNAME{self.dataDictionary.get('INP')}", "")
        
        # Handling special cases for Pandora and Spotify.
        if request.lower() == "song":
            if curInput in ["PANDORA", "SPOTIFY"]:
                return self.dataDictionary.get("TRACK", defaultString)
            else:
                return self.dataDictionary.get("SONG", defaultString)
        
        # Returning the input name, either default or custom.
        elif request.lower() == "inpname":
            return curInputName if curInputName else curInput
        
        # Default case for other data requests.
        else:
            return self.dataDictionary.get(request.upper(), defaultString)
    
    # Returns the timestamp of the last significant change.
    def LastChangeTimestamp(self):
        """
        Returns the timestamp of the last significant change in data.

        Returns:
            float: Timestamp of the last significant change.
            
        Note:
            Events that trigger a new timestamp are song starting, input changing, and playback stopping.
        """
        return self.lastChangeTimestamp