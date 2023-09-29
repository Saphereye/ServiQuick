from kivy.app import App
from kivy_garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer
from kivy.uix.boxlayout import BoxLayout
import requests
import wrapper

class MapWithRoute(BoxLayout):
    def __init__(self, **kwargs):
        super(MapWithRoute, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Initialize the map
        (lat, lon) = (float(i) for i in wrapper.get_lat_long().split(','))
        self.mapview = MapView(zoom=10, lat=lat, lon=lon)  # Hyderabad coordinates
        self.add_widget(self.mapview)

        # Request route information from HERE API
        route_data = self.get_route_data()
        if route_data:
            # Extract coordinates from the route data (e.g., list of latitudes and longitudes)
            route_coordinates = [(lat, lon) for lon, lat in route_data]

            # Draw the route on the map
            self.draw_route(route_coordinates)

    def get_route_data(self):
        # Make a request to HERE API to retrieve route data
        # Replace with your HERE API request logic and URL
        waypoint0 = '51.5074,-0.1278'  # London coordinates as the starting point
        waypoint1 = wrapper.get_lat_long()  # Destination coordinates
        mode = 'fastest;car;traffic:disabled'
        app_id = 'OnyJ5cxLBpW9KOhx3wCW'
        app_code = 'iWrpAat8eDeNt2CqqWtw6bQPweqd2xqCNk7wh9gR_p8'
    
        api_url = f'https://router.hereapi.com/v8/routes?transportMode=car&origin={waypoint0}&destination={waypoint1}&return=summary&apikey={app_code}'
        print(f"{api_url=}")

        response = requests.get(api_url)
        print(f"{response.json()=}")

        if response.status_code == 200:
            output = []
            for i in range(len(response.json()['routes'][0]['sections'])):
                output.append((
                    response.json()['routes'][0]['sections'][i]['arrival']['place']['location']['lat'],
                    response.json()['routes'][0]['sections'][i]['arrival']['place']['location']['lng']
                ))
            route_data = output
            # route_data = [(i['lat'], i['lng']) for i in response.json()['sections']['arrival']['location']]
            print(f"{route_data=}")
            return route_data
        else:
            print('Failed to retrieve route data.')
            return None

    def draw_route(self, route_coordinates):
        # # Draw the route using a Polyline
        # polyline = MapMarkerPopup()
        # polyline.source = './marker.png'  # You can use your own custom polyline image
        # polyline.add_polyline(route_coordinates)
        # self.mapview.add_marker(polyline)
        layer = ClusteredMarkerLayer()
        # print(help(layer.add_marker))
        for lat, lon in route_coordinates:
            layer.add_marker(lon=lon, lat=lat, cls=MapMarker)
        self.mapview.add_widget(layer)

class MapApp(App):
    def build(self):
        return MapWithRoute()

if __name__ == '__main__':
    MapApp().run()
