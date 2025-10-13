from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, ListProperty, NumericProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle, StencilPush, StencilUse, StencilUnUse, StencilPop
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.slider import MDSlider
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.snackbar import Snackbar

import socket
import threading
import random
import math

# ------------------- Comunicação com ESP  -------------------
class ComunicacaoESP:
    def __init__(self, ip="192.168.4.1", porta=8080):
        self.ip = ip
        self.porta = porta
        self.sock = None
        self.conectado = False

    def conectar(self):
        try:
            print(f"[ESP] Simulação de conexão a {self.ip}:{self.porta}")
            self.conectado = True
        except Exception as e:
            print(f"[ESP] Erro ao conectar: {e}")
            self.conectado = False

    def enviar_pares(self, **pares):
        msg = "".join(f"{k}:{v};" for k, v in pares.items()) + "\n"
        print(f"[DEBUG] Mensagem que seria enviada: {msg.strip()}")
        if not self.conectado:
            print("[ESP] Não conectado, mensagem não enviada.")

# ------------------- Widget de mapa animado -------------------
class MapWidget(Widget):
    robot_pos = ListProperty([0, 0])
    robot_angle = NumericProperty(0)
    path_points = ListProperty([])
    obstacles = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(250)
        Clock.schedule_once(self.setup, 0.1)
        self.bind(pos=self.redraw, size=self.redraw)

    def setup(self, *_):
        # Espera até o widget ter dimensões válidas
        if self.width <= 100 or self.height <= 100:
            Clock.schedule_once(self.setup, 0.1)
            return

        self.robot_pos = [self.center_x, self.center_y]
        self.path_points = [self.robot_pos[:]]
        self.generate_obstacles()
        Clock.schedule_interval(self.update_robot, 0.05)

    def generate_obstacles(self):
        # Gera obstáculos dentro dos limites válidos do widget
        if self.width <= 100 or self.height <= 100:
            return  # evita erro se chamado muito cedo

        self.obstacles = [
            [random.randint(int(self.x + 40), int(self.right - 40)),
             random.randint(int(self.y + 40), int(self.top - 40))]
            for _ in range(5)
        ]

    def update_robot(self, dt):
        # Movimento circular suave dentro do card
        self.robot_angle += 2
        rad = math.radians(self.robot_angle)
        cx, cy = self.center
        w, h = self.width * 0.35, self.height * 0.25
        self.robot_pos = [cx + w * math.cos(rad), cy + h * math.sin(rad)]
        self.path_points.append(self.robot_pos[:])

        # Detecção simples de obstáculos
        for obs in self.obstacles[:]:
            if math.dist(self.robot_pos, obs) < 25:
                print("[MAPA] Obstáculo detectado em:", obs)
                self.obstacles.remove(obs)

        self.redraw()

    def redraw(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Limita desenho ao card (Stencil)
            StencilPush()
            Rectangle(pos=self.pos, size=self.size)
            StencilUse()

            # Fundo
            Color(0.95, 0.95, 0.95)
            Rectangle(pos=self.pos, size=self.size)

            # Caminho
            Color(0, 0, 0, 1)
            if len(self.path_points) > 1:
                Line(points=sum(self.path_points, []), width=2)

            # Obstáculos
            Color(1, 0, 0, 1)
            for x, y in self.obstacles:
                Rectangle(pos=(x - 5, y - 5), size=(10, 10))

            # Robô
            Color(0, 0, 1, 1)
            Rectangle(pos=(self.robot_pos[0]-8, self.robot_pos[1]-8), size=(16, 16))

            # Finaliza recorte
            StencilUnUse()
            StencilPop()

# ------------------- Card expansível com mapa -------------------
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
        self.btn_expand = MDIconButton(icon="arrow-expand-down")
        self.btn_expand.bind(on_release=self.toggle_expand)
        header.add_widget(self.btn_expand)
        self.add_widget(header)

        # Widget do mapa
        self.map_widget = MapWidget()
        self.add_widget(self.map_widget)

    def toggle_expand(self, *args):
        if not self.expanded:
            Animation(height=Window.height * 0.6, d=0.4, t="out_quad").start(self)
            self.btn_expand.icon = "arrow-collapse-up"
            self.expanded = True
        else:
            Animation(height=dp(150), d=0.4, t="out_quad").start(self)
            self.btn_expand.icon = "arrow-expand-down"
            self.expanded = False

# ------------------- App principal -------------------
class AppRoboAspirador(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"
        Window.size = (480, 720)

        screen = MDScreen(md_bg_color=(0.95, 0.95, 0.95, 1))
        self.esp = ComunicacaoESP()
        threading.Thread(target=self.esp.conectar, daemon=True).start()

        layout = MDBoxLayout(orientation="vertical", spacing=dp(15), padding=dp(20))

        # Título
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

        # Controle de velocidade
        card_vel = MDCard(orientation="vertical", padding=dp(15),
                          radius=[20, 20, 20, 20], elevation=6)
        self.vel_label = MDLabel(text="Velocidade: 120", halign="center", font_style="H6")
        self.slider = MDSlider(min=0, max=255, value=120, size_hint_x=0.9)
        self.slider.bind(value=self.on_slider_change)
        card_vel.add_widget(self.vel_label)
        card_vel.add_widget(self.slider)
        layout.add_widget(card_vel)

        # Botão ligar/desligar
        self.toggle_btn = MDRaisedButton(
            text="Ligar", md_bg_color=(0.2, 0.7, 0.3, 1),
            text_color=(1, 1, 1, 1), size_hint_y=None, height=dp(50)
        )
        self.toggle_btn.bind(on_release=self.toggle_motor)
        layout.add_widget(self.toggle_btn)

        # Card motor de sucção
        card_motor = MDCard(orientation="horizontal", padding=dp(15),
                            radius=[20, 20, 20, 20], elevation=6,
                            size_hint_y=None, height=dp(60))
        card_motor.add_widget(MDLabel(text="Motor de Sucção", halign="center", font_style="H6"))
        self.suc_switch = MDSwitch(pos_hint={"center_y": 0.5})
        self.suc_switch.bind(active=self.toggle_suction)
        card_motor.add_widget(self.suc_switch)
        layout.add_widget(card_motor)

        # Mapa do ambiente
        layout.add_widget(MapCard())

        screen.add_widget(layout)
        return screen

    def on_slider_change(self, instance, value):
        self.vel_label.text = f"Velocidade: {int(value)}"
        self.esp.enviar_pares(velocidade=int(value))

    def toggle_motor(self, instance):
        if self.toggle_btn.text == "Ligar":
            self.toggle_btn.text = "Desligar"
            self.toggle_btn.md_bg_color = (0.8, 0.2, 0.2, 1)
            Snackbar(text="Robô Aspirador LIGADO").open()
            self.esp.enviar_pares(andarAutonomo=1)
        else:
            self.toggle_btn.text = "Ligar"
            self.toggle_btn.md_bg_color = (0.2, 0.7, 0.3, 1)
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


