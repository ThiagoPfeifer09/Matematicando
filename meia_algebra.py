from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, SlideTransition
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivymd.uix.button import MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivymd.uix.button import MDRectangleFlatButton
import matplotlib.pyplot as plt
import numpy as np
from kivy.uix.label import Label
from kivy.metrics import dp
from random import choice
from kivy.uix.carousel import Carousel
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.slider import MDSlider
from kivy.uix.scrollview import ScrollView
# =================== TELA PRINCIPAL ÁLGEBRA ===================
class AlgebraTela(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Fundo
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        layout.add_widget(fundo)

        # 2. Decoração de Fundo (Temática Álgebra)
        self.adicionar_decoracao_fundo(layout)

        self.title_image = Image(
            source="Bonecos/titulo_algebra.png",
            size_hint=(None, None),
            height=dp(80),
            width=dp(300),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={"center_x": 0.5, "top": 0.96},
        )

        layout.add_widget(self.title_image)

        # Botão voltar (Preto)
        self.back_button = MDIconButton(
            icon='arrow-left',
            pos_hint={'x': 0.02, 'top': 0.98},
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1), # Preto
            on_release=lambda x: self.voltar("conteudos")
        )
        layout.add_widget(self.back_button)

        # 4. Boneco
        boneco = Image(
            source="Bonecos/boneco_algebra.png",
            size_hint=(0.45, 0.50),
            pos_hint={"center_x": 0.5, "center_y": 0.70}
        )
        layout.add_widget(boneco)

        # --- CARD CENTRAL ---
        card_principal = MDCard(
            size_hint=(0.9, 0.40),
            pos_hint={"center_x": 0.5, "y": 0.12},
            md_bg_color=(1, 1, 1, 0.3), # Fundo translúcido
            radius=[25],
            elevation=0,
            line_color=(0, 0, 0, 0.1), # Borda sutil preta
            line_width=1
        )

        container = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15)
        )

        # Subtítulo (Preto)
        container.add_widget(MDLabel(
            text="Escolha a atividade:",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="Subtitle1",
            bold=True,
            size_hint_y=None,
            height=dp(30),
        ))

        # Botões Principais
        container.add_widget(self.create_icon_button(
            "Representações", "variable", lambda: self.ir_para("algebra_representacoes")
        ))

        container.add_widget(self.create_icon_button(
            "Definições", "book-open-variant", lambda: self.ir_para("algebra_definicoes")
        ))

        # Botão Jogar
        container.add_widget(self.create_icon_button(
            "Jogar", "gamepad-variant", lambda: self.ir_para("jogar")
        ))

        card_principal.add_widget(container)
        layout.add_widget(card_principal)

        self.add_widget(layout)

    # --- Funções Auxiliares ---

    def adicionar_decoracao_fundo(self, layout):
        """Ícones de álgebra escuros para preencher o vazio"""
        # Ícones: Variável (X), Função (f(x)), Somatório, Igual, Gráfico
        icones = [
            "variable", "function-variant", "sigma",
            "equal", "chart-bell-curve", "alpha", "beta"
        ]

        positions = [
            {"x": 0.05, "y": 0.85}, {"x": 0.85, "y": 0.9},
            {"x": 0.1, "y": 0.6}, {"x": 0.85, "y": 0.6},
            {"x": 0.05, "y": 0.2}, {"x": 0.9, "y": 0.25}
        ]

        for pos in positions:
            icon = MDIconButton(
                icon=choice(icones),
                theme_text_color="Custom",
                text_color=(0, 0, 0, 0.08), # Preto marca d'água
                pos_hint=pos,
                icon_size=dp(45),
                disabled=True
            )
            layout.add_widget(icon)

    def create_icon_button(self, text, icon, callback):
        card = MDCard(
            size_hint=(1, None),
            height=dp(50),
            md_bg_color=(0.15, 0.25, 0.75, 0.9), # Azul padrão
            radius=[15],
            elevation=3,
            ripple_behavior=True,
            padding=[dp(15), 0, dp(10), 0]
        )

        row = BoxLayout(orientation="horizontal", spacing=dp(15))

        # Ícone Esquerdo
        row.add_widget(MDIconButton(
            icon=icon,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(24), dp(24)),
            pos_hint={'center_y': 0.5},
            disabled=True
        ))

        # Texto
        row.add_widget(MDLabel(
            text=text,
            halign="left",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True
        ))

        # Seta Direita
        row.add_widget(MDIconButton(
            icon="chevron-right",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.7),
            size_hint=(None, None),
            size=(dp(24), dp(24)),
            pos_hint={'center_y': 0.5},
            disabled=True
        ))

        card.add_widget(row)
        card.on_release = lambda *a: [self.tocar_som_giz(), callback()]
        return card

    def digita_texto(self, label, texto, i=0):
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i + 1), 0.05)

    def tocar_som_giz(self):
        som = SoundLoader.load("giz_riscando.wav")
        if som:
            som.play()

    def ir_para(self, tela_nome):
        if self.manager:
            self.manager.transition = SlideTransition(direction="left", duration=0.4)
            self.manager.current = tela_nome

    def voltar(self, tela_nome):
        if self.manager:
            self.manager.transition = SlideTransition(direction="right", duration=0.4)
            self.manager.current = tela_nome

