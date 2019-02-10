# Works only with Python 3.6
import discord
import requests
import random
from tinydb import TinyDB, Query


def discord_client_start():
    return discord.Client()


def database_query_setup():
    return Query()


def discord_bot_run(discord_client, token):
    discord_client.run(token)


def database_setup(path):
    return TinyDB(path)


async def discord_send_message(client, channel, message):
    await client.send_message(channel, message)


def add_connection(db, subreddit, amount, frequency, selection, channel, server):
    return db.insert({'subreddit': subreddit, 'amount': amount, 'frequency': frequency, 'selection': selection,
                      'channel': channel, 'server': server})


#def remove_connection(db, query, subreddit, amount, frequency, selection, channel, server):
#    return db.remove((query.subreddit == subreddit) & (query.amount == amount) & (query.frequency == frequency) &
#                     (query.selection == selection) & (query.channel == channel) & (query.server == server))


def remove_connection(db, connection_id):
    return db.remove(doc_ids=[connection_id])


def get_connection(db, connection_id):
    el = db.get(doc_id=connection_id)
    if el is None:
        raise ValueError
    return el
    # Returns either one connection or type None


def get_connections(db, query, channel, server):
    return db.search((query.server == server.name) & (query.channel == channel.name))


def message_wrong_syntax(command_name):
    return f"Wrong syntax for command '{command_name}'. Check '--help' for info."


def message_error(command_name, msg):
    return f"Error occurred while executing command '{command_name}': {msg}"


def get_json(subreddit, amount, randomize):
    posts = requests.get(f'https://www.reddit.com/r/{subreddit}.json',
                         headers={'User-agent': 'shitposterBot 0.1'}).json()["data"]["children"]
    if randomize:
        random.shuffle(posts)  # todo CAN I DO THIS? Is it even a list?
    return [posts[x]["data"]["url"] for x in range(amount)]
    # TODO What happens if amount is greater than the amount of posts?
    # TODO What happens if there is no field: "url"?
