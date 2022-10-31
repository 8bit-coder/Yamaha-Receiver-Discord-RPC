# Yamaha Receiver Discord RPC Client [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) [![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence) [![Latest release](https://badgen.net/github/release/Naereen/Strapdown.js)](https://github.com/8bit-coder/Yamaha-Receiver-Discord-RPC/releases)  [![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)

This program allows Discord users with a network-capable Yamaha receiver to display their currently playing music in the Rich Presence format. I wrote this after searching Google and finding absolutely nothing that would allow me to show the playback of my Yamaha receiver as my Discord status. I ended up writing my own API of sorts to deal with getting information from the receiver and putting it into the custom Discord developer application I made.

##  Features

 - [x] Ability to display currently playing song and song's artist
 - [x] Ability to automatically detect current input & display it in the
       RPC status
 - [x] Ability to detect the receiver's model & display it in the RPC
       status
 - [x] Show the time elapsed on the current song
 - [x] Show when playback is stopped
 - [x] Display the input name and CinemaDSP program when using a
       non-network source (HDMI1, AUDIO1, etc.)

# Setup
First, head to the "releases" tab on this repository and download the latest release. Unzip it and place it in a folder that is easy to access. The program comes with a file called config.txt. This file is meant for users to put their receiver's IP address into the first line. By default, it comes preconfigured with the IP `192.168.1.143` which will **not** work and will require you to change to your own receiver's IP. To find your receiver's IP, follow the steps listed on the [Yamaha Website](https://faq.yamaha.com/usa/s/article/U0007526)(this will work for any networked receiver, not just the RX-V673). Once you've found the IP, simply replace the one in the config.txt file with your receiver's IP. 

Next, you will need to download pypresence. This is done by executing **`pip install pypresence`** in command prompt. Once that's installed and your receiver's IP is configured, you are ready to launch and use the program!

## Known Bugs / Issues
I've done extensive testing on two different receivers (Yamaha RX-A730 & Yamaha RX-V673) and have found a few issues. 

 - Mute functionality is incomplete as it's only detected when the volume is lowered to "mute", not when the mute button is pressed on the remote. Otherwise, it will keep displaying the current volume even when muted.
 - The program will crash if you turn off your receiver and back on.

If you find a bug that isn't mentioned above, please create an issue in the repository so I can look into fixing it. I will add debug logging to the program soon so you can send a debug log to help fixing problems. Also, I have no idea if this program works on Mac OS and Linux as I have only tested it on Windows 10 and 11. It theoretically should, but I have no guarantees. If you can, please make an issue describing how it performs on your platform.

## Planned features

 - [ ] Add functionality for detecting when a song is on repeat and display it accordingly.
 - [ ] Add full mute detection functionality.
 - [ ] Add functionality for possibly displaying album art? (might be impossible)
 - [ ] Add ability to configure what info is displayed in the RPC status.
 - [ ] Add ability to detect advanced input names (eg. HDMI1 - Apple TV 4K)
 - [ ] Add functionality to detect when the receiver is turned off and quit the program.
 - [ ] Add functionality to put the program into the tray (minimizing window clutter)
 - [ ] **Maintenance:**  Get rid of initSource and just detect the source at program startup
 - [ ] **Maintenance:** Add logging for debugging purposes
 - [ ] **Big picture:** Add ability to track played songs (similar to Apple Music's *replay* and Spotify's *wrapped*.
