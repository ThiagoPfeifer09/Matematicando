from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager


# --- Classe da Aba individual ---
class AbaJogos(MDBoxLayout, MDTabsBase):
    def __init__(self, titulo, jogos, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(10), padding=dp(10), **kwargs)

        self.add_widget(MDLabel(text=titulo, halign="center", font_style="H6"))

        # Adiciona os botões de cada jogo
        for nome, callback in jogos:
            self.add_widget(
                MDRaisedButton(
                    text=nome,
                    size_hint=(0.9, None),
                    height=dp(45),
                    pos_hint={"center_x": 0.5},
                    on_release=callback,
                )
            )


# --- Tela principal com abas ---
class TelaJogos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tabs = MDTabs()
        self.add_widget(self.tabs)

        # Define jogos por categoria
        jogos_primario = [
            ("Desafio das Raízes", lambda x: print("Primário - Raízes")),
            ("Cruzadinha Matemática", lambda x: print("Primário - Cruzadinha")),
        ]
        jogos_fundamental = [
            ("Frações Interativas", lambda x: print("Fundamental - Frações")),
            ("Equações de 1º Grau", lambda x: print("Fundamental - Equações")),
        ]
        jogos_medio = [
            ("Funções Quadráticas", lambda x: print("Médio - Funções")),
            ("Desafios de Álgebra", lambda x: print("Médio - Álgebra")),
        ]

        # Cria as abas
        self.tabs.add_widget(AbaJogos(text="Primário", titulo="Jogos do Fundamental I", jogos=jogos_primario))
        self.tabs.add_widget(AbaJogos(text="Fundamental", titulo="Jogos do Fundamental II", jogos=jogos_fundamental))
        self.tabs.add_widget(AbaJogos(text="Médio", titulo="Jogos do Ensino Médio", jogos=jogos_medio))


# --- App principal ---
class TesteApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TelaJogos(name="aba_jogos"))
        return sm


TesteApp().run()
