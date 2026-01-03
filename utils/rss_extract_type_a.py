import feedparser
import requests
from datetime import datetime, timezone
import hashlib

## TESTING VARIABLES
rss_url = "https://feeds.bbci.co.uk/news/rss.xml?edition=int"
source_id = "bbc_news_int"


def fetch_rss(url: str):
    """
    Fetch RSS content explicitly via HTTP.
    This avoids silent failures in some environments.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.content


def parse_rss(rss_bytes: bytes):
    """
    Parse RSS XML into structured Python objects.
    """
    feed = feedparser.parse(rss_bytes)
    return feed


def normalize_item(entry: dict):
    """
    Convert one RSS <item> into a normalized JSON record.
    """
    url = entry.get("link")

    # Stable unique ID (important for deduplication)
    uid = hashlib.sha256(
        f"{source_id}:{url}".encode("utf-8")
    ).hexdigest()

    published_at = None
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        published_at = datetime(
            *entry.published_parsed[:6],
            tzinfo=timezone.utc
        ).isoformat()

    thumbnail_url = None
    if "media_thumbnail" in entry and entry.media_thumbnail:
        thumbnail_url = entry.media_thumbnail[0].get("url")

    return {
        "id": uid,
        "source": source_id,
        "title": entry.get("title"),
        "summary": entry.get("summary"),
        "url": url,
        "published_at": published_at,
        "first_seen_at": datetime.now(timezone.utc).isoformat(),
        "thumbnail_url": thumbnail_url
    }


def extract_items(feed):
    """
    Extract and normalize all items from the feed.
    """
    records = []
    for entry in feed.entries:

        try:
            record = normalize_item(entry)
            records.append(record)

        except Exception as e:
            print(f"Failed to parse entry: {e}")

    return records


def main(source_id, rss_url):
    rss_bytes = fetch_rss(rss_url)
    feed = parse_rss(rss_bytes)
    records = extract_items(feed)[:2]
    base_dir = 'raw'

    print(f"Extracted {len(records)} items")

    return records
            


if __name__ == "__main__":
    main(source_id, rss_url)
