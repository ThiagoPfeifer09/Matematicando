from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivymd.uix.button import MDIconButton
from kivy.app import App

#=======================================================================================================================
# Tela de seleção da operação e rodadas do matematicando
class TelaJogar(Screen):
    def __init__(self, dificuldade, jogos, **kwargs):
        super().__init__(**kwargs)
        self.dificuldade = dificuldade
        self.jogos = jogos
        layout = FloatLayout()

        self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.bg_image)



        titulo = MDLabel(
            text=f"{dificuldade}\nSelecione o jogo que deseja jogar:",
            font_size=50,
            font_style='H4',
            halign="center",
            pos_hint={"center_x": 0.5, "top": 0.95},
            size_hint=(0.8, 0.2),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        layout.add_widget(titulo)

        self.back_button = MDIconButton(
            icon='arrow-left',
            pos_hint={'x': 0, 'top': 1},
            on_release=self.voltar
        )
        layout.add_widget(self.back_button)

        spacing_x, spacing_y = 0.3, 0.2
        start_x, start_y = 0.2, 0.7

        for index, jogo in enumerate(jogos):
            i, j = divmod(index, 3)
            pos = {"center_x": start_x + j * spacing_x, "center_y": start_y - i * spacing_y}

            card = MDCard(
                size_hint=(0.15, 0.15),
                pos_hint=pos,
                on_release=lambda instance, idx=index: self.aciona_jogo(idx),
                radius=[20],
                elevation=0,
                md_bg_color=(0, 0, 0, 0),
                ripple_behavior=True
            )

            img = Image(
                source=jogo["imagem"],
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(0.8, 0.8),
                pos_hint={"center_x": 0.5, "center_y": 0.5}
            )
            card.add_widget(img)
            layout.add_widget(card)

            label = MDLabel(
                text=jogo["nome"],
                halign="center",
                pos_hint={"center_x": pos["center_x"], "center_y": pos["center_y"] - 0.09},
                size_hint=(0.16, 0.15),
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
            layout.add_widget(label)

        self.add_widget(layout)

    def aciona_jogo(self, index):
        jogo = self.jogos[index]
        destino = self.manager.get_screen(jogo["tela"])

        # Define dificuldade antes de mudar de tela
        if hasattr(destino, "definir_dificuldade"):
            destino.definir_dificuldade(self.dificuldade)

        self.manager.current = jogo["tela"]

    def voltar(self, instance):
        self.manager.current = "seleciona"

# Tela dos jogos primario
class JogosPrimario:
    @staticmethod
    def get():
        return [
            {"nome": "Operações", "imagem": "matematicando.png", "tela": "primario"},
            {"nome": "Frações", "imagem": "fracoes.png", "tela": "fracoes"},
            {"nome": "Algebra", "imagem": "algebra.png", "tela": "algebra"},
            {"nome": "Cruzadinha", "imagem": "cross.png", "tela": "cross_p"},
            {"nome": "Não feito", "imagem": "nada.png", "tela": "nada"},
            {"nome": "Não feito", "imagem": "nada.png", "tela": "nada"},
            {"nome": "Não feito", "imagem": "nada.png", "tela": "nada"},
            {"nome": "Não feito", "imagem": "nada.png", "tela": "nada"},
            {"nome": "Não feito", "imagem": "nada.png", "tela": "nada"},
        ]

# Tela dos jogos fundamental
class JogosFundamental:
    @staticmethod
    def get():
        return [
            {"nome": "Operações", "imagem": "matematicando.png", "tela": "fundamental"},
            {"nome": "Álgebra", "imagem": "algebra.png", "tela": "algebra"},
            {"nome": "Frações", "imagem": "fracoes.png", "tela": "fracoes"},
            {"nome": "Cruzadinha", "imagem": "cross.png", "tela": "cross_f"},
            {"nome": "Não feito", "imagem": "n_feito.png", "tela": "nada"},
            {"nome": "Não feito", "imagem": "n_feito.png", "tela": "nada"},
            {"nome": "Não feito", "imagem": "n_feito.png", "tela": "nada"},
            {"nome": "Não feito", "imagem": "n_feito.png", "tela": "nada"},
            {"nome": "Não feito", "imagem": "n_feito.png", "tela": "nada"},
        ]

# Tela dos jogos medio
class JogosMedio:
    @staticmethod
    def get():
        return [
            {"nome": "Operações", "imagem": "matematicando.png", "tela": "medio"},
            {"nome": "Álgebra", "imagem": "algebra.png", "tela": "algebra"},
            {"nome": "Frações", "imagem": "fracoes.png", "tela": "fracoes"},
            {"nome": "Cruzadinha", "imagem": "cross.png", "tela": "cross"},
            {"nome": "Não feito", "imagem": "n_feito.png", "tela": "nada"},
            {"nome": "Não feito", "imagem": "n_feito.png", "tela": "nada"},
            {"nome": "Não feito", "imagem": "n_feito.png", "tela": "nada"},
            {"nome": "Não feito", "imagem": "n_feito.png", "tela": "nada"},
            {"nome": "Não feito", "imagem": "n_feito.png", "tela": "nada"},
        ]
#=======================================================================================================================


#=======================================================================================================================
# Tela de seleção da operação e rodadas do matematicando
class TelaEscolhaNivel(Screen):
    def __init__(self, dificuldade, titulo, tela_voltar, **kwargs):
        super().__init__(**kwargs)
        self.dificuldade = dificuldade
        self.tela_voltar = tela_voltar

        layout = FloatLayout()

        self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.bg_image)

        title = MDLabel(
            text=titulo,
            halign="center",
            font_style="H4",
            text_color=(1, 1, 1, 1),
            size_hint=(0.8, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.9},
        )
        layout.add_widget(title)

        rodadas_text = MDLabel(
            text="Quantas rodadas você deseja\n jogar em cada nível?",
            halign="center",
            font_size="20",
            text_color=(1, 1, 1, 1),
            size_hint=(0.5, None),
            height=50,
            pos_hint={"center_x": 0.3, "top": 0.8},
        )
        layout.add_widget(rodadas_text)

        self.button_3 = self.create_rodada_button("3 Rodadas", 0.7, 3)
        self.button_6 = self.create_rodada_button("6 Rodadas", 0.625, 6)
        self.button_10 = self.create_rodada_button("10 Rodadas", 0.55, 10)

        for btn in [self.button_3, self.button_6, self.button_10]:
            btn.pos_hint["center_x"] = 0.3
            btn.size_hint = (0.5, 0.08)
            btn.font_size = "50"
            layout.add_widget(btn)

        operacoes_text = MDLabel(
            text="Escolha a operação:",
            halign="center",
            font_size="20",
            text_color=(1, 1, 1, 1),
            size_hint=(0.5, None),
            height=50,
            pos_hint={"center_x": 0.7, "top": 0.8},
        )
        layout.add_widget(operacoes_text)

        self.op_soma = self.create_operacao_button("+ Soma", 0.7, "soma")
        self.op_subtracao = self.create_operacao_button("- Subtração", 0.625, "subtracao")
        self.op_multiplicacao = self.create_operacao_button("× Multiplicação", 0.55, "multiplicacao")
        self.op_divisao = self.create_operacao_button("÷ Divisão", 0.475, "divisao")

        for btn in [self.op_soma, self.op_subtracao, self.op_multiplicacao, self.op_divisao]:
            btn.pos_hint["center_x"] = 0.7
            btn.size_hint = (0.4, 0.06)
            btn.font_size = "50"
            layout.add_widget(btn)

        self.calculos_button = MDRaisedButton(
            text="Iniciar Partida",
            size_hint=(0.3, 0.08),
            height=50,
            font_size="24sp",
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            on_release=self.iniciar_jogo,
            md_bg_color=(0.5, 0.5, 0.5, 1),
            text_color=(1, 1, 1, 0.5),
            disabled=True
        )
        layout.add_widget(self.calculos_button)

        voltar_button = MDRaisedButton(
            text="Voltar",
            size_hint=(0.3, 0.08),
            height=50,
            font_size="24sp",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            on_release=self.voltar_tela_inicial,
            md_bg_color=(0.5, 0.5, 0.5, 1),
            text_color=(1, 1, 1, 1),
        )
        layout.add_widget(voltar_button)

        self.add_widget(layout)

        self.botao_selecionado = None
        self.operacao_selecionada = None

    def voltar_tela_inicial(self, instance):
        self.manager.current = self.tela_voltar


    def create_rodada_button(self, text, center_y, rodadas_value):
        return MDRaisedButton(
            text=text,
            size_hint=(0.17, 0.03),
            height=50,
            font_size="24sp",
            pos_hint={"center_y": center_y},
            on_release=lambda x: self.definir_rodadas(rodadas_value),
            md_bg_color=(0.2, 0.6, 0.8, 1),
            text_color=(1, 1, 1, 1),
        )

    def create_operacao_button(self, text, center_y, operacao_value):
        return MDRaisedButton(
            text=text,
            size_hint=(0.35, 0.05),
            height=50,
            font_size="20sp",
            pos_hint={"center_y": center_y},
            on_release=lambda x: self.definir_operacao(operacao_value),
            md_bg_color=(0.4, 0.4, 0.6, 1),
            text_color=(1, 1, 1, 1),
        )

    def definir_rodadas(self, rodadas_value):
        self.valor_rodadas = rodadas_value
        self.botao_selecionado = {
            3: self.button_3,
            6: self.button_6,
            10: self.button_10
        }[rodadas_value]

        for btn in [self.button_3, self.button_6, self.button_10]:
            btn.md_bg_color = (0.2, 0.6, 0.8, 1)
        self.botao_selecionado.md_bg_color = (0, 0.8, 0.4, 1)

        self.verificar_pronto()

    def definir_operacao(self, operacao_value):
        self.operacao_selecionada = operacao_value
        botoes = {
            "soma": self.op_soma,
            "subtracao": self.op_subtracao,
            "multiplicacao": self.op_multiplicacao,
            "divisao": self.op_divisao
        }

        for btn in botoes.values():
            btn.md_bg_color = (0.4, 0.4, 0.6, 1)
        botoes[operacao_value].md_bg_color = (0, 0.8, 0.4, 1)

        self.verificar_pronto()

    def verificar_pronto(self):
        if hasattr(self, 'valor_rodadas') and self.operacao_selecionada:
            self.calculos_button.disabled = False
            self.calculos_button.md_bg_color = (0, 0.6, 0, 1)
            self.calculos_button.text_color = (1, 1, 1, 1)

    def iniciar_jogo(self, instance):
        app = App.get_running_app()
        sm = app.root  # o ScreenManager principal
        sm.current = "game1"
        game1 = sm.get_screen("game1")

        game1.define_dificul(self.dificuldade)
        game1.confirma_rodadas(self.valor_rodadas)
        game1.escolha_modo("normal")
        game1.define_operacao(self.operacao_selecionada.lower())
        game1.inicia_nivel(1)

#=======================================================================================================================
