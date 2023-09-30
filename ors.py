import requests

# Replace with your OpenRouteService API key
API_KEY = '5b3ce3597851110001cf6248056ade7a5d63493cb05b0d6692675228'

def get_route(start_coords, end_coords):
    # Define the API endpoint URL
    endpoint = 'https://api.openrouteservice.org/v2/directions/driving-car'

    # Define the request parameters
    params = {
        'api_key': API_KEY,
        'start': f'{start_coords[1]},{start_coords[0]}',  # Latitude, Longitude
        'end': f'{end_coords[1]},{end_coords[0]}',  # Latitude, Longitude
    }

    try:
        # Send a GET request to the API
        response = requests.get(endpoint, params=params)

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

if __name__ == '__main__':
    # Define the coordinates of the starting and ending points (e.g., [latitude, longitude])
    start_coordinates = [52.5200, 13.4050]  # Example: Berlin, Germany
    end_coordinates = [48.8588, 2.2945]  # Example: Paris, France

    # Get the route geometry
    route_geometry = get_route(start_coordinates, end_coordinates)

    if route_geometry:
        print('Route coordinates:')
        for lat, lon in route_geometry:
            print(f'Latitude: {lat}, Longitude: {lon}')
