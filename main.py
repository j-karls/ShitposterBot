import connector
import messages
import loader
import re
import datetime
import asyncio
import os


def read_file(path):
    return open(path, 'r').read()
    # We don't close the stream ourselves, garbage collector will come along shortly
    # It may be worth doing explicitly


Client = connector.discord_client_start()
FilePath = os.path.join(os.path.dirname(__file__), "..", "shitposterFiles")
Db = connector.database_setup(os.path.abspath(os.path.join(FilePath, "db.json")))
Connections = connector.database_query_setup()


@Client.event
async def on_message(message):
    msg = message.content
    srv = message.server
    chn = message.channel

    # To avoid the bot to replying to itself
    if message.author == Client.user:
        return

    # elif msg.startswith('--test'):
    #     print(type(connector.get_connections(Db, Connections, chn, srv)[1]))
    # Test command

    if msg.startswith('--help'):
        await connector.discord_send_message(Client, chn, messages.message_help(message))

    elif msg.startswith('--connections'):
        await connector.discord_send_message(
            Client, chn, messages.message_connections(
                message, connector.get_connections(Db, Connections, chn, srv)))

    elif msg.startswith('--add'):
        try:
            regex = regex_search(r"--add\s+(\w*)\s+(\d*)\s+(\w*)\s+(\w*)", 4, msg)
            subreddit, amount, frequency, selection = \
                regex.group(1), regex.group(2), check_frequency(regex.group(3)), check_selection(regex.group(4))
            connector.add_connection(Db, subreddit, amount, frequency, selection, chn.name, srv.name,
                                     datetime.datetime.now().timestamp())
            await connector.discord_send_message(Client, chn,
                                                 messages.message_added_connection(message, subreddit, amount,
                                                                                   frequency, selection))
        except TypeError:
            await connector.discord_send_message(Client, chn, messages.message_wrong_syntax("--add"))

    elif msg.startswith('--remove'):
        try:
            regex = regex_search(r"--remove\s+(\d*)", 1, msg)
            connect_id = int(regex.group(1))
            info = connector.get_connection(Db, Connections, connect_id, chn, srv)
            connector.remove_connection(Db, Connections, connect_id, chn, srv)
            await connector.discord_send_message(Client, chn, messages.message_removed_connection(info))
        except TypeError:
            await connector.discord_send_message(Client, chn, messages.message_wrong_syntax("--remove"))
        except ValueError:
            await connector.discord_send_message(Client, chn, messages.message_error(
                    "--remove", "A connection with that ID does not exist"))

    elif msg.startswith('--post'):
        try:
            regex = regex_search(r"--post\s+(\d*)", 1, msg)
            connect_id = int(regex.group(1))
            connection = connector.get_connection(Db, Connections, connect_id, chn, srv)
            await post_connection(Client, connection, datetime.datetime.now())
        except TypeError:
            await connector.discord_send_message(Client, chn, messages.message_wrong_syntax("--post"))
        except ValueError:
            await connector.discord_send_message(Client, chn, messages.message_error(
                "--post", "A connection with that ID does not exist"))

# TODO Check if there's something behind my regex? I should only execute if there isnt.


def check_selection(selection):
    if not ((selection == "top") | (selection == "random")):
        raise TypeError
    return selection


def check_frequency(frequency):
    if not ((frequency == "hourly") | (frequency == "daily") | (frequency == "weekly") | (frequency == "monthly") |
            (frequency == "yearly")):
        raise TypeError
    return frequency


def regex_search(regex, number_of_match_groups, text):
    res = re.search(regex, text)
    for x in range(1, number_of_match_groups + 1):
        if res.group(x) is None:
            raise TypeError
    return res


def get_channel(client, channel_name, server_name):
    servers = [server for server in client.servers if server.name == server_name]
    for server in servers:
        for channel in server.channels:
            if channel.name == channel_name:
                return channel
                # Todo: Assumes that there's only ever one channel on the same server with the same name.
                # Todo: This really ought to be done with id's
    return None
    # Gets the reference to the channel we want


async def post_connection(client, connection, time_now, time_next_post=None):
    sub, amount, freq, random, chn = connection["subreddit"], int(connection["amount"]), connection["frequency"], \
                                (connection["selection"] == "random"), get_channel(client, connection["channel"],
                                                                                      connection["server"])
    links = loader.get_reddit_links(sub, amount, freq, random)
    await connector.discord_send_message(client, chn, messages.message_send_links(connection.eid, time_now))
    # todo channel id instead of name?
    [await connector.discord_send_message(client, chn, link) for link in links]
    # Todo change so that this also posts to the right server
    if time_next_post:
        await connector.discord_send_message(client, chn, messages.message_next_post(connection.eid, time_next_post))



@Client.event
async def on_ready():
    print('Logged in as')
    print(Client.user.name)
    print(Client.user.id)
    print('------')
    Client.loop.create_task(schedule_connection_dumps())


def calc_next_post_time(time_posted, frequency):
    return (time_posted + {
        "hourly": datetime.timedelta(hours=1),
        "daily": datetime.timedelta(days=1),
        "weekly": datetime.timedelta(days=7),
        "monthly": datetime.timedelta(days=30),
        "yearly": datetime.timedelta(days=365)
    }[frequency])


async def schedule_connection_dumps():
    while True:
        now = datetime.datetime.now()
        tasks = connector.get_connections_to_post(Db, Connections, now)
        for c in tasks:
            time_next_post = calc_next_post_time(now, c["frequency"])
            await post_connection(Client, c, now, time_next_post)
            c["time"] = time_next_post.timestamp()
            # The time field means: the time when the connection should be posted next
        connector.update_connections(Db, tasks)
        await asyncio.sleep(30)

connector.discord_bot_run(Client, read_file(os.path.abspath(os.path.join(FilePath, "bot-token.secret"))))
# Connects with the bot-token saved within file

