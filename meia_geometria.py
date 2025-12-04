from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton,MDFlatButton
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
import math
from kivy.graphics import Color, Line
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import Label as CoreLabel
from kivy.metrics import dp
from random import choice
from kivy.uix.label import Label
from kivy.uix.carousel import Carousel
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
# =================== TELA PRINCIPAL ÁLGEBRA ===================
class GeometriaTela(Screen):
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

        self.title_image = Image(
            source="Bonecos/titulo_geometria.png",
            size_hint=(None, None),
            height=dp(80),
            width=dp(300),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={"center_x": 0.5, "top": 0.96},
        )

        layout.add_widget(self.title_image)

        # Botão Voltar (Preto)
        self.back_button = MDIconButton(
            icon='arrow-left',
            pos_hint={'x': 0.02, 'top': 0.98},
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),  # Preto
            on_release=lambda x: self.voltar("conteudos")
        )
        layout.add_widget(self.back_button)

        # 4. Boneco
        boneco = Image(
            source="Bonecos/boneco_geometria.png",
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

        # Subtítulo do Card (Preto)
        container.add_widget(MDLabel(
            text="Escolha a atividade:",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1), # Preto
            font_style="Subtitle1",
            bold=True,
            size_hint_y=None,
            height=dp(30),
        ))

        # Botões Principais (Azuis com texto branco)
        container.add_widget(self.create_icon_button(
            "Representações", "shape-outline", lambda: self.ir_para("geometria_representacoes")
        ))

        container.add_widget(self.create_icon_button(
            "Definições", "ruler-square", lambda: self.ir_para("geometria_definicoes")
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
        """Ícones de geometria escuros para preencher o vazio"""
        # Ícones específicos de geometria
        icones = [
            "hexagon-outline", "triangle-outline", "square-outline",
            "circle-outline", "ruler", "protractor", "vector-square"
        ]

        # Posições espalhadas
        positions = [
            {"x": 0.05, "y": 0.85}, {"x": 0.85, "y": 0.9},
            {"x": 0.1, "y": 0.6}, {"x": 0.85, "y": 0.6},
            {"x": 0.05, "y": 0.2}, {"x": 0.9, "y": 0.25}
        ]

        for pos in positions:
            icon = MDIconButton(
                icon=choice(icones),
                theme_text_color="Custom",
                text_color=(0, 0, 0, 0.08), # Preto bem claro (marca d'água)
                pos_hint=pos,
                icon_size=dp(45),
                disabled=True
            )
            layout.add_widget(icon)

    def create_icon_button(self, text, icon, callback):
        card = MDCard(
            size_hint=(1, None),
            height=dp(50),
            md_bg_color=(0.15, 0.25, 0.75, 0.9), # Manteve o azul
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
        card.on_release = lambda *a: callback()
        return card

    def digita_texto(self, label, texto, i=0):
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i + 1), 0.05)

    def ir_para(self, tela_nome):
        if self.manager:
            self.manager.transition = SlideTransition(direction="left", duration=0.4)
            self.manager.current = tela_nome

    def voltar(self, tela_nome):
        if self.manager:
            self.manager.transition = SlideTransition(direction="right", duration=0.4)
            self.manager.current = tela_nome

# =================== TELA DEFINIÇÕES ===================

from meia_tela import BaseDefinicoesTela

class GeometriaDefinicoesTela(BaseDefinicoesTela):
    def __init__(self, **kwargs):
        super().__init__(titulo_secao="Áreas e Perímetros", **kwargs)

    def voltar(self, instance):
        # Ajuste "geometria_tela" para o nome exato no seu ScreenManager
        self.manager.transition.direction = "right"
        self.manager.current = "geometria_tela"

    def setup_slides(self):
        # ---------------------------------------------------------
        # SLIDE 1: QUADRADO
        # ---------------------------------------------------------
        texto_quadrado = (
            "O quadrado possui 4 lados iguais. Chamamos o tamanho do lado de [b]L[/b].\n\n"
            "[b]ÁREA (Preenchimento):[/b]\n"
            "A = L x L  (ou L²)\n\n"
            "[b]PERÍMETRO (Contorno):[/b]\n"
            "P = L + L + L + L  (ou 4 x L)"
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Quadrado",
            texto_definicao=texto_quadrado,
            icone="square-outline"
        ))

        # ---------------------------------------------------------
        # SLIDE 2: RETÂNGULO
        # ---------------------------------------------------------
        texto_retangulo = (
            "O retângulo tem lados opostos iguais. Identificamos como [b]Base (b)[/b] e [b]Altura (h)[/b].\n\n"
            "[b]ÁREA:[/b]\n"
            "A = b x h\n\n"
            "[b]PERÍMETRO:[/b]\n"
            "P = Soma de todos os lados\n"
            "P = 2b + 2h"
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Retângulo",
            texto_definicao=texto_retangulo,
            icone="rectangle-outline"
        ))

        # ---------------------------------------------------------
        # SLIDE 3: TRIÂNGULO
        # ---------------------------------------------------------
        texto_triangulo = (
            "Para a área, precisamos da [b]Base (b)[/b] e da [b]Altura (h)[/b] (linha reta do topo até a base).\n\n"
            "[b]ÁREA:[/b]\n"
            "A = (b x h) ÷ 2\n"
            "(É a metade da área de um retângulo!)\n\n"
            "[b]PERÍMETRO:[/b]\n"
            "P = Soma dos comprimentos dos 3 lados."
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Triângulo",
            texto_definicao=texto_triangulo,
            icone="triangle-outline"
        ))

        # ---------------------------------------------------------
        # SLIDE 4: CÍRCULO
        # ---------------------------------------------------------
        texto_circulo = (
            "Não tem lados! O tamanho é definido pelo [b]Raio (r)[/b], que vai do centro até a borda.\n\n"
            "[b]ÁREA:[/b]\n"
            "A = π x r²\n\n"
            "[b]COMPRIMENTO DA CIRCUNFERÊNCIA:[/b]\n"
            "C = 2 x π x r\n\n"
            "[i]Obs: O número Pi (π) vale aproximadamente 3,14.[/i]"
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Círculo",
            texto_definicao=texto_circulo,
            icone="circle-outline"
        ))

