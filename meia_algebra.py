from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, SlideTransition
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivymd.uix.button import MDIconButton
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivymd.uix.boxlayout import MDBoxLayout
import matplotlib.pyplot as plt
import numpy as np
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.button import MDRectangleFlatButton

LabelBase.register(name="ComicNeue", fn_regular="ComicNeue-Regular.ttf")

# =================== TELA PRINCIPAL ÁLGEBRA ===================
class AlgebraTela(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Fundo
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        layout.add_widget(fundo)

        # Título
        self.title_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            font_name="ComicNeue",
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(self.title_label)
        self.digita_texto(self.title_label, "ÁLGEBRA")

        # Botão voltar
        self.back_button = MDIconButton(
            icon='arrow-left',
            pos_hint={'x': 0, 'top': 1},
            on_release=lambda x: self.voltar("conteudos")
        )
        layout.add_widget(self.back_button)

        # Boneco
        boneco = Image(
            source="boneco.png",
            size_hint=(0.25, 0.35),
            pos_hint={"center_x": 0.5, "center_y": 0.65}
        )
        layout.add_widget(boneco)

        # Botões principais
        btn_representacoes = self.create_card_button(
            "Representações",
            0.3, 0.35,
            lambda: self.ir_para("algebra_representacoes")
        )
        btn_definicoes = self.create_card_button(
            "Definições",
            0.3, 0.2,
            lambda: self.ir_para("algebra_definicoes")
        )

        layout.add_widget(btn_representacoes)
        layout.add_widget(btn_definicoes)
        self.add_widget(layout)

    # Funções auxiliares
    def digita_texto(self, label, texto, i=0):
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i + 1), 0.05)

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
            font_size="18sp",
            font_name="ComicNeue"
        )
        card.add_widget(label)
        card.on_release = lambda *a: [self.tocar_som_giz(), callback()]
        return card

    def ir_para(self, tela_nome):
        self.manager.transition = SlideTransition(direction="left", duration=0.4)
        self.manager.current = tela_nome

    def voltar(self, tela_nome):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = tela_nome


