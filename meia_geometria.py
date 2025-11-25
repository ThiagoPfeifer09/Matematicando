<<<<<<< HEAD
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton,MDFlatButton
from kivy.graphics import Color, Line
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

# =================== TELA PRINCIPAL ÁLGEBRA ===================
class GeometriaTela(Screen):
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
        self.digita_texto(self.title_label, "GEOMETRIA")

        # Botão voltar
        self.back_button = MDIconButton(
            icon='arrow-left',
            pos_hint={'x': 0, 'top': 1},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # cor branca
            on_release=lambda x: self.voltar("conteudos")
        )
        layout.add_widget(self.back_button)

        # Boneco
        boneco = Image(
            source="boneco_geometria.png",
            size_hint=(0.5, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.65}
        )
        layout.add_widget(boneco)

        # Botões principais
        btn_representacoes = self.create_card_button(
            "Representações",
            0.3, 0.35,
            lambda: self.ir_para("geometria_representacoes")
        )
        btn_definicoes = self.create_card_button(
            "Definições",
            0.3, 0.2,
            lambda: self.ir_para("geometria_definicoes")
        )

        layout.add_widget(btn_representacoes)
        layout.add_widget(btn_definicoes)
        self.add_widget(layout)

    # Funções auxiliares
    def digita_texto(self, label, texto, i=0):
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i + 1), 0.05)

    def create_card_button(self, text, x, y, callback):
        card = MDCard(
            size_hint=(0.4, 0.08),
            pos_hint={"x": x, "y": y},
            md_bg_color=(0.2, 0.2, 0.6, 0.85),
            radius=[20],
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
        card.bind(on_release=lambda *a: callback())
        return card


    def ir_para(self, tela_nome):
        self.manager.transition = SlideTransition(direction="left", duration=0.4)
        self.manager.current = tela_nome

    def voltar(self, tela_nome):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = tela_nome


# =================== TELA DEFINIÇÕES ===================
class DefinicoesGeometria(Screen):
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
        self.digita_texto(self.title_label, "DEFINIÇÕES GEOMETRIA")

        # Lista de imagens (uma para cada operação)
        imagens = [
            "quadrado.jpeg",
            "triangulo.jpeg",
            "circulo.jpeg",
            "retangulo.jpeg"
        ]

        pos_y = [0.68, 0.68, 0.30, 0.30]
        pos_x = [0.26, 0.74, 0.26, 0.74]

        for i, img in enumerate(imagens):
            card = MDCard(
                size_hint=(0.45, 0.32),
                pos_hint={"center_x": pos_x[i], "center_y": pos_y[i]},
                radius=[20],
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
        self.manager.current = "geometria_tela"




class GeometriaRepresentacoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = FloatLayout()

        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        root.add_widget(fundo)

        titulo = MDLabel(
            text="📐 Representações Geométricas",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H5",
            size_hint=(1, None),
            height=60,
            pos_hint={"center_x": 0.5, "top": 0.98},
        )
        back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={"x": 0, "top": 0.98},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            on_release=lambda x: self.voltar("geometria_tela"),
        )
        root.add_widget(titulo)
        root.add_widget(back_button)

        main_box = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=[25, 70, 25, 25],
            size_hint=(1, 0.9),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        botoes_box = GridLayout(
            cols=3,
            spacing=10,
            size_hint=(1, 0.18),
            row_force_default=True,
            row_default_height="60dp"
        )

        formas = [
            ("Círculo", "circle", "circle-outline"),
            ("Quadrado", "square", "square-outline"),
            ("Retângulo", "rectangle", "rectangle-outline"),
            ("Triângulo", "triangle", "triangle-outline"),
            ("Trapézio", "trapezoid", "shape-outline"),
        ]

        for nome, forma, icone in formas:
            btn = MDFillRoundFlatIconButton(
                text=nome,
                icon=icone,
                on_release=lambda x, f=forma: self.selecionar_forma(f),
                md_bg_color=(0.2, 0.4, 0.7, 1),
                text_color=(1, 1, 1, 1),
                icon_color=(1, 1, 1, 1),
            )
            botoes_box.add_widget(btn)

        main_box.add_widget(botoes_box)

        meio_box = BoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint=(1, 0.55)
        )

        self.card_desenho = MDCard(
            orientation="vertical",
            size_hint=(0.6, 1),
            radius=[25],
            md_bg_color=(1, 1, 1, 0.95),
            padding=10
        )
        self.drawing_area = Widget()
        self.card_desenho.add_widget(self.drawing_area)

        self.slider_area = BoxLayout(
            orientation="vertical",
            spacing=15,
            size_hint=(0.4, 1)
        )

        meio_box.add_widget(self.card_desenho)
        meio_box.add_widget(self.slider_area)
        main_box.add_widget(meio_box)

        # Resultados card: agora com botão "Passo a passo"
        self.card_resultados = MDCard(
            orientation="vertical",
            size_hint=(1, 0.33),
            radius=[25],
            md_bg_color=(0.95, 0.97, 1, 0.95),
            padding=12,
        )

        header_box = BoxLayout(orientation="horizontal", size_hint_y=None, height="36dp")
        self.label_formulas = MDLabel(
            text="Selecione uma forma para ver as fórmulas:",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="Subtitle1"
        )
        header_box.add_widget(self.label_formulas)

        # botão passo a passo
        self.btn_passo = MDFlatButton(
            text="Passo a passo",
            on_release=lambda x: self.abrir_passo_a_passo(),
            pos_hint={"right": 1}
        )
        header_box.add_widget(self.btn_passo)
        self.card_resultados.add_widget(header_box)

        # labels resumidos
        self.label_area = MDLabel(
            text="Área: —",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )
        self.label_perimetro = MDLabel(
            text="Perímetro: —",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )
        self.card_resultados.add_widget(self.label_area)
        self.card_resultados.add_widget(self.label_perimetro)

        # scroll para passo a passo dinâmico
        scroll = ScrollView(size_hint=(1, 1))
        self.label_passo = MDLabel(
            text="",
            halign="left",
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            font_style="Body1",
            markup=True,
        )
        scroll.add_widget(self.label_passo)
        self.card_resultados.add_widget(scroll)


        main_box.add_widget(self.card_resultados)
        root.add_widget(main_box)
        self.add_widget(root)

        # estado
        self.forma_atual = None
        self.parametros = {}
        self.dialog_passo = None
        self.ultima_geracao_steps = ""  # cache do texto atual do passo a passo

    def voltar(self, tela_nome):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = tela_nome

    def selecionar_forma(self, forma):
        self.forma_atual = forma
        self.slider_area.clear_widgets()
        self.parametros.clear()

        explicacoes = {
            "circle": ("Círculo:\nÁrea = π·r²\nPerímetro = 2·π·r", [("raio", 1, 100, 40)]),
            "square": ("Quadrado:\nÁrea = L²\nPerímetro = soma dos 4 lados", [("lado", 1, 100, 60)]),
            "rectangle": ("Retângulo:\nÁrea = base × altura\nPerímetro = soma dos 4 lados",
                          [("base", 1, 120, 80), ("altura", 1, 100, 50)]),
            "triangle": ("Triângulo:\nÁrea = (base × altura)/2\nPerímetro ≈ base + 2·√((base/2)² + altura²)",
                         [("base", 1, 100, 70), ("altura", 1, 80, 50)]),
            "trapezoid": ("Trapézio:\nÁrea = ((B + b) × h)/2\nPerímetro = B + b + 2·lado",
                          [("base_maior", 1, 120, 90), ("base_menor", 1, 100, 60), ("altura", 1, 80, 50)])
        }

        self.label_formulas.text = explicacoes[forma][0]
        for nome, min_v, max_v, valor in explicacoes[forma][1]:
            self.add_slider(nome, min_v, max_v, valor)

        self.atualizar_desenho()

    def add_slider(self, nome, min_v, max_v, valor):
        lbl = MDLabel(
            text=f"{nome.capitalize()}: {valor:.0f}",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            halign="center",
            size_hint_y=None,
            height="28dp"
        )
        sld = Slider(min=min_v, max=max_v, value=valor)
        sld.bind(value=lambda instance, val, n=nome, l=lbl: self.on_slider_change(n, val, l))
        self.parametros[nome] = valor
        self.slider_area.add_widget(lbl)
        self.slider_area.add_widget(sld)

    def on_slider_change(self, nome, valor, label):
        self.parametros[nome] = valor
        label.text = f"{nome.capitalize()}: {valor:.0f}"
        self.atualizar_desenho()

    def draw_text(self, canvas, text, pos, color=(0, 0, 0, 1)):
        label = CoreLabel(text=text, font_size=18, color=color)
        label.refresh()
        texture = label.texture
        tw, th = texture.size
        x, y = pos
        with canvas:
            Color(1, 1, 1, 0.8)
            Rectangle(pos=(x - 2, y - 2), size=(tw + 4, th + 4))
            Color(*color)
            Rectangle(texture=texture, pos=pos, size=texture.size)

    def atualizar_desenho(self):
        self.drawing_area.canvas.clear()
        with self.drawing_area.canvas:
            Color(0, 0, 0)
            cx, cy = self.drawing_area.center
            escala = 1.8

            # === cálculo e desenho ===
            if self.forma_atual == "circle":
                r = self.parametros.get("raio", 0)
                Line(circle=(cx, cy, r * escala), width=2)
                area = math.pi * (r ** 2)
                per = 2 * math.pi * r

            elif self.forma_atual == "square":
                L = self.parametros.get("lado", 0)
                Line(rectangle=(cx - L, cy - L, 2 * L, 2 * L), width=2)
                area = L ** 2
                per = 4 * L

            elif self.forma_atual == "rectangle":
                b = self.parametros.get("base", 0)
                h = self.parametros.get("altura", 0)
                Line(rectangle=(cx - b, cy - h / 2, 2 * b, h), width=2)
                area = b * h
                per = 2 * (b + h)

            elif self.forma_atual == "triangle":
                b = self.parametros.get("base", 0)
                h = self.parametros.get("altura", 0)
                Line(points=[cx - b, cy - h / 2, cx + b, cy - h / 2, cx, cy + h / 2, cx - b, cy - h / 2], width=2)
                area = (b * h) / 2
                per = b + 2 * math.sqrt((b / 2) ** 2 + h ** 2)

            elif self.forma_atual == "trapezoid":
                B = self.parametros.get("base_maior", 0)
                b = self.parametros.get("base_menor", 0)
                h = self.parametros.get("altura", 0)
                lado = math.sqrt(h ** 2 + ((B - b) / 2) ** 2)
                Line(points=[
                    cx - B, cy - h / 2,
                    cx + B, cy - h / 2,
                    cx + b, cy + h / 2,
                    cx - b, cy + h / 2,
                    cx - B, cy - h / 2
                ], width=2)
                area = ((B + b) * h) / 2
                per = B + b + 2 * lado

            else:
                area = per = 0

        # atualiza textos
        self.label_area.text = f"Área = {area:.2f}"
        self.label_perimetro.text = f"Perímetro = {per:.2f}"

        # atualiza explicação detalhada diretamente no card
        self.label_passo.text = self.gerar_passo_a_passo(self.forma_atual, self.parametros, area, per)

    def gerar_passo_a_passo(self, forma, params, area_val, per_val):
        if not forma:
            return "Selecione uma forma para começar."

        fmt = lambda n: f"{n:.2f}".rstrip("0").rstrip(".")

        texto = ""
        if forma == "circle":
            r = params.get("raio", 0)
            texto = (
                f"[b]Círculo[/b]\n"
                f"Fórmulas:\nÁrea = π·r²\nPerímetro = 2·π·r\n\n"
                f"Substituindo:\n"
                f"r = {fmt(r)}\n"
                f"A = π·({fmt(r)})² = {fmt(math.pi * r * r)}\n"
                f"P = 2·π·{fmt(r)} = {fmt(2 * math.pi * r)}"
            )

        elif forma == "square":
            L = params.get("lado", 0)
            texto = (
                f"[b]Quadrado[/b]\n"
                f"Área = L² → ({fmt(L)})² = {fmt(L*L)}\n"
                f"Perímetro = soma dos 4 lados = 4·{fmt(L)} = {fmt(4*L)}"
            )

        elif forma == "rectangle":
            b = params.get("base", 0)
            h = params.get("altura", 0)
            texto = (
                f"[b]Retângulo[/b]\n"
                f"Área = base × altura = {fmt(b)} × {fmt(h)} = {fmt(b*h)}\n"
                f"Perímetro = 2×(base + altura) = 2×({fmt(b)} + {fmt(h)}) = {fmt(2*(b+h))}"
            )

        elif forma == "triangle":
            b = params.get("base", 0)
            h = params.get("altura", 0)
            texto = (
                f"[b]Triângulo[/b]\n"
                f"Área = (base × altura)/2 = ({fmt(b)} × {fmt(h)})/2 = {fmt((b*h)/2)}\n"
                f"Perímetro ≈ base + 2·√((base/2)² + altura²) = {fmt(b + 2*math.sqrt((b/2)**2 + h**2))}"
            )

        elif forma == "trapezoid":
            B = params.get("base_maior", 0)
            b = params.get("base_menor", 0)
            h = params.get("altura", 0)
            lado = math.sqrt(h**2 + ((B - b) / 2)**2)
            texto = (
                f"[b]Trapézio[/b]\n"
                f"Área = ((B + b) × h)/2 = (({fmt(B)} + {fmt(b)}) × {fmt(h)})/2 = {fmt(((B+b)*h)/2)}\n"
                f"Perímetro = B + b + 2·lado = {fmt(B)} + {fmt(b)} + 2×{fmt(lado)} = {fmt(B+b+2*lado)}"
            )

        return texto

    def abrir_passo_a_passo(self):
        # cria ou atualiza dialog com o texto já gerado (cache)
        texto = self.ultima_geracao_steps or self.gerar_passo_a_passo(self.forma_atual, self.parametros, 0, 0)
        if self.dialog_passo and self.dialog_passo.open:
            # se já aberto, atualiza conteúdo do texto (não obrigatório)
            try:
                self.dialog_passo.text = texto
            except Exception:
                pass
            return

        # Criar dialog com rolagem caso o texto seja longo
        # Usamos MDDialog simples com propriedade text (compatível com versões antigas)
        self.dialog_passo = MDDialog(
            title="Passo a passo",
            text=texto,
            size_hint=(0.9, None),
            height="420dp",
            buttons=[
                MDFlatButton(text="Fechar", on_release=lambda *a: self.dialog_passo.dismiss())
            ]
        )
        self.dialog_passo.open()
