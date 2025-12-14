from kivy.core.text import LabelBase
import os
from kivy.uix.boxlayout import BoxLayout
from random import choice
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDIconButton, MDRectangleFlatButton, MDRaisedButton, MDRectangleFlatIconButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.slider import MDSlider
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.card import MDCard
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivy.uix.modalview import ModalView
font_path = os.path.join(os.path.dirname(__file__), "Fontes", "Duo-Dunkel.ttf")
print("[DEBUG] Fonte:", font_path, "exists:", os.path.exists(font_path))
LabelBase.register(name="BungeeShade", fn_regular=font_path)
from kivy.animation import Animation

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
            source="matemas.webp",
            size_hint=(0.80, None),
            height=200,
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(logo)

        # --- BOTÕES PRINCIPAIS (Centralizados) ---
        botao_jogar = ImageButton(
            source="jogar.webp",
            size_hint=(None, None),
            size=(400, 180),
            pos_hint={"center_x": 0.5, "center_y": 0.68},
        )
        botao_jogar.bind(on_release=lambda *a: self.seleciona_n())
        layout.add_widget(botao_jogar)

        botao_conteudos = ImageButton(
            source="conteudos.webp",
            size_hint=(None, None),
            size=(400, 180),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        botao_conteudos.bind(on_release=lambda *a: self.acao_conteudos())
        layout.add_widget(botao_conteudos)

        botao_tutorial = ImageButton(
            source="tutorial.webp",
            size_hint=(None, None),
            size=(400, 180),
            pos_hint={"center_x": 0.5, "center_y": 0.32},
        )
        botao_tutorial.bind(on_release=lambda *a: self.acao_tutorial())
        layout.add_widget(botao_tutorial)

        # --- BOTÃO DE LOGIN (Novo - Canto Esquerdo) ---
        login_button = MDIconButton(
            icon="account-circle",
            icon_size=dp(32),
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1), # Preto igual ao config
            pos_hint={"x": 0.02, "top": 0.98},
        )
        login_button.bind(on_release=self.abrir_popup_login)
        layout.add_widget(login_button)

        # --- BOTÃO DE CONFIGURAÇÕES (Canto Direito) ---
        settings_button = MDIconButton(
            icon="cog",
            icon_size=dp(32), # Garante o mesmo tamanho do login
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            pos_hint={"right": 0.98, "top": 0.98},
        )
        settings_button.bind(on_release=lambda *a: self.abrir_tela_config())
        layout.add_widget(settings_button)

        self.add_widget(layout)

    # --- MÉTODOS DE ORGANIZAÇÃO ---

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
                text_color=(0, 0, 0, 0.08), # Marca d'água
                pos_hint=pos,
                icon_size=dp(45),
                disabled=True
            )
            layout.add_widget(icon)

    # --- AÇÕES DE NAVEGAÇÃO ---

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

    def abrir_popup_login(self, instance):
        # Certifique-se de que a variável CORAL está definida no topo do seu arquivo
        # Se não estiver, troque CORAL abaixo por (1, 0.5, 0.31, 1) ou outra cor.
        self.dialog_login = MDDialog(
            title="Conta",
            text="A sincronização com Google/Hotmail será implementada em breve!",
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=CORAL, # Verifique se CORAL está importada/definida
                    on_release=lambda x: self.dialog_login.dismiss()
                )
            ],
        )
        self.dialog_login.open()
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
            ("Estudos/novo_Operacoes.webp", "tela"),
            ("Estudos/novo_Algebra.webp", "algebra_tela"),
            ("Estudos/novo_Geometria.webp", "geometria_tela"),
            ("Estudos/novo_Grandezas.webp", "grandezas_tela"),
            ("Estudos/novo_Estatistica.webp", "estatistica_tela"),
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

