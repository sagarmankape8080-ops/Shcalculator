from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.animation import Animation
from datetime import datetime
import os

# Splash Screen
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.05, 0.05, 0.07, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=50)

        self.logo = Image(
            source='Sm.png',
            size_hint=(None, None),
            size=(180, 180),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        if os.path.exists("Sm.png"):
            self.logo.opacity = 0
            layout.add_widget(self.logo)

        self.add_widget(layout)

    def on_enter(self):
        if os.path.exists("Sm.png"):
            anim = Animation(opacity=1, duration=1.2, t='in_out_quad')
            anim.bind(on_complete=self.start_clock)
            anim.start(self.logo)
        else:
            self.switch_to_main(0)

    def start_clock(self, *args):
        Clock.schedule_once(self.switch_to_main, 0.5)

    def switch_to_main(self, dt):
        self.manager.current = "main"

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# Main Screen
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.1, 0.12, 0.16, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        main_layout = BoxLayout(
            orientation='vertical',
            spacing=25,
            padding=[30, 40, 30, 40]
        )

        title = Label(
            text="Age Calculator",
            font_size=28,
            bold=True,
            size_hint_y=None,
            height=40,
            color=(1, 1, 1, 1)
        )
        main_layout.add_widget(title)

        input_layout = BoxLayout(
            orientation='horizontal',
            spacing=15,
            size_hint_y=None,
            height=55
        )

        self.day_in = TextInput(
            hint_text="Day",
            multiline=False,
            input_filter='int'
        )

        self.month_in = TextInput(
            hint_text="Month",
            multiline=False,
            input_filter='int'
        )

        self.year_in = TextInput(
            hint_text="Year",
            multiline=False,
            input_filter='int'
        )

        input_layout.add_widget(self.day_in)
        input_layout.add_widget(self.month_in)
        input_layout.add_widget(self.year_in)

        main_layout.add_widget(input_layout)

        btn = Button(
            text="Calculate Age",
            font_size=20,
            size_hint_y=None,
            height=55,
            background_normal='',
            background_color=(0, 0.75, 0.45, 1)
        )

        btn.bind(on_press=self.calculate_age)
        main_layout.add_widget(btn)

        self.result_lbl = Label(
            text="Enter details above",
            font_size=22,
            markup=True
        )

        main_layout.add_widget(self.result_lbl)

        self.add_widget(main_layout)

    def calculate_age(self, instance):
        try:
            day = int(self.day_in.text)
            month = int(self.month_in.text)
            year = int(self.year_in.text)

            dob = datetime(year, month, day)
            today = datetime.now()

            age = today.year - dob.year

            if (today.month, today.day) < (dob.month, dob.day):
                age -= 1

            self.result_lbl.text = (
                f"🎉 [color=#00ff99][b]Age: {age} Years[/b][/color]"
            )

        except ValueError:
            self.result_lbl.text = (
                "[color=#ff4444]Please enter a valid date![/color]"
            )

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# App
class SrmApp(App):
    def build(self):
        sm = ScreenManager(
            transition=FadeTransition(duration=0.6)
        )

        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(name="main"))

        return sm


if __name__ == "__main__":
    SrmApp().run()