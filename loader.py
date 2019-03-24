# Loads the json file from web and handles it
import requests
import random


Freq_dict = {
    "hourly": "hour",
    "daily": "day",
    "weekly": "week",
    "monthly": "month",
    "yearly": "year"
}


def convert_frequency(frequency):
    return Freq_dict.get(frequency, "")


def get_reddit_links(subreddit, amount, frequency, randomize):
    ua, url = 'shitposterBot 0.1', f'https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=' \
        f'{convert_frequency(frequency)}'
    posts = requests.get(url, headers={'User-agent': ua}).json()["data"]["children"]

    links = [(post["data"]["title"], post["data"]["url"]) for post in posts if not post["data"]["is_self"]]
    # All non-self-posts are turned into their corresponding link

    if randomize:
        random.shuffle(links)
    return links[:amount]
