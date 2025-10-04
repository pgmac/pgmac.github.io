#!/usr/bin/env -S uv run --script
"""
GitHub Releases RSS Feed Generator

This script fetches release information from GitHub repositories you're watching
and generates an RSS feed.

Requirements:
- pip install requests feedgen

Usage:
1. Set your GitHub username and optionally a personal access token
2. Run the script to generate releases.xml
"""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "datetime",
#     "feedgen",
#     "requests",
# ]
# ///

# import json
import os
from datetime import datetime, timezone

import requests
from feedgen.feed import FeedGenerator


class GitHubRSSGenerator:
    def __init__(self, username, token=None):
        self.username = username
        self.token = token
        self.session = requests.Session()

        # Set up authentication if token provided
        if token:
            self.session.headers.update(
                {
                    "Authorization": f"token {token}",
                    "Accept": "application/vnd.github.v3+json",
                }
            )
        else:
            self.session.headers.update({"Accept": "application/vnd.github.v3+json"})

    def get_watched_repositories(self):
        """Get list of repositories the user is watching"""
        # url = f"https://api.github.com/users/{self.username}/subscriptions"
        url = "https://api.github.com/user/subscriptions"
        repos = []
        page = 1

        while True:
            response = self.session.get(url, params={"page": page, "per_page": 100})

            if response.status_code != 200:
                print(f"Error fetching watched repos: {response.status_code}")
                print(response.text)
                break

            page_repos = response.json()
            if not page_repos:
                break

            repos.extend(page_repos)
            page += 1

        return repos

    def get_latest_release(self, repo_full_name):
        """Get the latest release for a repository"""
        url = f"https://api.github.com/repos/{repo_full_name}/releases/latest"
        response = self.session.get(url)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # No releases found
            return None
        else:
            print(
                f"Error fetching release for {repo_full_name}: {response.status_code}"
            )
            return None

    def get_recent_releases(self, repo_full_name, limit=5):
        """Get recent releases for a repository"""
        url = f"https://api.github.com/repos/{repo_full_name}/releases"
        response = self.session.get(url, params={"per_page": limit})

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []
        else:
            print(
                f"Error fetching releases for {repo_full_name}: {response.status_code}"
            )
            return []

    def generate_rss_feed(self, include_all_recent=False, releases_per_repo=1):
        """Generate RSS feed from watched repositories' releases"""

        print(f"Fetching watched repositories for {self.username}...")
        watched_repos = self.get_watched_repositories()
        print(f"Found {len(watched_repos)} watched repositories")

        # Create feed
        fg = FeedGenerator()
        fg.title(f"{self.username}'s GitHub Releases")
        fg.link(href=f"https://github.com/{self.username}", rel="alternate")
        fg.description(f"Latest releases from repositories watched by {self.username}")
        fg.language("en")
        fg.lastBuildDate(datetime.now(timezone.utc))

        all_releases = []

        for repo_count, repo in enumerate(watched_repos):
            repo_name = repo["full_name"]
            print("\033[K", end="")  # Clear the line first
            print(
                f"Repo: {repo_count + 1}. Checking releases for {repo_name}...",
                end="\r",
            )

            if include_all_recent:
                releases = self.get_recent_releases(repo_name, releases_per_repo)
            else:
                latest_release = self.get_latest_release(repo_name)
                releases = [latest_release] if latest_release else []

            for release in releases:
                if release:  # Skip None releases
                    all_releases.append({"repo": repo, "release": release})
        print("")

        # Sort releases by published date (newest first)
        all_releases.sort(
            key=lambda x: datetime.fromisoformat(
                x["release"]["published_at"].replace("Z", "+00:00")
            ),
            reverse=True,
        )

        print(f"Adding {len(all_releases)} releases to RSS feed...")

        for item in all_releases:
            repo = item["repo"]
            release = item["release"]

            fe = fg.add_entry()
            fe.id(release["html_url"])
            fe.title(f"{repo['full_name']} - {release['tag_name']}")
            fe.link(href=release["html_url"])
            fe.description(f"""
            <h3>{release["name"] or release["tag_name"]}</h3>
            <p><strong>Repository:</strong> <a href="{repo["html_url"]}">{repo["full_name"]}</a></p>
            <p><strong>Release:</strong> {release["tag_name"]}</p>
            <p><strong>Published:</strong> {release["published_at"]}</p>
            {f"<p><strong>Author:</strong> {release['author']['login']}</p>" if release.get("author") else ""}
            <div>{release["body"] or "No release notes provided."}</div>
            """)
            fe.author(
                name=release["author"]["login"]
                if release.get("author")
                else repo["owner"]["login"]
            )
            fe.pubDate(
                datetime.fromisoformat(release["published_at"].replace("Z", "+00:00"))
            )

        return fg

    def save_feed(
        self,
        filename="github_releases.xml",
        include_all_recent=False,
        releases_per_repo=1,
    ):
        """Generate and save RSS feed to file"""
        fg = self.generate_rss_feed(include_all_recent, releases_per_repo)

        # Generate the RSS feed
        rss_str = fg.rss_str(pretty=True)

        # Save to file
        with open(filename, "wb") as f:
            f.write(rss_str)

        print(f"RSS feed saved to {filename}")
        return filename


def main():
    # Configuration
    USERNAME = "pgmac"  # Replace with your GitHub username
    TOKEN = os.getenv(
        "GITHUB_TOKEN"
    )  # Optional: GitHub personal access token for higher rate limits

    # You can get a token at: https://github.com/settings/tokens
    # TOKEN = "ghp_your_token_here"

    # Create generator
    generator = GitHubRSSGenerator(USERNAME, TOKEN)

    # Generate RSS feed
    # Options:
    # - include_all_recent=False: Only latest release per repo
    # - include_all_recent=True: Multiple recent releases per repo
    # - releases_per_repo: How many releases to include per repo (when include_all_recent=True)

    generator.save_feed(
        filename="github_releases.rss",
        include_all_recent=False,  # Set to True for more releases per repo
        releases_per_repo=3,  # Only used when include_all_recent=True
    )


if __name__ == "__main__":
    main()
