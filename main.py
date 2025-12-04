from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRectangleFlatButton
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.slider import MDSlider
from kivy.uix.switch import Switch
from kivy.core.text import LabelBase
import os
from kivy.metrics import dp
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.button import MDRaisedButton
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from random import choice

font_path = os.path.join(os.path.dirname(__file__), "Fontes", "Duo-Dunkel.ttf")
print("[DEBUG] Fonte:", font_path, "exists:", os.path.exists(font_path))
LabelBase.register(name="BungeeShade", fn_regular=font_path)


CORAL = (1, 0.44, 0.26, 1)   # #FF7043
LILAS = (0.65, 0.55, 0.98, 1)  # #A78BFA
PRETO = (0, 0, 0, 1)
PRETO_70 = (0, 0, 0, 0.7)


class ImageButton(ButtonBehavior, Image):
    pass


# -------------------------------------------------
# TELA INICIAL
# -------------------------------------------------
class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Configura Fundo
        self.setup_background(layout)

        # 2. ADICIONA DECORAÇÃO (Ícones variados de matemática)
        self.adicionar_decoracao_fundo(layout)

        # Logo
        logo = Image(
            source="matemas.png",
            size_hint=(0.80, None),
            height=200,
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(logo)

        # Botões principais (imagem)
        botao_jogar = ImageButton(
            source="jogar.png",
            size_hint=(None, None),
            size=(400, 180),
            pos_hint={"center_x": 0.5, "center_y": 0.68},
        )
        botao_jogar.bind(on_release=lambda *a: self.seleciona_n())
        layout.add_widget(botao_jogar)

        botao_conteudos = ImageButton(
            source="conteudos.png",
            size_hint=(None, None),
            size=(400, 180),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        botao_conteudos.bind(on_release=lambda *a: self.acao_conteudos())
        layout.add_widget(botao_conteudos)

        botao_tutorial = ImageButton(
            source="tutorial.png",
            size_hint=(None, None),
            size=(400, 180),
            pos_hint={"center_x": 0.5, "center_y": 0.32},
        )
        botao_tutorial.bind(on_release=lambda *a: self.acao_tutorial())
        layout.add_widget(botao_tutorial)

        # Configurações (Ícone Preto)
        settings_button = MDIconButton(
            icon="cog",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1), # Preto
            pos_hint={"right": 0.98, "top": 0.98},
        )
        settings_button.bind(on_release=lambda *a: self.abrir_tela_config())
        layout.add_widget(settings_button)

        self.add_widget(layout)

    def setup_background(self, layout):
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
        )
        layout.add_widget(fundo)

    def adicionar_decoracao_fundo(self, layout):
        """Ícones mistos para a tela inicial"""
        # Mix de álgebra, geometria, estatística e grandezas
        icones = [
            "calculator-variant", "shape-outline", "chart-pie",
            "ruler", "function-variant", "pi", "sigma"
        ]

        positions = [
            {"x": 0.05, "y": 0.85}, {"x": 0.85, "y": 0.9},
            {"x": 0.1, "y": 0.6}, {"x": 0.85, "y": 0.6},
            {"x": 0.05, "y": 0.15}, {"x": 0.9, "y": 0.2}
        ]

        for pos in positions:
            icon = MDIconButton(
                icon=choice(icones),
                theme_text_color="Custom",
                text_color=(0, 0, 0, 0.08), # Preto marca d'água (bem transparente)
                pos_hint=pos,
                icon_size=dp(45),
                disabled=True
            )
            layout.add_widget(icon)

    def seleciona_n(self):
        self.manager.current = "jogar"

    def acao_conteudos(self):
        if self.manager:
            self.manager.current = "conteudos"

    def acao_tutorial(self):
        if self.manager:
            self.manager.current = "tutorial"

    def abrir_tela_config(self):
        PainelConfiguracoes().open()

