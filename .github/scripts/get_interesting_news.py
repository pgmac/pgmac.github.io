#!/usr/bin/env python3

"""
Generate weekly blog posts from Link Ace bookmarks

This script fetches public links, tags, and notes from Link Ace and creates
a weekly blog post. Only public items (visibility == 1 or is_private == False)
are included in the generated post.
"""

import os
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests


class Config:
    """Configuration for the script"""

    API_BASE_URL = "https://links.pgmac.net.au/api/v2"
    LINKS_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    REQUEST_TIMEOUT = 30
    LINKS_PER_PAGE = 100
    MAX_RETRIES = 5
    INITIAL_BACKOFF = 2  # seconds
    MAX_BACKOFF = 60  # seconds

    def __init__(self):
        self.api_key = os.environ.get("PGLINKS_KEY")
        self.week_offset = int(os.environ.get("week_offset", 0))

        if not self.api_key:
            raise ValueError("PGLINKS_KEY environment variable is required")

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "accept": "application/json",
        }


class DateRange:
    """Calculate and store the date range for the blog post"""

    def __init__(self, week_offset: int = 0):
        today = datetime.now()
        days_since_sunday = (today.weekday() + 1) % 7
        end_day = today - timedelta(days_since_sunday + (week_offset * 7))
        start_day = end_day - timedelta(days=7)

        # Set start to beginning of day (00:00:00)
        self.start_date = start_day.replace(hour=0, minute=0, second=0, microsecond=0)
        # Set end to end of day (23:59:59)
        self.end_date = end_day.replace(
            hour=23, minute=59, second=59, microsecond=999999
        )

    def is_in_range(self, timestamp: datetime) -> bool:
        """Check if a timestamp falls within this date range (inclusive)"""
        return (
            self.start_date.timestamp()
            <= timestamp.timestamp()
            <= self.end_date.timestamp()
        )

    def format_title(self) -> str:
        """Format the date range for the post title"""
        return f"{self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}"

    def format_description(self) -> str:
        """Format the date range for the post description"""
        start_format = "%e %B" if self.start_date.month != self.end_date.month else "%e"
        return f"{self.start_date.strftime(start_format)} and {self.end_date.strftime('%e %B')}"

    def get_filename(self) -> str:
        """Get the filename for the blog post"""
        return f"_posts/{self.end_date.strftime('%Y-%m-%d')}-interesting-last-week.md"


