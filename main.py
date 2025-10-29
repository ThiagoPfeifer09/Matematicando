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


class ImageButton(ButtonBehavior, Image):
    pass

# ---------- Tela Inicial ----------
class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.setup_background(layout)

        # --- Logo / título como imagem estática ---
        logo = Image(
            source="matemas.png",  # substitua pelo nome da imagem do título
            size_hint=(0.8, None),
            height=150,
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(logo)

        # --- Botão JOGAR ---
        botao_jogar = ImageButton(
            source="jogar.png",
            size_hint=(None, None),
            size=(400, 180),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        botao_jogar.bind(on_release=lambda *a: self.seleciona_n())
        layout.add_widget(botao_jogar)

        # --- Botão CONTEÚDOS ---
        botao_conteudos = ImageButton(
            source="conteudos.png",
            size_hint=(None, None),
            size=(400, 180),
            pos_hint={"center_x": 0.5, "center_y": 0.35},
        )
        botao_conteudos.bind(on_release=lambda *a: self.acao_conteudos())
        layout.add_widget(botao_conteudos)

        # --- Botão CONFIGURAÇÕES ---
        settings_button = MDIconButton(
            icon="cog",
            theme_text_color="Custom",
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

    def seleciona_n(self):
        self.manager.current = "seleciona"

    def acao_conteudos(self):
        if self.manager:
            self.manager.current = "conteudos"

    def abrir_tela_config(self, *args):
        if self.manager:
            self.manager.current = "config"


# ---------- Tela de Conteúdos ----------
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

        # Botões de imagem com navegação
        topicos = [
            ("novo_Operacoes.png", "tela"),
            ("novo_Algebra.png", "algebra_tela"),
            ("novo_Geometria.png", "geometria_tela"),
            ("novo_Grandezas.png", "grandezas_tela"),
            ("novo_Estatistica.png", "geometria_tela"),
        ]

        for i, (img, tela) in enumerate(topicos):
            btn_img = ImageButton(
                source=img,
                size_hint=(0.45, 0.16),
                pos_hint={"center_x": 0.5, "center_y": 0.8 - i * 0.13},
            )
            # Bind para ir para a tela correspondente
            btn_img.bind(on_release=lambda *a, t=tela: self.ir_para(t))
            layout.add_widget(btn_img)

        # Botão voltar
        back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={"x": 0, "top": 1},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
        )
        back_button.bind(on_release=lambda *a: self.voltar())
        layout.add_widget(back_button)

        self.add_widget(layout)

    def ir_para(self, tela_destino):
        if tela_destino in self.manager.screen_names:
            self.manager.current = tela_destino
        else:
            print(f"⚠️ Tela '{tela_destino}' não existe!")

    def voltar(self):
        self.manager.current = "inicial"




# ---------- Seleciona Nível ----------
class Seleciona_Nivel(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.setup_background(layout)

        title = MDLabel(
            text="Selecione o nível dos jogos que deseja:",
            halign="center",
            font_style="H6",
            size_hint=(0.8, None),
            height=30,
            pos_hint={"center_x": 0.5, "top": 0.9},
            theme_text_color="Custom",
            text_color=(1, 0.8, 0, 1),
        )
        layout.add_widget(title)

        # --- Botão imagem: Ensino Primário ---
        btn_primario = ImageButton(
            source="primario.png",
            size_hint=(0.55, 0.22),
            pos_hint={"center_x": 0.5, "center_y": 0.68},
        )
        btn_primario.bind(on_release=lambda *args: self.ir_para_jogar_p())
        layout.add_widget(btn_primario)

        # --- Botão imagem: Ensino Fundamental ---
        btn_fundamental = ImageButton(
            source="fundamental.png",
            size_hint=(0.55, 0.22),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        btn_fundamental.bind(on_release=lambda *args: self.ir_para_jogar_f())
        layout.add_widget(btn_fundamental)

        # --- Botão imagem: Ensino Médio ---
        btn_medio = ImageButton(
            source="medio.png",
            size_hint=(0.55, 0.22),
            pos_hint={"center_x": 0.5, "center_y": 0.32},
        )
        btn_medio.bind(on_release=lambda *args: self.ir_para_jogar())
        layout.add_widget(btn_medio)

        # --- Botão de engrenagem (configurações ou voltar) ---
        back_button = MDIconButton(
            icon='cog',  # pode trocar por outro ícone, ex: 'arrow-left'
            pos_hint={'right': 0.98, 'top': 0.98},
            theme_icon_color="Custom",
            icon_color=(1, 0.8, 0, 1)
        )
        back_button.bind(on_release=self.voltar)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def setup_background(self, layout):
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
        )
        layout.add_widget(fundo)

    def voltar(self, instance):
        self.manager.current = "inicial"

    def ir_para_jogar_p(self):
        self.manager.current = "jogar_p"

    def ir_para_jogar_f(self):
        self.manager.current = "jogar_f"

    def ir_para_jogar(self):
        self.manager.current = "jogar"



# ---------- Tela de Configurações ----------
class TelaConfiguracoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Fundo da tela
        background = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        layout.add_widget(background)

        # Container principal (sem card, sem animações)
        conteudo = MDBoxLayout(
            orientation="vertical",
            spacing=25,
            size_hint=(0.85, 0.78),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            padding=[30, 40, 30, 40],
        )

        # Título
        titulo = MDLabel(
            text="CONFIGURAÇÕES",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.96, 0.92, 1, 1),
            font_style="H5",
        )
        conteudo.add_widget(titulo)

        # Linha de som (texto + switch)
        linha_som = MDBoxLayout(
            orientation="horizontal",
            spacing=15,
            adaptive_height=True,
        )
        linha_som.add_widget(
            MDLabel(
                text="Som ativado",
                halign="left",
                theme_text_color="Custom",
                text_color=(0.8, 0.85, 1, 1),
            )
        )
        self.switch_som = Switch(active=True)
        linha_som.add_widget(self.switch_som)
        conteudo.add_widget(linha_som)

        # Volume e slider
        self.label_volume = MDLabel(
            text="Volume: 75",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.5, 0.9, 1, 1),
            font_style="Subtitle1",
        )
        conteudo.add_widget(self.label_volume)

        self.slider_volume = MDSlider(min=0, max=100, value=75)
        self.slider_volume.bind(value=self.atualizar_volume)
        conteudo.add_widget(self.slider_volume)

        # Botões (sem animação)
        botao_reportar = MDRectangleFlatButton(
            text="Reportar erro",
            pos_hint={"center_x": 0.5},
        )
        botao_reportar.bind(on_release=lambda *a: print("Botão Reportar erro clicado"))
        conteudo.add_widget(botao_reportar)

        botao_dev = MDRectangleFlatButton(
            text="Ver desenvolvedores",
            pos_hint={"center_x": 0.5},
        )
        botao_dev.bind(on_release=lambda *a: print("Botão Ver desenvolvedores clicado"))
        conteudo.add_widget(botao_dev)

        botao_voltar = MDRectangleFlatButton(
            text="Voltar",
            pos_hint={"center_x": 0.5},
        )
        botao_voltar.bind(on_release=lambda *a: self.voltar_tela_inicial())
        conteudo.add_widget(botao_voltar)

        # Adiciona o conteúdo direto no layout
        layout.add_widget(conteudo)
        self.add_widget(layout)

    def atualizar_volume(self, instance, value):
        self.label_volume.text = f"Volume: {int(value)}"

    def voltar_tela_inicial(self):
        self.manager.current = "inicial"

    def voltar(self):
        self.manager.current = "inicial"

from meia_tela import TelaRepresentacoes, MeiaTela, DefinicoesTela
from grandezas_tela import GrandezasTela, GrandezasRepresentacoes, DefinicoesGrandezas
from meia_geometria import GeometriaRepresentacoes, DefinicoesGeometria, GeometriaTela
from jogar import TelaJogar, TelaEscolhaNivel, JogosPrimario, JogosFundamental, JogosMedio
from cross_nova import CruzadinhaScreen
from calculo import calculoI
from algebra import AlgebraGameScreen, TelaFimAlgebra
from fracoes import FracoesGameScreen, TelaFimFracoes
from meia_algebra import AlgebraTela, AlgebraRepresentacoes, AlgebraDefinicoes
# ---------- App Principal ----------
class TesteApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TelaInicial(name="inicial"))
        sm.add_widget(TelaConteudos(name="conteudos"))
        sm.add_widget(TelaConfiguracoes(name="config"))
        sm.add_widget(Seleciona_Nivel(name="seleciona"))
        sm.add_widget(TelaRepresentacoes(name="representacoes"))
        sm.add_widget(MeiaTela(name="tela"))
        sm.add_widget(DefinicoesTela(name="definicoes"))
        sm.add_widget(GrandezasRepresentacoes(name="grandezas_representacoes"))
        sm.add_widget(GrandezasTela(name="grandezas_tela"))
        sm.add_widget(DefinicoesGrandezas(name="grandezas_definicoes"))
        sm.add_widget(GeometriaTela(name="geometria_tela"))
        sm.add_widget(DefinicoesGeometria(name="geometria_definicoes"))
        sm.add_widget(GeometriaRepresentacoes(name="geometria_representacoes"))
        sm.add_widget(TelaJogar(name="jogar_p", dificuldade="Primário", jogos=JogosPrimario.get()))
        sm.add_widget(TelaJogar(name="jogar_f", dificuldade="Fundamental", jogos=JogosFundamental.get()))
        sm.add_widget(TelaJogar(name="jogar", dificuldade="Médio", jogos=JogosMedio.get()))
        sm.add_widget(TelaEscolhaNivel(name="primario", dificuldade="primario", titulo="Fundamental I", tela_voltar="jogar"))
        sm.add_widget(TelaEscolhaNivel(name="fundamental", dificuldade="fundamental", titulo="Fundamental II", tela_voltar="jogar"))
        sm.add_widget(TelaEscolhaNivel(name="medio", dificuldade="medio", titulo="Ensino Médio", tela_voltar="jogar"))
        sm.add_widget(calculoI(name="game1"))
        sm.add_widget(CruzadinhaScreen(name="cross_p", dificuldade="fundI"))
        sm.add_widget(CruzadinhaScreen(name="cross_f", dificuldade="fundII"))
        sm.add_widget(CruzadinhaScreen(name="cross", dificuldade="medio"))
        sm.add_widget(AlgebraGameScreen(name="algebra"))
        sm.add_widget(TelaFimAlgebra(name="fim_algebra"))
        sm.add_widget(TelaFimFracoes(name="fim_fracoes"))
        sm.add_widget(FracoesGameScreen(name="fracoes"))
        sm.add_widget(AlgebraTela(name="algebra_tela"))
        sm.add_widget(AlgebraRepresentacoes(name="algebra_representacoes"))
        sm.add_widget(AlgebraDefinicoes(name="algebra_definicoes"))
        return sm


if __name__ == "__main__":
    TesteApp().run()



