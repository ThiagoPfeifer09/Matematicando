from kivymd.uix.button import MDRaisedButton
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.widget import MDWidget
from kivy.core.text import LabelBase
import os
from kivy.uix.label import Label


font_path = os.path.join(os.path.dirname(__file__), "Fontes", "Duo-Dunkel.ttf")
print("[DEBUG] Fonte:", font_path, "exists:", os.path.exists(font_path))
LabelBase.register(name="BungeeShade", fn_regular=font_path)


class JogosPrimario:
    @staticmethod
    def get():
        return [
            {"nome": "Operações", "imagem": "Jogos/matematicando.webp", "tela": "primario"},
            {"nome": "Frações", "imagem": "Jogos/fracoes.webp", "tela": "fracoes_info"},
            {"nome": "Álgebra", "imagem": "Jogos/algebra.webp", "tela": "algebra"},
            {"nome": "Cruzadinha", "imagem": "Jogos/cross.webp", "tela": "cross_p"},
            {"nome": "Sudoku", "imagem": "Jogos/sudoku.webp", "tela": "sudoku"},
            {"nome": "Sudoku", "imagem": "Jogos/sudoku.webp", "tela": "sudoku"},
            {"nome": "Sudoku", "imagem": "Jogos/sudoku.webp", "tela": "sudoku"},
            {"nome": "Sudoku", "imagem": "Jogos/sudoku.webp", "tela": "sudoku"},
            {"nome": "Sudoku", "imagem": "Jogos/sudoku.webp", "tela": "sudoku"},
        ]

class JogosFundamental:
    @staticmethod
    def get():
        return [
            {"nome": "Operações", "imagem": "Jogos/matematicando.webp", "tela": "fundamental"},
            {"nome": "Álgebra", "imagem": "Jogos/algebra.webp", "tela": "algebra"},
            {"nome": "Frações", "imagem": "Jogos/fracoes.webp", "tela": "fracoes_info"},
            {"nome": "Cruzadinha", "imagem": "Jogos/cross.webp", "tela": "cross_f"},
            {"nome": "Sudoku", "imagem": "Jogos/sudoku.webp", "tela": "sudoku"},
            {"nome": "Frações", "imagem": "Jogos/fracoes.webp", "tela": "fracoes_info"},
            {"nome": "Frações", "imagem": "Jogos/fracoes.webp", "tela": "fracoes_info"},
            {"nome": "Frações", "imagem": "Jogos/fracoes.webp", "tela": "fracoes_info"},
            {"nome": "Frações", "imagem": "Jogos/fracoes.webp", "tela": "fracoes_info"},
        ]

class JogosMedio:
    @staticmethod
    def get():
        return [
            {"nome": "Operações", "imagem": "Jogos/matematicando.webp", "tela": "medio"},
            {"nome": "Álgebra", "imagem": "Jogos/algebra.webp", "tela": "algebra"},
            {"nome": "Frações", "imagem": "Jogos/fracoes.webp", "tela": "fracoes_info"},
            {"nome": "Cruzadinha", "imagem": "Jogos/cross.webp", "tela": "cross"},
            {"nome": "Sudoku", "imagem": "Jogos/sudoku.webp", "tela": "sudoku"},
            {"nome": "Cruzadinha", "imagem": "Jogos/cross.webp", "tela": "cross"},
            {"nome": "Cruzadinha", "imagem": "Jogos/cross.webp", "tela": "cross"},
            {"nome": "Cruzadinha", "imagem": "Jogos/cross.webp", "tela": "cross"},
            {"nome": "Cruzadinha", "imagem": "Jogos/cross.webp", "tela": "cross"},
        ]


class Tab(MDBoxLayout, MDTabsBase):
    """Aba personalizada para conter os jogos."""
    pass


