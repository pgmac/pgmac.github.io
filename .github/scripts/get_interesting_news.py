#!/usr/bin/env python3

"""Let's get some interesting things from Pocket and share them about"""

import os
from datetime import datetime, timedelta

import requests

tags = ["tag1"]  # Replace with your specific tags
week_offset = os.environ.get("week_offset", 0)

# Calculate the time range for the previous week
today = datetime.now()
idx = (today.weekday() + 1) % 7
sun = today - timedelta(idx + (int(week_offset) * 7))
last_week = sun - timedelta(days=7)
since = int(last_week.timestamp())


def get_link_tags(_linkid):
    """Get all the tags for a link"""
    api_url = f"https://links.pgmac.net.au/api/v2/links/{_linkid}"
    headers = {
        "Authorization": f"Bearer {os.environ.get('PGLINKS_KEY')}",
        "accept": "application/json",
    }
    try:
        response = requests.get(api_url, timeout=30, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching tags for link {_linkid}: {e}")
        return {}


def get_link_notes(_linkid):
    """Get all the notes for a link"""
    api_url = f"https://links.pgmac.net.au/api/v2/links/{_linkid}/notes"
    headers = {
        "Authorization": f"Bearer {os.environ.get('PGLINKS_KEY')}",
        "accept": "application/json",
    }
    try:
        response = requests.get(api_url, timeout=30, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching notes for link {_linkid}: {e}")
        return {}


def get_links():
    """Get all the Pocket posts with a tag"""
    api_url = "https://links.pgmac.net.au/api/v2/links"
    headers = {
        "Authorization": f"Bearer {os.environ.get('PGLINKS_KEY')}",
        "accept": "application/json",
    }
    params = {"per_page": 100, "order_by": "created_at", "order_dir": "desc"}
    try:
        response = requests.get(api_url, timeout=30, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching links from API: {e}")
        print(f"Request: {api_url}\n{headers}\n{params}")
        print(f"Response: {response.headers}")
        return {}
    return {}


def create_blog_post(_message):
    """Write the message contents to an appropriately named file"""
    with open(
        f"_posts/{sun.strftime('%Y-%m-%d')}-interesting-last-week.md",
        "w",
        encoding="utf-8",
    ) as blog_file:
        blog_file.write(_message)
    blog_file.close()


def main():
    # Fetch and send posts for each tag to my blog
    page_tags = []
    articles = ""
    print(
        f"Fetching links between {last_week.strftime('%Y-%m-%d')} to {sun.strftime('%Y-%m-%d')}"
    )
    # from pprint import pprint
    for tag in tags:
        posts = get_links()
        links_date_format = "%Y-%m-%dT%H:%M:%S.%fZ"  # 2025-05-27T15:10:04.000000Z

        if posts:
            post_titles = []
            print(
                "        Last week          <=      Link date      <=         Sunday             <-> Status"
            )
            # 2025-06-01 23:03:06.259047  2025-06-01 23:03:06.259047  2025-06-01 23:03:06.259047
            for item in posts["data"]:
                link_created_at = datetime.strptime(
                    item.get("created_at", "3999-12-31T23:59:59.999999Z"),
                    links_date_format,
                )
                print(f"{last_week} <= {link_created_at} <= {sun} <-> ", end="")
                if (
                    link_created_at.timestamp() <= last_week.timestamp()
                    or link_created_at.timestamp() >= sun.timestamp()
                ):
                    print("skipping")
                    continue
                else:
                    print("processing")
                title = item.get("title", "No Title")
                url = item.get("url", "#")
                excerpt = item.get("description", "&nbsp;")
                # time_added = datetime.fromtimestamp(datetime.strptime(item.get('created_at', '0000-00-00T00:00:00.000000Z'), links_date_format).timestamp())
                post_tags = []
                # item['tags'] = get_link_tags(item.get('id', 0)).get('tags', {})
                item["tags"] = [
                    tag["name"]
                    for tag in get_link_tags(item.get("id", 0)).get("tags", {})
                    if tag.get("visibility") == 1
                ]
                for post_tag in item.get("tags", {}):
                    post_tags.append(f"{post_tag}")
                    page_tags.append(f"{post_tag}")
                item["notes"] = [
                    note["note"]
                    for note in get_link_notes(item.get("id", 0)).get("data", {})
                    if note.get("visibility") == 1
                ]
                for post_note in item["notes"]:
                    excerpt += f"\n\n> {post_note.replace('\n', '\n> ')}"
                post_titles.append(title)
                articles = (
                    f'{articles}<a name="{title}">[{title}]({url})</a> - {excerpt}\n\n'
                )
        else:
            no_posts_message = "No posts found for this week"
            # send_to_slack(no_posts_message)
            print(no_posts_message)
            return

    last_week_format = "%e %B"
    if last_week.strftime("%B") == sun.strftime("%B"):
        last_week_format = "%e"

    message = (
        f"---\nlayout: last-week\n"
        f"title: Some things I found interesting from {last_week.strftime('%Y-%m-%d')} to {sun.strftime('%Y-%m-%d')}\n"
        f"category: Last-Week\n"
        f"tags: {page_tags}\n"
        f"author: pgmac\n"
        "---\n\n"
        f"Internet Discoveries between {last_week.strftime(last_week_format)} and {sun.strftime('%e %B')}\n\n"
    )
    for title in post_titles:
        message += f"- {title}\n"
    message += (
        f"\n## Interesting details\n\n"
        f"{articles}"
        f"\n---\n\nAll this was saved to my [Link Ace](https://links.pgmac.net.au/) over the week"
    )

    create_blog_post(message)


if __name__ == "__main__":
    main()
