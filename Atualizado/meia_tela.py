from kivy.uix.screenmanager import Screen, SlideTransition, ScreenManager
from kivy.core.text import LabelBase
import os
from kivy.uix.label import Label
from kivy.clock import Clock
from random import randint, choice
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.carousel import Carousel
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivymd.uix.slider import MDSlider

font_path = os.path.join(os.path.dirname(__file__), "Fontes", "Duo-Dunkel.ttf")
print("[DEBUG] Fonte:", font_path, "exists:", os.path.exists(font_path))
LabelBase.register(name="BungeeShade", fn_regular=font_path)


class MeiaTela(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Fundo
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
        )
        layout.add_widget(fundo)

        self.adicionar_decoracao_fundo(layout)

        self.title_image = Image(
            source="Bonecos/titulo_operacoes.webp",
            size_hint=(None, None),
            height=dp(80),
            width=dp(300),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={"center_x": 0.5, "top": 0.96},
        )

        layout.add_widget(self.title_image)

        # Botão Voltar (Escuro)
        layout.add_widget(
            MDIconButton(
                icon="arrow-left",
                theme_text_color="Custom",
                text_color=(0, 0, 0, 1), # Preto
                pos_hint={"x": 0.02, "top": 0.98},
                on_release=lambda x: self.voltar("conteudos")
            )
        )

        boneco = Image(
            source="Bonecos/boneco_operacao.webp",
            size_hint=(0.45, 0.50),
            pos_hint={"center_x": 0.5, "center_y": 0.70}
        )
        layout.add_widget(boneco)

        card_principal = MDCard(
            size_hint=(0.9, 0.40),
            pos_hint={"center_x": 0.5, "y": 0.12},
            md_bg_color=(1, 1, 1, 0.3),
            radius=[25],
            elevation=0,
            line_color=(0, 0, 0, 0.1),
            line_width=1
        )

        container = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15)
        )

        # Subtítulo (Texto Preto)
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

        # Botões do card
        container.add_widget(self.create_icon_button(
            "Representações", "image-outline", lambda: self.ir_para("representacoes")
        ))

        container.add_widget(self.create_icon_button(
            "Definições", "book-open-variant", lambda: self.ir_para("definicoes")
        ))

        # 4. Botão Jogar
        container.add_widget(self.create_icon_button(
            "Jogar", "gamepad-variant", lambda: self.ir_para("jogar")
        ))

        card_principal.add_widget(container)
        layout.add_widget(card_principal)

        self.add_widget(layout)

    def adicionar_decoracao_fundo(self, layout):
        """Ícones decorativos em tom escuro para combinar com o texto preto"""
        icones = ["plus", "minus", "division", "percent", "calculator", "function"]
        positions = [
            {"x": 0.05, "y": 0.85}, {"x": 0.85, "y": 0.9},
            {"x": 0.1, "y": 0.6}, {"x": 0.85, "y": 0.6},
            {"x": 0.05, "y": 0.2}, {"x": 0.9, "y": 0.25}
        ]

        for pos in positions:
            icon = MDIconButton(
                icon=choice(icones),
                theme_text_color="Custom",
                text_color=(0, 0, 0, 0.08), # Preto muito sutil (marca d'água)
                pos_hint=pos,
                icon_size=dp(45),
                disabled=True
            )
            layout.add_widget(icon)

    def create_icon_button(self, text, icon, callback):
        # Botão continua Azul com texto Branco (conforme pedido)
        card = MDCard(
            size_hint=(1, None),
            height=dp(50),
            md_bg_color=(0.15, 0.25, 0.75, 0.9), # Azul forte
            radius=[15],
            elevation=3,
            ripple_behavior=True,
            padding=[dp(15), 0, dp(10), 0]
        )

        row = BoxLayout(orientation="horizontal", spacing=dp(15))

        row.add_widget(MDIconButton(
            icon=icon,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1), # Ícone Branco
            size_hint=(None, None),
            size=(dp(24), dp(24)),
            pos_hint={'center_y': 0.5},
            disabled=True
        ))

        row.add_widget(MDLabel(
            text=text,
            halign="left",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1), # Texto do botão Branco
            bold=True
        ))

        # Seta indicativa
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
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i+1), 0.05)

    def tocar_som_giz(self):
        pass

    def voltar(self, screen_name):
        self.manager.current = "conteudos"

    def ir_para(self, screen_name):
        self.manager.current = screen_name

