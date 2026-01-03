import boto3
import os
from pathlib import Path
from dotenv import load_dotenv
import json
from datetime import datetime

# Load .env only if running locally
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)


def get_s3_client():
    endpoint_url = os.getenv("S3_ENDPOINT_URL")
    if endpoint_url == '':
        endpoint_url = None

    return boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION", "eu-south-2"),
        endpoint_url=endpoint_url,  # None in prod
    )


def load(data, source_id):
    s3_client = get_s3_client()

    try:
        published_at = data.get("published_at")

        if published_at:
            published_at_date = datetime.strptime(published_at[:10], "%Y-%m-%d")
        else:
            published_at_date = datetime.now()

        
        article_id = data['id']

        file_path = f"raw/{source_id}/{published_at_date.year}/{published_at_date.month:02}/{published_at_date.day:02}/{article_id}.json"


        s3_client.put_object(
            Bucket=os.getenv("S3_BUCKET"),
            Key=file_path,
            Body=json.dumps(data, ensure_ascii=False).encode("utf-8"),
        )

    except Exception as e:
        print(f"Upload failed for {source_id}, article {article_id}:", e)



if __name__ == '__main__':
    source_id = "bbc_news_int"
    article_id = 'test'
    dummy_data = {'id': '000342698943c91d145567f2c4addbe7f0c26d6a7167936ab7229c40d9236ed9', 'source': 'bbc_news_int', 'title': 'Video shows fire spreading across bar ceiling', 'summary': 'The moment a Swiss bar was set ablaze appears to have been captured on video.', 'url': 'https://www.bbc.com/news/videos/cwy1l7jwgjvo?at_medium=RSS&at_campaign=rss', 'published_at': '2026-01-01T14:49:31+00:00', 'first_seen_at': '2026-01-01T21:48:09.386992+00:00', 'thumbnail_url': 'https://ichef.bbci.co.uk/ace/standard/240/cpsprodpb/f5fc/live/62e877d0-e71f-11f0-aae2-2191c0e48a3b.jpg'}

    load(dummy_data, source_id)
    
