import requests
from enum import Enum

API_KEY = 'iWrpAat8eDeNt2CqqWtw6bQPweqd2xqCNk7wh9gR_p8'

# ipinfo.io
def get_lat_long() -> tuple[str, str]:
    api_url = "https://ipinfo.io"

    try:
        # Send a GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response if the API returns JSON data
            data = response.json()
            return data['loc']
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

class Service(Enum):
    HOSPITAL = 'hospital'
    FIRE_STATION = 'firestation'

# https://discover.search.hereapi.com/v1/discover?at=52.8173086,12.2368342&limit=2&lang=en&q=hospital+hyderbad&apiKey=iWrpAat8eDeNt2CqqWtw6bQPweqd2xqCNk7wh9gR_p8
def get_nearest_service(service: Service) -> dict[str, str]:
    loc = get_lat_long()

    api_url = f"https://discover.search.hereapi.com/v1/discover?at={loc}&limit=2&lang=en&q={service.value}&apiKey={API_KEY}"
    # print(api_url)

    try:
        # Send a GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response if the API returns JSON data
            data = response.json()
            # print(data['items'])

            return data['items'][0]['title']
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

# 'https://router.hereapi.com/v8/routes?transportMode=car&origin=52.5308,13.3847&destination=52.5323,13.3789&return=summary&apikey={YOUR_API_KEY}'
def get_route():
    pass

if __name__ == "__main__":
    # print(get_lat_long())
    print(get_nearest_service(Service.HOSPITAL))
    print(get_nearest_service(Service.FIRE_STATION))