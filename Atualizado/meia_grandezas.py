from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.slider import MDSlider
from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton
from random import choice
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.carousel import Carousel
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
# =================== TELA PRINCIPAL GRANDEZAS ===================
class GrandezasTela(Screen):
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
            source="Bonecos/titulo_grandezas.webp",
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
            source="Bonecos/Boneco_Grandezas.webp",
            size_hint=(0.47, 0.47),
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
            "Representações", "ruler", lambda: self.ir_para("grandezas_representacoes")
        ))

        container.add_widget(self.create_icon_button(
            "Definições", "scale-balance", lambda: self.ir_para("grandezas_definicoes")
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
        """Ícones de medidas escuros"""
        # Ícones: Régua, Balança, Relógio, Termômetro, Fita Métrica
        icones = [
            "ruler", "scale-balance", "timer-outline",
            "thermometer", "tape-measure", "weight-kilogram"
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

# =================== TELA DEFINIÇÕES ===================

from meia_tela import BaseDefinicoesTela

class GrandezasDefinicoesTela(BaseDefinicoesTela):
    def __init__(self, **kwargs):
        super().__init__(titulo_secao="Conversão de Medidas", **kwargs)

    def voltar(self, instance):
        # Ajuste "grandezas_tela" para o nome exato registrado no ScreenManager
        self.manager.transition.direction = "right"
        self.manager.current = "grandezas_tela"

    def setup_slides(self):
        # ---------------------------------------------------------
        # SLIDE 1: COMPRIMENTO
        # ---------------------------------------------------------
        texto_comprimento = (
            "A unidade base é o [b]Metro (m)[/b].\n"
            "Para transformar, usamos a base 10.\n\n"
            "[b]REGRA PRÁTICA:[/b]\n"
            "• Do maior para o menor (km → m): [b]Multiplica[/b] por 10, 100 ou 1000.\n"
            "• Do menor para o maior (m → km): [b]Divide[/b] por 10, 100 ou 1000.\n\n"
            "[b]Exemplo:[/b]\n"
            "1 km = 1.000 metros\n"
            "1 metro = 100 centímetros"
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Comprimento",
            texto_definicao=texto_comprimento,
            icone="ruler"
        ))

        # ---------------------------------------------------------
        # SLIDE 2: MASSA
        # ---------------------------------------------------------
        texto_massa = (
            "Massa mede a quantidade de matéria. A unidade padrão é o [b]Grama (g)[/b] ou Quilograma (kg).\n\n"
            "[b]CONVERSÃO COMUM:[/b]\n"
            "• 1 kg = 1.000 g\n"
            "• 1 tonelada = 1.000 kg\n\n"
            "Para passar de Kg para Gramas, basta multiplicar por 1000 (adicionar três zeros)."
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Massa",
            texto_definicao=texto_massa,
            icone="weight-kilogram"
        ))

        # ---------------------------------------------------------
        # SLIDE 3: VOLUME / CAPACIDADE
        # ---------------------------------------------------------
        texto_volume = (
            "Para líquidos, usamos o [b]Litro (L)[/b] e o Mililitro (ml).\n\n"
            "[b]RELAÇÃO PRINCIPAL:[/b]\n"
            "• 1 Litro = 1.000 ml\n\n"
            "[b]Curiosidade:[/b]\n"
            "1 litro de água ocupa exatamente o espaço de um cubo de 10cm x 10cm x 10cm (1 decímetro cúbico)."
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Volume e Capacidade",
            texto_definicao=texto_volume,
            icone="cup-water"
        ))

        # ---------------------------------------------------------
        # SLIDE 4: TEMPO
        # ---------------------------------------------------------
        texto_tempo = (
            "O tempo [b]NÃO[/b] é decimal! Ele usa o sistema sexagesimal (base 60).\n\n"
            "[b]TABELA:[/b]\n"
            "• 1 Hora = 60 minutos\n"
            "• 1 Minuto = 60 segundos\n\n"
            "[b]Atenção:[/b] 1,5 horas não é 1h e 50min, e sim 1 hora e 30 minutos (metade de 60)."
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Tempo",
            texto_definicao=texto_tempo,
            icone="clock-time-four-outline"
        ))

        # ---------------------------------------------------------
        # SLIDE 5: TEMPERATURA
        # ---------------------------------------------------------
        texto_temp = (
            "Mede o grau de agitação das moléculas. No Brasil usamos a escala [b]Celsius (°C)[/b].\n\n"
            "[b]PONTOS CHAVE:[/b]\n"
            "• 0°C: A água congela.\n"
            "• 100°C: A água ferve.\n\n"
            "Existem outras escalas como Fahrenheit (EUA) e Kelvin (Científica)."
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Temperatura",
            texto_definicao=texto_temp,
            icone="thermometer"
        ))




from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from random import choice

