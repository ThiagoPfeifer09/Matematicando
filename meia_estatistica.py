from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton, MDRaisedButton
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import numpy as np
import matplotlib.pyplot as plt
import random
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from random import choice
from kivy.uix.carousel import Carousel
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView

from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard

# =================== TELA PRINCIPAL ESTATÍSTICA ===================
class EstatisticaTela(Screen):
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

        # 2. Decoração de Fundo (Temática Estatística)
        self.adicionar_decoracao_fundo(layout)

        self.title_image = Image(
            source="Bonecos/titulo_estatistica.png",
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
            source="Bonecos/Boneco_Estatistica.png",
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
            "Representações", "chart-bar", lambda: self.ir_para("estatistica_representacoes")
        ))

        container.add_widget(self.create_icon_button(
            "Definições", "book-open-variant", lambda: self.ir_para("estatistica_definicoes")
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
        """Ícones de estatística escuros"""
        # Ícones: Gráfico de barras, Pizza, Linha, Porcentagem, Enquete
        icones = [
            "chart-bar", "chart-pie", "chart-line",
            "percent", "poll", "trending-up", "table-large"
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


# =================== TELA DEFINIÇÕES ESTATÍSTICA ===================

from meia_tela import BaseDefinicoesTela
class EstatisticaDefinicoesTela(BaseDefinicoesTela):
    def __init__(self, **kwargs):
        # Define o título do topo
        super().__init__(titulo_secao="Estatística Básica", **kwargs)

    def voltar(self, instance):
        # Define a tela de retorno
        self.manager.transition.direction = "right"
        self.manager.current = "estatistica_tela"

    def setup_slides(self):
        # ---------------------------------------------------------
        # SLIDE 1: MÉDIA
        # ---------------------------------------------------------
        texto_media = (
            "A Média é o valor que representa o equilíbrio dos dados. "
            "Calculamos somando todos os valores e dividindo pela quantidade deles.\n\n"
            "[b]EXEMPLO PRÁTICO:[/b]\n"
            "Notas: 6, 7 e 8\n\n"
            "1. Soma: 6 + 7 + 8 = 21\n"
            "2. Quantidade: 3 números\n"
            "3. Média: 21 ÷ 3 = [b]7[/b]"
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Média Aritmética",
            texto_definicao=texto_media,
            icone="chart-bar"
        ))

        # ---------------------------------------------------------
        # SLIDE 2: MEDIANA
        # ---------------------------------------------------------
        texto_mediana = (
            "A Mediana é o valor que está exatamente no [b]MEIO[/b] "
            "de uma lista de dados ordenados.\n\n"
            "[b]EXEMPLO (Ímpar):[/b]\n"
            "Lista: { 2, 5, [b]8[/b], 10, 12 }\n"
            "O 8 está exatamente no meio.\n\n"
            "[b]DICA:[/b] Se a quantidade de números for par, somamos os "
            "dois do meio e dividimos por 2!"
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Mediana",
            texto_definicao=texto_mediana,
            icone="format-align-middle"
        ))

        # ---------------------------------------------------------
        # SLIDE 3: MODA
        # ---------------------------------------------------------
        texto_moda = (
            "A Moda é simplesmente o valor que aparece com [b]MAIOR FREQUÊNCIA[/b] "
            "em um conjunto de dados. É o número que está 'na moda'.\n\n"
            "[b]EXEMPLO:[/b]\n"
            "Lista: { 4, 2, [b]5[/b], 8, [b]5[/b], 9 }\n\n"
            "O número 5 aparece duas vezes.\n"
            "Logo, a Moda é [b]5[/b]."
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Moda",
            texto_definicao=texto_moda,
            icone="star-circle-outline"
        ))

        # ---------------------------------------------------------
        # SLIDE 4: AMPLITUDE
        # ---------------------------------------------------------
        texto_amplitude = (
            "A Amplitude mede o quanto os dados variam. "
            "É a diferença entre o [b]MAIOR[/b] e o [b]MENOR[/b] valor.\n\n"
            "[b]EXEMPLO:[/b]\n"
            "Idades: 10, 15, 30, 50\n\n"
            "Maior valor: 50\n"
            "Menor valor: 10\n\n"
            "Amplitude: 50 - 10 = [b]40[/b]"
        )

        self.carrossel.add_widget(self.criar_slide_conteudo(
            titulo="Amplitude",
            texto_definicao=texto_amplitude,
            icone="arrow-expand-horizontal"
        ))


from random import randint
import numpy as np


