#!/bin/bash

# Run setup script as sudo

# apt-get install git
# git clone "https://github.com/Volkarl/ShitposterBot.git"

apt-get update -y
apt-get install python3.6 -y
apt-get install python3-pip -y

pip3 install discord
pip3 install datetime
pip3 install asyncio
pip3 install requests
pip3 install tinydb

# Could not find package
# pip3 install re
# pip3 install random

mkdir shitposterFiles

# Now import the bot secret into the folder shitposterFiles
# Then run with command: sudo nohup python3 ShitposterBot/main.py
# Nohup prevents the process from being terminated when the terminal (ssh connection or whatever it is) is disconnected