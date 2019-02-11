# Loads the json file from web and handles it
import requests
import random


Freq_dict = {
    "hourly": "hour",
    "daily": "day",
    "weekly": "weekly",
    "monthly": "month",
    "yearly": "year"
}


def convert_frequency(frequency):
    return Freq_dict.get(frequency, "")


# TODO WHAT ABOUT FREQUENCY? /top = daily??
def get_reddit_links(subreddit, amount, frequency, randomize):
    ua, url = 'shitposterBot 0.1', f'https://www.reddit.com/r/{subreddit}.json'
    posts = requests.get(url, headers={'User-agent': ua}).json()["data"]["children"]

    links = [post["data"]["url"] for post in posts if not post["data"]["is_self"]]
    # All non-self-posts are turned into their corresponding link

    if randomize:
        random.shuffle(links)
    return links[:amount]
