import connector
import messages
import loader
import re
import datetime


def read_file(path):
    return open(path, 'r').read()
    # We don't close the stream ourselves, garbage collector will come along shortly
    # It may be worth doing explicitly


Client = connector.discord_client_start()
FilePath = './../shitposterFiles'
Db = connector.database_setup(f'{FilePath}/db.json')
Connections = connector.database_query_setup()


@Client.event
async def on_message(message):
    msg = message.content
    srv = message.server
    chn = message.channel

    # To avoid the bot to replying to itself
    if message.author == Client.user:
        return

    elif msg.startswith('--test'):
        print(type(connector.get_connections(Db, Connections, chn, srv)[1]))

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
            connector.add_connection(Db, subreddit, amount, frequency, selection, chn.name, srv.name)
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
            links = loader.get_reddit_links(
                connection["subreddit"], int(connection["amount"]), check_frequency(connection["frequency"]),
                ((check_selection(connection["selection"])) == "randomize"))
            await connector.discord_send_message(
                Client, chn, messages.message_send_links(connect_id, datetime.datetime.now()))
            [await connector.discord_send_message(Client, chn, link) for link in links]
        except TypeError:
            await connector.discord_send_message(Client, chn, messages.message_wrong_syntax("--post"))
        except ValueError:
            await connector.discord_send_message(Client, chn, messages.message_error(
                "--post", "A connection with that ID does not exist"))


# TODO Check if there's something behind my regex? I should only execute if there isnt.


def check_selection(selection):
    if not ((selection == "top") | (selection == "randomize")):
        raise TypeError
    return selection


def check_frequency(frequency):
    if not ((frequency == "hourly") | (frequency == "daily") | (frequency == "weekly") | (frequency == "monthly") |
            (frequency == "yearly")):
        raise TypeError
    return frequency


def regex_search(regex, number_of_match_groups, text):
    res = re.search(regex, text)
    # print(f"{0} {res.group(0)}")
    for x in range(1, number_of_match_groups + 1):
        # print(f"{x} {res.group(x)}")
        if res.group(x) is None:
            raise TypeError
    return res


@Client.event
async def on_ready():
    print('Logged in as')
    print(Client.user.name)
    print(Client.user.id)
    print('------')


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


connector.discord_bot_run(Client, read_file(f'{FilePath}/bot-token.secret'))
# Connects with the bot-token saved within file
