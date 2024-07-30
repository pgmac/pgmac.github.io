#!/usr/bin/env python3

""" Let's get some interesting things from Pocket and share them about
"""

from datetime import datetime, timedelta
import os
import requests

# Replace these with your Pocket API and Slack credentials
CONSUMER_KEY = os.environ.get('consumer_key')
ACCESS_TOKEN = 'YOUR_POCKET_ACCESS_TOKEN'
tags = ['tag1']  # Replace with your specific tags
week_offset = os.environ.get('week_offset', 0)

# Calculate the time range for the previous week
today = datetime.now()
idx = (today.weekday() + 1) % 7
sun = today - timedelta(idx + (int(week_offset)*7))
last_week = sun - timedelta(days=7)
since = int(last_week.timestamp())

# Pocket API endpoint
POCKET_HOST = 'https://getpocket.com'
POCKET_GET_URL = '/v3/get'
POCKET_OAUTH_REQUEST = '/v3/oauth/request'
POCKET_OAUTH_AUTH = '/v3/oauth/authorize'
POCKET_REDIRECT_URI = 'News:authorizationFinished'


# Function to get oauth token

def get_oauth_token():
    """ Auth on Oauth
    """
    try:
        access_token = os.environ.get('access_token')
        return (access_token)
    except:
        pass

    try:
        with open("tokens.txt", "r") as in_file:
            for line in in_file:
                access_token = line
        in_file.close()
        return (access_token)
    except:
        pass

    params = {
        'consumer_key': CONSUMER_KEY,
        'redirect_uri': POCKET_REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Accept': 'application/json'
    }
    response = requests.post(
        f"{POCKET_HOST}{POCKET_OAUTH_REQUEST}", headers=headers, json=params, timeout=5)
    if response.status_code == 200:
        data = response.json()
        _params = {
            'consumer_key': CONSUMER_KEY,
            'code': data.get('code')
        }

        print(f"{POCKET_HOST}/auth/authorize?request_token={
            data.get('code')}&redirect_uri={POCKET_REDIRECT_URI}")
        letsgo = input("Auth this app, then go again")

        # Make it into an access_token now
        access = requests.post(
            f"{POCKET_HOST}{POCKET_OAUTH_AUTH}", headers=headers, json=_params, timeout=5)
        if access.status_code == 200:
            atdata = access.json()
            with open("tokens.txt", "w") as out_file:
                out_file.write(atdata.get('access_token'))
            out_file.close()
            return data.get('access_token')


# Function to get posts for a specific tag

def get_posts_for_tag(_tag):
    """ Get all the Pocket posts with a tag
    """
    ACCESS_TOKEN = get_oauth_token()
    params = {
        'consumer_key': CONSUMER_KEY,
        'access_token': ACCESS_TOKEN,
        'since': since,
        'detailType': 'complete',
        'sort': 'oldest'
    }

    response = requests.post(
        f"{POCKET_HOST}{POCKET_GET_URL}", json=params, timeout=5)

    if response.status_code == 200:
        data = response.json()
        return data.get('list', {}).items()
    else:
        print(f"Error: {response.status_code}")
        # print(response.json())
        return []

# Function to create the actual blog post entry


def create_blog_post(_message):
    """ Write the message contents to an appropriately named file
    """
    with open(
            f"_posts/{sun.strftime("%Y-%m-%d")}-interesting-last-week.md",
            "w", encoding="utf-8") as blog_file:
        blog_file.write(_message)
    blog_file.close()


# Fetch and send posts for each tag to my blog
page_tags = []
message = ""
for tag in tags:
    # print(f"Posts with tag '{tag}':")
    posts = get_posts_for_tag(tag)

    if posts:
        for item_id, item in posts:
            if int(item['time_added']) > sun.timestamp():
                continue
            title = item.get('resolved_title', 'No Title')
            url = item.get('resolved_url')
            excerpt = item.get('excerpt')
            time_added = datetime.fromtimestamp(int(item['time_added']))
            post_tags = []
            for post_tag in item.get('tags'):
                post_tags.append(f"{post_tag}")
                page_tags.append(f"{post_tag}")
            message = (f"{message}"
                       f"[{title}]({url}) - "
                       f"{excerpt}\n\n")
            # send_to_slack(message)
    else:
        no_posts_message = f"No posts found for this week"
        # send_to_slack(no_posts_message)
        print(no_posts_message)

message = (f"---\nlayout: post\n"
           f"title: Some things I found interesting from {
               last_week.strftime("%Y-%m-%d")} to {sun.strftime("%Y-%m-%d")}\n"
           f"category: Last-Week\n"
           f"tags: {page_tags}\n"
           f"author: pgmac\n"
           "---\n\n"
           f"# Interesting things\n\n"
           f"{message}\n\n"
           f"All this was saved to my [GetPocket](https://getpocket.com/) over the week")

create_blog_post(message)
