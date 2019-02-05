# Works only with Python 3.6
import discord
import re
import requests
import random
from tinydb import TinyDB, Query


def discord_startClient():
    return discord.Client()


def discord_startBot(client, token):
    client.run(token)


def read_file(path):
    return open(path, 'r').read()
    # We don't close the stream ourselves, garbage collector will come along shortly
    # It may be worth doing explicitly


def database_setup(path):
    return TinyDB(path)


client = discord_startClient()
db = database_setup('./../db.json')
connections = Query()
# Setup tinydb database


#from apscheduler.scheduler import Scheduler

# Start the scheduler
#sched = Scheduler()
#sched.daemonic = False
#sched.start()

#def job_function():
#    print("Hello World")
#    print(datetime.datetime.now())
#    time.sleep(20)

# Schedules job_function to be run once each minute
#sched.add_cron_job(job_function,  minute='0-59')



@client.event
async def on_message(message):
    # To avoid the bot to replying to itself
    if message.author == client.user:
        return

    if message.content.startswith('--help'):
        await discord_send_message(message.channel, message_help(message))

    elif message.content.startswith('--connections'):
        await discord_send_message(message.channel, message_connections(message, get_connections(message.channel,
                                                                                                 message.server)))

    elif message.content.startswith('--add'):
        try:
            regex = regex_search(r"--add\s+(\w*)\s+(\w*)\s+(\w*)\s+(\w*)", 4, message.content)
            subreddit, amount, frequency, selection = regex.group(1), regex.group(2), regex.group(3), regex.group(4)
            add_connection(subreddit, amount, frequency, selection, message.channel, message.server)
            await discord_send_message(message.channel, message_added_connection(message, subreddit, amount, frequency,
                                                                                 selection))
        except TypeError:
            await discord_send_message(message.channel, message_wrong_syntax("--add"))

    elif message.content.startswith('--remove'):
        try:
            regex = regex_search(r"--remove\s+(\d*)", 1, message.content)
            info = get_connection_info(regex.group(1))
            remove_connection(info['subreddit'], info['amount'], info['frequency'],
                              info['selection'], message.channel, message.server)
            await discord_send_message(message.channel, message_removed_connection(info))
        except TypeError:
            await discord_send_message(message.channel, message_wrong_syntax("--remove"))
        # Todo what about except valueError if the user types in to remove something that doesnt exist?
# TODO Check if there's something behind my regex? Only if there isn't, do I execute it.


def regex_search(regex, number_of_match_groups, text):
    res = re.search(regex, text)
    for x in range(1, number_of_match_groups):
        if res.group(x) is None:
            raise TypeError
    return res


async def discord_send_message(channel, message):
    await client.send_message(channel, message)


def add_connection(subreddit, amount, frequency, selection, channel, server):
    return db.insert({'subreddit': subreddit, 'amount': amount, 'frequency': frequency, 'selection': selection,
                      'channel': channel, 'server': server})


def remove_connection(subreddit, amount, frequency, selection, channel, server):
    db.remove(connections.subreddit == subreddit & connections.amount == amount & connections.frequency == frequency &
              connections.selection == selection & connections.channel == channel & connections.server == server)


def get_connection_info(connection_eid):
    return db.get(connection_eid)
# Todo Check for errors boi. What if there are none?


def get_connections(channel, server):
    return db.search(connections.server == server & connections.channel == channel)


def message_wrong_syntax(command_name):
    return f"Wrong syntax for command '{command_name}'. Check '--help' for info."


def get_json(subreddit, amount, randomize):
    posts = requests.get(f'https://www.reddit.com/r/{subreddit}.json').json()["data"]["children"]
    if randomize:
        random.shuffle(posts)  # todo CAN I DO THIS? Is it even a list?
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
    return f'All connections in channel(?) and server (?){connections}'  # TODO for each element also show its eid
    # connection.eid
    # return list of connections


def message_added_connection(message, subreddit, amount, selection, frequency):
    return 'Added connection: \n' \
          f'{subreddit} linked to channel {message.channel}. \n' \
          f'It will write {amount} {selection} posts every {frequency}'


def message_removed_connection(connection_info):
    return 'Removed Connection: \n' \
          f'{connection_info}'


discord_startBot(client, read_file('bot-token.secret'))
# Connects with the bot-token saved within file





