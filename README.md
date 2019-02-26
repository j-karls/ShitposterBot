# ShitposterBot

## Functionality
A bot that posts content from Reddit subreddits to discord channels in different intervals. Allows you to link a subreddit with a channel, specifying how often it should post (hourly, daily, weekly, monthly, yearly) from the top of that subreddit, how many links it should post at a time, and whether they should be chosen randomly or from the top. 

For example, I may add a connection that posts the top 5 weekly pictures of subreddit "pics" once every week. 

The bot can be run both on Windows and Linux (tested on Ubunto VM on Azure)

## Setup
To host the bot yourself:
- Add an application to your discord profile: "https://discordapp.com/developers/applications"
- Git clone this repository onto whichever machine you want to host the bot
- Run the setup.sh script with sudo/admin privileges
- Add the bot secret (found in step 1) into the folder shitposterFiles in a file named: "bot-token.secret"
- Run the program with command: "sudo nohup python3 ShitposterBot/main.py"
- Add the bot to your server by using the link: "https://discordapp.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=0" where you replace YOUR_CLIENT_ID with the bot client ID also found in step 1
