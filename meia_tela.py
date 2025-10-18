from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, SlideTransition, ScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivymd.app import MDApp
from functools import partial
from kivymd.uix.button import MDIconButton
from kivy.core.text import LabelBase

# =================== TELA PRINCIPAL ===================
class MeiaTela(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Fundo
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        layout.add_widget(fundo)

        # Título
        self.title_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(self.title_label)
        self.digita_texto(self.title_label, "OPERAÇÕES")

        self.back_button = MDIconButton(
            icon='arrow-left',
            pos_hint={'x': 0, 'top': 1},
            on_release=lambda x: self.voltar("conteudos")
        )
        layout.add_widget(self.back_button)

        # Bonequinho
        boneco = Image(
            source="boneco.png",
            size_hint=(0.25, 0.35),
            pos_hint={"center_x": 0.5, "center_y": 0.65}
        )
        layout.add_widget(boneco)

        # --- BOTÕES CENTRAIS ---
        # Posições centralizadas verticalmente
        btn_representacoes = self.create_card_button(
            "Representações",
            0.3, 0.35,
            lambda: self.ir_para("representacoes")
        )
        btn_definicoes = self.create_card_button(
            "Definições",
            0.3, 0.2,
            lambda: self.ir_para("definicoes")
        )

        layout.add_widget(btn_representacoes)
        layout.add_widget(btn_definicoes)

        self.add_widget(layout)

    # --- Funções auxiliares ---
    def digita_texto(self, label, texto, i=0):
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i+1), 0.05)

    def tocar_som_giz(self):
        som = SoundLoader.load("giz_riscando.wav")
        if som:
            som.play()

    def create_card_button(self, text, x, y, callback):
        card = MDCard(
            size_hint=(0.4, 0.08),
            pos_hint={"x": x, "y": y},
            md_bg_color=(0.2, 0.2, 0.6, 0.85),
            radius=[20],
            elevation=10,
            ripple_behavior=True
        )
        label = MDLabel(
            text=text,
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size="18sp"
        )
        card.add_widget(label)
        card.on_release = lambda *a: [self.tocar_som_giz(), callback()]
        return card

    def ir_para(self, tela_nome):
        self.manager.transition = SlideTransition(direction="left", duration=0.4)
        self.manager.current = tela_nome

    def voltar(self, tela_nome):
        self.manager.transition = SlideTransition(direction="left", duration=0.4)
        self.manager.current = tela_nome