# -------------------------------------------------
# TELA DE CONTEÚDOS
# -------------------------------------------------
class TelaConteudos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Fundo
        background = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
        )
        layout.add_widget(background)

        # ADICIONA DECORAÇÃO
        self.adicionar_decoracao_fundo(layout)

        # --- CORREÇÃO AQUI ---
        # Em vez de calcular posições, usamos um container vertical (BoxLayout)
        # que organiza os botões automaticamente sem sobreposição.
        container_botoes = BoxLayout(
            orientation="vertical",
            spacing=dp(15),          # Espaço entre os botões
            padding=[0, dp(20), 0, dp(20)], # Margem interna
            size_hint=(0.55, 0.75),  # Largura 55%, Altura 75% da tela
            pos_hint={"center_x": 0.5, "center_y": 0.5} # Centralizado
        )

        topicos = [
            ("Estudos/novo_Operacoes.png", "tela"),
            ("Estudos/novo_Algebra.png", "algebra_tela"),
            ("Estudos/novo_Geometria.png", "geometria_tela"),
            ("Estudos/novo_Grandezas.png", "grandezas_tela"),
            ("Estudos/novo_Estatistica.png", "estatistica_tela"),
        ]

        for img, tela in topicos:
            # O botão agora se ajusta automaticamente dentro do container
            btn_img = ImageButton(
                source=img,
                size_hint=(1, 1),    # Ocupa o espaço disponível na caixa
                allow_stretch=True,  # Permite esticar se necessário
                keep_ratio=True      # Mas mantém o formato original da imagem
            )
            btn_img.bind(on_release=lambda *a, t=tela: self.ir_para(t))
            container_botoes.add_widget(btn_img)

        layout.add_widget(container_botoes)
        # ---------------------

        # Botão voltar (ícone preto)
        back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={"x": 0, "top": 1},
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1), # Preto
        )
        back_button.bind(on_release=lambda *a: self.voltar())
        layout.add_widget(back_button)

        self.add_widget(layout)

    def adicionar_decoracao_fundo(self, layout):
        """Ícones mistos espalhados para preencher o vazio"""
        icones = [
            "book-open-page-variant", "lightbulb-outline", "school",
            "pencil", "notebook", "calculator", "brain"
        ]

        # Posições focadas mais nas laterais para não brigar com a lista central
        positions = [
            {"x": 0.05, "y": 0.9}, {"x": 0.85, "y": 0.88},
            {"x": 0.02, "y": 0.5}, {"x": 0.9, "y": 0.55},
            {"x": 0.05, "y": 0.1}, {"x": 0.85, "y": 0.15}
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

    def ir_para(self, tela_destino):
        if tela_destino in self.manager.screen_names:
            self.manager.current = tela_destino
        else:
            print(f"⚠️ Tela '{tela_destino}' não existe!")

    def voltar(self):
        self.manager.current = "inicial"


class PainelConfiguracoes(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fundo transparente
        self.background_color = (0, 0, 0, 0)
        self.auto_dismiss = False
        self.size_hint = (1, 1)

        # Largura do painel
        self.painel_width = 0.90

        # Painel lateral
        self.painel = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(25),
            size_hint=(self.painel_width, 1),
            md_bg_color=(1, 0.8588, 0.7333, 1),  # #FFDBBB
        )
        self.add_widget(self.painel)

        # ============================================
        #                TOPO (X + título)
        # ============================================
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(40),
            spacing=dp(10),
        )

        btn_fechar = MDIconButton(
            icon="close",
            icon_size=dp(28),
            on_release=lambda *a: self.fechar()
        )

        titulo = MDLabel(
            text="Configurações",
            font_style="H5",
            valign="center",
            halign="left"
        )

        header.add_widget(btn_fechar)
        header.add_widget(titulo)
        self.painel.add_widget(header)

        # ============================================
        #              SWITCH DO VOLUME
        # ============================================
        self.label_som = MDLabel(
            text="Ligar Volume",
            halign="left"
        )

        self.switch_volume = Switch(
            active=True
        )
        self.switch_volume.bind(active=self.atualizar_label_som)

        linha_switch = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(50),
            spacing=dp(10)
        )

        linha_switch.add_widget(self.label_som)
        linha_switch.add_widget(self.switch_volume)

        self.painel.add_widget(linha_switch)

        # ============================================
        #             SLIDER DE VOLUME
        # ============================================
        self.painel.add_widget(
            MDLabel(text="Ajustar Volume", halign="left")
        )

        self.slider = MDSlider(value=75)
        self.painel.add_widget(self.slider)

        # ============================================
        #           BOTÕES: REPORTAR / DEV
        # ============================================
        botoes_box = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(150),
            padding=dp(20),
            spacing=dp(15),
        )

        botoes_box.add_widget(
            MDRaisedButton(text="Reportar Erro", pos_hint={"center_x": 0.5})
        )

        botoes_box.add_widget(
            MDRaisedButton(text="Desenvolvedores", pos_hint={"center_x": 0.5})
        )

        self.painel.add_widget(botoes_box)

    # =====================================
    #     TEXTO DO SWITCH (dinâmico)
    # =====================================
    def atualizar_label_som(self, switch, ativo):
        self.label_som.text = "Ligar Volume" if ativo else "Desligar Volume"

    # =====================================
    #           ANIMAÇÕES
    # =====================================
    def open(self, *args):
        super().open()
        self.painel.x = self.width
        destino = self.width * (1 - self.painel_width)
        Animation(x=destino, d=0.25).start(self.painel)

    def fechar(self, *args):
        anim = Animation(x=self.width, d=0.25)
        anim.bind(on_complete=lambda *a: ModalView.dismiss(self))
        anim.start(self.painel)

    # Fecha ao clicar fora da barra
    def on_touch_down(self, touch):
        if not self.painel.collide_point(*touch.pos):
            self.fechar()
            return True
        return super().on_touch_down(touch)


