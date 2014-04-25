from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, \
    ReferenceListProperty, ListProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.graphics import Color, Line, Rectangle, Rotate, PushMatrix, PopMatrix
import math
from random import randint

class SillyBird(Widget):
    x_step = 1
    x_pos = NumericProperty(-3.00)
    velocity_y = NumericProperty(0.00)
    velocity = ReferenceListProperty(velocity_y)
    points = []
    rotation = NumericProperty(10)

    def function(self, x):
        return x * x * (-0.05)

    def next_position(self):
        self.velocity_y = self.function(self.x_pos + self.x_step) - \
            self.function(self.x_pos) 
        self.x_pos = self.x_step + self.x_pos

    def move(self):
        self.next_position()
        self.pos = Vector([0, self.velocity[0]]) + self.pos
        rad = math.atan(self.velocity_y / self.x_step)
        self.rotation = math.degrees(rad)

    def reset(self):
        self.x_pos = -30
        self.velocity_y = 00


class SillyColumn(Widget):
    pos_x = NumericProperty(0)
    pos_y = NumericProperty(0)
    col_height = NumericProperty(0)
    type = StringProperty()
    passed = False

    def __init__(self, pos_y, height, game, type):
        super(SillyColumn, self).__init__()
        self.type = type
        self.pos_y = pos_y
        self.col_height = height
        self.pos_x = game.width
        self.game = game

    def update(self):
        PushMatrix()
        self.pos_x -= 2
        PopMatrix()
        self.check_passed()

    def check_passed(self):
        if self.x + self.size[0] < self.game.bird.pos[0] and not self.passed:
            self.game.points += 0.5
            self.passed = True


class SillyGame(Widget):
    bird = ObjectProperty(None)
    columns = ListProperty([])
    points = NumericProperty(0)
    gap = 50
    
    def __init__(self):
        super(SillyGame, self).__init__()
        self.bird = SillyBird()
        self.add_widget(self.bird)
        self.bird.pos = [20, 150]

    def update(self, dt):
        self.bird.move()
        if len(self.columns) > 0:
            if self.columns[0].pos_x < -50:
                self.remove_widget(self.columns[0])
                self.remove_widget(self.columns[1])
                del self.columns[0]
                del self.columns[0]
        for c in self.columns:
            c.update() 
            self.check_collide(c)
    # TODO
    def collide(self):
        print "Bird collided"

    def check_collide(self, c):
        if self.bird.collide_widget(c):
            self.collide()


    def new_column(self, dt):
        mid = randint(self.height/2 - self.gap, \
            self.height/2 + self.gap)
        height = mid - self.gap/2
        y_pos = height + 2*self.gap
        column_bot = SillyColumn(0, height, self, 'up')
        column_top = SillyColumn(y_pos, self.height - height, self, 'down')
        self.add_widget(column_bot)
        self.add_widget(column_top)
        self.columns.append(column_bot)
        self.columns.append(column_top)

    def on_touch_down(self, touch):
        self.bird.reset()


class SillyApp(App):
    def build(self):
        game = SillyGame()
        Clock.schedule_interval(game.update, 1./60)
        Clock.schedule_interval(game.new_column, 1.7)
        return game


if __name__ == '__main__':
    SillyApp().run()
