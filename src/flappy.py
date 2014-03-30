from kivy.app import App
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock

class FlappyBird(Widget):
    position_x = NumericProperty(0)
    position_y = NumericProperty(0)

    def next_position(self):
        # -x*x * 1/4
        pass

    def move(self):
        pass

    def reset(self):
        pass

class FlappyColumn(Widget):
    def new(self):
        pass

class FlappyGame(Widget):
    bird = ObjectProperty(None)

    def update(self, dt):
        bird.move()

    def on_touch_down(self, touch):
        bird.reset()
        print self.bird.pos

class FlappyApp(App):
    def build(self):
        game = FlappyGame()
        Clock.schedule_interval(game.update, 1 / 60)
        return game

if __name__ == '__main__':
    FlappyApp().run()