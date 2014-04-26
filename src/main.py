from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, \
    ReferenceListProperty, ListProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.graphics import Color, Line, Rectangle, Rotate, PushMatrix, PopMatrix
from random import randint
import math

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
        self.velocity_y = 0

    def die_anim(self, dt):
        if self.pos[1] > 20:
            self.pos[1] -= 5
        else:
            return False

    def die(self):
        Clock.schedule_interval(self.die_anim, 1./60)


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
        if self.x + self.size[0] < self.game.bird.pos[0] and not self.passed \
            and self.type == 'up':
            self.game.points += 1
            self.passed = True


class SillyGame(Widget):
    bird = ObjectProperty(None)
    columns = ListProperty([])
    points = NumericProperty(0)
    gap = 50
    # status
    # 'run' game is running
    # 'stop' game is stopped 
    # 'pause' game is paused   
    status = ''

    def __init__(self):
        super(SillyGame, self).__init__()

    def update(self, dt):
        if self.status == 'stop' or self.status == 'pause':
            return
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

    def collide(self):
        self.finish()

    def check_collide(self, c):
        if self.bird.collide_widget(c):
            self.collide()


    def new_column(self, dt):
        if self.status == 'stop' or self.status == 'pause':
            return
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
        if touch.pos[0] < 100:
            self.toggle_pause()
            return
        if self.status == 'stop':
            self.start()
            return
        self.bird.reset()

    def finish(self):
        self.bird.die()
        self.stop()

    def toggle_pause(self):
        if self.status == 'pause':
            self.status = 'run'
        elif self.status == 'run':
            self.status = 'pause'

    def stop(self):
        self.status = 'stop'

    def start(self):
        self.status = 'run'
        self.restart()
        Clock.unschedule(self.update)
        Clock.unschedule(self.new_column)        
        Clock.schedule_interval(self.update, 1./60)
        Clock.schedule_interval(self.new_column, 1.7)

    def restart(self):
        self.points = 0
        for c in self.columns:
            self.remove_widget(c)
            del c
        self.columns = []
        self.remove_widget(self.bird)
        self.bird = SillyBird()
        self.add_widget(self.bird)
        self.bird.pos = [20, 150]


class SillyApp(App):
    def build(self):
        game = SillyGame()
        game.start()
        return game


if __name__ == '__main__':
    SillyApp().run()