class LinkAceAPI:
    """Client for interacting with the Link Ace API"""

    def __init__(self, config: Config):
        self.config = config

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a request to the API with exponential backoff for rate limiting"""
        url = f"{self.config.API_BASE_URL}/{endpoint}"
        backoff = self.config.INITIAL_BACKOFF

        for attempt in range(self.config.MAX_RETRIES):
            try:
                response = requests.get(
                    url,
                    timeout=self.config.REQUEST_TIMEOUT,
                    headers=self.config.headers,
                    params=params,
                )

                if response.status_code == 429:
                    if attempt < self.config.MAX_RETRIES - 1:
                        # Check for Retry-After header
                        retry_after = response.headers.get("Retry-After")
                        if retry_after:
                            try:
                                wait_time = int(retry_after)
                            except ValueError:
                                wait_time = backoff
                        else:
                            wait_time = backoff

                        print(
                            f"Rate limited on {endpoint}. Waiting {wait_time}s before retry {attempt + 1}/{self.config.MAX_RETRIES}..."
                        )
                        time.sleep(wait_time)

                        # Exponential backoff with cap
                        backoff = min(backoff * 2, self.config.MAX_BACKOFF)
                        continue
                    else:
                        print(
                            f"Rate limit exceeded for {endpoint} after {self.config.MAX_RETRIES} retries"
                        )
                        return {}

                response.raise_for_status()
                return response.json()

            except requests.RequestException as e:
                if attempt < self.config.MAX_RETRIES - 1:
                    print(
                        f"Request error on {endpoint}: {e}. Retrying in {backoff}s..."
                    )
                    time.sleep(backoff)
                    backoff = min(backoff * 2, self.config.MAX_BACKOFF)
                    continue
                else:
                    print(
                        f"Error fetching from {endpoint} after {self.config.MAX_RETRIES} retries: {e}"
                    )
                    return {}

        return {}

    def get_links(self) -> Dict:
        """Get all public links from the API"""
        params = {
            "per_page": self.config.LINKS_PER_PAGE,
            "order_by": "created_at",
            "order_dir": "desc",
            "private": 0,
        }
        return self._make_request("links", params)

    def get_link_tags(self, link_id: int) -> List[str]:
        """Get all public tags for a link"""
        response = self._make_request(f"links/{link_id}")
        tags = response.get("tags", [])
        return [tag["name"] for tag in tags if tag.get("visibility") == 1]

    def get_link_notes(self, link_id: int) -> List[str]:
        """Get all public notes for a link"""
        response = self._make_request(f"links/{link_id}/notes")
        notes = response.get("data", [])
        return [note["note"] for note in notes if note.get("visibility") == 1]


class Link:
    """Represents a link with its metadata"""

    YOUTUBE_PATTERNS = [
        r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)",
        r"(?:https?://)?(?:www\.)?youtu\.be/([^?]+)",
        r"(?:https?://)?(?:www\.)?youtube\.com/embed/([^?]+)",
        r"(?:https?://)?(?:www\.)?youtube\.com/v/([^?]+)",
    ]

    def __init__(self, data: Dict, api: LinkAceAPI, fetch_details: bool = True):
        self.id = data.get("id", 0)
        self.title = self._sanitize(data.get("title") or "No Title")
        self.url = data.get("url", "#")
        self.description = self._sanitize(data.get("description") or "&nbsp;")
        self.is_private = data.get("is_private", False)
        self.created_at = datetime.strptime(
            data.get("created_at", "3999-12-31T23:59:59.999999Z"),
            Config.LINKS_DATE_FORMAT,
        )
        self.tags = []
        self.notes = []

        if fetch_details:
            self.tags = api.get_link_tags(self.id)
            self.notes = api.get_link_notes(self.id)

    @staticmethod
    def _sanitize(text: str) -> str:
        """Sanitize text for markdown output"""
        return text.replace('"', "&quot;").replace("|", "-")

    @property
    def youtube_id(self) -> Optional[str]:
        """Extract YouTube video ID if this is a YouTube link"""
        for pattern in self.YOUTUBE_PATTERNS:
            match = re.search(pattern, self.url)
            if match:
                return match.group(1)
        return None

    def format_excerpt(self) -> str:
        """Format the description with notes"""
        excerpt = self.description
        for note in self.notes:
            sanitized_note = self._sanitize(note).replace("\n", "\n> ")
            excerpt += f"\n\n> {sanitized_note}"
        return excerpt

    def to_markdown(self) -> str:
        """Convert link to markdown format"""
        anchor = f'<a name="{self.title}"></a>'
        excerpt = self.format_excerpt()

        if self.youtube_id:
            return (
                f"{anchor}**[{self.title}]({self.url})**\n\n"
                f'{{% include youtube.html id="{self.youtube_id}" %}}\n\n'
                f"{excerpt}\n\n"
            )
        else:
            return f"{anchor}[{self.title}]({self.url}) - {excerpt}\n\n"


class BlogPostGenerator:
    """Generates the blog post from links"""

    def __init__(self, api: LinkAceAPI, date_range: DateRange):
        self.api = api
        self.date_range = date_range

    def fetch_links(self) -> List[Link]:
        """Fetch and filter links for the date range"""
        print(f"Fetching links between {self.date_range.format_title()}")
        print(
            "        Start date         <=      Link date      <=         End date           <-> Status"
        )

        response = self.api.get_links()
        if not response or "data" not in response:
            print("No posts found for this week")
            return []

        links = []
        for item in response["data"]:
            if item.get("is_private", False):
                print(f"Skipping private link: {item.get('title', 'No Title')}")
                continue

            # Create link without fetching details yet
            link = Link(item, self.api, fetch_details=False)
            print(
                f"{self.date_range.start_date} <= {link.created_at} <= {self.date_range.end_date} <-> ",
                end="",
            )

            if self.date_range.is_in_range(link.created_at):
                print("processing")
                # Only fetch tags and notes for links in the date range
                link.tags = self.api.get_link_tags(link.id)
                link.notes = self.api.get_link_notes(link.id)
                # Only keep YouTube videos with a 'liked' tag (case-insensitive)
                if link.youtube_id and any(t.lower() == "liked" for t in link.tags):
                    links.append(link)
                else:
                    print("skipping liked filter")
            else:
                print("skipping")

        # Sort links by created_at
        links.sort(key=lambda l: l.created_at)
        return links

    def generate_post(self, links: List[Link]) -> str:
        """Generate the complete blog post content"""
        if not links:
            return ""

        all_tags = []
        articles = ""
        titles = []

        for link in links:
            all_tags.extend(link.tags)
            titles.append(link.title)
            articles += link.to_markdown()

        front_matter = (
            f"---\n"
            f"layout: last-week\n"
            f"title: Some things I found interesting from {self.date_range.format_title()}\n"
            f"category: Last-Week\n"
            f"tags: {all_tags}\n"
            f"author: pgmac\n"
            f"---\n\n"
        )

        intro = (
            f"Internet Discoveries between {self.date_range.format_description()}\n\n"
        )

        toc = "".join(f"- {title}\n" for title in titles)

        footer = "\n---\n\nAll this was saved to my [Link Ace](https://links.pgmac.net.au/) over the week"

        return (
            f"{front_matter}{intro}{toc}\n## Interesting details\n\n{articles}{footer}"
        )

    def save_post(self, content: str) -> None:
        """Save the blog post to a file"""
        if not content:
            print("No content to save")
            return

        filename = self.date_range.get_filename()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Blog post saved to {filename}")


def main():
    """Main entry point for the script"""
    try:
        config = Config()
        date_range = DateRange(config.week_offset)
        api = LinkAceAPI(config)
        generator = BlogPostGenerator(api, date_range)

        links = generator.fetch_links()
        if not links:
            print("No links found for the specified date range")
            return

        content = generator.generate_post(links)
        generator.save_post(content)

    except Exception as e:
        print(f"Error generating blog post: {e}")
        raise


if __name__ == "__main__":
    main()
