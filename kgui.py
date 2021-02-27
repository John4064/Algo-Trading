from config import *
from kivy.app import App
from kivy.uix.widget import Widget
import kivy
from kivy.graphics import Color, Ellipse
kivy.require('2.0.0')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
'''class MyPaintWidget(Widget):
    def on_touch_move(self, touch):
        with self.canvas:
            Color(0, 255,255)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
    def on_touch_down(self, touch):
        with self.canvas:
            Color(244, 255, 0)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            '''
class Controller(FloatLayout):
    '''Create a controller that receives a custom widget from the kv lang file.
    Add an action to be called from the kv lang file.
    '''
    label_wid = ObjectProperty()
    info = StringProperty()

    def do_action(self):
        self.label_wid.text = 'My label after button press'
        self.info = 'New info text'

class MyApp(App):

    def build(self):
        return Controller(info='Hello world')