# =================== TELA DEFINIÇÕES ÁLGEBRA ===================

from meia_tela import BaseDefinicoesTela

class AlgebraDefinicoesTela(BaseDefinicoesTela):
    def __init__(self, **kwargs):
        super().__init__(titulo_secao="Álgebra e Funções", **kwargs)

    def voltar(self, instance):
        # Ajuste "algebra_tela" para o nome correto no seu ScreenManager
        self.manager.transition.direction = "right"
        self.manager.current = "algebra_tela"

    def setup_slides(self):
        # ---------------------------------------------------------
        # SLIDE 1: CONCEITOS BÁSICOS
        # ---------------------------------------------------------
        texto_intro = (
            "A Álgebra usa letras para representar números desconhecidos.\n\n"
            "[b]A INCÓGNITA (x):[/b]\n"
            "É o valor que queremos descobrir.\n"
            "Ex: 2 + x = 5\n"
            "O 'x' só pode ser 3, pois 2 + 3 = 5.\n\n"
            "Uma [b]Função[/b] é uma regra que relaciona cada valor de x a um resultado f(x) ou y."
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="O que é Álgebra?",
            texto_definicao=texto_intro,
            icone="variable" # Ícone de X
        ))

        # ---------------------------------------------------------
        # SLIDE 2: FUNÇÃO DE 1º GRAU
        # ---------------------------------------------------------
        texto_grau1 = (
            "É uma reta. A fórmula geral é:\n"
            "[b]f(x) = ax + b[/b]\n\n"
            "[b]COMO RESOLVER (A Raiz):[/b]\n"
            "Igualamos a zero para achar onde a reta corta o eixo X.\n\n"
            "Ex: 2x - 4 = 0\n"
            "2x = 4\n"
            "x = 4 ÷ 2  -->  [b]x = 2[/b]"
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Função de 1º Grau",
            texto_definicao=texto_grau1,
            icone="chart-line" # Ícone de gráfico de linha
        ))

        # ---------------------------------------------------------
        # SLIDE 3: FUNÇÃO DE 2º GRAU
        # ---------------------------------------------------------
        texto_grau2 = (
            "O gráfico é uma curva chamada [b]Parábola[/b].\n"
            "Fórmula geral:\n"
            "[b]f(x) = ax² + bx + c[/b]\n\n"
            "• Se 'a' for positivo: Sorriso (U)\n"
            "• Se 'a' for negativo: Triste (∩)\n\n"
            "O valor [b]c[/b] é onde a curva corta o eixo vertical (Y)."
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Função de 2º Grau",
            texto_definicao=texto_grau2,
            icone="chart-bell-curve" # Ícone de curva
        ))

        # ---------------------------------------------------------
        # SLIDE 4: RAÍZES (BHASKARA)
        # ---------------------------------------------------------
        texto_bhaskara = (
            "Para achar as raízes (onde corta o eixo X), usamos a fórmula de Bhaskara:\n\n"
            "1. Ache o Delta (Δ):\n"
            "[b]Δ = b² - 4.a.c[/b]\n\n"
            "2. Ache o x:\n"
            "[b]x = (-b ± √Δ) ÷ 2a[/b]\n\n"
            "Isso nos dá dois resultados: x' e x''."
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Raízes (Bhaskara)",
            texto_definicao=texto_bhaskara,
            icone="calculator-variant"
        ))

        # ---------------------------------------------------------
        # SLIDE 5: VÉRTICE DA PARÁBOLA
        # ---------------------------------------------------------
        texto_vertice = (
            "O Vértice é o ponto de virada da curva (o ponto mais alto ou mais baixo).\n\n"
            "[b]Coordenadas do Vértice (V):[/b]\n\n"
            "• Xv = -b ÷ 2a\n"
            "• Yv = -Δ ÷ 4a\n\n"
            "É essencial para saber o valor máximo ou mínimo de uma função."
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Vértice e Máximos",
            texto_definicao=texto_vertice,
            icone="axis-arrow"
        ))