# =================== TELA DEFINIÇÕES ÁLGEBRA ===================
class AlgebraDefinicoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        layout.add_widget(fundo)

        self.title_label = MDLabel(
            text="DEFINIÇÕES ÁLGEBRA",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            font_name="ComicNeue",
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(self.title_label)

        # Cards de exemplo — substitua com imagens de conceitos algébricos
        imagens = [
            "img_variaveis.png",
            "img_expressao.png",
            "img_equacao.png",
            "img_termos.png"
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
            card.add_widget(Image(source=img, allow_stretch=True, keep_ratio=False))
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
            text_color=(1, 1, 1, 1),
            font_name="ComicNeue"
        ))
        btn_voltar.on_release = lambda *a: self.voltar()
        layout.add_widget(btn_voltar)
        self.add_widget(layout)

    def voltar(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "algebra_tela"



class AlgebraRepresentacoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # --- Fundo ---
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        layout.add_widget(fundo)

        # --- Título ---
        self.title_label = MDLabel(
            text="Representações Algébricas",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            size_hint=(1, None),
            height=60,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(self.title_label)

        # --- Botão Voltar ---
        self.btn_voltar = MDIconButton(
            icon="arrow-left",
            pos_hint={"x": 0.02, "top": 0.95},
            user_font_size="32sp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.btn_voltar.bind(on_release=self.voltar)
        layout.add_widget(self.btn_voltar)

        # --- Card principal de resultado ---
        self.card_resultado = MDCard(
            size_hint=(0.75, 0.22),
            pos_hint={"center_x": 0.5, "center_y": 0.68},
            md_bg_color=(1, 1, 1, 0.9),
            radius=[25],
            elevation=10
        )
        self.resultado_label = MDLabel(
            text="Escolha 1º ou 2º grau",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_name="ComicNeue",
            font_style="H6"
        )
        self.card_resultado.add_widget(self.resultado_label)
        layout.add_widget(self.card_resultado)

        # --- Card de Passo a Passo ---
        self.card_passos = MDCard(
            size_hint=(0.75, 0.28),
            pos_hint={"center_x": 0.5, "center_y": 0.38},
            md_bg_color=(0.98, 0.98, 1, 0.85),
            radius=[25],
            elevation=10,
        )
        self.passos_label = MDLabel(
            text="🧩 Passo a passo aparecerá aqui",
            halign="left",
            valign="top",
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.2, 1),
            font_style="Subtitle1",
            padding=(20, 10)
        )
        self.card_passos.add_widget(self.passos_label)
        layout.add_widget(self.card_passos)

        # --- Sliders compactos (à esquerda) ---
        self.sliders_layout = BoxLayout(
            orientation="vertical",
            spacing=6,
            size_hint=(0.28, 0.25),
            pos_hint={"x": 0.05, "y": 0.05}
        )

        self.slider_a, self.label_a = self.criar_slider("a", -5, 5, 1, 1)
        self.slider_b, self.label_b = self.criar_slider("b", -10, 10, 0, 1)
        self.slider_c, self.label_c = self.criar_slider("c", -10, 10, 0, 1)

        for label, slider in [(self.label_a, self.slider_a),
                              (self.label_b, self.slider_b),
                              (self.label_c, self.slider_c)]:
            self.sliders_layout.add_widget(label)
            self.sliders_layout.add_widget(slider)

        layout.add_widget(self.sliders_layout)

        # --- Botões menores e à direita ---
        self.botao_layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint=(0.25, 0.15),
            pos_hint={"x": 0.7, "y": 0.05}
        )
        btn_1grau = self.criar_botao("Função 1º Grau", lambda: self.selecionar_tipo("1grau"))
        btn_2grau = self.criar_botao("Função 2º Grau", lambda: self.selecionar_tipo("2grau"))
        self.botao_layout.add_widget(btn_1grau)
        self.botao_layout.add_widget(btn_2grau)
        layout.add_widget(self.botao_layout)

        self.add_widget(layout)
        self.tipo_funcao = None
        self.atualizar_equacao()

    # ------------------- Funções auxiliares -------------------
    def criar_slider(self, nome, minimo, maximo, valor, passo):
        label = MDLabel(
            text=f"{nome}: {valor}",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="Subtitle2",
        )
        slider = Slider(min=minimo, max=maximo, value=valor, step=passo)
        slider.size_hint_y = 0.25
        slider.bind(value=lambda inst, val: self.atualizar_label(label, nome, val))
        return slider, label

    def criar_botao(self, texto, callback):
        botao = MDRectangleFlatButton(
            text=texto,
            pos_hint={"center_x": 0.5},
            line_color=(0.6, 0.8, 1, 1),
            text_color=(1, 1, 1, 1),
            on_release=lambda *a: callback(),
        )
        return botao

    def selecionar_tipo(self, tipo):
        self.tipo_funcao = tipo
        # Mostrar/ocultar slider c
        if tipo == "1grau":
            self.slider_c.opacity = 0
            self.label_c.opacity = 0
            self.slider_c.disabled = True
        else:
            self.slider_c.opacity = 1
            self.label_c.opacity = 1
            self.slider_c.disabled = False

        self.atualizar_equacao()

    def atualizar_label(self, label, nome, val):
        label.text = f"{nome}: {val:.1f}"
        self.atualizar_equacao()

    def atualizar_equacao(self):
        if not self.tipo_funcao:
            self.resultado_label.text = "Escolha 1º ou 2º grau"
            self.passos_label.text = "🧩 Ajuste os sliders e selecione o tipo de função"
            return

        a, b, c = self.slider_a.value, self.slider_b.value, self.slider_c.value

        if self.tipo_funcao == "1grau":
            if a != 0:
                raiz = -b / a
                self.resultado_label.text = f"f(x) = {a:.1f}x + {b:.1f}\nRaiz: x = {raiz:.2f}"
                self.passos_label.text = (
                    "📘 Passo a passo:\n"
                    f"1️⃣ Equação: {a:.1f}x + {b:.1f} = 0\n"
                    f"2️⃣ Isolando x → x = -b/a\n"
                    f"3️⃣ Substituindo: x = -({b:.1f}) / {a:.1f}\n"
                    f"4️⃣ Resultado: x = {raiz:.2f}"
                )
            else:
                self.resultado_label.text = f"f(x) = {a:.1f}x + {b:.1f}\nRaiz indefinida"
                self.passos_label.text = "❌ O coeficiente a = 0, não é função de 1º grau."

        elif self.tipo_funcao == "2grau":
            if a != 0:
                delta = b**2 - 4*a*c
                xv = -b / (2*a)
                yv = a*xv**2 + b*xv + c

                if delta > 0:
                    x1 = (-b + delta**0.5) / (2*a)
                    x2 = (-b - delta**0.5) / (2*a)
                    raiz_texto = f"x₁ = {x1:.2f}, x₂ = {x2:.2f}"
                elif delta == 0:
                    x1 = -b / (2*a)
                    raiz_texto = f"x = {x1:.2f}"
                else:
                    raiz_texto = "Raízes complexas"

                self.resultado_label.text = (
                    f"f(x) = {a:.1f}x² + {b:.1f}x + {c:.1f}\n"
                    f"Ponto de {'mínimo' if a > 0 else 'máximo'}: ({xv:.2f}, {yv:.2f})\n"
                    f"{raiz_texto}"
                )

                self.passos_label.text = (
                    "📗 Passo a passo:\n"
                    f"1️⃣ Equação: {a:.1f}x² + {b:.1f}x + {c:.1f} = 0\n"
                    f"2️⃣ Δ = b² - 4ac = ({b:.1f})² - 4({a:.1f})({c:.1f}) = {delta:.2f}\n"
                    f"3️⃣ Raízes: x = (-b ± √Δ) / (2a)\n"
                    f"4️⃣ Resultado: {raiz_texto}\n"
                    f"5️⃣ Vértice: ({xv:.2f}, {yv:.2f})"
                )
            else:
                self.resultado_label.text = "Não é uma função de 2º grau."
                self.passos_label.text = "⚠️ O coeficiente a = 0, vira função de 1º grau."

    def voltar(self, *args):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "meia_tela"