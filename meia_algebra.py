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
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.button import MDRectangleFlatButton
import matplotlib.pyplot as plt
import numpy as np
import math
from kivy.metrics import dp
import cmath

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
            source="boneco_algebra.png",
            size_hint=(0.5, 0.5),
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
            font_size="18sp"
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
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.95}
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
            text_color=(1, 1, 1, 1)
        ))
        btn_voltar.on_release = lambda *a: self.voltar()
        layout.add_widget(btn_voltar)
        self.add_widget(layout)

    def voltar(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "algebra_tela"



from math import sqrt
import cmath
from kivymd.uix.screen import MDScreen


class AlgebraRepresentacoes(MDScreen):
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
            pos_hint={"center_x": 0.5, "top": 0.97},
        )
        layout.add_widget(self.title_label)

        # --- Botão Voltar ---
        self.btn_voltar = MDIconButton(
            icon="arrow-left",
            pos_hint={"x": 0.02, "top": 0.97},
            user_font_size="32sp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.btn_voltar.bind(on_release=self.voltar)
        layout.add_widget(self.btn_voltar)

        # --- CARD 1 (Função e Resultados) ---
        self.card_resultado = MDCard(
            size_hint=(0.9, 0.16),
            pos_hint={"center_x": 0.5, "top": 0.90},
            md_bg_color=(1, 1, 1, 0.9),
            radius=[25],
            elevation=10
        )
        self.resultado_label = MDLabel(
            text="Escolha 1º ou 2º grau",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="H6"
        )
        self.card_resultado.add_widget(self.resultado_label)
        layout.add_widget(self.card_resultado)

        # --- CARD 2 (Passo a passo) ---
        self.card_passos = MDCard(
            size_hint=(0.9, 0.18),
            pos_hint={"center_x": 0.5, "top": 0.68},
            md_bg_color=(0.97, 0.97, 1, 0.9),
            radius=[25],
            elevation=10,
        )
        self.passos_label = MDLabel(
            text="Passo a passo aparecerá aqui",
            halign="left",
            valign="top",
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.2, 1),
            font_style="Subtitle1",
            padding=(20, 15)
        )
        self.card_passos.add_widget(self.passos_label)
        layout.add_widget(self.card_passos)

        # --- Botões de seleção (1º e 2º grau) ---
        botoes_layout = BoxLayout(
            orientation="horizontal",
            spacing=12,
            size_hint=(0.32, 0.065),
            pos_hint={"x": 0.07, "top": 0.44}
        )
        btn_1grau = self.criar_botao("Função 1º Grau", lambda: self.selecionar_tipo("1grau"))
        btn_2grau = self.criar_botao("Função 2º Grau", lambda: self.selecionar_tipo("2grau"))
        botoes_layout.add_widget(btn_1grau)
        botoes_layout.add_widget(btn_2grau)
        layout.add_widget(botoes_layout)

        # --- Parte inferior (sliders à esquerda + gráfico à direita) ---
        parte_inferior = BoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint=(0.9, 0.32),
            pos_hint={"center_x": 0.5, "y": 0.02}
        )

        # Sliders
        self.sliders_layout = BoxLayout(
            orientation="vertical",
            spacing=5,
            size_hint=(0.35, 1)
        )
        self.slider_a, self.label_a = self.criar_slider("a", -5, 5, 1, 1)
        self.slider_b, self.label_b = self.criar_slider("b", -10, 10, 0, 1)
        self.slider_c, self.label_c = self.criar_slider("c", -10, 10, 0, 1)
        for label, slider in [(self.label_a, self.slider_a),
                              (self.label_b, self.slider_b),
                              (self.label_c, self.slider_c)]:
            self.sliders_layout.add_widget(label)
            self.sliders_layout.add_widget(slider)

        # Gráfico
        self.fig, self.ax = plt.subplots(figsize=(0.8, 0.8))
        self.ax.set_facecolor("white")
        self.graph_canvas = FigureCanvasKivyAgg(self.fig)

        # --- NOVOS BOTÕES ACIMA DO GRÁFICO ---
        botoes_grafico_layout = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(0.7, 0.12),
            pos_hint={"center_x": 0.6, "top": 0.47}
        )
        self.btn_raizes = self.criar_botao("Raízes", self.mostrar_raizes)
        self.btn_interseccao = self.criar_botao("Intersecção Y", self.mostrar_interseccao)
        self.btn_vertice = self.criar_botao("Vértice", self.mostrar_vertice)
        botoes_grafico_layout.add_widget(self.btn_raizes)
        botoes_grafico_layout.add_widget(self.btn_interseccao)
        botoes_grafico_layout.add_widget(self.btn_vertice)
        layout.add_widget(botoes_grafico_layout)

        self.graph_layout = BoxLayout(orientation="vertical", size_hint=(0.65, 1))
        self.graph_layout.add_widget(self.graph_canvas)

        parte_inferior.add_widget(self.sliders_layout)
        parte_inferior.add_widget(self.graph_layout)
        layout.add_widget(parte_inferior)

        self.add_widget(layout)

        # Estado inicial
        self.tipo_funcao = None
        self.marcadores = []
        self.atualizar_equacao()

    # --- Funções auxiliares ---
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
        return MDRectangleFlatButton(
            text=texto,
            line_color=(0.6, 0.8, 1, 1),
            text_color=(1, 1, 1, 1),
            on_release=lambda *a: callback(),
        )

    def selecionar_tipo(self, tipo):
        self.tipo_funcao = tipo
        self.btn_vertice.opacity = 1 if tipo == "2grau" else 0
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

    def limpar_marcadores(self):
        # Garante que a lista exista
        if not hasattr(self, "marcadores") or self.marcadores is None:
            self.marcadores = []

        for art in list(self.marcadores):
            try:
                # tenta remover normalmente
                art.remove()
            except Exception:
                # Se não der para remover diretamente, tenta remover da lista de linhas do axes (caso seja Line2D)
                try:
                    if art in self.ax.lines:
                        self.ax.lines.remove(art)
                except Exception:
                    # ignora qualquer erro residual
                    pass
        # limpa a lista e redesenha
        self.marcadores.clear()
        try:
            self.graph_canvas.draw()
        except Exception:
            pass


    def atualizar_equacao(self):
        if not self.tipo_funcao:
            self.resultado_label.text = "Escolha 1º ou 2º grau"
            self.passos_label.text = "Ajuste os sliders e selecione o tipo de função"
            return
        self.limpar_marcadores()
        a, b, c = self.slider_a.value, self.slider_b.value, self.slider_c.value

        x = np.linspace(-10, 10, 400)
        y = a * x + b if self.tipo_funcao == "1grau" else a * x**2 + b * x + c
        self.ax.clear()
        self.ax.set_facecolor("white")
        self.ax.plot(x, y, color="blue")
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.graph_canvas.draw()

        # Mantém função no título do card
        func_text = f"f(x) = {a:.1f}x + {b:.1f}" if self.tipo_funcao == "1grau" else f"f(x) = {a:.1f}x² + {b:.1f}x + {c:.1f}"

        # --- Atualiza textos ---
        if self.tipo_funcao == "1grau":
            if a != 0:
                raiz = -b / a
                self.resultado_label.text = f"{func_text} | Raiz: x={raiz:.2f}"
                self.passos_label.text = (
                    "Passo a passo:\n"
                    f"1- Equação: {a:.1f}x + {b:.1f} = 0\n"
                    f"2- Isolando x → x = -b/a\n"
                    f"3- Substituindo: x = -({b:.1f}) / {a:.1f}\n"
                    f"4- Resultado: x = {raiz:.2f}"
                )
            else:
                self.resultado_label.text = f"{func_text} | Raiz indefinida"
                self.passos_label.text = "a=0 → não é função de 1º grau."
        else:
            if a != 0:
                delta = b**2 - 4*a*c
                xv = -b / (2*a)
                yv = a*xv**2 + b*xv + c
                raiz_delta = cmath.sqrt(delta)
                x1 = (-b + raiz_delta) / (2*a)
                x2 = (-b - raiz_delta) / (2*a)
                if delta > 0:
                    tipo_raiz = "Duas raízes reais:"
                    raiz_texto = f"x1 = {x1.real:.2f}, x2 = {x2.real:.2f}"
                elif delta == 0:
                    tipo_raiz = "Uma raiz real dupla:"
                    raiz_texto = f"x = {x1.real:.2f}"
                else:
                    tipo_raiz = "Raízes complexas:"
                    raiz_texto = f"x1 = {x1.real:.2f} + {x1.imag:.2f}i, x2 = {x2.real:.2f} + {x2.imag:.2f}i"
                self.resultado_label.text = (
                    f"f(x) = {a:.1f}x² + {b:.1f}x + {c:.1f}\n"
                    f"Ponto de {'mínimo' if a > 0 else 'máximo'}: ({xv:.2f}, {yv:.2f})\n"
                    f"{raiz_texto}"
                )
                self.passos_label.text = (
                    "Passo a passo:\n"
                    f"1- Equação: {a:.1f}x² + {b:.1f}x + {c:.1f} = 0\n"
                    f"2- Δ = b² - 4ac = ({b:.1f})² - 4({a:.1f})({c:.1f}) = {delta:.2f}\n"
                    f"3- Substituindo: x = (-({b:.1f}) ± √({delta:.2f})) / (2×{a:.1f})\n"
                    f"4- {tipo_raiz} {raiz_texto}\n"
                    f"5- Vértice: ({xv:.2f}, {yv:.2f})"
                )
            else:
                self.resultado_label.text = "Não é uma função de 2º grau."
                self.passos_label.text = "⚠️ O coeficiente a = 0, vira função de 1º grau."
                
    # --- NOVAS FUNÇÕES PARA MOSTRAR PONTOS ---
    def mostrar_raizes(self, *args):
        if not self.tipo_funcao: return
        self.limpar_marcadores()
        a, b, c = self.slider_a.value, self.slider_b.value, self.slider_c.value
        if self.tipo_funcao == "1grau":
            x = -b / a; y = 0
            m, = self.ax.plot(x, y, "rv", markersize=10, label="Raiz")
            self.marcadores.append(m)
        else:
            delta = b**2 - 4*a*c
            if delta < 0: return
            raiz1 = (-b + np.sqrt(delta)) / (2*a)
            raiz2 = (-b - np.sqrt(delta)) / (2*a)
            for r in [raiz1, raiz2]:
                m, = self.ax.plot(r, 0, "rv", markersize=10)
                self.marcadores.append(m)
        self.graph_canvas.draw()

    def mostrar_interseccao(self, *args):
        if not self.tipo_funcao: return
        self.limpar_marcadores()
        a, b, c = self.slider_a.value, self.slider_b.value, self.slider_c.value
        y = c if self.tipo_funcao == "2grau" else b
        m, = self.ax.plot(0, y, "bo", markersize=10, label="Intersecção Y")
        self.marcadores.append(m)
        self.graph_canvas.draw()

    def mostrar_vertice(self, *args):
        if self.tipo_funcao != "2grau": return
        self.limpar_marcadores()
        a, b, c = self.slider_a.value, self.slider_b.value, self.slider_c.value
        xv, yv = -b / (2*a), a * (-b / (2*a))**2 + b * (-b / (2*a)) + c
        m, = self.ax.plot(xv, yv, "go", markersize=10, label="Vértice")
        self.marcadores.append(m)
        self.graph_canvas.draw()

    def voltar(self, *args):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "algebra_tela"