# =================== TELA DEFINIÇÕES ===================

class DefinicoesCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            radius=[25],
            elevation=15,
            padding=dp(20),
            size_hint=(0.9, 0.65),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=(1, 1, 1, 1),
            **kwargs
        )

class BaseDefinicoesTela(Screen):
    def __init__(self, titulo_secao="Definições", **kwargs):
        super().__init__(**kwargs)
        self.titulo_secao = titulo_secao

        # Fundo
        bg = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(bg)

        # Layout Principal
        self.layout = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        self.add_widget(self.layout)

        # Cabeçalho
        header = MDBoxLayout(size_hint_y=None, height=dp(50))
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            on_release=self.voltar
        )
        lbl_titulo = MDLabel(
            text=self.titulo_secao,
            halign="center",
            font_style="H5",
            bold=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )
        dummy = MDIconButton(icon="arrow-left", opacity=0, disabled=True)

        header.add_widget(back_btn)
        header.add_widget(lbl_titulo)
        header.add_widget(dummy)
        self.layout.add_widget(header)

        # Card e Carrossel
        self.card = DefinicoesCard()
        self.layout.add_widget(self.card)

        self.carrossel = Carousel(direction="right", loop=False)
        self.card.add_widget(self.carrossel)

        # Navegação
        nav = MDBoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(60), padding=[dp(20), 0])
        nav.add_widget(MDFillRoundFlatButton(text="Anterior", md_bg_color=(0.6, 0.6, 0.6, 1), on_release=lambda x: self.carrossel.load_previous()))
        nav.add_widget(MDBoxLayout()) # Espaçador
        nav.add_widget(MDFillRoundFlatButton(text="Próximo", md_bg_color=(0.2, 0.6, 1, 1), on_release=lambda x: self.carrossel.load_next()))
        self.layout.add_widget(nav)

        self.setup_slides()

    def setup_slides(self):
        pass

    def voltar(self, instance):
        self.manager.current = "tela"

    def criar_slide_conteudo(self, titulo, texto_definicao, icone="book-open-variant"):
        slide = MDBoxLayout(orientation="vertical", spacing=dp(10), padding=dp(5))

        # Ícone Grande
        slide.add_widget(MDIconButton(
            icon=icone,
            pos_hint={"center_x": 0.5},
            icon_size=dp(70),
            theme_text_color="Custom",
            text_color=(0.2, 0.2, 0.6, 1)
        ))

        # Título
        slide.add_widget(MDLabel(
            text=titulo,
            halign="center",
            font_style="H5",
            bold=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(40)
        ))

        # Texto com rolagem
        scroll = ScrollView()
        lbl_texto = MDLabel(
            text=texto_definicao,
            halign="center",
            valign="top",
            font_style="Body1",
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            markup=True # Permite usar negrito [b] no texto
        )
        lbl_texto.bind(texture_size=lbl_texto.setter('size'))
        scroll.add_widget(lbl_texto)
        slide.add_widget(scroll)

        return slide

