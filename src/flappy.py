from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, \
    ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.graphics import Color, Line
import math

class FlappyBird(Widget):
    x_step = 1
    x_pos = NumericProperty(-3.00)
    velocity_y = NumericProperty(0.00)
    velocity = ReferenceListProperty(velocity_y)
    points = []

    def function(self, x):
        return x * x * (-0.05)

    def next_position(self):
        self.velocity_y = self.function(self.x_pos + 1) - \
            self.function(self.x_pos)
        self.x_pos = 1 + self.x_pos

    def move(self):
        self.next_position()
        self.pos = Vector([0, self.velocity[0]]) + self.pos

    def reset(self):
        self.x_pos = -30
        self.velocity_y = 0

class FlappyColumn(Widget):
    gap = NumericProperty(80)
    max_c = NumericProperty(0)
    min_c = NumericProperty(0)
    position_x = NumericProperty(0)
    position_y = NumericProperty(0)
    position = ReferenceListProperty(position_x, position_y)

    def new(self):
        print "New column"

    def update(self):
        print "update"

class FlappyGame(Widget):
    bird = ObjectProperty(None)
    columns = ListProperty(None)

    def update(self, dt):
        self.bird.move()

    def new_column(self, dt):
        pass

    def on_touch_down(self, touch):
        self.bird.reset()

class FlappyApp(App):
    def build(self):
        game = FlappyGame()
        Clock.schedule_interval(game.update, 1/60)
        Clock.schedule_interval(game.new_column, 2)
        return game

if __name__ == '__main__':
    FlappyApp().run()