class TelaJogar(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Variável para controlar qual aba está ativa (Padrão inicial)
        self.categoria_atual = "Fundamental I"

        # ===== Fundo =====
        bg = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(bg)

        # ===== Layout principal =====
        main_layout = MDBoxLayout(orientation="vertical")
        self.add_widget(main_layout)

        top_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(90),
            padding=[dp(10), dp(20), dp(10), dp(5)],
            spacing=dp(10)
        )

        # Botão voltar
        back_btn = MDIconButton(
            icon="arrow-left",
            pos_hint={"center_y": 0.5},
            icon_size=dp(36),
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            on_release=self.voltar
        )
        top_layout.add_widget(back_btn)

        title = Label(
            text="SELECIONE O JOGO",
            font_name="BungeeShade",
            font_size="22sp",
            color=(0, 0, 0, 1),
            size_hint=(None, 1),
            halign="left",
            valign="middle",
        )

        # Necessário para o texto respeitar halign/valign
        title.bind(texture_size=lambda inst, val: setattr(inst, "width", val[0] + dp(20)))

        top_layout.add_widget(title)

        # empurra levemente para a direita
        top_layout.add_widget(MDWidget())

        main_layout.add_widget(top_layout)

        # ===== Lista de jogos =====
        self.content_area = MDBoxLayout()
        main_layout.add_widget(self.content_area)

        # ===== Bottom Bar =====
        self.bottom_bar = BottomBar(self.trocar_aba)
        main_layout.add_widget(self.bottom_bar)

        self.mostrar_jogos("Fundamental I")

    # ======================================================================
    def trocar_aba(self, nome):
        self.mostrar_jogos(nome)

    # ======================================================================
    def mostrar_jogos(self, categoria):
        # 1. ATUALIZAÇÃO AQUI: Salva a categoria atual para usar no clique
        self.categoria_atual = categoria

        self.content_area.clear_widgets()

        if categoria == "Fundamental I":
            jogos = JogosPrimario.get()
        elif categoria == "Fundamental II":
            jogos = JogosFundamental.get()
        else:
            jogos = JogosMedio.get()

        jogos = jogos[:9]

        container = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
            padding=[dp(15), dp(2), dp(15), dp(5)],
            spacing=dp(5)
        )

        grid = MDGridLayout(
            cols=3,
            spacing=dp(12),
            padding=dp(10),
            adaptive_height=True,
            size_hint=(1, None),
        )

        for jogo in jogos:
            card = MDCard(
                size_hint=(1, None),
                height=dp(150),
                radius=[18],
                elevation=4,
                md_bg_color=(1, 1, 1, 0.96),
                ripple_behavior=True,
                on_release=lambda inst, j=jogo: self.aciona_jogo(j),
            )

            box = MDBoxLayout(
                orientation="vertical",
                padding=dp(8),
                spacing=dp(6),
            )

            img = Image(
                source=jogo["imagem"],
                size_hint=(1, 1),
                allow_stretch=True,
                keep_ratio=True
            )

            nome = MDLabel(
                text=jogo["nome"],
                halign="center",
                theme_text_color="Custom",
                text_color=(0, 0, 0, 1),
                font_size="14sp",
                size_hint_y=None,
                height=dp(22),
            )

            box.add_widget(img)
            box.add_widget(nome)
            card.add_widget(box)
            grid.add_widget(card)

        container.add_widget(grid)
        self.content_area.add_widget(container)

    # ======================================================================
    def aciona_jogo(self, jogo):
        nome_tela = jogo["tela"]

        # Define a dificuldade baseada na aba atual
        dificuldade = "Primario"
        if self.categoria_atual == "Fundamental I":
            dificuldade = "Primario"
        elif self.categoria_atual == "Fundamental II":
            dificuldade = "Fundamental"
        else:
            dificuldade = "Medio"

        try:
            # Pega a tela pelo gerenciador
            screen = self.manager.get_screen(nome_tela)

            # SE a tela tiver a função 'definir_dificuldade', a gente chama ela
            if hasattr(screen, 'definir_dificuldade'):
                screen.definir_dificuldade(dificuldade)
                print(f"Dificuldade {dificuldade} definida para {nome_tela}")

        except Exception as e:
            print(f"Erro ao configurar dificuldade: {e}")

        # Muda para a tela do jogo
        self.manager.current = nome_tela

    def voltar(self, instance):
        self.manager.current = "inicial"


