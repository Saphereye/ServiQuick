from kivy.app import App
from kivy_garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton, ToggleButtonBehavior
from kivymd.uix.label import MDIcon
from kivy.graphics import Line, Color
import requests
import wrapper

# class RouteWidget(Widget):
#     def __init__(self, **kwargs):
#         super(RouteWidget, self).__init__(**kwargs)
#         self.route_coordinates = []

#     def set_route_coordinates(self, coordinates):
#         self.route_coordinates = coordinates

#     def draw_route(self):
#         with self.canvas:
#             Color(0, 1, 1, 1)
#             Line(points=self.route_coordinates, width=4, joint_presicion=100)

class MapWithRoute(BoxLayout):
    def __init__(self, **kwargs):
        super(MapWithRoute, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.latlong = wrapper.get_lat_long()

        # Initialize the map
        (lat, lon) = (float(i) for i in self.latlong.split(','))
        self.mapview = MapView(zoom=10, lat=lat, lon=lon)  # Hyderabad coordinates
        self.add_widget(self.mapview)

        # Add buttons for Hospital, Firefighter, and Police
        self.add_buttons()

        # Initialize route data with Hospital as the initial service
        self.current_service = wrapper.Service.HOSPITAL
        self.update_route()

    def add_buttons(self):
        # Create buttons for Hospital, Firefighter, and Police
        # background_normal='./Flag_of_the_Red_Cross.svg.png'
        self.hospital_button = ToggleButton(text="🏥", font_name="seguiemj", font_size='36sp', color='red')
        self.firefighter_button = ToggleButton(text="🔥", font_name="seguiemj", font_size='36sp')
        self.police_button = ToggleButton(text="👮", font_name="seguiemj", font_size='36sp')

        # Bind button press events to corresponding functions
        self.hospital_button.bind(on_release=self.on_hospital_button_press)
        self.firefighter_button.bind(on_release=self.on_firefighter_button_press)
        self.police_button.bind(on_release=self.on_police_button_press)

        self.hospital_button.state = 'down'

        # Add buttons to the layout
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        button_layout.add_widget(self.hospital_button)
        button_layout.add_widget(self.firefighter_button)
        button_layout.add_widget(self.police_button)
        self.add_widget(button_layout)

    def on_hospital_button_press(self, instance):
        self.current_service = wrapper.Service.HOSPITAL
        self.hospital_button.state = 'down'
        self.firefighter_button.state = 'normal'
        self.police_button.state = 'normal'
        self.update_route()

    def on_firefighter_button_press(self, instance):
        self.current_service = wrapper.Service.FIRE_STATION
        self.hospital_button.state = 'normal'
        self.firefighter_button.state = 'down'
        self.police_button.state = 'normal'
        self.update_route()

    def on_police_button_press(self, instance):
        self.current_service = wrapper.Service.POLICE
        self.hospital_button.state = 'normal'
        self.firefighter_button.state = 'normal'
        self.police_button.state = 'down'
        self.update_route()

    def update_route(self):
        self.draw_route(wrapper.get_route(self.latlong, self.current_service))

    def draw_route(self, route_coordinates):
        # Create a new marker layer
        layer = ClusteredMarkerLayer()

        print(route_coordinates)

        # Add markers for the route
        for location in route_coordinates:
            layer.add_marker(lon=location[0], lat=location[1], cls=MapMarker)

        # Add the marker layer to the map
        self.mapview.add_widget(layer)

        # with self.canvas:
        #     Color( 0, 1 , 1 , 1)
        #     Line(points=route_coordinates , width=10 , joint_presicion = 100)

        # # Clear existing route if any
        # self.mapview.remove_widget(self.route_line)

        # Create a Line object to draw the route
        # self.route_line = Line(points=[], width=4)

        # # Convert geographical coordinates to screen coordinates and add to the Line
        # for lat, lon in route_coordinates:
        #     screen_x, screen_y = self.mapview.get_window_xy_from(lat, lon, self.mapview.zoom)
        #     self.route_line.points.extend([screen_x, screen_y])

        # # Add the Line to the map
        # self.mapview.add_widget(self.route_line)

        #  # Create a Line object to draw the route
        # line = Line(points=[], width=4)
        # self.mapview.add_widget(line)

        # # Convert geographical coordinates to screen coordinates
        # screen_coordinates = []
        # for lat, lon in route_coordinates:
        #     screen_x, screen_y = self.mapview.get_window_xy_from(lat, lon)
        #     screen_coordinates.extend([screen_x, screen_y])

        # # Set the Line's points to draw the route
        # line.points = screen_coordinates



class MapApp(App):
    def build(self):
        return MapWithRoute()

if __name__ == '__main__':
    MapApp().run()
