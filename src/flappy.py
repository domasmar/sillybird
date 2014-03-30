from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, \
    ReferenceListProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.graphics import Color, Line, Rectangle
import math
from random import randint

class FlappyBird(Widget):
    x_step = 1
    x_pos = NumericProperty(-3.00)
    velocity_y = NumericProperty(0.00)
    velocity = ReferenceListProperty(velocity_y)
    points = []

    def function(self, x):
        return x * x * (-0.1)

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
    gap = 100
    max_c = 0
    min_c = 0
    top_column_position = []
    bottom_column_position = []

    def __init__(self, game):
        super(FlappyColumn, self).__init__()
        self.game = game
        with self.game.canvas:
            Color(randint(10, 100) / 100.0, randint(10, 100) / 100.0, randint(10, 100) / 100.0)
            self.rect_t = Rectangle(pos=[0,0], size= [30, self.game.height])
            self.rect_b = Rectangle(pos=[0,0], size= [30, self.game.height])

    def repaint(self):
        with self.game.canvas:
            Color(.98, .98, .0)
            self.rect_t.pos = self.top_column_position
            self.rect_b.pos = self.bottom_column_position

    def new(self, diff):
        self.min_c = randint(self.game.height/2 - diff/2, self.game.height/2 + diff/2)
        self.max_c = self.min_c + self.gap
        self.top_column_position = [self.game.width, self.max_c]
        self.bottom_column_position = [self.game.width, self.min_c - self.game.height]
        self.repaint()

    def update(self):
        self.top_column_position[0] -= 3
        self.bottom_column_position[0] -= 3
        self.repaint()
        self.collision()

    def collision(self):
        if self.game.collide_widget(self.game.bird) or self.game.collide_widget(self.game.bird):
            pass
            # print "Kolizija"

class FlappyColumns():
    columns = []

    def __init__(self, game):
        self.game = game

    def new(self, point):
        column = FlappyColumn(self.game)
        column.new(point)
        self.columns.append(column)

    def update(self):
        for c in self.columns:
            c.update() 


class FlappyGame(Widget):
    bird = ObjectProperty(None)
    points = NumericProperty(0)

    def __init__(self):
        super(FlappyGame, self).__init__()
        self.columns = FlappyColumns(self)

    def update(self, dt):
        self.bird.move()
        self.columns.update()

    def new_column(self, dt):
        self.columns.new(self.points * 1.1)

    def on_touch_down(self, touch):
        self.bird.reset()

class FlappyApp(App):
    def build(self):
        game = FlappyGame()
        Clock.schedule_interval(game.update, 1/60)
        Clock.schedule_interval(game.new_column, 1.5)
        return game

if __name__ == '__main__':
    FlappyApp().run()