from math import sqrt
import math
from kivymd.uix.screen import MDScreen

class AlgebraRepresentacoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Fundo
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        layout.add_widget(fundo)

        self.adicionar_decoracao_fundo(layout)

        # 2. Cabeçalho
        layout.add_widget(MDIconButton(
            icon="arrow-left",
            pos_hint={"x": 0.02, "top": 0.98},
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            on_release=self.voltar
        ))

        self.title_label = Label(
            text="FUNCOES",
            color=(0, 0, 0, 1),
            font_name="BungeeShade",
            font_size="28sp",
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "top": 0.96},
        )
        layout.add_widget(self.title_label)

        # 3. CARD DE INFORMAÇÕES
        self.info_card = MDCard(
            size_hint=(0.9, 0.22),
            pos_hint={"center_x": 0.5, "top": 0.88},
            md_bg_color=(1, 1, 1, 0.95),
            radius=[15],
            elevation=4,
            orientation="vertical",
            padding=[dp(15), dp(10), dp(15), dp(10)]
        )

        self.lbl_equacao = MDLabel(
            text="f(x) = ...",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        self.info_card.add_widget(self.lbl_equacao)

        self.scroll_passos = ScrollView(size_hint=(1, 1))
        self.lbl_passos = MDLabel(
            text="Passo a passo aparecerá aqui...",
            halign="left",
            valign="top",
            theme_text_color="Custom",
            text_color=(0.2, 0.2, 0.2, 1),
            font_style="Body2",
            size_hint_y=None,
            markup=True
        )
        self.lbl_passos.bind(texture_size=self.lbl_passos.setter('size'))
        self.scroll_passos.add_widget(self.lbl_passos)
        self.info_card.add_widget(self.scroll_passos)

        layout.add_widget(self.info_card)

        # 4. ÁREA DO GRÁFICO
        self.graph_box = BoxLayout(
            size_hint=(0.9, 0.30),
            pos_hint={"center_x": 0.5, "top": 0.65}
        )

        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_alpha(0)
        self.ax.set_facecolor("#ffffffcc")
        self.graph_widget = FigureCanvasKivyAgg(self.fig)
        self.graph_box.add_widget(self.graph_widget)

        layout.add_widget(self.graph_box)

        # 5. CONTROLES INFERIORES
        controls_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.95, 0.32),
            pos_hint={"center_x": 0.5, "y": 0.01},
            spacing=dp(5)
        )

        # Botões de Tipo
        type_box = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(40))
        self.btn_1grau = MDFillRoundFlatButton(
            text="1º Grau", md_bg_color=(0.2, 0.4, 0.9, 1), size_hint_x=0.5, on_release=lambda x: self.mudar_tipo("1grau")
        )
        self.btn_2grau = MDFillRoundFlatButton(
            text="2º Grau", md_bg_color=(0.6, 0.6, 0.6, 1), size_hint_x=0.5, on_release=lambda x: self.mudar_tipo("2grau")
        )
        type_box.add_widget(self.btn_1grau)
        type_box.add_widget(self.btn_2grau)
        controls_layout.add_widget(type_box)

        # Sliders
        sliders_box = BoxLayout(orientation="vertical", spacing=dp(2))

        self.lbl_a = MDLabel(text="a = 1", halign="center", theme_text_color="Custom", text_color=(0,0,0,1), font_style="Caption")
        self.slider_a = MDSlider(min=-5, max=5, value=1, step=0.5, color=(0,0,0,1))
        self.slider_a.bind(value=self.atualizar_grafico)
        sliders_box.add_widget(self.lbl_a)
        sliders_box.add_widget(self.slider_a)

        self.lbl_b = MDLabel(text="b = 0", halign="center", theme_text_color="Custom", text_color=(0,0,0,1), font_style="Caption")
        self.slider_b = MDSlider(min=-10, max=10, value=0, step=1, color=(0,0,0,1))
        self.slider_b.bind(value=self.atualizar_grafico)
        sliders_box.add_widget(self.lbl_b)
        sliders_box.add_widget(self.slider_b)

        self.lbl_c = MDLabel(text="c = 0", halign="center", theme_text_color="Custom", text_color=(0,0,0,1), font_style="Caption", opacity=0)
        self.slider_c = MDSlider(min=-10, max=10, value=0, step=1, color=(0,0,0,1), opacity=0, disabled=True)
        self.slider_c.bind(value=self.atualizar_grafico)
        sliders_box.add_widget(self.lbl_c)
        sliders_box.add_widget(self.slider_c)

        controls_layout.add_widget(sliders_box)

        # Ações (Raízes, Vértice, etc)
        actions_box = BoxLayout(orientation="horizontal", spacing=dp(5), size_hint_y=None, height=dp(40))

        self.btn_raizes = MDRectangleFlatButton(text="Raízes", line_color=(0,0,0,1), text_color=(0,0,0,1), size_hint_x=0.33)
        self.btn_raizes.bind(on_release=self.mostrar_raizes)

        self.btn_inter = MDRectangleFlatButton(text="Intersec. Y", line_color=(0,0,0,1), text_color=(0,0,0,1), size_hint_x=0.33)
        self.btn_inter.bind(on_release=self.mostrar_interseccao)

        self.btn_vertice = MDRectangleFlatButton(text="Vértice", line_color=(0,0,0,1), text_color=(0,0,0,1), size_hint_x=0.33, opacity=0, disabled=True)
        self.btn_vertice.bind(on_release=self.mostrar_vertice)

        actions_box.add_widget(self.btn_raizes)
        actions_box.add_widget(self.btn_inter)
        actions_box.add_widget(self.btn_vertice)

        controls_layout.add_widget(actions_box)

        layout.add_widget(controls_layout)
        self.add_widget(layout)

        # Inicialização
        self.tipo_atual = "1grau"
        self.atualizar_grafico()

    def adicionar_decoracao_fundo(self, layout):
        icones = ["alpha", "beta", "function", "variable", "chart-bell-curve"]
        positions = [{"x": 0.05, "y": 0.85}, {"x": 0.85, "y": 0.9}, {"x": 0.1, "y": 0.5}, {"x": 0.85, "y": 0.5}]
        for pos in positions:
            layout.add_widget(MDIconButton(icon=choice(icones), theme_text_color="Custom", text_color=(0,0,0,0.05), pos_hint=pos, icon_size=dp(50), disabled=True))

    def mudar_tipo(self, tipo):
        self.tipo_atual = tipo
        if tipo == "1grau":
            self.btn_1grau.md_bg_color = (0.2, 0.4, 0.9, 1)
            self.btn_2grau.md_bg_color = (0.6, 0.6, 0.6, 1)
            self.lbl_c.opacity = 0; self.slider_c.opacity = 0; self.slider_c.disabled = True
            self.btn_vertice.opacity = 0; self.btn_vertice.disabled = True
        else:
            self.btn_1grau.md_bg_color = (0.6, 0.6, 0.6, 1)
            self.btn_2grau.md_bg_color = (0.2, 0.4, 0.9, 1)
            self.lbl_c.opacity = 1; self.slider_c.opacity = 1; self.slider_c.disabled = False
            self.btn_vertice.opacity = 1; self.btn_vertice.disabled = False
        self.atualizar_grafico()

    def limpar_plot(self):
        self.ax.clear()

        # Grid mais suave
        self.ax.grid(True, linestyle="--", alpha=0.3)

        # Eixos principais mais fortes
        self.ax.axhline(0, color='black', linewidth=1.2)
        self.ax.axvline(0, color='black', linewidth=1.2)

        # Labels dos Eixos
        self.ax.set_xlabel("Eixo X", fontsize=8, loc='right')
        self.ax.set_ylabel("Eixo Y", fontsize=8, loc='top')

        # Remove bordas desnecessárias (topo e direita)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        # Limites fixos
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

    def gerar_explicacao(self, a, b, c):
        if self.tipo_atual == "1grau":
            if a == 0: return f"[b]Função Constante:[/b]\nReta horizontal em y = {b}."
            raiz = -b/a
            return (
                f"[b]Raiz (f(x)=0):[/b]\n"
                f"1. {a}x + ({b}) = 0\n"
                f"2. {a}x = -({b})\n"
                f"3. x = {-b}/{a} = [b]{raiz:.2f}[/b]"
            )
        else:
            if a == 0: return "a=0 transforma em função de 1º grau."
            delta = b**2 - 4*a*c
            passos = f"[b]Bhaskara:[/b]\nΔ = ({b})² - 4.({a}).({c}) = [b]{delta:.2f}[/b]\n\n"
            if delta > 0:
                x1 = (-b + math.sqrt(delta)) / (2*a)
                x2 = (-b - math.sqrt(delta)) / (2*a)
                passos += f"Raízes: x'={x1:.2f}, x''={x2:.2f}"
            elif delta == 0:
                x1 = -b / (2*a)
                passos += f"Raiz única: x={x1:.2f}"
            else:
                passos += "Δ < 0: Sem raízes reais."
            return passos

    def atualizar_grafico(self, *args):
        self.limpar_plot()
        a = self.slider_a.value
        b = self.slider_b.value
        c = self.slider_c.value

        self.lbl_a.text = f"a = {a:.1f}"; self.lbl_b.text = f"b = {b:.1f}"; self.lbl_c.text = f"c = {c:.1f}"
        x = np.linspace(-12, 12, 400)

        if self.tipo_atual == "1grau":
            y = a*x + b
            equacao_str = f"f(x) = {a:.1f}x + {b:.1f}"
            titulo = "Função Afim (1º Grau)"
        else:
            y = a*(x**2) + b*x + c
            equacao_str = f"f(x) = {a:.1f}x² + {b:.1f}x + {c:.1f}"
            titulo = "Função Quadrática (2º Grau)"

        # Plota a linha principal com label para a legenda
        self.ax.plot(x, y, color='#1565C0', linewidth=2, label='f(x)')

        # Título do Gráfico
        self.ax.set_title(titulo, fontsize=10, fontweight='bold', pad=10)

        # Configuração da Legenda (Melhorada)
        self.ax.legend(loc='upper right', fontsize=8, shadow=True, fancybox=True, framealpha=0.9, facecolor='white')

        self.graph_widget.draw()

        # Atualiza Card
        self.lbl_equacao.text = equacao_str
        self.lbl_passos.text = self.gerar_explicacao(a, b, c)

    def mostrar_raizes(self, *args):
        self.atualizar_grafico()
        a = self.slider_a.value
        b = self.slider_b.value
        c = self.slider_c.value

        if self.tipo_atual == "1grau":
            if a != 0:
                raiz = -b/a
                self.ax.plot(raiz, 0, 'ro', markersize=7, label="Raiz")
        else:
            if a != 0:
                delta = b**2 - 4*a*c
                if delta >= 0:
                    x1 = (-b + np.sqrt(delta)) / (2*a)
                    x2 = (-b - np.sqrt(delta)) / (2*a)
                    self.ax.plot([x1, x2], [0, 0], 'ro', markersize=7, linestyle='None', label="Raízes")

        # Atualiza legenda para incluir os pontos novos
        self.ax.legend(loc='upper right', fontsize=8, shadow=True, framealpha=0.9)
        self.graph_widget.draw()

    def mostrar_interseccao(self, *args):
        self.atualizar_grafico()
        val = self.slider_b.value if self.tipo_atual == "1grau" else self.slider_c.value
        self.ax.plot(0, val, 'mo', markersize=7, label="Intersec. Y")
        self.ax.legend(loc='upper right', fontsize=8, shadow=True, framealpha=0.9)
        self.graph_widget.draw()

    def mostrar_vertice(self, *args):
        if self.tipo_atual != "2grau": return
        self.atualizar_grafico()
        a, b, c = self.slider_a.value, self.slider_b.value, self.slider_c.value
        if a != 0:
            xv = -b / (2*a)
            yv = -(b**2 - 4*a*c) / (4*a)
            self.ax.plot(xv, yv, 'go', markersize=7, label="Vértice")
            self.ax.legend(loc='upper right', fontsize=8, shadow=True, framealpha=0.9)
        self.graph_widget.draw()

    def voltar(self, *args):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "algebra_tela"