# =================== TELA DEFINIÇÕES OPERAÇÕES ===================
class OperacoesDefinicoesTela(BaseDefinicoesTela):
    def __init__(self, **kwargs):
        # Define o título do topo
        super().__init__(titulo_secao="Operações Básicas", **kwargs)

    def voltar(self, instance):
        # Ajuste "meia_tela" para o nome correto da sua tela de menu de operações
        self.manager.transition.direction = "right"
        self.manager.current = "tela"

    def setup_slides(self):
        # ---------------------------------------------------------
        # SLIDE 1: ADIÇÃO
        # ---------------------------------------------------------
        texto_adicao = (
            "A adição é o ato de juntar quantidades.\n\n"
            "[b]TERMOS DA ADIÇÃO:[/b]\n\n"
            "   12    (Parcela)\n"
            "+ 15    (Parcela)\n"
            "------\n"
            "   27    (Soma ou Total)\n\n"
            "[b]Dica:[/b] A ordem das parcelas não altera a soma. "
            "Isso se chama propriedade comutativa!"
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Adição (+)",
            texto_definicao=texto_adicao,
            icone="plus-circle-outline"
        ))

        # ---------------------------------------------------------
        # SLIDE 2: SUBTRAÇÃO
        # ---------------------------------------------------------
        texto_subtracao = (
            "A subtração é usada para tirar uma quantidade de outra ou comparar valores.\n\n"
            "[b]TERMOS DA SUBTRAÇÃO:[/b]\n\n"
            "   50    (Minuendo)\n"
            "-  20    (Subtraendo)\n"
            "------\n"
            "   30    (Resto ou Diferença)\n\n"
            "[b]Atenção:[/b] Na subtração de números naturais, o Minuendo "
            "deve ser sempre maior ou igual ao Subtraendo."
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Subtração (-)",
            texto_definicao=texto_subtracao,
            icone="minus-circle-outline"
        ))

        # ---------------------------------------------------------
        # SLIDE 3: MULTIPLICAÇÃO
        # ---------------------------------------------------------
        texto_multiplicacao = (
            "A multiplicação é uma forma rápida de somar parcelas iguais.\n\n"
            "[b]TERMOS DA MULTIPLICAÇÃO:[/b]\n\n"
            "    5     (Fator)\n"
            " x  3     (Fator)\n"
            "------\n"
            "   15     (Produto)\n\n"
            "[b]Curiosidade:[/b] O número 1 é o elemento neutro. "
            "Qualquer número multiplicado por 1 continua sendo ele mesmo!"
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Multiplicação (x)",
            texto_definicao=texto_multiplicacao,
            icone="close-circle-outline" # Ícone de X
        ))

        # ---------------------------------------------------------
        # SLIDE 4: DIVISÃO
        # ---------------------------------------------------------
        texto_divisao = (
            "A divisão é o ato de repartir uma quantidade em partes iguais.\n\n"
            "[b]TERMOS DA DIVISÃO:[/b]\n\n"
            "Dividendo  |_ Divisor __\n"
            "Resto           Quociente\n\n"
            "Exemplo: 20 ÷ 4 = 5\n"
            "• 20 é o Dividendo\n"
            "• 4 é o Divisor\n"
            "• 5 é o Quociente\n\n"
            "[b]Regra de Ouro:[/b] Nunca se pode dividir um número por Zero!"
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Divisão (÷)",
            texto_definicao=texto_divisao,
            icone="division"
        ))