class CardJogo(MDCard):
    def __init__(self, nome, imagem, on_release, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = (dp(260), dp(120))
        self.radius = [25]
        self.elevation = 8
        self.md_bg_color = (1,1,1,1)
        self.ripple_behavior = True
        self.on_release = on_release
        self.padding = dp(12)

        layout = MDBoxLayout(orientation="horizontal", spacing=dp(15))

        layout.add_widget(
            Image(source=imagem, size_hint=(None,None), size=(dp(70),dp(70)))
        )

        layout.add_widget(
            MDLabel(
                text=nome,
                halign="left",
                valign="center",
                font_style="H6",
                theme_text_color="Custom",
                text_color=(0,0,0,1)
            )
        )

        self.add_widget(layout)


class BottomBar(MDBoxLayout):
    def __init__(self, on_change, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(70)
        self.padding = dp(10)
        self.spacing = dp(20)
        self.md_bg_color = (1, 1, 1, 1)
        self.radius = [20, 20, 0, 0]

        self.on_change = on_change
        self.buttons = {}

        abas = [
            ("Fundamental I", "school"),
            ("Fundamental II", "book-open-variant"),
            ("Médio", "chart-bar"),
        ]

        for nome, icon in abas:

            # === Botão principal ===
            btn = MDBoxLayout(
                orientation="horizontal",
                spacing=dp(10),
                padding=[dp(10), dp(5), dp(10), dp(5)],
                size_hint=(1, 1),
                on_touch_down=self._make_callback(nome),
            )

            # Ícone centralizado verticalmente
            ic = MDIconButton(
                icon=icon,
                theme_text_color="Custom",
                text_color=(0.4, 0.4, 0.4, 1),
                icon_size=dp(24),
                size_hint=(None, None),
                size=(dp(40), dp(40)),
                pos_hint={"center_y": 0.4},
            )

            # ===== Textos centralizados =====
            text_box = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, 1),
                spacing=dp(0),
                pos_hint={"center_y": 0.5},
            )

            lbl_top = Label(
                text="Ensino",
                halign="center",
                valign="middle",
                font_size=40,
                color=(0.4, 0.4, 0.4, 1),
                size_hint_y=None,
                height=dp(18),
            )

            lbl_bottom = Label(
                text=nome,
                halign="center",
                valign="middle",
                font_size=33,
                color=(0.4, 0.4, 0.4, 1),
                size_hint_y=None,
                height=dp(18),
            )

            text_box.add_widget(lbl_top)
            text_box.add_widget(lbl_bottom)

            # monta o botão
            btn.add_widget(ic)
            btn.add_widget(text_box)

            # adiciona no bottom bar
            self.add_widget(btn)

            # salva para depois alterar cor
            self.buttons[nome] = (ic, lbl_top, lbl_bottom)


        self.selecionar("Fundamental I")

    def selecionar(self, nome):
        # resetar todos
        for ic, t1, t2 in self.buttons.values():
            cor = (0.5, 0.5, 0.5, 1)
            ic.text_color = cor
            t1.text_color = cor
            t2.text_color = cor

        # destacar selecionado
        ic, t1, t2 = self.buttons[nome]
        azul = (0, 0.45, 1, 1)
        ic.text_color = azul
        t1.text_color = azul
        t2.text_color = azul

    def _make_callback(self, nome):
        def callback(instance, touch):
            if instance.collide_point(*touch.pos):
                self.selecionar(nome)
                # corrige nomes diferentes
                if nome == "Médio":
                    self.on_change("Medio")
                else:
                    self.on_change(f"Fundamental {nome[-1]}")
        return callback


from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatIconButton
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.metrics import dp, sp # Importante para tamanhos corretos
from kivy.app import App

