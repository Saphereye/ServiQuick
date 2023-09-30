import requests
from enum import Enum
import polyline

# todo use environment variables
API_KEY = 'iWrpAat8eDeNt2CqqWtw6bQPweqd2xqCNk7wh9gR_p8'
ORS_API_KEY = '5b3ce3597851110001cf6248056ade7a5d63493cb05b0d6692675228'

# ipinfo.io
def get_lat_long() -> str:
    api_url = "https://ipinfo.io"

    try:
        # Send a GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response if the API returns JSON data
            data = response.json()
            print("Current latlong: " + data['loc'])
            return data['loc']
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

class Service(Enum):
    HOSPITAL = 'hospital'
    FIRE_STATION = 'firestation'
    POLICE = 'police'

# https://discover.search.hereapi.com/v1/discover?at=52.8173086,12.2368342&limit=2&lang=en&q=hospital+hyderbad&apiKey=iWrpAat8eDeNt2CqqWtw6bQPweqd2xqCNk7wh9gR_p8
def get_nearest_service(service: Service) -> str:
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
            print(data['items'][0]['title'])
            print(data['items'][0]['position']['lat'], data['items'][0]['position']['lng'])

            return f"{data['items'][0]['position']['lat']},{data['items'][0]['position']['lng']}"
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

# # 'https://router.hereapi.com/v8/routes?transportMode=car&origin=52.5308,13.3847&destination=52.5323,13.3789&return=summary&apikey={YOUR_API_KEY}'
# def get_route():
#     waypoint0 = get_lat_long()
#     waypoint1 = get_nearest_service(Service.HOSPITAL)
#     mode = 'car'
#     app_id = 'OnyJ5cxLBpW9KOhx3wCW'
#     app_code = 'iWrpAat8eDeNt2CqqWtw6bQPweqd2xqCNk7wh9gR_p8'

#     api_url = f'https://router.hereapi.com/v8/routes?transportMode={mode}&origin={waypoint0}&destination={waypoint1}&return=summary&apikey={app_code}'
#     print(f"{api_url=}")

#     response = requests.get(api_url)
#     print(f"{response.json()=}")

#     if response.status_code == 200:
#         route_polyline = response.json()['routes'][0]['sections'][0]['polyline']
#         route_coordinates = polyline.decode(route_polyline)

#         # route_coordinates now contains the detailed list of coordinates along the route
#         for lat, lon in route_coordinates:
#             print(f"Latitude: {lat}, Longitude: {lon}")
#     else:
#         print('Failed to retrieve route data.')

def get_route(service: Service) -> list[list[float]]:
    start_coords = get_lat_long().split(',')
    end_coords = get_nearest_service(service).split(',')

    # Define the API endpoint URL
    endpoint = 'https://api.openrouteservice.org/v2/directions/driving-car'

    # Define the request parameters
    params = {
        'api_key': ORS_API_KEY,
        'start': f'{start_coords[1]},{start_coords[0]}',  # Latitude, Longitude
        'end': f'{end_coords[1]},{end_coords[0]}',  # Latitude, Longitude
    }

    try:
        # Send a GET request to the API
        response = requests.get(endpoint, params=params)

        print(f"{response=}")

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract the route geometry (list of coordinates)
            if 'features' in data and len(data['features']) > 0:
                route_geometry = data['features'][0]['geometry']['coordinates']
                return route_geometry
            else:
                print('No route data found in the response.')
                return None
        else:
            print(f'Failed to retrieve route data. Status code: {response.status_code}')
            return None

    except requests.exceptions.RequestException as e:
        print(f'Request error: {e}')
        return None

if __name__ == "__main__":
    print(get_lat_long())
    # print(get_nearest_service(Service.HOSPITAL))
    # print(get_nearest_service(Service.FIRE_STATION))
    print(get_route(Service.HOSPITAL))