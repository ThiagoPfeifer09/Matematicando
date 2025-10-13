from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.slider import MDSlider
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout

import socket
import threading

# ------------------- Comunicação com ESP -------------------
class ComunicacaoESP:
    def __init__(self, ip="192.168.4.1", porta=8080):
        self.ip = ip
        self.porta = porta
        self.sock = None
        self.conectado = False

    def conectar(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((self.ip, self.porta))
            self.conectado = True
            print(f"[ESP] Conectado ao ESP32 em {self.ip}:{self.porta}")
        except Exception as e:
            print(f"[ESP] Erro ao conectar: {e}")
            self.conectado = False

    def enviar_pares(self, **pares):
        # Monta a mensagem
        msg = "".join(f"{chave}:{valor};" for chave, valor in pares.items()) + "\n"

        # PRINT DE DEBUG sempre ativo
        print(f"[DEBUG] Mensagem que seria enviada: {msg.strip()}")

        if not self.conectado:
            print("[ESP] Não conectado, mensagem não enviada.")
            return

        try:
            self.sock.sendall(msg.encode("utf-8"))
            print(f"[ESP] Enviado: {msg.strip()}")
        except Exception as e:
            print(f"[ESP] Erro ao enviar: {e}")
            self.sock.close()
            self.conectado = False

# ------------------- Card expansível de mapa -------------------
class MapCard(MDCard):
    expanded = BooleanProperty(False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(15)
        self.size_hint_y = None
        self.height = dp(150)
        self.radius = [20, 20, 20, 20]
        self.elevation = 6
        self.md_bg_color = (0.95, 0.95, 0.95, 1)

        header = MDBoxLayout(orientation="horizontal", adaptive_height=True)
        header.add_widget(MDLabel(
            text="Mapa do Ambiente",
            halign="center",
            bold=True,
            theme_text_color="Primary"
        ))
        self.btn_expand = MDIconButton(
            icon="arrow-expand-down",
            pos_hint={"center_y": 0.5},
            theme_text_color="Primary"
        )
        self.btn_expand.bind(on_release=self.toggle_expand)
        header.add_widget(self.btn_expand)
        self.add_widget(header)

        self.map_label = MDLabel(
            text="(Mapa será exibido aqui)",
            halign="center",
            theme_text_color="Secondary"
        )
        self.add_widget(self.map_label)

    def toggle_expand(self, *args):
        if not self.expanded:
            anim = Animation(height=Window.height * 0.55, d=0.3)
            anim.start(self)
            self.btn_expand.icon = "arrow-collapse-up"
            self.expanded = True
        else:
            anim = Animation(height=dp(150), d=0.3)
            anim.start(self)
            self.btn_expand.icon = "arrow-expand-down"
            self.expanded = False

# ------------------- App ------------------- #
class AppRoboAspirador(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"

        Window.size = (480, 720)
        screen = MDScreen(md_bg_color=(0.95, 0.95, 0.95, 1))

        # Comunicação ESP
        self.esp = ComunicacaoESP()
        threading.Thread(target=self.esp.conectar, daemon=True).start()

        layout = MDBoxLayout(orientation="vertical", spacing=dp(15), padding=dp(20))

        # Título com ícone de robô
        layout.add_widget(MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
            children=[
                MDIconButton(icon="robot-vacuum", user_font_size="36sp"),
                MDLabel(text="Robô Aspirador", halign="left", font_style="H5", bold=True)
            ]
        ))

        layout.add_widget(Widget(size_hint_y=None, height=dp(2)))

        # Card de velocidade
        card_vel = MDCard(orientation="vertical", padding=dp(15), radius=[20,20,20,20], elevation=6)
        self.vel_label = MDLabel(text="Velocidade: 120", halign="center", font_style="H6")
        self.slider = MDSlider(min=0, max=255, value=120, size_hint_x=0.9)
        self.slider.bind(value=self.on_slider_change)
        card_vel.add_widget(self.vel_label)
        card_vel.add_widget(self.slider)
        layout.add_widget(card_vel)

        # Botão ligar/desligar
        self.toggle_btn = MDRaisedButton(
            text="Ligar",
            md_bg_color=(0.2,0.7,0.3,1),
            text_color=(1,1,1,1),
            size_hint_y=None,
            height=dp(50)
        )
        self.toggle_btn.bind(on_release=self.toggle_motor)
        layout.add_widget(self.toggle_btn)

        # Motor de sucção em card
        card_motor = MDCard(orientation="horizontal", padding=dp(15), radius=[20,20,20,20], elevation=6, size_hint_y=None, height=dp(60))
        card_motor.add_widget(MDLabel(text="Motor de Sucção", halign="center", font_style="H6"))
        self.suc_switch = MDSwitch(pos_hint={"center_y":0.5})
        self.suc_switch.bind(active=self.toggle_suction)
        card_motor.add_widget(self.suc_switch)
        layout.add_widget(card_motor)

        # Status bateria
        card_bat = MDCard(orientation="horizontal", padding=dp(15), radius=[20,20,20,20], elevation=6, size_hint_y=None, height=dp(100))
        card_bat.add_widget(MDIconButton(icon="battery-80", theme_text_color="Custom", text_color=(0,0.6,0,1)))
        self.bat_label = MDLabel(text="Bateria: 85%", halign="center", font_style="H6")
        card_bat.add_widget(self.bat_label)
        layout.add_widget(card_bat)

        # Parâmetros de navegação
        card_nav = MDCard(orientation="vertical", padding=dp(15), radius=[20,20,20,20], elevation=6, size_hint_y=None, height=dp(160))
        card_nav.add_widget(MDLabel(text="Parâmetros de Navegação", halign="center", bold=True, font_style="H6"))
        self.dist_text = MDTextField(hint_text="Distância mínima (cm)")
        self.ang_text = MDTextField(hint_text="Ângulo de rotação (°)")
        card_nav.add_widget(self.dist_text)
        card_nav.add_widget(self.ang_text)
        layout.add_widget(card_nav)

        # Mapa
        layout.add_widget(MapCard())

        screen.add_widget(layout)
        return screen

    # ---------------- Funções de interação ----------------
    def on_slider_change(self, instance, value):
        self.vel_label.text = f"Velocidade: {int(value)}"
        self.esp.enviar_pares(velocidade=int(value))

    def toggle_motor(self, instance):
        if self.toggle_btn.text == "Ligar":
            self.toggle_btn.text = "Desligar"
            self.toggle_btn.md_bg_color = (0.8,0.2,0.2,1)
            Snackbar(text="Robô Aspirador LIGADO").open()
            self.esp.enviar_pares(andarAutonomo=1)
        else:
            self.toggle_btn.text = "Ligar"
            self.toggle_btn.md_bg_color = (0.2,0.7,0.3,1)
            Snackbar(text="Robô Aspirador DESLIGADO").open()
            self.esp.enviar_pares(andarAutonomo=0)

    def toggle_suction(self, switch, value):
        if value:
            Snackbar(text="Motor de sucção ATIVADO").open()
            self.esp.enviar_pares(motorSucao=1)
        else:
            Snackbar(text="Motor de sucção DESATIVADO").open()
            self.esp.enviar_pares(motorSucao=0)

if __name__ == "__main__":
    AppRoboAspirador().run()