class TelaRepresentacoes(Screen):
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
            on_release=self.voltar
        ))

        self.title_label = Label(
            text="SIMULADOR",
            color=(0, 0, 0, 1),
            font_name="BungeeShade",
            font_size="28sp",
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "top": 0.96},
        )
        layout.add_widget(self.title_label)

        # 3. CARD DO RESULTADO
        card_resultado = MDCard(
            size_hint=(0.85, 0.25),
            pos_hint={"center_x": 0.5, "top": 0.82},
            md_bg_color=(1, 1, 1, 0.9),
            radius=[20],
            elevation=4,
            orientation="vertical",
            padding=dp(10)
        )

        self.conta_label = MDLabel(
            text="5 + 5 = 10",
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="H4",
            bold=True
        )
        card_resultado.add_widget(self.conta_label)

        self.info_label = MDLabel(
            text="Parcela + Parcela = Soma",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            font_style="Subtitle1"
        )
        card_resultado.add_widget(self.info_label)

        layout.add_widget(card_resultado)

        # 4. ÁREA DOS SLIDERS (Valores)
        sliders_box = BoxLayout(
            orientation="vertical",
            size_hint=(0.8, 0.35),
            pos_hint={"center_x": 0.5, "y": 0.22},
            spacing=dp(10)
        )

        # Slider 1
        self.label_s1 = MDLabel(
            text="Valor 1: 5",
            halign="center",
            bold=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )
        sliders_box.add_widget(self.label_s1)

        self.slider1 = MDSlider(min=1, max=20, value=5, step=1, color=(0.2, 0.4, 0.8, 1))
        self.slider1.bind(value=self.atualizar_calculo)
        sliders_box.add_widget(self.slider1)

        # Slider 2
        self.label_s2 = MDLabel(
            text="Valor 2: 5",
            halign="center",
            bold=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )
        sliders_box.add_widget(self.label_s2)

        self.slider2 = MDSlider(min=1, max=20, value=5, step=1, color=(0.2, 0.4, 0.8, 1))
        self.slider2.bind(value=self.atualizar_calculo)
        sliders_box.add_widget(self.slider2)

        layout.add_widget(sliders_box)

        # 5. BOTÕES DE OPERAÇÃO (Centralizados)
        ops_box = BoxLayout(
            orientation="horizontal",
            size_hint=(0.9, 0.12),
            pos_hint={"center_x": 0.5, "y": 0.05}, # Centralizado no eixo X
            spacing=dp(15),
            padding=dp(5)
        )

        self.botoes_op = {}

        operacoes = [
            ("+", "plus", "soma"),
            ("-", "minus", "subtracao"),
            ("×", "close", "multiplicacao"),
            ("÷", "division", "divisao")
        ]

        for simbolo, icone, id_op in operacoes:
            btn = MDIconButton(
                icon=icone,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                md_bg_color=(0.2, 0.4, 0.9, 1),
                icon_size="32sp",
                size_hint=(None, None),
                size=(dp(56), dp(56)),
                pos_hint={"center_y": 0.5}
            )
            btn.bind(on_release=lambda x, op=id_op: self.mudar_operacao(op))
            ops_box.add_widget(btn)
            self.botoes_op[id_op] = btn

        layout.add_widget(ops_box)
        self.add_widget(layout)

        # Estado inicial
        self.op_atual = "soma"
        self.atualizar_visual_botoes()
        self.atualizar_calculo()

    def adicionar_decoracao_fundo(self, layout):
        icones = ["calculator", "plus", "minus", "percent"]
        positions = [
            {"x": 0.05, "y": 0.85}, {"x": 0.85, "y": 0.9},
            {"x": 0.1, "y": 0.15}, {"x": 0.9, "y": 0.2}
        ]
        for pos in positions:
            layout.add_widget(MDIconButton(
                icon=choice(icones), theme_text_color="Custom",
                text_color=(0, 0, 0, 0.05), pos_hint=pos,
                icon_size=dp(50), disabled=True
            ))

    def mudar_operacao(self, nova_op):
        self.op_atual = nova_op
        self.atualizar_visual_botoes()
        self.atualizar_calculo()

    def atualizar_visual_botoes(self):
        cor_ativa = (1, 0.5, 0, 1) # Laranja para o selecionado
        cor_inativa = (0.2, 0.4, 0.9, 1) # Azul para os outros

        for op, btn in self.botoes_op.items():
            if op == self.op_atual:
                btn.md_bg_color = cor_ativa
            else:
                btn.md_bg_color = cor_inativa

    def atualizar_calculo(self, *args):
        val1 = int(self.slider1.value)
        val2 = int(self.slider2.value)

        if self.op_atual == "soma":
            self.label_s1.text = f"Parcela 1: {val1}"
            self.label_s2.text = f"Parcela 2: {val2}"
            res = val1 + val2
            self.conta_label.text = f"{val1} + {val2} = {res}"
            self.info_label.text = "Soma (Total)"

        elif self.op_atual == "subtracao":
            # MODIFICAÇÃO: Permite negativos (Valor1 - Valor2 direto)
            self.label_s1.text = f"Minuendo: {val1}"
            self.label_s2.text = f"Subtraendo: {val2}"
            res = val1 - val2
            self.conta_label.text = f"{val1} - {val2} = {res}"

            if res < 0:
                self.info_label.text = "Resultado Negativo"
            else:
                self.info_label.text = "Diferença"

        elif self.op_atual == "multiplicacao":
            self.label_s1.text = f"Fator 1: {val1}"
            self.label_s2.text = f"Fator 2: {val2}"
            res = val1 * val2
            self.conta_label.text = f"{val1} × {val2} = {res}"
            self.info_label.text = "Produto"

        elif self.op_atual == "divisao":
            # MODIFICAÇÃO: Divisão com vírgula (float)
            divisor = val2 if val2 > 0 else 1
            dividendo = val1

            self.label_s1.text = f"Dividendo: {dividendo}"
            self.label_s2.text = f"Divisor: {divisor}"

            # Divisão real (float)
            res = dividendo / divisor

            # Formatação: Inteiro se não tiver decimal, senão 2 casas
            if res.is_integer():
                res_formatado = f"{int(res)}"
            else:
                res_formatado = f"{res:.2f}".replace('.', ',')

            self.conta_label.text = f"{dividendo} ÷ {divisor} = {res_formatado}"
            self.info_label.text = "Quociente (Decimal)"

    def voltar(self, *args):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "tela" # Confirme se este é o nome da tela anterior