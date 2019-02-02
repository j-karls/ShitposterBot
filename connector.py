# Works only with Python 3.6
import discord
import re
import requests
import random


def discord_connect(token):
    connection = discord.Client()
    connection.run(token)
    return connection


def read_file(path):
    open(path, 'r').read()
    # We don't close the stream ourselves, garbage collector will come along shortly
    # It may be worth doing explicitly


client = discord_connect(read_file('bot-token.secret'))
# Connects with the bot-token saved within file


@client.event
async def on_message(message):
    # To avoid the bot to replying to itself
    if message.author == client.user:
        return

    if message.content.startswith('--help'):
        await discord_send_message(message.channel, message_help(message.author.mention))

    elif message.content.startswith('--connections'):
        await discord_send_message(message.channel, message_connections(message, get_connections()))

    elif message.content.startswith('--add'):
        try:
            regex = regex_search(r"--add\s+(\w*)\s+(\w*)\s+(\w*)\s+(\w*)", 4, message.content)
            subreddit, amount, frequency, selection = regex.group(1), regex.group(2), regex.group(3), regex.group(4)
            add_connection(subreddit, amount, frequency, selection)
            await discord_send_message(message.channel,
                                       message_added_connection(message, subreddit, amount, frequency, selection))
        except TypeError:
            await discord_send_message(message.channel, message_wrong_syntax("--add"))

    elif message.content.startswith('--remove'):
        try:
            regex = regex_search(r"--remove\s+(\d*)", 1, message.content)
            connection_number, connection_info = regex.group(1), get_connection_info(regex.group(1))
            remove_connection(connection_number)
            await discord_send_message(message.channel, message_removed_connection(connection_info))
        except TypeError:
            await discord_send_message(message.channel, message_wrong_syntax("--remove"))
# TODO Check if there's something behind my regex? Only if there isn't, do I execute it.


def regex_search(regex, number_of_match_groups, text):
    res = re.search(regex, text)
    for x in range(1, number_of_match_groups):
        if res.group(x) is None:
            raise TypeError
    return res


async def discord_send_message(channel, message):
    await client.send_message(channel, message)


def add_connection(subreddit, amount, frequency, selection):
    # TODO


def get_connection_info(connection):
    # TODO


def remove_connection(connection_number):
    # TODO


def get_connections():
    # TODO


def message_wrong_syntax(command_name):
    return f"Wrong syntax for command '{command_name}'. Check '--help' for info."


def get_json(subreddit, amount, randomize):
    posts = requests.get(f'https://www.reddit.com/r/{subreddit}.json').json()["data"]["children"]
    if randomize:
        random.shuffle(posts) # CAN I DO THIS? Is it even a list?
    return [posts[x]["data"]["url"] for x in range(amount)]
    # TODO What happens if amount is greater than the amount of posts?
    # TODO What happens if there is no field: "url"?


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def message_help(message):
    return f'Hello {message.author.mention} \n' \
            '\n' \
            'Commands: \n' \
            '--help | Opens the help menu \n' \
            '--connections | Shows the list of subreddits connected to this Discord channel \n' \
            '--add [subreddit] [amount] [frequency] [selection] | Connects a subreddit to the Discord channel \n' \
            '--remove [connectionNumber] | Removes a subreddit connection \n' \
            '\n' \
            'Parameters: \n' \
            'subreddit: A subreddit name \n' \
            'amount: Amount of posts, between 0 and 25 \n' \
            'frequency: hourly, daily, weekly, monthly, yearly \n' \
            'selection: top, random \n' \
            'connectionNumber: A number found in the list of connections with command --connections'


def message_connections(message, connections):
    return "All connections in channel(?) and server (?)"
    # return list of connections


def message_added_connection(message, subreddit, amount, selection, frequency):
    return 'Added connection: \n' \
          f'{subreddit} linked to channel {message.channel}. \n' \
          f'It will write {amount} {selection} posts every {frequency}'


def message_removed_connection(connection_info):
    return 'Removed Connection: \n' \
          f'{connection_info}'