class EstatisticaRepresentacoes(Screen):
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

        # 2. Cabeçalho (Fixo no Topo)
        header = FloatLayout(size_hint=(1, None), height=dp(80), pos_hint={"top": 1})

        btn_back = MDIconButton(
            icon="arrow-left",
            pos_hint={"x": 0.02, "center_y": 0.5},
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            on_release=lambda x: self.voltar("estatistica_tela")
        )

        lbl_title = Label(
            text="ESTATÍSTICA",
            color=(0, 0, 0, 1),
            font_name="BungeeShade",
            font_size="28sp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        header.add_widget(btn_back)
        header.add_widget(lbl_title)
        layout.add_widget(header)

        # 3. CONTAINER PRINCIPAL
        main_box = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(600),
            pos_hint={"top": 0.88},
            spacing=dp(10),
            padding=[dp(10), 0, dp(10), 0]
        )
        main_box.bind(minimum_height=main_box.setter('height'))
        main_box.size_hint_y = 0.88

        # --- A. CARD DE EXPLICAÇÃO (Topo) ---
        self.info_card = MDCard(
            size_hint=(1, 0.25),
            md_bg_color=(1, 1, 1, 0.95),
            radius=[15],
            elevation=3,
            orientation="vertical",
            padding=dp(15),
            spacing=dp(5)
        )

        self.lbl_conceito = MDLabel(
            text="SELECIONE UM CONCEITO",
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex("#1565C0"),
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )

        self.scroll_text = ScrollView(size_hint=(1, 1))
        self.lbl_texto_dinamico = MDLabel(
            text="Escolha uma opção abaixo para ver a definição e o cálculo passo a passo.",
            halign="left",
            valign="top",
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            font_style="Body2",
            markup=True,
            size_hint_y=None
        )
        self.lbl_texto_dinamico.bind(texture_size=self.lbl_texto_dinamico.setter('size'))
        self.scroll_text.add_widget(self.lbl_texto_dinamico)

        self.info_card.add_widget(self.lbl_conceito)
        self.info_card.add_widget(self.scroll_text)
        main_box.add_widget(self.info_card)

        # --- B. ÁREA DO GRÁFICO (Meio) ---
        self.graph_box = BoxLayout(size_hint=(1, 0.45))

        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_alpha(0)
        self.ax.set_facecolor("#ffffffcc")
        self.graph_widget = FigureCanvasKivyAgg(self.fig)
        self.graph_box.add_widget(self.graph_widget)

        main_box.add_widget(self.graph_box)

        # --- C. PAINEL DE CONTROLE (Base) ---
        control_panel = MDCard(
            size_hint=(1, 0.30),
            md_bg_color=(0.95, 0.95, 0.95, 1),
            radius=[20, 20, 0, 0],
            elevation=10,
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        # Linha 1: Input + Botão Dados (RESTAURADO O BOTÃO DE DADO)
        input_row = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(50))

        self.input_valores = MDTextField(
            hint_text="Ex: 5, 8, 2, 10",
            mode="fill",
            fill_color_normal=(1, 1, 1, 1),
            size_hint_x=0.8,
        )
        self.input_valores.bind(text=self.calcular_estatistica_bind)

        # --- O BOTÃO QUE VOCÊ GOSTAVA ---
        self.btn_random = MDIconButton(
            icon="dice-multiple",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),      # Ícone branco
            md_bg_color=(0.2, 0.4, 0.9, 1), # Fundo azul
            size_hint=(None, None),
            size=(dp(48), dp(48)),        # Tamanho fixo e quadrado/redondo
            pos_hint={"center_y": 0.5},
            on_release=self.gerar_lista_aleatoria
        )

        input_row.add_widget(self.input_valores)
        input_row.add_widget(self.btn_random)
        control_panel.add_widget(input_row)

        # Linha 2: Botões de Conceito
        scroll_btns = ScrollView(size_hint=(1, 1), do_scroll_y=False)
        box_btns = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_x=None, padding=[0, dp(5)])
        box_btns.bind(minimum_width=box_btns.setter('width'))

        opcoes = [
            ("Média", "#4CAF50"),
            ("Mediana", "#9C27B0"),
            ("Moda", "#FF9800"),
            ("Amplitude", "#F44336")
        ]

        for nome, cor in opcoes:
            btn = MDFillRoundFlatButton(
                text=nome,
                md_bg_color=get_color_from_hex(cor),
                text_color=(1, 1, 1, 1),
                font_style="Button",
                on_release=lambda x, n=nome: self.selecionar_conceito(n)
            )
            box_btns.add_widget(btn)

        scroll_btns.add_widget(box_btns)
        control_panel.add_widget(scroll_btns)

        main_box.add_widget(control_panel)
        layout.add_widget(main_box)

        self.add_widget(layout)

        # Dicionário de Definições
        self.definicoes = {
            "Média": "O ponto de equilíbrio. Imagine juntar tudo e dividir igualmente.",
            "Mediana": "O valor central. Se colocar todos em fila, quem está no meio?",
            "Moda": "O valor mais 'famoso'. É o número que mais se repete.",
            "Amplitude": "A distância entre o menor e o maior valor da lista."
        }

        # Estado Inicial
        self.conceito_atual = "Média"
        self.gerar_lista_aleatoria()

    def adicionar_decoracao_fundo(self, layout):
        icones = ["chart-bar", "chart-pie", "poll", "trending-up"]
        positions = [{"x": 0.05, "y": 0.85}, {"x": 0.85, "y": 0.9}, {"x": 0.1, "y": 0.5}, {"x": 0.85, "y": 0.5}]
        for pos in positions:
            layout.add_widget(MDIconButton(
                icon=np.random.choice(icones), theme_text_color="Custom",
                text_color=(0,0,0,0.05), pos_hint=pos,
                icon_size=dp(50), disabled=True
            ))

    def gerar_lista_aleatoria(self, *args):
        lista = [randint(1, 10) for _ in range(8)]
        self.input_valores.text = ", ".join(map(str, lista))
        self.calcular_estatistica()

    def selecionar_conceito(self, nome):
        self.conceito_atual = nome
        self.lbl_conceito.text = nome.upper()
        self.calcular_estatistica()

    def calcular_estatistica_bind(self, instance, text):
        self.calcular_estatistica()

    def calcular_estatistica(self):
        texto = self.input_valores.text
        if not texto: return

        try:
            valores = [float(x.strip()) for x in texto.split(",") if x.strip()]
            if not valores: return
        except ValueError:
            self.lbl_texto_dinamico.text = "Digite apenas números separados por vírgula."
            return

        resultado_val = 0
        texto_passo = ""
        cor_linha = 'red'
        definicao = self.definicoes.get(self.conceito_atual, "")

        if self.conceito_atual == "Média":
            resultado_val = np.mean(valores)
            texto_passo = (
                f"[b]Definição:[/b] {definicao}\n\n"
                f"[b]Cálculo:[/b]\n"
                f"1. Soma: {sum(valores):.0f}\n"
                f"2. Quantidade: {len(valores)}\n"
                f"3. Divisão: {sum(valores):.0f} ÷ {len(valores)} = [b]{resultado_val:.2f}[/b]"
            )
            cor_linha = '#4CAF50'

        elif self.conceito_atual == "Mediana":
            resultado_val = np.median(valores)
            sorted_vals = sorted(valores)
            texto_passo = (
                f"[b]Definição:[/b] {definicao}\n\n"
                f"[b]Cálculo:[/b]\n"
                f"1. Ordenar: {sorted_vals}\n"
                f"2. Centro: [b]{resultado_val:.2f}[/b]"
            )
            cor_linha = '#9C27B0'

        elif self.conceito_atual == "Moda":
            vals, counts = np.unique(valores, return_counts=True)
            max_count = np.max(counts)
            if max_count == 1:
                resultado_val = None
                texto_passo = f"[b]Definição:[/b] {definicao}\n\n[b]Cálculo:[/b]\nNenhum número se repete. [b]Amodal[/b]."
            else:
                modas = vals[counts == max_count]
                resultado_val = modas[0]
                lista_modas = ", ".join([str(m) for m in modas])
                texto_passo = (
                    f"[b]Definição:[/b] {definicao}\n\n"
                    f"[b]Cálculo:[/b]\n"
                    f"O número [b]{lista_modas}[/b] aparece {max_count} vezes."
                )
            cor_linha = '#FF9800'

        elif self.conceito_atual == "Amplitude":
            mini = np.min(valores)
            maxi = np.max(valores)
            resultado_val = maxi
            amplitude = maxi - mini
            texto_passo = (
                f"[b]Definição:[/b] {definicao}\n\n"
                f"[b]Cálculo:[/b]\n"
                f"Maior ({maxi}) - Menor ({mini}) = [b]{amplitude}[/b]"
            )
            cor_linha = '#F44336'

        self.lbl_texto_dinamico.text = texto_passo
        self.plotar_grafico(valores, resultado_val, cor_linha)

    def plotar_grafico(self, valores, linha_ref, cor):
        self.ax.clear()
        self.ax.set_facecolor("#ffffffcc")

        self.ax.set_title("Distribuição dos Valores", fontsize=12, fontweight='bold', pad=10)

        x_pos = range(len(valores))
        self.ax.bar(x_pos, valores, color='#2196F3', alpha=0.7, edgecolor='black')

        if linha_ref is not None:
            self.ax.axhline(y=linha_ref, color=cor, linestyle='--', linewidth=2.5, label=self.conceito_atual)
            self.ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)

        self.ax.set_xticks(list(x_pos))
        self.ax.set_xticklabels([f"{v:.0f}" for v in valores], rotation=45 if len(valores) > 8 else 0)
        self.ax.grid(axis='y', linestyle='--', alpha=0.5)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        self.graph_widget.draw()

    def voltar(self, tela_anterior):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = tela_anterior