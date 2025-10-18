from kivymd.app import MDApp
from gui import AppGUI

class MobileApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        gui = AppGUI()
        return gui.build_gui()


MobileApp().run()