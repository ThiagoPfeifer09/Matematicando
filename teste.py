<<<<<<< HEAD
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.carousel import Carousel
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivy.factory import Factory
from kivy.uix.image import Image


# ================================================================
# CARD MODELO
# ================================================================
class TutorialCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            radius=[25],
            elevation=15,
            padding=20,
            size_hint=(0.9, 0.65),  # Mantém 70% da tela (aprox.)
            pos_hint={"center_x": 0.5, "center_y": 0.5},  # Centralizado
            **kwargs
        )


# ================================================================
# COMPONENTE — ÍCONE + TEXTO (BOTÕES DOS JOGOS)
# ================================================================
class TopicIcon(MDCard):
    """
    Card que mostra um ícone e um texto embaixo.
    Instancie diretamente: TopicIcon(text='...', icon='calculator', color=(...))
    """
    def __init__(self, text="", icon="help", color=(0.3, 0.5, 1, 1), **kwargs):
        super().__init__(
            orientation="vertical",
            size_hint_y=None,
            height=dp(100),
            radius=[15],
            md_bg_color=(1, 1, 1, 1),
            elevation=4,
            padding=[8, 6, 8, 6],
            **kwargs
        )

        self.text = text
        self.icon = icon
        self.color = color

        # Ícone no topo
        self.icon_btn = MDIconButton(
            icon=self.icon,
            halign="center",
            theme_text_color="Custom",
            text_color=self.color,
            font_size="38sp",
            size_hint_y=None,
            height=dp(48),
            pos_hint={"center_x": 0.5}
        )
        self.add_widget(self.icon_btn)

        # Texto abaixo
        self.label = MDLabel(
            text=self.text,
            halign="center",
            font_style="Subtitle1",
            size_hint_y=None,
            height=dp(32),
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            bold=True
        )
        self.add_widget(self.label)


# Opcional: registrar se você quiser usar Factory.TopicIcon() em outro lugar
Factory.register("TopicIcon", cls=TopicIcon)


