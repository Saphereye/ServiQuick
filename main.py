from kivy.app import App
from kivy_garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton, ToggleButtonBehavior
from kivymd.uix.label import MDIcon
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line, Color
from kivy.uix.label import Label

import requests
import wrapper
from enum import Enum

from helper import *

class DisplayOption(Enum):
    ClosestService = 1
    PathToService = 2

class MapWithRoute(FloatLayout):
    def __init__(self, **kwargs):
        super(MapWithRoute, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.latlong = wrapper.get_lat_long()
        self.layer = None

        # Initialize the map
        (lat, lon) = (float(i) for i in self.latlong.split(','))
        # Hyderabad coordinates
        self.mapview = MapView(zoom=100, lat=lat, lon=lon)
        self.add_widget(self.mapview)

        # Add buttons for Hospital, Firefighter, and Police
        self.add_buttons()

        # Initialize route data with Hospital as the initial service
        self.current_service = wrapper.Service.HOSPITAL
        self.update_route()

    def add_buttons(self):
        # Create buttons for Hospital, Firefighter, and Police
        # background_normal='./Flag_of_the_Red_Cross.svg.png'
        self.hospital_button = ToggleButton(
            text="🏥", font_name="seguiemj", font_size='36sp')
        self.firefighter_button = ToggleButton(
            text="🔥", font_name="seguiemj", font_size='36sp')
        self.police_button = ToggleButton(
            text="👮", font_name="seguiemj", font_size='36sp')

        # Bind button press events to corresponding functions
        self.hospital_button.bind(on_release=self.on_hospital_button_press)
        self.firefighter_button.bind(
            on_release=self.on_firefighter_button_press)
        self.police_button.bind(on_release=self.on_police_button_press)

        # self.hospital_button.state = 'down'

        # Add buttons to the layout
        button_layout = BoxLayout(orientation='horizontal', size_hint=(0.8, 0.2), padding = 10)
        # self.label = Label(text="Top Label", size_hint=(0, 10))
        # button_layout.add_widget(self.label)
        button_layout.add_widget(self.hospital_button)
        button_layout.add_widget(self.firefighter_button)
        button_layout.add_widget(self.police_button)
        # self.label = Label(text="Top Label", size_hint=(5, 10))
        # button_layout.add_widget(self.label)
        self.add_widget(button_layout)

    def on_hospital_button_press(self, instance):
        self.current_service = wrapper.Service.HOSPITAL
        # self.hospital_button.state = 'down'
        # self.firefighter_button.state = 'normal'
        # self.police_button.state = 'normal'
        self.update_route()

    def on_firefighter_button_press(self, instance):
        self.current_service = wrapper.Service.FIRE_STATION
        # self.hospital_button.state = 'normal'
        # self.firefighter_button.state = 'down'
        # self.police_button.state = 'normal'
        self.update_route()

    def on_police_button_press(self, instance):
        self.current_service = wrapper.Service.POLICE
        # self.hospital_button.state = 'normal'
        # self.firefighter_button.state = 'normal'
        # self.police_button.state = 'down'
        self.update_route()

    def update_route(self):
        self.reset_map()
        self.draw_route(wrapper.get_route(
            self.latlong, self.current_service), DisplayOption.PathToService)

    def reset_map(self):
        # self.clear_widgets()
        # self.remove_widget(self.mapview)
        # (lat, lon) = (float(i) for i in self.latlong.split(','))
        # self.mapview = MapView(zoom=20, lat=lat, lon=lon)  # Hyderabad coordinates
        # self.add_widget(self.mapview)
        pass

    def draw_route(self, route_coordinates, display_option: DisplayOption):
        # engine.say(f"Showing the fastest route")
        # engine.runAndWait()
        speak(f"Showing the fastest route")
        match display_option:
            case DisplayOption.PathToService:
                if self.layer:
                    self.mapview.remove_widget(self.layer)
                # Create a new marker layer
                self.layer = ClusteredMarkerLayer()

                # print(route_coordinates)

                # Add markers for the route
                for location in route_coordinates[1:-1]:
                    custom_icon = "circle.png"
                    self.layer.add_marker(lon=location[0], lat=location[1], cls=MapMarker, options={
                        'source': custom_icon,
                    })

                self.layer.add_marker(
                    lon=route_coordinates[0][0], lat=route_coordinates[0][1], cls=MapMarker)
                self.layer.add_marker(
                    lon=route_coordinates[-1][0], lat=route_coordinates[-1][1], cls=MapMarker)

                # Add the marker self.layer to the map
                self.mapview.add_widget(self.layer)
            case DisplayOption.ClosestService:
                pass


class MapApp(App):
    def build(self):
        return MapWithRoute()


if __name__ == '__main__':
    MapApp().run()
