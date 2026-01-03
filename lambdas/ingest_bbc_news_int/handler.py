from utils import rss_extract_type_a, s3_loader
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Lambda started")
    logger.debug("This is a debug message")

    rss_url = "https://feeds.bbci.co.uk/news/rss.xml?edition=int"
    source_id = "bbc_news_int"

    try:
        records = rss_extract_type_a.main(source_id, rss_url)
        for file in records[:2]:
            s3_loader.load(file, source_id)

        logger.info("Extraction completed")
    except Exception as e:
        logger.exception(e)
        raise
    
    return {
        "status": "success",
        "count": len(records),
    }

if __name__ == '__main__':
    lambda_handler(None, None)