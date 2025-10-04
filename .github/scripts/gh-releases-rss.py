#!/usr/bin/env -S uv run --script
"""
GitHub Releases RSS Feed Generator

Generates an RSS feed from releases of starred GitHub repositories.

Usage:
    ./gh-releases-rss.py <username> [options]
    ./gh-releases-rss.py pgmac -o releases.xml -n 5
    ./gh-releases-rss.py pgmac --debug

Environment Variables:
    GITHUB_TOKEN - GitHub personal access token (recommended for higher rate limits)
"""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "feedgen",
#     "requests",
# ]
# ///

import argparse
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import requests
from feedgen.feed import FeedGenerator


# Constants
GITHUB_API_BASE = "https://api.github.com"
ITEMS_PER_PAGE = 100
DEFAULT_RELEASES_PER_REPO = 3


@dataclass
class FeedConfig:
    """Configuration for RSS feed generation"""

    username: str
    output_file: str = "github_releases.xml"
    releases_per_repo: int = DEFAULT_RELEASES_PER_REPO
    verbose: bool = False


class GitHubAPIClient:
    """Client for interacting with GitHub API"""

    def __init__(self, token: Optional[str] = None):
        self.session = requests.Session()
        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self.session.headers.update(headers)

    def _paginate(self, url: str, resource_name: str) -> list[dict]:
        """Generic pagination handler for GitHub API endpoints"""
        items = []
        page = 1

        while True:
            response = self.session.get(
                url, params={"page": page, "per_page": ITEMS_PER_PAGE}
            )

            if response.status_code != 200:
                print(f"Error fetching {resource_name}: {response.status_code}")
                print(response.text)
                break

            page_items = response.json()
            if not page_items:
                break

            items.extend(page_items)
            page += 1

        return items

    def get_starred_repositories(self) -> list[dict]:
        """Fetch all starred repositories for the authenticated user"""
        url = f"{GITHUB_API_BASE}/user/starred"
        return self._paginate(url, "starred repositories")

    def get_recent_releases(self, repo_full_name: str, limit: int) -> list[dict]:
        """Fetch recent releases for a repository"""
        url = f"{GITHUB_API_BASE}/repos/{repo_full_name}/releases"
        response = self.session.get(url, params={"per_page": limit})

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []
        else:
            return []


class GitHubReleasesRSSGenerator:
    """Generator for creating RSS feeds from GitHub releases"""

    def __init__(self, config: FeedConfig, api_client: GitHubAPIClient):
        self.config = config
        self.api = api_client

    def _create_feed(self) -> FeedGenerator:
        """Initialize RSS feed with metadata"""
        fg = FeedGenerator()
        fg.title(f"{self.config.username}'s Starred Repo Releases")
        fg.link(
            href=f"https://github.com/{self.config.username}?tab=stars", rel="alternate"
        )
        fg.description(
            f"Latest releases from repositories starred by {self.config.username}"
        )
        fg.language("en")
        fg.lastBuildDate(datetime.now(timezone.utc))
        return fg

    def _parse_datetime(self, date_str: str) -> datetime:
        """Parse GitHub datetime string to datetime object"""
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    def _add_release_entry(
        self, feed: FeedGenerator, repo: dict, release: dict
    ) -> None:
        """Add a single release entry to the RSS feed"""
        entry = feed.add_entry()
        entry.id(release["html_url"])
        entry.title(f"{repo['full_name']} - {release['tag_name']}")
        entry.link(href=release["html_url"])

        # Build description HTML
        description = f"""
        <h3>{release.get("name") or release["tag_name"]}</h3>
        <p><strong>Repository:</strong> <a href="{repo["html_url"]}">{repo["full_name"]}</a></p>
        <p><strong>Release:</strong> {release["tag_name"]}</p>
        <p><strong>Published:</strong> {release["published_at"]}</p>
        """

        if release.get("author"):
            description += (
                f"<p><strong>Author:</strong> {release['author']['login']}</p>"
            )

        description += f"<div>{release.get('body') or 'No release notes provided.'}</div>"

        entry.description(description)

        # Set author
        author_name = (
            release["author"]["login"]
            if release.get("author")
            else repo["owner"]["login"]
        )
        entry.author(name=author_name)

        # Set publication date
        entry.pubDate(self._parse_datetime(release["published_at"]))

    def _collect_releases(self, repos: list[dict]) -> list[dict]:
        """Collect all releases from the given repositories"""
        all_releases = []
        total = len(repos)

        for idx, repo in enumerate(repos, 1):
            repo_name = repo["full_name"]

            # Progress indicator
            print(f"\rProcessing {idx}/{total}: {repo_name:<60}", end="", flush=True)

            releases = self.api.get_recent_releases(
                repo_name, self.config.releases_per_repo
            )

            if releases and self.config.verbose:
                print(f"\n  Found {len(releases)} release(s)")

            for release in releases:
                all_releases.append({"repo": repo, "release": release})

        print()  # New line after progress
        return all_releases

    def generate(self) -> str:
        """Generate RSS feed and save to file"""
        print(f"Fetching starred repositories for {self.config.username}...")
        repos = self.api.get_starred_repositories()
        print(f"Found {len(repos)} starred repositories\n")

        # Collect all releases
        all_releases = self._collect_releases(repos)

        # Sort by publication date (newest first)
        all_releases.sort(
            key=lambda x: self._parse_datetime(x["release"]["published_at"]),
            reverse=True,
        )

        print(f"\nBuilding RSS feed with {len(all_releases)} release(s)...")

        # Create feed and add entries
        feed = self._create_feed()
        for item in all_releases:
            self._add_release_entry(feed, item["repo"], item["release"])

        # Save to file
        rss_content = feed.rss_str(pretty=True)
        with open(self.config.output_file, "wb") as f:
            f.write(rss_content)

        print(f"✓ RSS feed saved to {self.config.output_file}")
        return self.config.output_file


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate RSS feed from GitHub starred repository releases"
    )
    parser.add_argument(
        "username",
        help="GitHub username to fetch starred repositories for",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="github_releases.xml",
        help="Output file path (default: github_releases.xml)",
    )
    parser.add_argument(
        "-n",
        "--num-releases",
        type=int,
        default=3,
        help="Number of releases per repository (default: 3)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Debug mode: show starred repos count only",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args()

    # Load GitHub token
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print(
            "Warning: GITHUB_TOKEN not set. API rate limits will be lower.",
            file=sys.stderr,
        )

    # Initialize API client
    api_client = GitHubAPIClient(token)

    # Debug mode: just show starred repos
    if args.debug:
        print("=== DEBUG MODE ===")
        repos = api_client.get_starred_repositories()
        print(f"Total starred repositories: {len(repos)}")
        if repos:
            print(f"First repository: {repos[0]['full_name']}")
        return

    # Generate RSS feed
    config = FeedConfig(
        username=args.username,
        output_file=args.output,
        releases_per_repo=args.num_releases,
        verbose=args.verbose,
    )

    generator = GitHubReleasesRSSGenerator(config, api_client)
    generator.generate()


if __name__ == "__main__":
    main()