from kivymd.uix.slider import MDSlider
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Line, Rectangle
from kivy.core.text import Label as CoreLabel  # Importante para escrever no canvas
from kivy.metrics import dp
from random import choice
import math

# KivyMD Imports
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.slider import MDSlider

class GeometriaRepresentacoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Fundo do App
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
            on_release=lambda x: self.voltar("geometria_tela")
        ))

        self.title_label = Label(
            text="GEOMETRIA",
            color=(0, 0, 0, 1),
            font_name="BungeeShade",
            font_size="28sp",
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "top": 0.96},
        )
        layout.add_widget(self.title_label)

        # 3. CARD DE INFORMAÇÕES (Resultados)
        self.info_card = MDCard(
            size_hint=(0.9, 0.25),
            pos_hint={"center_x": 0.5, "top": 0.88},
            md_bg_color=(1, 1, 1, 0.95),
            radius=[15],
            elevation=4,
            orientation="vertical",
            padding=[dp(15), dp(10), dp(15), dp(10)]
        )

        self.lbl_titulo_forma = MDLabel(
            text="Selecione uma forma",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        self.info_card.add_widget(self.lbl_titulo_forma)

        self.scroll_passos = ScrollView(size_hint=(1, 1))
        self.lbl_passos = MDLabel(
            text="As fórmulas aparecerão aqui...",
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

        # 4. ÁREA DE DESENHO (Com fundo branco)
        # Usamos um MDCard como container para garantir o fundo branco visualmente bonito
        self.drawing_container = MDCard(
            size_hint=(0.9, 0.35),
            pos_hint={"center_x": 0.5, "top": 0.62},
            md_bg_color=(1, 1, 1, 1), # Fundo branco SÓLIDO para o desenho
            radius=[15],
            elevation=2
        )
        self.drawing_area = Widget()
        self.drawing_container.add_widget(self.drawing_area)
        layout.add_widget(self.drawing_container)

        # 5. CONTROLES INFERIORES
        controls_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.95, 0.25),
            pos_hint={"center_x": 0.5, "y": 0.02},
            spacing=dp(5)
        )

        # Container dos Sliders
        self.sliders_container = BoxLayout(
            orientation="vertical",
            size_hint_y=0.6,
            padding=[dp(5), 0],
            spacing=dp(5)
        )
        controls_layout.add_widget(self.sliders_container)

        # Botões de Seleção
        shapes_box = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=0.4)

        formas = [
            ("Quadrado", "square-outline", "square"),
            ("Retângulo", "rectangle-outline", "rectangle"),
            ("Triângulo", "triangle-outline", "triangle"),
            ("Círculo", "circle-outline", "circle")
        ]

        for nome, icone, id_forma in formas:
            btn = MDIconButton(
                icon=icone,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                md_bg_color=(0.2, 0.4, 0.9, 1),
                icon_size="32sp",
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                pos_hint={"center_y": 0.5}
            )
            btn.bind(on_release=lambda x, f=id_forma: self.selecionar_forma(f))
            shapes_box.add_widget(btn)

        # Botão extra Trapézio
        btn_trap = MDIconButton(
            icon="shape-outline",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(0.2, 0.4, 0.9, 1),
            icon_size="32sp",
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={"center_y": 0.5},
            on_release=lambda x: self.selecionar_forma("trapezoid")
        )
        shapes_box.add_widget(btn_trap)

        controls_layout.add_widget(shapes_box)
        layout.add_widget(controls_layout)

        self.add_widget(layout)

        # Estado Inicial
        self.forma_atual = None
        self.sliders_refs = {}
        self.selecionar_forma("square")

    def adicionar_decoracao_fundo(self, layout):
        icones = ["shape-outline", "triangle-outline", "vector-square", "ruler"]
        positions = [
            {"x": 0.05, "y": 0.85}, {"x": 0.85, "y": 0.9},
            {"x": 0.1, "y": 0.5}, {"x": 0.85, "y": 0.5},
            {"x": 0.05, "y": 0.15}, {"x": 0.9, "y": 0.2}
        ]
        for pos in positions:
            layout.add_widget(MDIconButton(
                icon=choice(icones), theme_text_color="Custom",
                text_color=(0,0,0,0.05), pos_hint=pos,
                icon_size=dp(50), disabled=True
            ))

    def selecionar_forma(self, forma):
        self.forma_atual = forma
        self.sliders_container.clear_widgets()
        self.sliders_refs = {}

        # Configuração: (Nome Slider, Min, Max, Valor Inicial)
        configs = {
            "circle": [("Raio", 10, 80, 40)],
            "square": [("Lado", 20, 100, 60)],
            "rectangle": [("Base", 20, 150, 80), ("Altura", 20, 100, 50)],
            "triangle": [("Base", 30, 150, 80), ("Altura", 30, 100, 60)],
            "trapezoid": [("Base Maior", 40, 150, 100), ("Base Menor", 20, 80, 60), ("Altura", 20, 80, 50)]
        }

        # Cria Cards brancos para cada slider
        for nome, min_v, max_v, val_inicial in configs[forma]:
            # Card Container para o Slider
            card_slider = MDCard(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(40),
                radius=[10],
                md_bg_color=(1, 1, 1, 0.9), # Fundo branco levemente translúcido
                elevation=2,
                padding=[dp(10), 0]
            )

            lbl = MDLabel(text=f"{nome}: {val_inicial}", size_hint_x=0.4, theme_text_color="Custom", text_color=(0,0,0,1), bold=True, font_style="Caption")
            sld = MDSlider(min=min_v, max=max_v, value=val_inicial, step=1, size_hint_x=0.6, color=(0.2, 0.4, 0.9, 1))

            # Binding
            sld.bind(value=lambda instance, v, n=nome, l=lbl: self.atualizar_valores(n, v, l))

            card_slider.add_widget(lbl)
            card_slider.add_widget(sld)
            self.sliders_container.add_widget(card_slider)

            self.sliders_refs[nome] = sld

        # Tradução do Título
        traducoes = {
            "circle": "Círculo", "square": "Quadrado",
            "rectangle": "Retângulo", "triangle": "Triângulo",
            "trapezoid": "Trapézio"
        }
        self.lbl_titulo_forma.text = traducoes.get(forma, forma)
        self.desenhar_forma()

    def atualizar_valores(self, nome, valor, label):
        label.text = f"{nome}: {int(valor)}"
        self.desenhar_forma()

    # --- FUNÇÃO AUXILIAR PARA DESENHAR TEXTO NO CANVAS ---
    def desenhar_texto_canvas(self, texto, x, y):
        """Desenha um texto diretamente na área de desenho nas coordenadas X, Y"""
        label = CoreLabel(text=texto, font_size=14, color=(0, 0, 0, 1))
        label.refresh()
        texture = label.texture

        # Desenha um fundinho branco atrás do texto para ler melhor
        Color(1, 1, 1, 0.7)
        Rectangle(pos=(x, y), size=texture.size)

        # Desenha o texto preto
        Color(0, 0, 0, 1)
        Rectangle(texture=texture, pos=(x, y), size=texture.size)

    def desenhar_forma(self):
        self.drawing_area.canvas.clear()

        # Ajuste do centro relativo ao container
        cx, cy = self.drawing_area.center_x, self.drawing_area.center_y

        vals = {k: v.value for k, v in self.sliders_refs.items()}

        area = 0
        perimetro = 0
        texto_passo = ""
        fmt = lambda x: f"{x:.0f}"

        with self.drawing_area.canvas:
            Color(0.2, 0.4, 0.9, 1) # Cor Azul das linhas

            if self.forma_atual == "circle":
                r = vals["Raio"]
                Line(circle=(cx, cy, r), width=2)
                # Raio (linha visual)
                Color(1, 0, 0, 1) # Vermelho
                Line(points=[cx, cy, cx + r, cy], width=1.5)
                self.desenhar_texto_canvas(f"Raio: {fmt(r)}", cx + r/2 - 10, cy + 5)

                area = math.pi * r**2
                perimetro = 2 * math.pi * r
                texto_passo = (
                    f"[b]Círculo:[/b]\n"
                    f"A = π.r² = 3,14 x {fmt(r)}² = [b]{area:.1f}[/b]\n"
                    f"C = 2.π.r = 2 x 3,14 x {fmt(r)} = [b]{perimetro:.1f}[/b]\n"
                    f"(Comprimento da Circunferência)"
                )

            elif self.forma_atual == "square":
                l = vals["Lado"]
                Line(rectangle=(cx - l/2, cy - l/2, l, l), width=2)
                self.desenhar_texto_canvas(f"Lado: {fmt(l)}", cx - 20, cy + l/2 + 5)

                area = l**2
                perimetro = 4 * l
                texto_passo = (
                    f"[b]Quadrado:[/b]\n"
                    f"A = L² = {fmt(l)} x {fmt(l)} = [b]{area:.0f}[/b]\n"
                    f"P = L + L + L + L = 4 x {fmt(l)} = [b]{perimetro:.0f}[/b]\n"
                    f"(Soma dos 4 lados)"
                )

            elif self.forma_atual == "rectangle":
                b = vals["Base"]
                h = vals["Altura"]
                Line(rectangle=(cx - b/2, cy - h/2, b, h), width=2)
                self.desenhar_texto_canvas(f"Base: {fmt(b)}", cx - 20, cy - h/2 - 20)
                self.desenhar_texto_canvas(f"Alt: {fmt(h)}", cx + b/2 + 5, cy)

                area = b * h
                perimetro = 2*b + 2*h
                texto_passo = (
                    f"[b]Retângulo:[/b]\n"
                    f"A = Base x Altura = {fmt(b)} x {fmt(h)} = [b]{area:.0f}[/b]\n"
                    f"P = Soma dos lados = {fmt(b)} + {fmt(b)} + {fmt(h)} + {fmt(h)} = [b]{perimetro:.0f}[/b]"
                )

            elif self.forma_atual == "triangle":
                b = vals["Base"]
                h = vals["Altura"]
                # Triângulo isósceles
                pts = [cx - b/2, cy - h/2, cx + b/2, cy - h/2, cx, cy + h/2, cx - b/2, cy - h/2]
                Line(points=pts, width=2)

                # Linha da altura pontilhada
                Color(0.5, 0.5, 0.5, 1)
                Line(points=[cx, cy + h/2, cx, cy - h/2], width=1, dash_length=5)
                self.desenhar_texto_canvas(f"Alt: {fmt(h)}", cx + 2, cy)
                self.desenhar_texto_canvas(f"Base: {fmt(b)}", cx - 20, cy - h/2 - 20)

                area = (b * h) / 2
                lado_inclinado = math.sqrt((b/2)**2 + h**2)
                perimetro = b + 2 * lado_inclinado

                texto_passo = (
                    f"[b]Triângulo (Isósceles):[/b]\n"
                    f"A = (Base x Altura) / 2 = ({fmt(b)} x {fmt(h)}) / 2 = [b]{area:.1f}[/b]\n"
                    # CORREÇÃO NA LINHA ABAIXO:
                    # Antes: {fmt(lado_inclinado):.1f} (Erro)
                    # Agora: {lado_inclinado:.1f}      (Correto)
                    f"P = Soma dos lados ≈ {fmt(b)} + {lado_inclinado:.1f} + {lado_inclinado:.1f} = [b]{perimetro:.1f}[/b]"
                )

            elif self.forma_atual == "trapezoid":
                B = vals["Base Maior"]
                b = vals["Base Menor"]
                h = vals["Altura"]

                pts = [
                    cx - B/2, cy - h/2,  # Inf Esq
                    cx + B/2, cy - h/2,  # Inf Dir
                    cx + b/2, cy + h/2,  # Sup Dir
                    cx - b/2, cy + h/2,  # Sup Esq
                    cx - B/2, cy - h/2   # Fecha
                ]
                Line(points=pts, width=2)

                self.desenhar_texto_canvas(f"b: {fmt(b)}", cx - 10, cy + h/2 + 5)
                self.desenhar_texto_canvas(f"B: {fmt(B)}", cx - 10, cy - h/2 - 20)
                self.desenhar_texto_canvas(f"h: {fmt(h)}", cx + B/2 + 5, cy) # Aproximado

                area = ((B + b) * h) / 2
                cateto = abs(B - b) / 2
                lado_inclinado = math.sqrt(cateto**2 + h**2)
                perimetro = B + b + 2 * lado_inclinado

                texto_passo = (
                    f"[b]Trapézio:[/b]\n"
                    f"A = ((Maior + Menor) x Altura) / 2\n"
                    f"A = (({fmt(B)} + {fmt(b)}) x {fmt(h)}) / 2 = [b]{area:.1f}[/b]\n"
                    f"P = Soma dos lados ≈ [b]{perimetro:.1f}[/b]"
                )

        self.lbl_passos.text = texto_passo

    def voltar(self, tela_nome):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = tela_nome