# ================================================================
# TELA DO TUTORIAL (com todos os slides originais)
# ================================================================
class TelaTutorial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ===== Fundo =====
        bg = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(bg)

        # LAYOUT PRINCIPAL
        self.layout = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        self.add_widget(self.layout)


        # 🔙 BOTÃO VOLTAR (TOPO ESQUERDA)
        back_btn = MDIconButton(
            icon="arrow-left",
            pos_hint={"top": 1, "x": 0},
            icon_size=dp(36),
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            on_release=self.voltar
        )
        self.layout.add_widget(back_btn)

        # CARD PRINCIPAL
        self.card = TutorialCard()
        self.layout.add_widget(self.card)

        # CARROSSEL
        self.carrossel = Carousel(direction="right", loop=True)
        self.card.add_widget(self.carrossel)

        # SLIDES
        self.carrossel.add_widget(self.criar_slide_boas_vindas())
        self.carrossel.add_widget(self.criar_slide_jogos())
        self.carrossel.add_widget(self.criar_slide_estudos())
        self.carrossel.add_widget(self.criar_slide_navegacao())


        # BOTÕES DE NAVEGAÇÃO
        nav = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(60),
            spacing=20,
            pos_hint={"center_x": 0.5}
        )

        nav.add_widget(MDFillRoundFlatButton(
            text="Anterior",
            on_release=lambda x: self.carrossel.load_previous()
        ))

        nav.add_widget(MDFillRoundFlatButton(
            text="Próximo",
            on_release=lambda x: self.carrossel.load_next()
        ))

        self.layout.add_widget(nav)


    # --------------------------
    # VOLTAR TELA
    # --------------------------
    def voltar(self, instance):
        self.manager.current = "inicial"


    def _criar_bloco_diagrama(self, texto, icone, cor):
        box = MDCard(
            orientation="vertical",
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            padding=10,
            radius=[15],
            md_bg_color=cor,
            elevation=5
        )
        box.add_widget(MDIconButton(icon=icone, halign="center", font_size="40sp"))
        box.add_widget(MDLabel(text=texto, halign="center", bold=True))
        return box

    def _criar_titulo_slide(self, texto, icone, cor):
        header = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=0.3)
        header.add_widget(MDIconButton(icon=icone, halign="center", font_size="60sp", text_color=cor))
        header.add_widget(MDLabel(text=texto, halign="center", bold=True, font_style="H5"))
        return header

    # ================================================================
    # SLIDE 1 — BOAS VINDAS (mantido igual ao original)
    # ================================================================
    def criar_slide_boas_vindas(self):
        card = MDBoxLayout(orientation="vertical", spacing=10, padding=10)

        # TOPO
        header = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=0.4)
        img_icon = MDIconButton(
            icon="calculator-variant",
            halign="center",
            font_size="80sp",
            text_color=(0.2, 0.6, 1, 1)
        )
        title = MDLabel(
            text="Bem-vindo ao\nMatematicando",
            halign="center",
            bold=True,
            font_style="H5"
        )

        header.add_widget(img_icon)
        header.add_widget(title)

        # DIAGRAMA
        diagrama = MDBoxLayout(orientation='vertical', spacing=10, padding=10)

        lbl_info = MDLabel(
            text="Aqui vou te ensinar a como navegar pelo app!",
            halign="center"
        )

        flow = MDBoxLayout(orientation='horizontal', spacing=10, pos_hint={"center_x": .5})

        box_jogos = self._criar_bloco_diagrama("Jogos", "gamepad-variant", (1, 0.7, 0.4, 1))
        seta = MDIconButton(icon="arrow-left-right", halign="center")
        box_estudos = self._criar_bloco_diagrama("Estudar", "book-open-variant", (0.4, 0.7, 1, 1))

        flow.add_widget(box_jogos)
        flow.add_widget(seta)
        flow.add_widget(box_estudos)

        diagrama.add_widget(lbl_info)
        diagrama.add_widget(flow)

        card.add_widget(header)
        card.add_widget(diagrama)
        return card

    # ================================================================
    # SLIDE 2 — JOGOS (corrigido para instanciar TopicIcon diretamente)
    # ================================================================
    def criar_slide_jogos(self):
        card = MDBoxLayout(orientation="vertical", spacing=15)

        header = self._criar_titulo_slide("Jogos", "gamepad-variant", (0.9, 0.5, 0.2, 1))
        card.add_widget(header)

        content = MDBoxLayout(
            orientation="vertical",
            spacing=20,
            padding=10,
            size_hint_y=1
        )
        card.add_widget(content)

        # Escolha nível
        lbl1 = MDLabel(text="1. Escolha seu Nível", halign="center", bold=True)
        grid_niveis = MDGridLayout(cols=3, adaptive_height=True, spacing=10, padding=10)

        for nivel in ["Fund. I", "Fund. II", "Médio"]:
            btn = MDFillRoundFlatButton(
                text=nivel,
                md_bg_color=(0.95, 0.8, 0.6, 1),
                text_color=(0, 0, 0, 1),
            )
            grid_niveis.add_widget(btn)

        # Jogos
        lbl2 = MDLabel(text="2. Pratique Habilidades", halign="center", bold=True)
        grid_tipos = MDGridLayout(cols=3, adaptive_height=True, spacing=15, padding=10)

        # Ícones válidos do conjunto padrão (substitua se quiser outros)
        jogos = [
            ("Operações", "calculator-variant"),
            ("Álgebra", "alpha"),
            ("Frações", "chart-arc"),
            ("Cruzadinha", "grid-large"),
            ("Sudoku", "numeric"),
            # Se quiser mais, adicione aqui
        ]

        for nome, icone in jogos:
            # instancio diretamente a classe Python (não uso Factory.TopicIcon())
            item = TopicIcon(text=nome, icon=icone, color=(0.8, 0.4, 0.1, 1))
            grid_tipos.add_widget(item)

        content.add_widget(lbl1)
        content.add_widget(grid_niveis)
        content.add_widget(lbl2)
        content.add_widget(grid_tipos)

        return card

    # ================================================================
    # SLIDE 3 — ESTUDOS (mantido)
    # ================================================================
    def criar_slide_estudos(self):
        card = MDBoxLayout(orientation="vertical", spacing=15)

        header = self._criar_titulo_slide("Estudar", "book-open-page-variant", (0.2, 0.5, 0.8, 1))
        card.add_widget(header)

        content = MDBoxLayout(
            orientation="vertical",
            spacing=15,
            padding=10,
            size_hint_y=1
        )

        card.add_widget(content)

        desc = MDLabel(
            text="Na aba estudar você encontrará representações\n e definições organizados por temas.",
            halign="center",
            font_style="Body2"
        )
        content.add_widget(desc)

        grid = MDGridLayout(cols=2, adaptive_height=True, spacing=15, padding=10)

        categorias = [
            ("Operações", "calculator", "Somas e divisões"),
            ("Álgebra", "function-variant", "Equações e incógnitas"),
            ("Geometria", "shape-outline", "Formas e áreas"),
            ("Grandezas", "ruler", "Unidades e escalas"),
            ("Estatística", "chart-bar", "Gráficos e dados"),
        ]

        for titulo, icone, subtitulo in categorias:
            box = MDCard(
                orientation="vertical",
                size_hint_y=None,
                height=dp(100),
                padding=10,
                radius=[12],
                elevation=2
            )
            box.add_widget(MDIconButton(icon=icone, halign="center", font_size="28sp"))
            box.add_widget(MDLabel(text=titulo, halign="center", bold=True))
            box.add_widget(MDLabel(text=subtitulo, halign="center", font_style="Caption"))
            grid.add_widget(box)

        content.add_widget(grid)
        return card

    # ================================================================
    # SLIDE 4 — NAVEGAÇÃO FINAL (mantido)
    # ================================================================
    def criar_slide_navegacao(self):
        card = MDBoxLayout(orientation='vertical', spacing=10, padding=10)

        header = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=0.3)
        header.add_widget(MDIconButton(icon="gesture-tap", halign="center", font_size="60sp"))
        header.add_widget(MDLabel(text="Pronto para começar?", halign="center", bold=True, font_style="H6"))

        dica_box = MDCard(radius=[10], padding=15)
        dica_box.add_widget(MDLabel(
            text="Use o botão voltar no topo da tela para retornar ao menu.",
            halign="center"
        ))

        card.add_widget(header)
        card.add_widget(dica_box)
        return card


# ================================================================
# TESTE / APP
# ================================================================
class TestApp(MDApp):
    def build(self):
        return TelaTutorial()


if __name__ == "__main__":
    TestApp().run()
=======
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
>>>>>>> 2269faa7446d3e2311a76c04b2417a3f19598fc4