# -------------------------------------------------
# TELA DE CONFIGURAÇÕES
# -------------------------------------------------
class PainelConfiguracoes(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Configurações do Modal (Fundo transparente)
        self.background_color = (0, 0, 0, 0)
        self.auto_dismiss = False
        self.size_hint = (1, 1)

        # Largura do painel (90% da tela)
        self.painel_width = 0.90

        # --- CONTAINER PRINCIPAL (PAINEL LATERAL) ---
        # Definindo uma cor de fundo fixa (Bege) para o painel
        self.painel = MDBoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(10),
            size_hint=(self.painel_width, 1),
            md_bg_color=(1, 1, 1, 1),  # #FFDBBB (Bege)
        )
        self.add_widget(self.painel)

        # ============================================
        # 1. CABEÇALHO (Botão Fechar + Título)
        # ============================================
        header_box = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(50),
            spacing=dp(10),
        )

        btn_fechar = MDIconButton(
            icon="close",
            icon_size=dp(28),
            theme_text_color="Custom",
            text_color=PRETO,
            on_release=lambda *a: self.fechar()
        )

        lbl_titulo = MDLabel(
            text="Configurações",
            font_style="H5",
            theme_text_color="Custom",
            text_color=PRETO,
            valign="center",
            bold=True
        )

        header_box.add_widget(btn_fechar)
        header_box.add_widget(lbl_titulo)
        self.painel.add_widget(header_box)

        # ============================================
        # 2. ÁREA DE ROLAGEM (Para o conteúdo caber)
        # ============================================
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)

        # Conteúdo interno (Vertical)
        conteudo = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            size_hint_y=None,
            adaptive_height=True,
            padding=[0, dp(10), 0, dp(20)] # Padding interno
        )

        # --- A. PERFIL DO USUÁRIO (GAMIFICADO) ---
        card_perfil = MDCard(
            orientation="vertical",
            size_hint_y=None,
            height=dp(180),
            padding=dp(15),
            spacing=dp(10),
            radius=[dp(15)],
            elevation=2,
            md_bg_color=(1, 1, 1, 1) # Fundo branco no card para contraste
        )

        # Linha topo: Avatar + Nome
        linha_topo = MDBoxLayout(orientation="horizontal", spacing=dp(15), size_hint_y=None, height=dp(60))

        avatar = Image(
            source="matemas.webp", # Certifique-se que a imagem existe
            size_hint=(None, 1),
            width=dp(60),
            allow_stretch=True
        )

        box_nome = MDBoxLayout(orientation="vertical", pos_hint={'center_y': 0.5})
        linha_nome = MDBoxLayout(orientation="horizontal", spacing=dp(5))

        lbl_nome_user = MDLabel(text="Jogador: Breno", font_style="H6", theme_text_color="Primary", bold=True, adaptive_size=True)
        btn_edit = MDIconButton(icon="pencil", icon_size=dp(16), theme_text_color="Hint", pos_hint={'center_y': 0.5})

        linha_nome.add_widget(lbl_nome_user)
        linha_nome.add_widget(btn_edit)

        lbl_titulo_nivel = MDLabel(text="Iniciante", theme_text_color="Secondary", font_style="Caption")

        box_nome.add_widget(linha_nome)
        box_nome.add_widget(lbl_titulo_nivel)

        linha_topo.add_widget(avatar)
        linha_topo.add_widget(box_nome)
        card_perfil.add_widget(linha_topo)

        # Barra de XP
        box_xp = MDBoxLayout(orientation="vertical", spacing=dp(5), size_hint_y=None, height=dp(30))
        linha_txt_xp = MDBoxLayout(orientation="horizontal")
        linha_txt_xp.add_widget(MDLabel(text="Nível 1", bold=True, theme_text_color="Primary", font_style="Subtitle2"))
        linha_txt_xp.add_widget(MDLabel(text="120/500 XP", halign="right", theme_text_color="Secondary", font_style="Caption"))

        barra_xp = MDProgressBar(value=24, color=LILAS, size_hint_y=None, height=dp(8))

        box_xp.add_widget(linha_txt_xp)
        box_xp.add_widget(barra_xp)
        card_perfil.add_widget(box_xp)

        # Estatísticas
        linha_stats = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(40))

        def criar_stat(icone, valor, cor_icone):
            box = MDBoxLayout(orientation="horizontal", spacing=dp(5), adaptive_width=True)
            icon = MDIcon(icon=icone, theme_text_color="Custom", text_color=cor_icone, pos_hint={'center_y': 0.5})
            label = MDLabel(text=valor, theme_text_color="Primary", font_style="Subtitle2", pos_hint={'center_y': 0.5}, adaptive_width=True)
            box.add_widget(icon)
            box.add_widget(label)
            return box

        linha_stats.add_widget(criar_stat("fire", "3 Dias", CORAL))
        linha_stats.add_widget(criar_stat("trophy", "12", (1, 0.8, 0, 1)))
        linha_stats.add_widget(criar_stat("bitcoin", "850", LILAS))

        card_perfil.add_widget(linha_stats)
        conteudo.add_widget(card_perfil)

        # --- B. PREFERÊNCIAS ---
        card_prefs = MDCard(
            orientation="vertical",
            size_hint_y=None,
            adaptive_height=True,
            padding=[dp(20), dp(25), dp(20), dp(25)],
            radius=[dp(15)],
            elevation=2,
            spacing=dp(25),
            md_bg_color=(1, 1, 1, 1)
        )
        card_prefs.add_widget(MDLabel(text="Preferências", theme_text_color="Primary", bold=True, adaptive_height=True))

        # Modo Escuro
        linha_tema = MDBoxLayout(orientation="horizontal", size_hint=(None, None), height=dp(40), adaptive_width=True, spacing=dp(20), pos_hint={"center_x": 0.5})
        linha_tema.add_widget(MDIcon(icon="theme-light-dark", pos_hint={"center_y": 0.5}, theme_text_color="Primary"))
        linha_tema.add_widget(MDLabel(text="Modo Escuro", pos_hint={"center_y": 0.5}, theme_text_color="Primary", adaptive_width=True))

        app = MDApp.get_running_app()
        is_dark = (app.theme_cls.theme_style == "Dark")

        self.switch_tema = MDSwitch(pos_hint={"center_y": 0.5}, size_hint_x=None, width=dp(64))
        self.switch_tema.active = is_dark
        self.switch_tema.bind(active=self.atualizar_tema)

        linha_tema.add_widget(self.switch_tema)
        card_prefs.add_widget(linha_tema)

        # Som
        linha_som = MDBoxLayout(orientation="horizontal", size_hint=(None, None), height=dp(40), adaptive_width=True, spacing=dp(20), pos_hint={"center_x": 0.5})
        linha_som.add_widget(MDIcon(icon="volume-high", pos_hint={"center_y": 0.5}, theme_text_color="Primary"))
        linha_som.add_widget(MDLabel(text="Efeitos Sonoros", pos_hint={"center_y": 0.5}, theme_text_color="Primary", adaptive_width=True))

        self.switch_som = MDSwitch(pos_hint={"center_y": 0.5}, size_hint_x=None, width=dp(64))
        self.switch_som.active = True
        self.switch_som.bind(active=self.atualizar_som)

        linha_som.add_widget(self.switch_som)
        card_prefs.add_widget(linha_som)

        # Slider Volume
        box_slider = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(15))
        self.label_volume = MDLabel(text="Volume: 75", theme_text_color="Secondary", font_style="Caption", halign="center")

        self.slider_volume = MDSlider(min=0, max=100, value=75, hint=True, size_hint_y=None, height=dp(40))
        self.slider_volume.bind(value=self.atualizar_volume)

        box_slider.add_widget(self.label_volume)
        box_slider.add_widget(self.slider_volume)
        card_prefs.add_widget(box_slider)

        conteudo.add_widget(card_prefs)

        # --- C. SUPORTE ---
        card_suporte = MDCard(
            orientation="vertical",
            size_hint_y=None,
            adaptive_height=True,
            padding=dp(15),
            spacing=dp(10),
            radius=[dp(15)],
            elevation=2,
            md_bg_color=(1, 1, 1, 1)
        )
        card_suporte.add_widget(MDLabel(text="Suporte", theme_text_color="Primary", bold=True, adaptive_height=True))

        btn_report = MDRectangleFlatIconButton(
            icon="bug", text="Reportar um problema",
            theme_text_color="Custom", text_color=PRETO,
            line_color=CORAL, icon_color=CORAL,
            size_hint_x=0.7, pos_hint={"center_x": 0.5}
        )
        self.btn_report_ref = btn_report

        btn_dev = MDRectangleFlatIconButton(
            icon="code-tags", text="Desenvolvedores",
            theme_text_color="Custom", text_color=PRETO,
            line_color=LILAS, icon_color=LILAS,
            size_hint_x=0.7, pos_hint={"center_x": 0.5}
        )
        self.btn_dev_ref = btn_dev

        card_suporte.add_widget(btn_report)
        card_suporte.add_widget(btn_dev)
        conteudo.add_widget(card_suporte)

        # Adicionar scroll ao painel
        scroll.add_widget(conteudo)
        self.painel.add_widget(scroll)


    # =====================================
    #           LÓGICA E MÉTODOS
    # =====================================

    def atualizar_volume(self, instance, value):
        self.label_volume.text = f"Volume: {int(value)}"

    def atualizar_tema(self, instance, value):
        app = MDApp.get_running_app()
        app.mudar_tema_global(value)

        # Como o fundo do painel é bege fixo, o texto precisa ser escuro
        # ou precisamos mudar a cor do painel também.
        # Aqui, mantive a lógica original, mas cuidado com contraste.
        cor_texto = (1, 1, 1, 1) if value else PRETO

        if hasattr(self, 'btn_report_ref'):
            self.btn_report_ref.text_color = cor_texto
        if hasattr(self, 'btn_dev_ref'):
            self.btn_dev_ref.text_color = cor_texto

    def atualizar_som(self, instance, value):
        app = MDApp.get_running_app()
        if hasattr(app, 'som_ligado'):
            app.som_ligado = value
        print(f"Som alterado para: {value}")

    # =====================================
    #           ANIMAÇÕES
    # =====================================
    def open(self, *args):
        super().open()
        # Posiciona o painel fora da tela (à direita)
        self.painel.x = self.width
        # Calcula posição final
        destino = self.width * (1 - self.painel_width)
        # Anima entrada
        Animation(x=destino, d=0.25, t='out_cubic').start(self.painel)

    def fechar(self, *args):
        # Anima saída para a direita
        anim = Animation(x=self.width, d=0.20, t='in_cubic')
        anim.bind(on_complete=lambda *a: ModalView.dismiss(self))
        anim.start(self.painel)

    def on_touch_down(self, touch):
        # Se clicar fora do painel, fecha
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

        sm.add_widget(calculoI(name="game1", dificuldade="primario"))
        sm.add_widget(calculoI(name="game2", dificuldade="funndamental"))
        sm.add_widget(calculoI(name="game3", dificuldade="medio"))

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
        sm.add_widget(TelaFimDeJogo(name="fim_de_jogo"))

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



