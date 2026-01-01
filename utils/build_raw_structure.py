import os
import hashlib
from datetime import datetime

def build_article_path(base_dir, source, article_url, published_at, file_name=None):
    """
    Create folder structure and deterministic filename for an article.
    
    Args:
        base_dir (str): Base directory, e.g., "raw"
        source (str): Feed/source name, e.g., "bbc_news_int"
        article_url (str): URL of the article
        published_at (str or datetime): Article publish datetime
    Returns:
        str: Full path to save the article JSON
    """
    
    year = published_at.year
    month = f"{published_at.month:02d}"
    day = f"{published_at.day:02d}"
    
    # Folder path
    folder_path = os.path.join(base_dir, f"{source}", f"{year}", f"{month}", f"{day}")
    
    # Ensure folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    # Deterministic filename using SHA1 of URL
    if file_name:
        filename = file_name + ".json"
    else:
        filename = hashlib.sha1(article_url.encode()).hexdigest() + ".json"
    
    return os.path.join(folder_path, filename)

if __name__ == '__main__':
    # Example usage
    base_dir = "raw"
    source = "bbc_news_int"
    article_url = "https://www.bbc.com/news/articles/cvg13333lvko"
    published_at = "Tue, 30 Dec 2025 18:23:55 GMT"

    file_path = build_article_path(base_dir, source, article_url, published_at)
    print("Save article to:", file_path)

    # Now you can write the article JSON
    article_json = {
        "url": article_url,
        "title": "Mum and children who died in Boxing Day fire named",
        "published_at": published_at
    }

    import json
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(article_json, f, ensure_ascii=False, indent=2)
