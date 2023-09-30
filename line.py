from kivy_garden.mapview import MapView
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Line
from kivy.app import App

class MyMapView(MapView):
    def do_update(self, dt):  # this over-rides the do_update() method of MapView
        super(MyMapView, self).do_update(dt)
        self.draw_lines()

    def draw_lines(self):
        points = [[self.longitude, self.latitude], [self.longitude + 0.01, self.latitude + 0.01]]  # get the points for the lines
        lines = Line()
        lines.points = points
        lines.width = 2
        if self.grp is not None:
            # just update the group with updated lines lines
            self.grp.clear()
            self.grp.add(lines)
        else:
            with self.canvas.after:
                #  create the group and add the lines
                Color(1,0,0,1)  # line color
                self.grp = InstructionGroup()
                self.grp.add(lines)

class MyApp(App):
    def build(self):
        return MyMapView(zoom=11, lat=50.6394, lon=3.057)

if __name__ == '__main__':
    MyApp().run()