# KivyMD Imports
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.slider import MDSlider
# Removemos o MDProgressBar

class GrandezasRepresentacoes(Screen):
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
            on_release=lambda x: self.voltar("grandezas_tela")
        ))

        self.title_label = Label(
            text="CONVERSOR",
            color=(0, 0, 0, 1),
            font_name="BungeeShade",
            font_size="28sp",
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "top": 0.96},
        )
        layout.add_widget(self.title_label)

        # 3. ÁREA VISUAL HERO (Ícone + Valor Gigante)
        self.hero_box = BoxLayout(
            orientation="vertical",
            size_hint=(1, 0.25),
            pos_hint={"center_x": 0.5, "top": 0.85},
            padding=[0, dp(10), 0, 0]
        )

        self.hero_icon = MDIconButton(
            icon="ruler",
            icon_size="90sp",
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color=(0.2, 0.6, 0.4, 1),
            disabled=True
        )
        self.hero_box.add_widget(self.hero_icon)

        self.hero_value = MDLabel(
            text="10 m",
            halign="center",
            font_style="H3",
            theme_text_color="Custom",
            text_color=(0.2, 0.6, 0.4, 1),
            bold=True
        )
        self.hero_box.add_widget(self.hero_value)

        layout.add_widget(self.hero_box)

        # 4. CARD DE CONTROLE E RESULTADO (Painel Principal)
        self.panel_card = MDCard(
            orientation="vertical",
            size_hint=(0.92, 0.55),
            pos_hint={"center_x": 0.5, "y": 0.02},
            radius=[25],
            md_bg_color=(1, 1, 1, 0.95),
            elevation=6,
            padding=dp(20),
            spacing=dp(10) # Espaçamento reduzido entre elementos
        )

        # --- REMOVIDO: Label e Barra de Progresso ---

        # -- Slider (Agora fica no topo do card) --
        # Adicionei um label pequeno para indicar o que é o slider
        lbl_slider = MDLabel(text="Ajuste o valor:", font_style="Caption", halign="center", size_hint_y=None, height=dp(20))
        self.panel_card.add_widget(lbl_slider)

        self.slider = MDSlider(
            min=0, max=100, value=10,
            color=(0.2, 0.6, 0.4, 1),
            size_hint_y=None,
            height=dp(40)
        )
        self.slider.bind(value=self.atualizar_interface)
        self.panel_card.add_widget(self.slider)

        # -- Área de Resultados (Scrollável) --
        # O ScrollView agora tem size_hint=(1, 1) para ocupar todo o espaço ganho
        self.scroll_res = ScrollView(size_hint=(1, 1))

        self.lbl_resultados = MDLabel(
            text="Selecione uma categoria...",
            halign="center",
            valign="top", # Texto alinhado ao topo
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            font_style="Body1",
            markup=True,
            size_hint_y=None,
            padding=[0, dp(10)] # Um pouco de respiro
        )
        self.lbl_resultados.bind(texture_size=self.lbl_resultados.setter('size'))
        self.scroll_res.add_widget(self.lbl_resultados)
        self.panel_card.add_widget(self.scroll_res)

        box_botoes = GridLayout(
            rows=1,
            spacing=dp(5), # Espaço pequeno entre eles para caber tudo
            size_hint=(1, None),
            height=dp(80),
            padding=[dp(5), dp(10)]
        )

        categorias = [
            ("Comprimento", "ruler", "#4CAF50"),
            ("Massa", "weight-kilogram", "#9C27B0"),
            ("Volume", "cup-water", "#2196F3"),
            ("Tempo", "clock-outline", "#FF9800"),
            ("Temperatura", "thermometer", "#F44336")
        ]

        self.btns_dict = {}
        for nome, icone, cor in categorias:
            # Usamos AnchorLayout para centralizar cada botão na sua célula do Grid
            wrapper = AnchorLayout(anchor_x='center', anchor_y='center')

            btn = MDIconButton(
                icon=icone,
                icon_size="26sp", # Levemente menor para garantir que 5 caibam em telas pequenas
                theme_text_color="Custom",
                text_color=get_color_from_hex(cor),
                md_bg_color=(0.95, 0.95, 0.95, 1),
                size_hint=(None, None),
                size=(dp(48), dp(48)), # Botão um pouco mais compacto
                on_release=lambda x, n=nome, c=cor, i=icone: self.mudar_categoria(n, c, i)
            )
            self.btns_dict[nome] = btn

            wrapper.add_widget(btn)
            box_botoes.add_widget(wrapper)

        self.panel_card.add_widget(box_botoes)

        layout.add_widget(self.panel_card)
        self.add_widget(layout)

        # Estado Inicial
        self.cat_atual = "Comprimento"
        self.cor_atual = "#4CAF50"
        self.mudar_categoria("Comprimento", "#4CAF50", "ruler")

    def adicionar_decoracao_fundo(self, layout):
        icones = ["ruler", "flask", "clock", "scale", "thermometer"]
        positions = [{"x": 0.1, "y": 0.8}, {"x": 0.9, "y": 0.85}, {"x": 0.15, "y": 0.2}, {"x": 0.85, "y": 0.25}]
        for pos in positions:
            layout.add_widget(MDIconButton(
                icon=choice(icones), theme_text_color="Custom",
                text_color=(0,0,0,0.05), pos_hint=pos,
                icon_size=dp(60), disabled=True
            ))

    def mudar_categoria(self, nome, cor_hex, icone):
        self.cat_atual = nome
        self.cor_atual = cor_hex
        rgba = get_color_from_hex(cor_hex)

        # Atualiza visuais
        self.hero_icon.icon = icone
        self.hero_icon.text_color = rgba
        self.hero_value.text_color = rgba
        self.slider.color = rgba

        # Destaca botão
        for n, btn in self.btns_dict.items():
            if n == nome:
                btn.md_bg_color = (rgba[0], rgba[1], rgba[2], 0.2)
                btn.icon_size = "40sp"
            else:
                btn.md_bg_color = (0.95, 0.95, 0.95, 1)
                btn.icon_size = "32sp"

        # Reseta sliders
        if nome == "Temperatura":
            self.slider.min = 0; self.slider.max = 100; self.slider.value = 25
        elif nome == "Tempo":
            self.slider.min = 1; self.slider.max = 120; self.slider.value = 60
        else:
            self.slider.min = 1; self.slider.max = 100; self.slider.value = 10

        self.atualizar_interface()

    def atualizar_interface(self, *args):
        val = int(self.slider.value)
        # REMOVIDO: Atualização da self.progress_bar

        g = self.cat_atual
        texto = ""
        simbolo_base = ""

        # (O restante da lógica de texto permanece igual, usando self.cor_atual para colorir)
        if g == "Comprimento":
            simbolo_base = "m"
            cm = val * 100
            km = val / 1000
            texto = (
                f"[size=20][b]Conversões de Metro:[/b][/size]\n\n"
                f"[color={self.cor_atual}]• {cm} cm[/color] (Centímetros)\n"
                f"  [i](Multiplicamos por 100)[/i]\n\n"
                f"[color={self.cor_atual}]• {km:.3f} km[/color] (Quilômetros)\n"
                f"  [i](Dividimos por 1000)[/i]"
            )
        elif g == "Massa":
            simbolo_base = "kg"
            g_total = val * 1000
            t = val / 1000
            texto = (
                f"[size=20][b]Conversões de Massa:[/b][/size]\n\n"
                f"[color={self.cor_atual}]• {g_total} g[/color] (Gramas)\n"
                f"  [i](Multiplicamos por 1000)[/i]\n\n"
                f"[color={self.cor_atual}]• {t:.3f} t[/color] (Toneladas)\n"
                f"  [i](Dividimos por 1000)[/i]"
            )
        elif g == "Volume":
            simbolo_base = "L"
            ml = val * 1000
            texto = (
                f"[size=20][b]Conversões de Volume:[/b][/size]\n\n"
                f"[color={self.cor_atual}]• {ml} mL[/color] (Mililitros)\n"
                f"  [i](Multiplicamos por 1000)[/i]\n\n"
                f"[color={self.cor_atual}]• {val} dm³[/color] (Decímetros cúbicos)\n"
                f"  [i](É equivalente: 1 L = 1 dm³)[/i]"
            )
        elif g == "Tempo":
            simbolo_base = "min"
            seg = val * 60
            h = val // 60
            min_rest = val % 60
            texto = (
                f"[size=20][b]Conversões de Tempo:[/b][/size]\n\n"
                f"[color={self.cor_atual}]• {seg} s[/color] (Segundos)\n"
                f"  [i](Multiplicamos por 60)[/i]\n\n"
                f"[color={self.cor_atual}]• {h}h {min_rest}min[/color]\n"
                f"  [i](Sistema base 60)[/i]"
            )
        elif g == "Temperatura":
            simbolo_base = "°C"
            f = (val * 1.8) + 32
            k = val + 273.15
            texto = (
                f"[size=20][b]Escalas Termométricas:[/b][/size]\n\n"
                f"[color={self.cor_atual}]• {f:.1f} °F[/color] (Fahrenheit)\n"
                f"  [i](°C x 1.8 + 32)[/i]\n\n"
                f"[color={self.cor_atual}]• {k:.2f} K[/color] (Kelvin)\n"
                f"  [i](°C + 273.15)[/i]"
            )

        self.hero_value.text = f"{val} {simbolo_base}"
        self.lbl_resultados.text = texto

    def voltar(self, tela_anterior):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = tela_anterior