# =======================================================================================================================
# Tela de seleção da operação e rodadas do matematicando
class TelaEscolhaNivel(MDScreen):
    def __init__(self, dificuldade, titulo, tela_voltar, **kwargs):
        super().__init__(**kwargs)
        self.dificuldade = dificuldade
        self.tela_voltar = tela_voltar

        # Layout principal
        layout = FloatLayout()

        # Imagem de fundo
        self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.bg_image)

        # --- TÍTULO PRINCIPAL ---
        title = MDLabel(
            text=titulo,
            halign="center",
            font_name="BungeeShade", # Certifique-se que a fonte existe, senão remova essa linha
            font_style="H4", # Estilo de tamanho padrão do Material Design
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1), # Texto preto para contraste ou branco dependendo do fundo
            pos_hint={"center_x": 0.5, "top": 0.95},
            size_hint=(1, None),
            height=dp(50)
        )
        layout.add_widget(title)

        # --- CARD DE FUNDO (Área dos botões) ---
        # Isso ajuda a ler o texto independente da imagem de fundo
        card_bg = MDCard(
            size_hint=(0.9, 0.65),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            radius=[20, 20, 20, 20],
            md_bg_color=(1, 1, 1, 0.8), # Branco semi-transparente
            elevation=2
        )
        layout.add_widget(card_bg)

        # --- COLUNA ESQUERDA: RODADAS ---
        rodadas_label = MDLabel(
            text="Rodadas",
            halign="center",
            font_size="22sp",
            bold=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            pos_hint={"center_x": 0.28, "top": 0.85}, # Alinhado à esquerda
            size_hint=(0.4, None),
            height=dp(30)
        )
        layout.add_widget(rodadas_label)

        # Botões de Rodadas (Alinhados verticalmente na esquerda)
        self.button_3 = self.create_rodada_button("3", 0.75, 3, "numeric-3-circle")
        self.button_6 = self.create_rodada_button("6", 0.65, 6, "numeric-6-circle")
        self.button_10 = self.create_rodada_button("10", 0.55, 10, "numeric-10-circle")

        for btn in [self.button_3, self.button_6, self.button_10]:
            layout.add_widget(btn)

        # --- COLUNA DIREITA: OPERAÇÕES ---
        operacoes_label = MDLabel(
            text="Operação",
            halign="center",
            font_size="22sp",
            bold=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            pos_hint={"center_x": 0.72, "top": 0.85}, # Alinhado à direita
            size_hint=(0.4, None),
            height=dp(30)
        )
        layout.add_widget(operacoes_label)

        # Botões de Operação (Alinhados verticalmente na direita)
        # Ajustei os espaçamentos para caberem 4 botões
        self.op_soma = self.create_operacao_button("Soma", 0.75, "soma", "plus")
        self.op_subtracao = self.create_operacao_button("Subtração", 0.65, "subtracao", "minus")
        self.op_multiplicacao = self.create_operacao_button("Mult.", 0.55, "multiplicacao", "close")
        self.op_divisao = self.create_operacao_button("Divisão", 0.45, "divisao", "division")

        for btn in [self.op_soma, self.op_subtracao, self.op_multiplicacao, self.op_divisao]:
            layout.add_widget(btn)

        # --- RODAPÉ: BOTÕES DE AÇÃO ---

        # Botão Iniciar (Maior e com destaque)
        self.calculos_button = MDRaisedButton(
            text="INICIAR PARTIDA",
            size_hint=(0.6, None),
            height=dp(55),
            font_size="20sp",
            pos_hint={"center_x": 0.5, "center_y": 0.15},
            on_release=self.iniciar_jogo,
            md_bg_color=(0.8, 0.8, 0.8, 1), # Cinza desabilitado inicial
            text_color=(1, 1, 1, 1),
            elevation=3,
            disabled=True
        )
        layout.add_widget(self.calculos_button)

        # Botão Voltar (Menor, discreto)
        voltar_button = MDRaisedButton(
            text="Voltar",
            size_hint=(0.3, None),
            height=dp(40),
            font_size="16sp",
            pos_hint={"center_x": 0.5, "center_y": 0.06},
            on_release=self.voltar_tela_inicial,
            md_bg_color=(0.8, 0.4, 0.4, 1), # Vermelho suave
            text_color=(1, 1, 1, 1),
            elevation=1
        )
        layout.add_widget(voltar_button)

        self.add_widget(layout)

        self.botao_selecionado = None
        self.operacao_selecionada = None

    # --- FUNÇÕES DE CRIAÇÃO VISUAL ---

    def create_rodada_button(self, text, center_y, rodadas_value, icon_name):
        return MDFillRoundFlatIconButton(
            text=f"{text} Rounds",
            icon=icon_name,
            size_hint=(0.40, None), # Ocupa 40% da largura
            height=dp(50),
            font_size="16sp",
            pos_hint={"center_x": 0.28, "center_y": center_y},
            on_release=lambda x: self.definir_rodadas(rodadas_value),
            md_bg_color=(0.2, 0.6, 0.8, 1), # Azul padrão
            text_color=(1, 1, 1, 1),
            icon_color=(1, 1, 1, 1)
        )

    def create_operacao_button(self, text, center_y, operacao_value, icon_name):
        return MDFillRoundFlatIconButton(
            text=text,
            icon=icon_name,
            size_hint=(0.40, None), # Ocupa 40% da largura
            height=dp(50),
            font_size="16sp",
            pos_hint={"center_x": 0.72, "center_y": center_y},
            on_release=lambda x: self.definir_operacao(operacao_value),
            md_bg_color=(0.4, 0.4, 0.6, 1), # Roxo padrão
            text_color=(1, 1, 1, 1),
            icon_color=(1, 1, 1, 1)
        )

    # --- LÓGICA (Mantida praticamente igual, apenas cores atualizadas) ---

    def voltar_tela_inicial(self, instance):
        self.manager.current = self.tela_voltar

    def definir_rodadas(self, rodadas_value):
        self.valor_rodadas = rodadas_value

        # Mapeamento para acesso fácil
        mapa_botoes = {
            3: self.button_3,
            6: self.button_6,
            10: self.button_10
        }
        self.botao_selecionado = mapa_botoes[rodadas_value]

        # Reseta cores
        for btn in mapa_botoes.values():
            btn.md_bg_color = (0.2, 0.6, 0.8, 1) # Azul padrão
            btn.elevation = 1

        # Destaca selecionado
        self.botao_selecionado.md_bg_color = (0, 0.7, 0, 1) # Verde Selecionado
        self.botao_selecionado.elevation = 4

        self.verificar_pronto()

    def definir_operacao(self, operacao_value):
        self.operacao_selecionada = operacao_value
        botoes = {
            "soma": self.op_soma,
            "subtracao": self.op_subtracao,
            "multiplicacao": self.op_multiplicacao,
            "divisao": self.op_divisao
        }

        # Reseta cores
        for btn in botoes.values():
            btn.md_bg_color = (0.4, 0.4, 0.6, 1) # Roxo padrão
            btn.elevation = 1

        # Destaca selecionado
        botoes[operacao_value].md_bg_color = (0, 0.7, 0, 1) # Verde Selecionado
        botoes[operacao_value].elevation = 4

        self.verificar_pronto()

    def verificar_pronto(self):
        if hasattr(self, 'valor_rodadas') and self.operacao_selecionada:
            self.calculos_button.disabled = False
            self.calculos_button.md_bg_color = (0, 0.6, 0, 1) # Verde Sólido
            self.calculos_button.text_color = (1, 1, 1, 1)
            # Animação simples de pulso poderia ser adicionada aqui

    def iniciar_jogo(self, instance):
        app = App.get_running_app()
        sm = app.root
        sm.current = "game1"
        game1 = sm.get_screen("game1")

        game1.define_dificul(self.dificuldade)
        game1.confirma_rodadas(self.valor_rodadas)
        game1.escolha_modo("normal")
        game1.define_operacao(self.operacao_selecionada.lower())
        game1.inicia_nivel(1)