=======
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton,MDFlatButton
from kivy.graphics import Color, Line
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

# =================== TELA PRINCIPAL ÁLGEBRA ===================
class GeometriaTela(Screen):
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
        self.digita_texto(self.title_label, "GEOMETRIA")

        # Botão voltar
        self.back_button = MDIconButton(
            icon='arrow-left',
            pos_hint={'x': 0, 'top': 1},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # cor branca
            on_release=lambda x: self.voltar("conteudos")
        )
        layout.add_widget(self.back_button)

        # Boneco
        boneco = Image(
            source="boneco_geometria.png",
            size_hint=(0.5, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.65}
        )
        layout.add_widget(boneco)

        # Botões principais
        btn_representacoes = self.create_card_button(
            "Representações",
            0.3, 0.35,
            lambda: self.ir_para("geometria_representacoes")
        )
        btn_definicoes = self.create_card_button(
            "Definições",
            0.3, 0.2,
            lambda: self.ir_para("geometria_definicoes")
        )

        layout.add_widget(btn_representacoes)
        layout.add_widget(btn_definicoes)
        self.add_widget(layout)

    # Funções auxiliares
    def digita_texto(self, label, texto, i=0):
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i + 1), 0.05)

    def create_card_button(self, text, x, y, callback):
        card = MDCard(
            size_hint=(0.4, 0.08),
            pos_hint={"x": x, "y": y},
            md_bg_color=(0.2, 0.2, 0.6, 0.85),
            radius=[20],
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
        card.bind(on_release=lambda *a: callback())
        return card


    def ir_para(self, tela_nome):
        self.manager.transition = SlideTransition(direction="left", duration=0.4)
        self.manager.current = tela_nome

    def voltar(self, tela_nome):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = tela_nome


# =================== TELA DEFINIÇÕES ===================
class DefinicoesGeometria(Screen):
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
        self.digita_texto(self.title_label, "DEFINIÇÕES GEOMETRIA")

        # Lista de imagens (uma para cada operação)
        imagens = [
            "quadrado.jpeg",
            "triangulo.jpeg",
            "circulo.jpeg",
            "retangulo.jpeg"
        ]

        pos_y = [0.68, 0.68, 0.30, 0.30]
        pos_x = [0.26, 0.74, 0.26, 0.74]

        for i, img in enumerate(imagens):
            card = MDCard(
                size_hint=(0.45, 0.32),
                pos_hint={"center_x": pos_x[i], "center_y": pos_y[i]},
                radius=[20],
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
        self.manager.current = "geometria_tela"




class GeometriaRepresentacoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = FloatLayout()

        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        root.add_widget(fundo)

        titulo = MDLabel(
            text="📐 Representações Geométricas",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H5",
            size_hint=(1, None),
            height=60,
            pos_hint={"center_x": 0.5, "top": 0.98},
        )
        back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={"x": 0, "top": 0.98},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            on_release=lambda x: self.voltar("geometria_tela"),
        )
        root.add_widget(titulo)
        root.add_widget(back_button)

        main_box = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=[25, 70, 25, 25],
            size_hint=(1, 0.9),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        botoes_box = GridLayout(
            cols=3,
            spacing=10,
            size_hint=(1, 0.18),
            row_force_default=True,
            row_default_height="60dp"
        )

        formas = [
            ("Círculo", "circle", "circle-outline"),
            ("Quadrado", "square", "square-outline"),
            ("Retângulo", "rectangle", "rectangle-outline"),
            ("Triângulo", "triangle", "triangle-outline"),
            ("Trapézio", "trapezoid", "shape-outline"),
        ]

        for nome, forma, icone in formas:
            btn = MDFillRoundFlatIconButton(
                text=nome,
                icon=icone,
                on_release=lambda x, f=forma: self.selecionar_forma(f),
                md_bg_color=(0.2, 0.4, 0.7, 1),
                text_color=(1, 1, 1, 1),
                icon_color=(1, 1, 1, 1),
            )
            botoes_box.add_widget(btn)

        main_box.add_widget(botoes_box)

        meio_box = BoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint=(1, 0.55)
        )

        self.card_desenho = MDCard(
            orientation="vertical",
            size_hint=(0.6, 1),
            radius=[25],
            md_bg_color=(1, 1, 1, 0.95),
            padding=10
        )
        self.drawing_area = Widget()
        self.card_desenho.add_widget(self.drawing_area)

        self.slider_area = BoxLayout(
            orientation="vertical",
            spacing=15,
            size_hint=(0.4, 1)
        )

        meio_box.add_widget(self.card_desenho)
        meio_box.add_widget(self.slider_area)
        main_box.add_widget(meio_box)

        # Resultados card: agora com botão "Passo a passo"
        self.card_resultados = MDCard(
            orientation="vertical",
            size_hint=(1, 0.33),
            radius=[25],
            md_bg_color=(0.95, 0.97, 1, 0.95),
            padding=12,
        )

        header_box = BoxLayout(orientation="horizontal", size_hint_y=None, height="36dp")
        self.label_formulas = MDLabel(
            text="Selecione uma forma para ver as fórmulas:",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="Subtitle1"
        )
        header_box.add_widget(self.label_formulas)

        # botão passo a passo
        self.btn_passo = MDFlatButton(
            text="Passo a passo",
            on_release=lambda x: self.abrir_passo_a_passo(),
            pos_hint={"right": 1}
        )
        header_box.add_widget(self.btn_passo)
        self.card_resultados.add_widget(header_box)

        # labels resumidos
        self.label_area = MDLabel(
            text="Área: —",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )
        self.label_perimetro = MDLabel(
            text="Perímetro: —",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )
        self.card_resultados.add_widget(self.label_area)
        self.card_resultados.add_widget(self.label_perimetro)

        # scroll para passo a passo dinâmico
        scroll = ScrollView(size_hint=(1, 1))
        self.label_passo = MDLabel(
            text="",
            halign="left",
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            font_style="Body1",
            markup=True,
        )
        scroll.add_widget(self.label_passo)
        self.card_resultados.add_widget(scroll)


        main_box.add_widget(self.card_resultados)
        root.add_widget(main_box)
        self.add_widget(root)

        # estado
        self.forma_atual = None
        self.parametros = {}
        self.dialog_passo = None
        self.ultima_geracao_steps = ""  # cache do texto atual do passo a passo

    def voltar(self, tela_nome):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = tela_nome

    def selecionar_forma(self, forma):
        self.forma_atual = forma
        self.slider_area.clear_widgets()
        self.parametros.clear()

        explicacoes = {
            "circle": ("Círculo:\nÁrea = π·r²\nPerímetro = 2·π·r", [("raio", 1, 100, 40)]),
            "square": ("Quadrado:\nÁrea = L²\nPerímetro = soma dos 4 lados", [("lado", 1, 100, 60)]),
            "rectangle": ("Retângulo:\nÁrea = base × altura\nPerímetro = soma dos 4 lados",
                          [("base", 1, 120, 80), ("altura", 1, 100, 50)]),
            "triangle": ("Triângulo:\nÁrea = (base × altura)/2\nPerímetro ≈ base + 2·√((base/2)² + altura²)",
                         [("base", 1, 100, 70), ("altura", 1, 80, 50)]),
            "trapezoid": ("Trapézio:\nÁrea = ((B + b) × h)/2\nPerímetro = B + b + 2·lado",
                          [("base_maior", 1, 120, 90), ("base_menor", 1, 100, 60), ("altura", 1, 80, 50)])
        }

        self.label_formulas.text = explicacoes[forma][0]
        for nome, min_v, max_v, valor in explicacoes[forma][1]:
            self.add_slider(nome, min_v, max_v, valor)

        self.atualizar_desenho()

    def add_slider(self, nome, min_v, max_v, valor):
        lbl = MDLabel(
            text=f"{nome.capitalize()}: {valor:.0f}",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            halign="center",
            size_hint_y=None,
            height="28dp"
        )
        sld = Slider(min=min_v, max=max_v, value=valor)
        sld.bind(value=lambda instance, val, n=nome, l=lbl: self.on_slider_change(n, val, l))
        self.parametros[nome] = valor
        self.slider_area.add_widget(lbl)
        self.slider_area.add_widget(sld)

    def on_slider_change(self, nome, valor, label):
        self.parametros[nome] = valor
        label.text = f"{nome.capitalize()}: {valor:.0f}"
        self.atualizar_desenho()

    def draw_text(self, canvas, text, pos, color=(0, 0, 0, 1)):
        label = CoreLabel(text=text, font_size=18, color=color)
        label.refresh()
        texture = label.texture
        tw, th = texture.size
        x, y = pos
        with canvas:
            Color(1, 1, 1, 0.8)
            Rectangle(pos=(x - 2, y - 2), size=(tw + 4, th + 4))
            Color(*color)
            Rectangle(texture=texture, pos=pos, size=texture.size)

    def atualizar_desenho(self):
        self.drawing_area.canvas.clear()
        with self.drawing_area.canvas:
            Color(0, 0, 0)
            cx, cy = self.drawing_area.center
            escala = 1.8

            # === cálculo e desenho ===
            if self.forma_atual == "circle":
                r = self.parametros.get("raio", 0)
                Line(circle=(cx, cy, r * escala), width=2)
                area = math.pi * (r ** 2)
                per = 2 * math.pi * r

            elif self.forma_atual == "square":
                L = self.parametros.get("lado", 0)
                Line(rectangle=(cx - L, cy - L, 2 * L, 2 * L), width=2)
                area = L ** 2
                per = 4 * L

            elif self.forma_atual == "rectangle":
                b = self.parametros.get("base", 0)
                h = self.parametros.get("altura", 0)
                Line(rectangle=(cx - b, cy - h / 2, 2 * b, h), width=2)
                area = b * h
                per = 2 * (b + h)

            elif self.forma_atual == "triangle":
                b = self.parametros.get("base", 0)
                h = self.parametros.get("altura", 0)
                Line(points=[cx - b, cy - h / 2, cx + b, cy - h / 2, cx, cy + h / 2, cx - b, cy - h / 2], width=2)
                area = (b * h) / 2
                per = b + 2 * math.sqrt((b / 2) ** 2 + h ** 2)

            elif self.forma_atual == "trapezoid":
                B = self.parametros.get("base_maior", 0)
                b = self.parametros.get("base_menor", 0)
                h = self.parametros.get("altura", 0)
                lado = math.sqrt(h ** 2 + ((B - b) / 2) ** 2)
                Line(points=[
                    cx - B, cy - h / 2,
                    cx + B, cy - h / 2,
                    cx + b, cy + h / 2,
                    cx - b, cy + h / 2,
                    cx - B, cy - h / 2
                ], width=2)
                area = ((B + b) * h) / 2
                per = B + b + 2 * lado

            else:
                area = per = 0

        # atualiza textos
        self.label_area.text = f"Área = {area:.2f}"
        self.label_perimetro.text = f"Perímetro = {per:.2f}"

        # atualiza explicação detalhada diretamente no card
        self.label_passo.text = self.gerar_passo_a_passo(self.forma_atual, self.parametros, area, per)

    def gerar_passo_a_passo(self, forma, params, area_val, per_val):
        if not forma:
            return "Selecione uma forma para começar."

        fmt = lambda n: f"{n:.2f}".rstrip("0").rstrip(".")

        texto = ""
        if forma == "circle":
            r = params.get("raio", 0)
            texto = (
                f"[b]Círculo[/b]\n"
                f"Fórmulas:\nÁrea = π·r²\nPerímetro = 2·π·r\n\n"
                f"Substituindo:\n"
                f"r = {fmt(r)}\n"
                f"A = π·({fmt(r)})² = {fmt(math.pi * r * r)}\n"
                f"P = 2·π·{fmt(r)} = {fmt(2 * math.pi * r)}"
            )

        elif forma == "square":
            L = params.get("lado", 0)
            texto = (
                f"[b]Quadrado[/b]\n"
                f"Área = L² → ({fmt(L)})² = {fmt(L*L)}\n"
                f"Perímetro = soma dos 4 lados = 4·{fmt(L)} = {fmt(4*L)}"
            )

        elif forma == "rectangle":
            b = params.get("base", 0)
            h = params.get("altura", 0)
            texto = (
                f"[b]Retângulo[/b]\n"
                f"Área = base × altura = {fmt(b)} × {fmt(h)} = {fmt(b*h)}\n"
                f"Perímetro = 2×(base + altura) = 2×({fmt(b)} + {fmt(h)}) = {fmt(2*(b+h))}"
            )

        elif forma == "triangle":
            b = params.get("base", 0)
            h = params.get("altura", 0)
            texto = (
                f"[b]Triângulo[/b]\n"
                f"Área = (base × altura)/2 = ({fmt(b)} × {fmt(h)})/2 = {fmt((b*h)/2)}\n"
                f"Perímetro ≈ base + 2·√((base/2)² + altura²) = {fmt(b + 2*math.sqrt((b/2)**2 + h**2))}"
            )

        elif forma == "trapezoid":
            B = params.get("base_maior", 0)
            b = params.get("base_menor", 0)
            h = params.get("altura", 0)
            lado = math.sqrt(h**2 + ((B - b) / 2)**2)
            texto = (
                f"[b]Trapézio[/b]\n"
                f"Área = ((B + b) × h)/2 = (({fmt(B)} + {fmt(b)}) × {fmt(h)})/2 = {fmt(((B+b)*h)/2)}\n"
                f"Perímetro = B + b + 2·lado = {fmt(B)} + {fmt(b)} + 2×{fmt(lado)} = {fmt(B+b+2*lado)}"
            )

        return texto

    def abrir_passo_a_passo(self):
        # cria ou atualiza dialog com o texto já gerado (cache)
        texto = self.ultima_geracao_steps or self.gerar_passo_a_passo(self.forma_atual, self.parametros, 0, 0)
        if self.dialog_passo and self.dialog_passo.open:
            # se já aberto, atualiza conteúdo do texto (não obrigatório)
            try:
                self.dialog_passo.text = texto
            except Exception:
                pass
            return

        # Criar dialog com rolagem caso o texto seja longo
        # Usamos MDDialog simples com propriedade text (compatível com versões antigas)
        self.dialog_passo = MDDialog(
            title="Passo a passo",
            text=texto,
            size_hint=(0.9, None),
            height="420dp",
            buttons=[
                MDFlatButton(text="Fechar", on_release=lambda *a: self.dialog_passo.dismiss())
            ]
        )
        self.dialog_passo.open()
>>>>>>> 2269faa7446d3e2311a76c04b2417a3f19598fc4
