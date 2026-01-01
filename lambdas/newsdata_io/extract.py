import requests
import json

api_key = 'pub_5dbb6750374a46d0a83800ccb551245f'

url = 'https://newsdata.io/api/1/latest?apikey=pub_5dbb6750374a46d0a83800ccb551245f&q=pizza'
# url = 'https://newsdata.io/api/1/archive?apikey=pub_5dbb6750374a46d0a83800ccb551245f&q=example&language=en&from_date=2025-12-23&to_date=2025-12-30'


headers = {
    "X-ACCESS-KEY": api_key,
    "Accept": "application/json",
    "Content-Type": "application/json",
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # Raises HTTPError for 4xx/5xx

    data = response.json()
    print("Success:", data)

except requests.exceptions.HTTPError as http_err:
    print("HTTP error:", http_err)
    print("Response body:", response.text)

except requests.exceptions.RequestException as err:
    print("Request failed:", err)