# =================== TELA DEFINIÇÕES ===================
class DefinicoesTela(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Fundo
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        layout.add_widget(fundo)

        # Título
        self.title_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(self.title_label)
        self.digita_texto(self.title_label, "DEFINIÇÕES OPERAÇÕES")

        # Lista de imagens (uma para cada operação)
        imagens = [
            "img_adicao.jpeg",
            "img_subtracao.jpeg",
            "img_multiplicacao.jpeg",
            "img_divisao.jpeg"
        ]

        pos_y = [0.68, 0.68, 0.30, 0.30]
        pos_x = [0.26, 0.74, 0.26, 0.74]

        for i, img in enumerate(imagens):
            card = MDCard(
                size_hint=(0.45, 0.32),
                pos_hint={"center_x": pos_x[i], "center_y": pos_y[i]},
                radius=[20],
                elevation=10,
                orientation="vertical"
            )

            # Imagem dentro do card
            card.add_widget(Image(
                source=img,
                allow_stretch=True,
                keep_ratio=False
            ))

            layout.add_widget(card)

        # Botão voltar
        btn_voltar = MDCard(
            size_hint=(0.18, 0.06),
            pos_hint={"x": 0.05, "y": 0.05},
            md_bg_color=(0.2, 0.2, 0.6, 0.85),
            radius=[20],
            elevation=10,
            ripple_behavior=True
        )
        btn_voltar.add_widget(MDLabel(
            text="Voltar",
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        ))
        btn_voltar.on_release = lambda *a: self.voltar()
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def digita_texto(self, label, texto, i=0):
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i+1), 0.05)

    def voltar(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "meia_tela"

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, SlideTransition
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, Rectangle
import random
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout


# =================== TELA REPRESENTAÇÕES ===================
class TelaRepresentacoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        layout.add_widget(fundo)

        self.title_label = MDLabel(
            text="Representações das Operações",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            size_hint=(1, None),
            height=60,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(self.title_label)

        self.card_resultado = MDCard(
            size_hint=(0.9, 0.3),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            md_bg_color=(1, 1, 1, 0.85),
            radius=[25],
            elevation=12
        )
        self.resultado_label = MDLabel(
            text="Escolha valores e operação",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="H5"
        )
        self.card_resultado.add_widget(self.resultado_label)
        layout.add_widget(self.card_resultado)

        # Label do resto (para divisão)
        self.resto_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
            size_hint=(1, None),
            height=40,
            pos_hint={"center_x": 0.5, "y": 0.48},
        )
        layout.add_widget(self.resto_label)

        # Layout sliders
        self.sliders_layout = BoxLayout(
            orientation="vertical",
            spacing=15,
            size_hint=(0.6, 0.25),
            pos_hint={"center_x": 0.5, "y": 0.2}
        )

        # Slider 1
        self.slider1 = Slider(min=1, max=20, value=1, step=1)
        self.label1 = MDLabel(
            text="Valor 1: 1",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.slider1.bind(value=lambda instance, val: self.update_label(self.label1, val, 1))
        self.sliders_layout.add_widget(self.label1)
        self.sliders_layout.add_widget(self.slider1)

        # Slider 2
        self.slider2 = Slider(min=1, max=20, value=1, step=1)
        self.label2 = MDLabel(
            text="Valor 2: 1",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.slider2.bind(value=lambda instance, val: self.update_label(self.label2, val, 2))
        self.sliders_layout.add_widget(self.label2)
        self.sliders_layout.add_widget(self.slider2)

        layout.add_widget(self.sliders_layout)

        # Botões de operação
        ops = ["+", "-", "×", "÷"]
        self.op_escolhida = "+"
        for i, op in enumerate(ops):
            btn = self.create_card_button(
            op,
            0.15 + i * 0.2,
            0.1,
            partial(self.set_op, op)
            )
        layout.add_widget(btn)

        # Botão voltar
        btn_voltar = self.create_card_button("Voltar", 0.05, 0.02, self.voltar)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)
        self.update_slider_labels()  # inicializa os nomes corretos

    def update_label(self, label, val, slider_num):
        if slider_num == 1:
            label.text = f"{self.nome1}: {int(val)}"
        else:
            label.text = f"{self.nome2}: {int(val)}"
        self.mostrar_representacao()

    def create_card_button(self, text, x, y, callback):
        card = MDCard(
            size_hint=(0.18, 0.08),
            pos_hint={"x": x, "y": y},
            md_bg_color=(0.2, 0.4, 0.9, 0.9),
            radius=[20],
            elevation=12,
            ripple_behavior=True
        )
        label = MDLabel(
            text=text,
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        card.add_widget(label)
        card.bind(on_release=lambda *a: callback())
        return card

    def set_op(self, op):
        self.op_escolhida = op
        self.update_slider_labels()
        self.mostrar_representacao()

    def update_slider_labels(self):
        """Atualiza os nomes dos sliders de acordo com a operação"""
        if self.op_escolhida == "+":
            self.nome1, self.nome2 = "Parcela 1", "Parcela 2"
        elif self.op_escolhida == "-":
            self.nome1, self.nome2 = "Minuendo", "Subtraendo"
        elif self.op_escolhida == "×":
            self.nome1, self.nome2 = "Fator 1", "Fator 2"
        elif self.op_escolhida == "÷":
            self.nome1, self.nome2 = "Dividendo", "Divisor"
        else:
            self.nome1, self.nome2 = "Valor 1", "Valor 2"

        self.label1.text = f"{self.nome1}: {int(self.slider1.value)}"
        self.label2.text = f"{self.nome2}: {int(self.slider2.value)}"

    def mostrar_representacao(self):
        v1 = int(self.slider1.value)
        v2 = int(self.slider2.value)
        op = self.op_escolhida
        self.resto_label.text = ""  # limpa o resto por padrão

        if op == "+":
            resultado = v1 + v2
        elif op == "-":
            resultado = v1 - v2
        elif op == "×":
            resultado = v1 * v2
        elif op == "÷":
            if v2 == 0:
                resultado = "Indefinido"
            else:
                quociente = v1 // v2
                resto = v1 % v2
                resultado = f"{v1} ÷ {v2} = {quociente}"
                self.resto_label.text = f"Resto: {resto}"
        else:
            resultado = "?"

        if op != "÷":
            self.resultado_label.text = f"{v1} {op} {v2} = {resultado}"
        else:
            self.resultado_label.text = resultado

    def voltar(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "meia_tela"