#TELAS JOGOS
from jogar import TelaJogar, TelaEscolhaNivel, JogosPrimario, JogosFundamental, JogosMedio
from cross_nova import CruzadinhaScreen
from calculo import calculoI, TelaFimDeJogo
from algebra import AlgebraGameScreen, TelaFimAlgebra
from fracoes import FracoesGameScreen, TelaFimFracoes
from sudoku_logic import TelaSudoku
from fracoes1 import TelaFracoesInfo, TelaFracoesRepresentacoes, TelaFracoesExplicacoes, TelaFracoesPropriedades


#TELA TUTORIAL
from tutorial import TelaTutorial

#TELAS ESTUDO
from meia_tela import TelaRepresentacoes, MeiaTela, OperacoesDefinicoesTela
from meia_algebra import AlgebraTela, AlgebraRepresentacoes, AlgebraDefinicoesTela
from meia_grandezas import GrandezasTela, GrandezasRepresentacoes, GrandezasDefinicoesTela
from meia_geometria import GeometriaRepresentacoes, GeometriaDefinicoesTela, GeometriaTela
from meia_estatistica import EstatisticaTela, EstatisticaRepresentacoes, EstatisticaDefinicoesTela
# ---------- App Principal ----------
class TesteApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TelaInicial(name="inicial"))
        sm.add_widget(TelaConteudos(name="conteudos"))
        sm.add_widget(TelaTutorial(name="tutorial"))
        sm.add_widget(TelaJogar(name="jogar"))
        sm.add_widget(TelaEscolhaNivel(name="primario", dificuldade="primario", titulo="Fundamental I", tela_voltar="jogar"))
        sm.add_widget(TelaEscolhaNivel(name="fundamental", dificuldade="fundamental", titulo="Fundamental II", tela_voltar="jogar"))
        sm.add_widget(TelaEscolhaNivel(name="medio", dificuldade="medio", titulo="Ensino Médio", tela_voltar="jogar"))
        sm.add_widget(calculoI(name="game1"))
        sm.add_widget(CruzadinhaScreen(name="cross_p", dificuldade="fundI"))
        sm.add_widget(CruzadinhaScreen(name="cross_f", dificuldade="fundII"))
        sm.add_widget(CruzadinhaScreen(name="cross", dificuldade="medio"))
        sm.add_widget(AlgebraGameScreen(name="algebra"))
        sm.add_widget(TelaFimAlgebra(name="fim_algebra"))
        sm.add_widget(FracoesGameScreen(name="fracoes"))
        sm.add_widget(TelaSudoku(name="sudoku"))
        sm.add_widget(TelaFracoesInfo(name="fracoes_info"))
        sm.add_widget(TelaFracoesPropriedades(name="fracoes_propriedades"))
        sm.add_widget(TelaFracoesRepresentacoes(name="fracoes_representacoes"))
        sm.add_widget(TelaFracoesExplicacoes(name="fracoes_explicacoes"))

        #TELAS ESTUDO
        sm.add_widget(OperacoesDefinicoesTela(name="definicoes"))
        sm.add_widget(TelaRepresentacoes(name="representacoes"))
        sm.add_widget(MeiaTela(name="tela"))
        sm.add_widget(GrandezasRepresentacoes(name="grandezas_representacoes"))
        sm.add_widget(GrandezasTela(name="grandezas_tela"))
        sm.add_widget(GrandezasDefinicoesTela(name="grandezas_definicoes"))
        sm.add_widget(GeometriaTela(name="geometria_tela"))
        sm.add_widget(GeometriaDefinicoesTela(name="geometria_definicoes"))
        sm.add_widget(GeometriaRepresentacoes(name="geometria_representacoes"))
        sm.add_widget(AlgebraTela(name="algebra_tela"))
        sm.add_widget(AlgebraRepresentacoes(name="algebra_representacoes"))
        sm.add_widget(AlgebraDefinicoesTela(name="algebra_definicoes"))
        sm.add_widget(EstatisticaTela(name="estatistica_tela"))
        sm.add_widget(EstatisticaRepresentacoes(name="estatistica_representacoes"))
        sm.add_widget(EstatisticaDefinicoesTela(name="estatistica_definicoes"))

        return sm

if __name__ == "__main__":
    TesteApp().run()



