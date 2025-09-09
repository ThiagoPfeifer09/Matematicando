from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.core.text import LabelBase
import random

LabelBase.register(name="ComicNeue", fn_regular="ComicNeue-Regular.ttf")


class CardBotao(MDRaisedButton):
    def __init__(self, texto, on_press_func, **kwargs):
        super().__init__(
            text=texto,
            on_release=lambda x: on_press_func(texto),
            size_hint=(1, 1),
            font_size="20sp",
            md_bg_color=random.choice([
                (1.0, 111 / 255, 64 / 255, 1),
                (0.36, 0.8, 0.96, 1),
                (0.85, 0.53, 0.97, 1),
                (0.59, 0.43, 0.91, 1),
            ]),
            text_color=(1, 1, 1, 1),
            font_name="ComicNeue",
            elevation=6,
            **kwargs
        )


class TelaCruzadinha7x7(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs = []
        self.gabarito = []

        # Fundo
        self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False,
                              size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.bg_image)

        self.main_layout = FloatLayout()
        self.add_widget(self.main_layout)

        # Barra superior
        self.top_layout = MDBoxLayout(orientation='horizontal', padding=[dp(10), dp(10)], spacing=dp(10),
                                      size_hint=(1, 0.1), pos_hint={"top": 1})
        self.btn_voltar = MDIconButton(icon="arrow-left", on_release=self.voltar)
        self.pontuacao_label = MDLabel(text="Pontuação: 0", halign="right", font_style="H6",
                                       theme_text_color="Custom", text_color=(1, 1, 1, 1), font_name="ComicNeue")
        self.top_layout.add_widget(self.btn_voltar)
        self.top_layout.add_widget(self.pontuacao_label)
        self.main_layout.add_widget(self.top_layout)

        # Grid 7x7
        self.grid = MDGridLayout(cols=7, rows=7, spacing=dp(5), padding=dp(5),
                                 size_hint=(0.95, 0.7), pos_hint={"center_x": 0.5, "top": 0.9})
        self.main_layout.add_widget(self.grid)

        # Barra inferior
        self.base_layout = MDBoxLayout(orientation='horizontal', spacing=dp(20), padding=dp(20),
                                       size_hint=(1, 0.2), pos_hint={'y': 0})
        self.btn_verificar = CardBotao("Verificar", self.verificar_respostas)
        self.btn_limpar = CardBotao("Limpar", self.limpar_respostas)
        self.btn_nova = CardBotao("Nova cruzadinha", self.nova_cruzadinha)

        self.base_layout.add_widget(self.btn_verificar)
        self.base_layout.add_widget(self.btn_limpar)
        self.base_layout.add_widget(self.btn_nova)
        self.main_layout.add_widget(self.base_layout)

        # Primeira cruzadinha
        self.gerar_cruzadinha()

    def gerar_cruzadinha(self):
        self.inputs.clear()
        self.gabarito.clear()
        self.grid.clear_widgets()

        # Layout fixo 7x7
        layout = [
            ["VAL", "+", "VAL", "-", "VAL", "=", ""],
            ["÷", None, "÷", None, "+", None, None],
            ["VAL", "+", "VAL", "+", "VAL", "=", "VAL"],
            ["×", None, "+", None, "+", None, None],
            ["VAL", "+", "VAL", "-", "VAL", "=", "VAL"],
            ["=", None, "=", None, "=", None, None],
            ["VAL", None, "VAL", None, "VAL", None, None],
        ]

        matriz = [[None for _ in range(7)] for _ in range(7)]

        # Geração dos valores
        while True:
            # Linha 0: A + B = C
            A = random.randint(5, 15)
            B = random.randint(2, 10)
            C = A + B

            # Linha 4: D × E = F
            D = random.randint(2, 5)
            E = random.randint(2, 5)
            F = D * E

            # Linha 6: G + H = I
            G = random.randint(3, 10)
            H = random.randint(3, 10)
            I = G + H

            if len({A, B, C, D, E, F, G, H, I}) < 7:
                continue
            break

        # Preencher matriz
        matriz[0][0] = A
        matriz[0][2] = B
        matriz[0][4] = C

        matriz[4][0] = D
        matriz[4][2] = E
        matriz[4][4] = F

        matriz[6][0] = G
        matriz[6][2] = H
        matriz[6][4] = I

        # Construção do grid
        for i in range(7):
            for j in range(7):
                val = layout[i][j]
                dado = matriz[i][j]
                conteudo = None

                if val is None:
                    conteudo = MDCard(
                        md_bg_color=(0, 0, 0, 0),
                        style="outlined",
                        line_color=(0, 0, 0, 1),
                        radius=[dp(4)],
                        size_hint=(1, 1),
                        elevation=0,
                    )
                elif val == "":
                    if dado is None:
                        dado = 0
                    campo = TextInput(
                        multiline=False,
                        halign="center",
                        font_size=32,
                        font_name="ComicNeue",
                        size_hint=(1, 1),
                        background_color=(1, 1, 1, 0),
                        foreground_color=(1, 1, 1, 1),
                        cursor_color=(1, 1, 1, 1),
                        padding=(10, 10)
                    )
                    self.inputs.append(campo)
                    self.gabarito.append(str(dado))

                    conteudo = MDCard(
                        md_bg_color=(0, 0, 0, 0),
                        style="outlined",
                        line_color=(0, 0, 0, 1),
                        padding=dp(4),
                        size_hint=(1, 1),
                        elevation=0,
                    )
                    conteudo.add_widget(campo)

                elif val in ["+", "-", "×", "÷", "="]:
                    lbl = MDLabel(
                        text=val,
                        halign="center",
                        valign="middle",
                        font_style="H6",
                        font_size="32sp",
                        font_name="ComicNeue",
                        theme_text_color="Custom",
                        text_color=(1, 1, 1, 1),
                    )
                    lbl.bind(size=lbl.setter("text_size"))
                    conteudo = MDCard(
                        md_bg_color=(0, 0, 0, 0),
                        style="outlined",
                        line_color=(0, 0, 0, 1),
                        padding=dp(4),
                        size_hint=(1, 1),
                        elevation=0,
                    )
                    conteudo.add_widget(lbl)

                elif val == "VAL":
                    if dado is None:
                        dado = 0
                    lbl = MDLabel(
                        text=str(dado),
                        halign="center",
                        valign="middle",
                        font_style="H6",
                        font_size="32sp",
                        font_name="ComicNeue",
                        theme_text_color="Custom",
                        text_color=(1, 1, 1, 1),
                    )
                    lbl.bind(size=lbl.setter("text_size"))
                    conteudo = MDCard(
                        md_bg_color=(0, 0, 0, 0),
                        style="outlined",
                        line_color=(0, 0, 0, 1),
                        padding=dp(4),
                        size_hint=(1, 1),
                        elevation=0,
                    )
                    conteudo.add_widget(lbl)

                self.grid.add_widget(conteudo)

        print("Gabarito esperado:", self.gabarito)

    def verificar_respostas(self, texto):
        pontuacao = 0
        for campo, resposta_correta in zip(self.inputs, self.gabarito):
            resposta = campo.text.strip().replace(",", ".")
            try:
                if int(float(resposta)) == int(float(resposta_correta)):
                    pontuacao += 10
                    campo.background_color = (0.6, 1, 0.6, 0.8)
                else:
                    campo.background_color = (1, 0.6, 0.6, 0.8)
            except:
                campo.background_color = (1, 0.6, 0.6, 0.8)
        self.pontuacao_label.text = f"Pontuação: {pontuacao}"

    def limpar_respostas(self, texto):
        for campo in self.inputs:
            campo.text = ""
            campo.background_color = (1, 1, 1, 0.9)

    def nova_cruzadinha(self, texto):
        self.limpar_respostas(texto)
        self.gerar_cruzadinha()

    def voltar(self, instance):
        self.manager.current = "inicial"


# Exemplo de execução
class TesteApp(MDApp):
    def build(self):
        return TelaCruzadinha7x7()


if __name__ == "__main__":
    TesteApp().run()
