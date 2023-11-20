# Yamaha Receiver Discord RPC Client [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) [![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence) [![Latest release](https://badgen.net/github/release/Naereen/Strapdown.js)](https://github.com/8bit-coder/Yamaha-Receiver-Discord-RPC/releases) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
![Demo 1](https://media.discordapp.net/attachments/815992022992945212/1175958998982344724/image.png?ex=656d2029&is=655aab29&hm=5e0fe421f7e4ea442d7749554a28de1a4975bfb105c8142d171a3ab793725f9f&=&width=501&height=237)
![Demo 2](https://media.discordapp.net/attachments/815992022992945212/1175957449015033948/image.png?ex=656d1eb8&is=655aa9b8&hm=d9c1278ac847af9f1a2eeee7b7f8a94a4d4e86b07ee0701677416f50b1ed13be&=&width=537&height=233)

This program allows Discord users with a network-capable Yamaha receiver to display their currently playing music in the Discord Rich Presence format. I wrote this after searching Google and finding absolutely nothing that would allow me to show the playback of my Yamaha receiver as my Discord status (similar to my friends showing Spotify or Apple Music). I ended up writing my own API to deal with getting information from the receiver and putting it into a custom Discord developer application.

##  Features

 - [x] Display currently playing song and song's artist
 - [x] Show the time elapsed on the current song
 - [x] Show when playback is stopped
 - [x] Automatically detect current input (and custom input name) & display it in the
       RPC status
 - [x] Detect the receiver's model & display it in the RPC
       status
 - [x] Display the input name and CinemaDSP program when using a
       non-network source (HDMI1, AUDIO1, etc.)
 - [x] Detect Pure Direct Mode and other DSP bypasses & display it in the RPC status

# Setup
First, make sure you have python installed on your system. If you don't already have it installed, click on the big red "made with Python" badge at the top of this README to download and install the latest version.

Then, head to the "releases" tab on this repository and download the latest release. Unzip it and place it in a folder that is easy to access. The program comes with a file called config.txt. This file is meant for users to put their receiver's IP address into the first line. By default, it comes preconfigured with the IP `10.158.203.218` which will **not** work and will require you to change to your own receiver's IP. To find your receiver's IP, follow the steps listed on the [Yamaha Website](https://faq.yamaha.com/usa/s/article/U0007526) (this will work for any networked receiver, not just the RX-V673). Once you've found the IP, simply replace the one in the config.txt file with your receiver's IP. 

Next, you will need to download pypresence. This is done by executing **`pip install pypresence`** in command prompt. Once that's installed and your receiver's IP is configured, you are ready to launch and use the program!

## Known Bugs / Issues
I've done extensive testing on these receivers:
 - Yamaha RX-A2010
 - Yamaha RX-A820
 - Yamaha RX-A730
 - Yamaha RX-A660
 - Yamaha RX-V673
 - Yamaha TSR-7790

If you find something that you think might be a bug, please create an issue in the repository so I can look into fixing it. Also, I have no idea if this program works on Mac OS and Linux as I have only tested it on Windows 10 and 11. It theoretically should, but I have no guarantees. If you can, please make an issue describing how it performs on your platform.

# Planned features

 - [ ] Add functionality to detect when the receiver is turned off and quit the program.
 - [ ] Add functionality to put the program into the tray (minimizing window clutter)
 - [ ] **Maintenance:** Add logging for debugging purposes
 - [ ] **Big picture:** Add ability to track played songs (similar to Apple Music's *replay* and Spotify's *wrapped*.
