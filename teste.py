from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.app import MDApp
from kivy.uix.behaviors import ButtonBehavior



# --- App base ---
class MobileApp(MDApp):
    def build(self):
        sm = ScreenManager()
        return sm


if __name__ == "__main__":
    MobileApp().run()
