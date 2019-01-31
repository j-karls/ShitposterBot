# Works only with Python 3.6
import discord
import re

TOKEN = open('bot-token.secret', 'r').read()
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('--help'):
        msg = f'Hello {message.author.mention} \n' \
               '\n' \
               'Commands: \n' \
               '--help | Opens the help menu \n' \
               '--connections | Shows the list of subreddits connected to this Discord channel \n' \
               '--add [subreddit] [amount] [frequency] [selection] | Connects a subreddit to the Discord channel \n' \
               '--remove [connectionNumber] | Removes a subreddit connection \n' \
               '\n' \
               'Parameters: \n' \
               'subreddit: A subreddit name \n' \
               'amount: Amount of posts, between 0 and 25' \
               'frequency: hourly, daily, weekly, monthly, yearly \n' \
               'selection: top, random \n' \
               'connectionNumber: A number found in the list of connections with command --connections'
        await client.send_message(message.channel, msg)

    elif message.content.startswith('--connections'):
        msg = f'Connections:'
        await client.send_message(message.channel, msg)

    elif message.content.startswith('--add'):
        regex = re.search(r"--add\s(\w*)\s(\w*)\s(\w*)\s(\w*)", message.content)
        if regex:
            subreddit = regex.group(1)
            amount = regex.group(2)
            frequency = regex.group(3)
            selection = regex.group(4)
            msg = 'Added connection: \n' \
                 f'{subreddit} linked to channel {message.channel}. \n' \
                 f'It will write {amount} {selection} posts every {frequency}'
            await client.send_message(message.channel, msg)

    elif message.content.startswith('--remove'):
        regex = re.search(r"--add\s(\d*)", message.content)
        if regex:
            number = regex.group(1)
            connectioninfo = "somethingsomethingredditsomething"
            #connectioninfo = connections[number]
            msg = f'Removed:' \
                  f'Removed connection {connectioninfo}'
            await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)