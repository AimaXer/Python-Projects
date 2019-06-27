import kivy
kivy.require('1.10.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.lang import Builder

presentation = Builder.load_file('widgets2.kv')

class Widgets(Widget):
    def on_touch_down(self, touch):
        print(touch)
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        print(touch)
        touch.ud["line"].points += (touch.x, touch.y)

    def on_touch_up(self, touch):
        print("RELEASED!", touch)


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        self.add_widget(Widgets())

class main(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    main().run()