from pypresence import Presence
from YamahaAPI import YamahaAPI

#open the config file, read the ip from it, and close the file
with open("config.txt", "r") as configFile:
    receiverIP = configFile.read()

#these are the sources that support song and artist names
detailedSources = ["Pandora", "Rhapsody", "SiriusXM", "Spotify", "AirPlay", "SERVER", "USB", "PC", "NET RADIO"]

#the text to display when there is no data (to prevent pyPresence from crashing)
defaultText = " - "

#the button displayed under the rich presence info
rpcButton = [{"label": "Have a Yamaha Receiver?", "url": "https://github.com/8bit-coder/Yamaha-Receiver-Discord-RPC"}]

#create a Yamaha receiver object with the IP and zone
Receiver = YamahaAPI(receiverIP, zone=1)

#connect to the discord developer application ID
discordRPC = Presence("1035741925468291134")
discordRPC.connect()

while True: #program runs forever
    try: #failsafe incase socket craps out
        Receiver.UpdateData(0.25)
    except Exception as e:
        print(f"Error updating data: {e}")

    #gather data
    currentInput = Receiver.GetData("inp", defaultText)
    currentInputName = Receiver.GetData("inpname", defaultText)
    currentModel = Receiver.GetData("modelname", defaultText)
    currentVolume = Receiver.GetData("vol", defaultText)
    currentMute = Receiver.GetData("mute", defaultText)
    currentSoundProgram = Receiver.GetData("soundprg", defaultText)
    playbackStart = Receiver.LastChangeTimestamp()
    
    #these three lines will be what will be sent to discord
    hoverText = defaultText
    firstLine = defaultText
    secondLine = defaultText
    
    if currentMute == "On":
        currentSoundProgram = "Receiver Muted"
    elif Receiver.GetData("puredirmode") == "On": #if the receiver is on pure direct mode, ignore the sound program
        currentSoundProgram = "Pure Direct Mode"
    elif Receiver.GetData("straight") == "On": #same thing if the receiver is on straight mode
        currentSoundProgram = "DSP Passthrough"
    
    if currentInput in detailedSources: #if the source supports it, display song and artist title
        currentSong = Receiver.GetData("song", defaultText)
        currentArtist = Receiver.GetData("artist", defaultText)
        playingStatus = Receiver.GetData("playbackinfo", defaultText)
        
        if playingStatus == "Stop": #if the source is stopped
            hoverText = f'{currentModel}: {currentVolume}dB'
            firstLine = f'{currentInput}'
            secondLine = f'Playback Stopped'
        elif currentMute == "On": #if the source is playing but is muted
            hoverText = f'{currentModel}: {currentInput} {currentVolume}dB'
            firstLine = f'Receiver Muted'
            secondLine = f'{defaultText}'
        else:
            hoverText = f'{currentModel}: {currentInput} {currentVolume}dB'
            firstLine = f'{currentSong}'
            
            if currentInput == "NET RADIO": #if the source is net radio, second line should be station since no artist is reported
                currentStation = Receiver.GetData("station", defaultText)
                secondLine = f'{currentStation}'
            else:
                secondLine = f'{currentArtist}'
    
    elif currentInputName != currentInput: #if there is a custom input name
        hoverText = f'{currentModel}: {currentVolume}dB'
        firstLine = f'{currentInput} - {currentInputName}'
        secondLine = f'{currentSoundProgram}'
    
    elif currentInputName == "TUNER": #if the radio tuner is being used
        currentTunerBand = Receiver.GetData("band", defaultText)

        hoverText = f'{currentModel}: {currentVolume}dB'
        
        if currentTunerBand.upper() == "AM":
            firstLine = f'AM Radio'
            
            try:
                secondLine = f'{float(Receiver.GetData("amfreq")):0.0f} kHz'
            except ValueError: #this is if the receiver reports something other than numbers
                secondLine = f'Unknown Frequency' 
        elif currentTunerBand.upper() == "FM":
            firstLine = f'FM Radio'
            
            try:
                secondLine = f'{float(Receiver.GetData("fmfreq")):0.1f} MHz'
            except ValueError: #once again, this is if the receiver reports something other than numbers
                secondLine = f'Unknown Frequency' 
        else: #failsafes incase the receiver doesn't even report the band
            firstLine = f'{currentInput}' 
            secondLine = f'{currentSoundProgram}'
    else:
        hoverText = f'{currentModel}: {currentVolume}dB'
        firstLine = f'{currentInput}'
        secondLine = f'{currentSoundProgram}'
    
    #finally, send the data over to discord
    discordRPC.update(large_image="yamaha-logo-light", large_text=hoverText, details=firstLine, state=secondLine, start=playbackStart, buttons=rpcButton)
