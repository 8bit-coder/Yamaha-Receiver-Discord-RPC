from pypresence import Presence
from YamahaAPI import YamahaAPI

# Read the IP address of the Yamaha receiver from a configuration file.
with open("config.txt", "r") as configFile:
    receiverIP = configFile.read()

# List of sources that support detailed information like song and artist names.
detailedSources = ["Pandora", "Rhapsody", "SiriusXM", "Spotify", "AirPlay", "SERVER", "USB", "PC", "NET RADIO", "Bluetooth"]

# Default text to display when no data is available.
defaultText = " - "
mutedText = "Receiver Muted"

# Button configuration for the Discord Rich Presence.
rpcButton = [{"label": "Have a Yamaha Receiver?", "url": "https://github.com/8bit-coder/Yamaha-Receiver-Discord-RPC"}]

# Create a Yamaha receiver object with the specified IP and default to zone 1.
Receiver = YamahaAPI(receiverIP, zone=1)

# Connect to Discord using the application ID.
discordRPC = Presence("1035741925468291134")
discordRPC.connect()

while True:  # The main loop to keep the program running.
    try:
        # Update receiver data at a fixed interval.
        Receiver.UpdateData(0.25)
    except Exception as e:
        print(f"Error updating data: {e}")

    # Gather data from the receiver.
    currentInput = Receiver.GetData("inp", defaultText)
    currentInputName = Receiver.GetData("inpname", defaultText)
    currentModel = Receiver.GetData("modelname", defaultText)
    currentVolume = Receiver.GetData("vol", defaultText)   
    currentSoundProgram = Receiver.GetData("soundprg", defaultText)
    playbackStart = Receiver.LastChangeTimestamp()
    if currentVolume == "-80.5":
        currentMute = "On"
    else:
        currentMute = Receiver.GetData("mute", defaultText)
    
    # Initialize text variables for Discord Rich Presence.
    hoverText = defaultText
    firstLine = defaultText
    secondLine = defaultText
    
    # Adjust the displayed information based on the receiver's status.
    if currentMute == "On":
        currentSoundProgram = mutedText
    elif Receiver.GetData("puredirmode") == "On":
        currentSoundProgram = "Pure Direct Mode"
    elif Receiver.GetData("straight") == "On":
        currentSoundProgram = "DSP Passthrough"
    
    # Handle detailed source information for Discord display.
    if currentInput in detailedSources:
        currentSong = Receiver.GetData("song", defaultText)
        currentArtist = Receiver.GetData("artist", defaultText)
        playingStatus = Receiver.GetData("playbackinfo", defaultText)
        
        # Determine the text to display based on playback status and source details.
        if playingStatus == "Stop" or playingStatus == "Pause":
            hoverText = f'{currentModel}: {currentVolume}dB'
            firstLine = f'{currentInput}'
            secondLine = f'Playback Stopped'
        elif currentMute == "On":
            hoverText = f'{currentModel}: {currentInput} {currentVolume}dB'
            firstLine = f'Receiver Muted'
            secondLine = f'{defaultText}'
        else:
            hoverText = f'{currentModel}: {currentInput} {currentVolume}dB'
            firstLine = f'{currentSong}'
            
            #If the source is Net Radio, display the Station as the second line.
            if currentInput == "NET RADIO": 
                currentStation = Receiver.GetData("station", defaultText)
                secondLine = f'{currentStation}'
            else:
                secondLine = f'{currentArtist}'
    
    # Handle custom input names.
    elif currentInputName != currentInput:
        hoverText = f'{currentModel}: {currentVolume}dB'
        firstLine = f'{currentInput} - {currentInputName}'
        secondLine = f'{currentSoundProgram}'
    
    # Handle radio tuner information.
    elif currentInputName == "TUNER":
        currentTunerBand = Receiver.GetData("band", defaultText)

        hoverText = f'{currentModel}: {currentVolume}dB'
        
        if currentTunerBand.upper() == "AM":
            firstLine = f'AM Radio'
            
            # Check if the receiver reports something other than numbers
            try:
                secondLine = f'{float(Receiver.GetData("amfreq")):0.0f} kHz'
            except ValueError:
                secondLine = f'Unknown Frequency' 
        elif currentTunerBand.upper() == "FM":
            firstLine = f'FM Radio'
            
            # Check if the receiver reports something other than numbers
            try:
                secondLine = f'{float(Receiver.GetData("fmfreq")):0.1f} MHz'
            except ValueError:
                secondLine = f'Unknown Frequency'
        # In case the receiver reports nothing
        else:
            firstLine = f'{currentInput}' 
            secondLine = f'{currentSoundProgram}'
    else:
        # Default display when no specific conditions are met.
        hoverText = f'{currentModel}: {currentVolume}dB'
        firstLine = f'{currentInput}'
        secondLine = f'{currentSoundProgram}'
    
    # Update the Discord Rich Presence with the gathered information.
    discordRPC.update(
        large_image="yamaha-logo-light", 
        large_text=hoverText, 
        details=firstLine, 
        state=secondLine, 
        start=playbackStart, 
        buttons=rpcButton
    )