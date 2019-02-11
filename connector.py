# Works only with Python 3.6
import discord
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


def remove_connection(db, connection_id):
    return db.remove(doc_ids=[connection_id])


def get_connection(db, connection_id):
    el = db.get(doc_id=connection_id)
    if el is None:
        raise ValueError
    return el
    # Get returns either one connection or type None


def get_connections(db, query, channel, server):
    return db.search((query.server == server.name) & (query.channel == channel.name))

