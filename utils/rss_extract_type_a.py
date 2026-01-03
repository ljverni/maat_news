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


def sanitize_for_json(obj):
    """
    Recursively convert objects into JSON-serializable types.
    - dict/FeedParserDict -> dict
    - list -> list
    - datetime -> isoformat string
    - bytes -> utf-8 string
    - other non-serializable -> str
    """
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        return obj.decode('utf-8', errors='ignore')
    elif hasattr(obj, "get") and hasattr(obj, "keys"):  # FeedParserDict
        return {k: sanitize_for_json(obj[k]) for k in obj.keys()}
    else:
        return obj


def normalize_item(entry: dict, source_id: str):
    """
    Convert one RSS <item> into a normalized JSON record.
    """
    url = entry.get("link")

    # Stable unique ID
    uid = hashlib.sha256(f"{source_id}:{url}".encode("utf-8")).hexdigest()

    published_at = None
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        published_at = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

    thumbnail_url = None
    if "media_thumbnail" in entry and entry.media_thumbnail:
        thumbnail_url = entry.media_thumbnail[0].get("url")

    record = {
        "id": uid,
        "source": source_id,
        "title": entry.get("title"),
        "summary": entry.get("summary"),
        "url": url,
        "published_at": published_at,
        "first_seen_at": datetime.now(timezone.utc),
        "thumbnail_url": thumbnail_url
    }

    # Sanitize record to make it JSON-safe
    return sanitize_for_json(record)


def extract_items(feed, source_id: str):
    """
    Extract and normalize all items from the feed.
    """
    records = []
    for entry in feed.entries:
        try:
            record = normalize_item(entry, source_id)
            records.append(record)
        except Exception as e:
            print(f"Failed to parse entry: {e}")
    return records


def main(source_id, rss_url, limit=None):
    """
    Fetch, parse, and normalize RSS feed items.
    Returns a list of JSON-safe dictionaries.
    """
    rss_bytes = fetch_rss(rss_url)
    feed = parse_rss(rss_bytes)
    records = extract_items(feed, source_id)

    if limit:
        records = records[:limit]

    print(f"Extracted {len(records)} items from {source_id}")
    return records


if __name__ == "__main__":
    records = main(source_id, rss_url, limit=2)
    for r in records:
        print(r)
