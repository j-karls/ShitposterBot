import connector
import messages
import re


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
    # To avoid the bot to replying to itself
    if message.author == Client.user:
        return

    if message.content.startswith('--help'):
        await connector.discord_send_message(Client, message.channel, messages.message_help(message))

    elif message.content.startswith('--connections'):
        await connector.discord_send_message(Client, message.channel,
                messages.message_connections(message, connector.get_connections(Db, Connections, message.channel,
                                             message.server)))

    elif message.content.startswith('--add'):
        print(f"{type(message.channel)} + {type(message.channel.name)}")
        try:
            regex = regex_search(r"--add\s+(\w*)\s+(\d*)\s+(\w*)\s+(\w*)", 4, message.content)
            subreddit, amount, frequency, selection = regex.group(1), regex.group(2), regex.group(3), regex.group(4)
            connector.add_connection(Db, subreddit, amount, frequency, selection, message.channel.name,
                                     message.server.name)
            await connector.discord_send_message(Client, message.channel,
                                                 messages.message_added_connection(message, subreddit, amount,
                                                                                   frequency, selection))
        except TypeError:
            await connector.discord_send_message(Client, message.channel, connector.message_wrong_syntax("--add"))

    elif message.content.startswith('--remove'):
        try:
            regex = regex_search(r"--remove\s+(\d*)", 1, message.content)
            info = connector.get_connection_info(Db, regex.group(1))
            connector.remove_connection(Db, Connections, info['subreddit'], info['amount'], info['frequency'],
                                        info['selection'], message.channel.name, message.server.name)
            await connector.discord_send_message(Client, message.channel, messages.message_removed_connection(info))
        except TypeError:
            await connector.discord_send_message(Client, message.channel, connector.message_wrong_syntax("--remove"))
        # Todo what about except valueError if the user types in to remove something that doesnt exist?
# TODO Check if there's something behind my regex? Only if there isn't, do I execute it.


def regex_search(regex, number_of_match_groups, text):
    res = re.search(regex, text)
    print(f"{0} {res.group(0)}")
    for x in range(1, number_of_match_groups + 1):
        print(f"{x} {res.group(x)}")
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
