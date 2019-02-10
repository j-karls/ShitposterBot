def message_help(message):
    return f'Hello {message.author.mention} \n' \
            '\n' \
            'Commands: \n' \
            '`--help` | Opens the help menu \n' \
            '`--connections` | Shows the list of subreddits connected to this Discord channel \n' \
            '`--add` [subreddit] [amount] [frequency] [selection] | Connects a subreddit to the Discord channel \n' \
            '`--remove` [connectionNumber] | Removes a subreddit connection \n' \
            '\n' \
            'Parameters: \n' \
            'subreddit: A subreddit name \n' \
            'amount: Amount of posts, between 0 and 25 \n' \
            'frequency: hourly, daily, weekly, monthly, yearly \n' \
            'selection: top, random \n' \
            'connectionNumber: A number found in the list of connections with command --connections'


def message_connections(message, connections):
    c_string = format_connections(connections)
    return f'All connections in `{message.channel}` on `{message.server}`: \n ' \
        f'[ID] | [subreddit] [amount] [frequency] [selection]' \
        '```' \
        f'{c_string} \n' \
        f'```'


def format_connection(connection):
    return f"{connection['subreddit']} {connection['amount']} {connection['frequency']} {connection['selection']}"


def format_connections(connections):
    c_list = [f"{x.eid} | {format_connection(x)}" for x in connections]
    return "\n".join(c_list)


def message_added_connection(message, subreddit, amount, selection, frequency):
    return 'Added connection: \n' \
          f'`{subreddit}` linked to channel `{message.channel}`. \n' \
          f'It will write `{amount}` `{frequency}` posts `{selection}`'


def message_removed_connection(connection):
    return 'Removed Connection: \n' \
           '```' \
          f'{format_connection(connection)} \n' \
           '```'
