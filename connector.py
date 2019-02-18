# Works only with Python 3.6
import discord
import datetime
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
    # Todo change to post in a particular channel in a particular server: do something with channel.id and server.id
    # Todo what if the server or channel no longer exists?


def add_connection(db, subreddit, amount, frequency, selection, channel, server, time_posted):
    return db.insert({'subreddit': subreddit, 'amount': amount, 'frequency': frequency, 'selection': selection,
                      'channel': channel, 'server': server, 'time': time_posted})


def remove_connection(db, query, connection_id, channel, server):
    try:
        get_connection(db, query, connection_id, channel, server)
        # If we can successfully get the item, that means that it does exist within the correct channel and server
    except ValueError as e:
        raise e
    return db.remove(doc_ids=[connection_id])
    # doc_ids appears to override any query I input, so I cannot mix both


def get_connection(db, query, connection_id, channel, server):
    el = [lst for lst in db.search(is_server_and_channel(query, channel, server)) if lst.eid == connection_id]
    if not el:
        # No fitting connection
        print("here")
        raise ValueError
    if len(el) != 1:
        raise TypeError
        # This should never happen, as there should only ever be at max one element with a specific ID
    return el[0]
    # Finds all channel/server connections, compares with the ID and then returns the one element that fits (if any)


def get_connections(db, query, channel, server):
    return db.search(is_server_and_channel(query, channel, server))


def is_server_and_channel(query, channel, server):
    return (query.server == server.name) & (query.channel == channel.name)
# Todo change to server and channel ids


def get_connections_to_post(db, query, time):
    return db.search(time > datetime.datetime.fromtimestamp(query.time))


def update_connections(db, connections):
    db.write_back(connections)
