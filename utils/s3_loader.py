import boto3
import os

def get_s3_client():
    return boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),  # None in prod
    )


# def run_etl():
#     data = fetch_api_data()
#     s3 = get_s3_client()

#     s3.put_object(
#         Bucket=os.environ["S3_BUCKET"],
#         Key="raw/data.json",
#         Body=json.dumps(data),
#     )

if __name__ == '__main__':
    s3_client = get_s3_client()
    print(s3_client.list_buckets())