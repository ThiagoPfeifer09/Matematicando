from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton, MDRaisedButton
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import numpy as np
import matplotlib.pyplot as plt
import random

# =================== TELA PRINCIPAL estatistica ===================
class EstatisticaTela(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Fundo
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        layout.add_widget(fundo)

        # Título
        self.title_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(self.title_label)
        self.digita_texto(self.title_label, "ESTATISTICA")

        # Botão voltar
        self.back_button = MDIconButton(
            icon='arrow-left',
            pos_hint={'x': 0, 'top': 1},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # cor branca
            on_release=lambda x: self.voltar("conteudos")
        )
        layout.add_widget(self.back_button)

        # Boneco
        boneco = Image(
            source="Boneco_Estatistica.png",
            size_hint=(0.47, 0.47),
            pos_hint={"center_x": 0.5, "center_y": 0.65}
        )
        layout.add_widget(boneco)

        # Botões principais
        btn_representacoes = self.create_card_button(
            "Representações",
            0.3, 0.35,
            lambda: self.ir_para("estatistica_representacoes")
        )
        btn_definicoes = self.create_card_button(
            "Definições",
            0.3, 0.2,
            lambda: self.ir_para("estatistica_definicoes")
        )

        layout.add_widget(btn_representacoes)
        layout.add_widget(btn_definicoes)
        self.add_widget(layout)

    # Funções auxiliares
    def digita_texto(self, label, texto, i=0):
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i + 1), 0.05)


    def create_card_button(self, text, x, y, callback):
        card = MDCard(
            size_hint=(0.4, 0.08),
            pos_hint={"x": x, "y": y},
            md_bg_color=(0.2, 0.2, 0.6, 0.85),
            radius=[20],
            elevation=10,
            ripple_behavior=True
        )
        label = MDLabel(
            text=text,
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size="18sp"
        )
        card.add_widget(label)
        card.bind(on_release=lambda *a: callback())
        return card


    def ir_para(self, tela_nome):
        self.manager.transition = SlideTransition(direction="left", duration=0.4)
        self.manager.current = tela_nome

    def voltar(self, tela_nome):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = tela_nome


# =================== TELA DEFINIÇÕES ===================
class DefinicoesEstatistica(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Fundo
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        layout.add_widget(fundo)

        # Título
        self.title_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(self.title_label)
        self.digita_texto(self.title_label, "DEFINIÇÕES ESTATISTICA")

        # Lista de imagens (uma para cada operação)
        imagens = [
            "quadrado.jpeg",
            "triangulo.jpeg",
            "circulo.jpeg",
            "retangulo.jpeg"
        ]

        pos_y = [0.68, 0.68, 0.30, 0.30]
        pos_x = [0.26, 0.74, 0.26, 0.74]

        for i, img in enumerate(imagens):
            card = MDCard(
                size_hint=(0.45, 0.32),
                pos_hint={"center_x": pos_x[i], "center_y": pos_y[i]},
                radius=[20],
                elevation=10,
                orientation="vertical"
            )

            # Imagem dentro do card
            card.add_widget(Image(
                source=img,
                allow_stretch=True,
                keep_ratio=False
            ))

            layout.add_widget(card)

        # Botão voltar
        btn_voltar = MDCard(
            size_hint=(0.18, 0.06),
            pos_hint={"x": 0.05, "y": 0.05},
            md_bg_color=(0.2, 0.2, 0.6, 0.85),
            radius=[20],
            elevation=10,
            ripple_behavior=True
        )
        btn_voltar.add_widget(MDLabel(
            text="Voltar",
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        ))
        btn_voltar.on_release = lambda *a: self.voltar()
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def digita_texto(self, label, texto, i=0):
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i+1), 0.05)

    def voltar(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "estatistica_tela"





class EstatisticaRepresentacoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()

        # ================== FUNDO ==================
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        root.add_widget(fundo)

        # ================== LAYOUT PRINCIPAL ==================
        main_box = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=[20, 80, 20, 20],
            size_hint=(1, 0.9),
            pos_hint={"center_x": 0.5, "center_y": 0.45}
        )

        # ================== CARD EXPLICATIVO ==================
        self.card_explicacao = MDCard(
            orientation="vertical",
            size_hint=(1, 0.35),
            elevation=10,
            radius=[25],
            md_bg_color=(1, 1, 1, 0.9),
            padding=20,
            spacing=10
        )
        self.label_titulo = MDLabel(
            text="Selecione um conceito estatístico:",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="H6"
        )
        self.label_explicacao = MDLabel(
            text="Aqui aparecerá a explicação do conceito escolhido.",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="Subtitle1"
        )
        self.card_explicacao.add_widget(self.label_titulo)
        self.card_explicacao.add_widget(self.label_explicacao)

        # ================== CARD INTERATIVO ==================
        self.card_interativo = MDCard(
            orientation="vertical",
            size_hint=(1, 0.6),
            radius=[25],
            elevation=10,
            md_bg_color=(1, 1, 1, 0.9),
            padding=20,
            spacing=10
        )

        self.label_input = MDLabel(
            text="Digite uma lista de números separados por vírgula:",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )

        self.input_valores = MDTextField(
            hint_text="Ex: 2, 4, 5, 8, 10",
            mode="rectangle",
            helper_text="Use vírgulas para separar os valores",
            helper_text_mode="on_focus"
        )
        self.input_valores.bind(text=self.calcular_estatistica)

        # === BOTÃO DE GERAR LISTA ALEATÓRIA ===
        self.btn_gerar_lista = MDRaisedButton(
            text="🎲 Gerar Lista Aleatória",
            md_bg_color=(0.2, 0.6, 0.8, 1),
            text_color=(1, 1, 1, 1),
            on_release=self.gerar_lista_aleatoria
        )

        self.label_resultado = MDLabel(
            text="Resultados aparecerão aqui.",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="Subtitle1"
        )

        self.graph_area = BoxLayout(size_hint=(1, 0.7))
        self.card_interativo.add_widget(self.label_input)
        self.card_interativo.add_widget(self.input_valores)
        self.card_interativo.add_widget(self.btn_gerar_lista)  # <-- adicionado aqui
        self.card_interativo.add_widget(self.label_resultado)
        self.card_interativo.add_widget(self.graph_area)

        # ================== BOTÕES DE CONCEITOS ==================
        botoes = BoxLayout(spacing=10, size_hint=(1, 0.15))
        conceitos = [
            ("Média", "calculator", "A média é a soma dos valores dividida pela quantidade."),
            ("Mediana", "chart-line", "A mediana é o valor central em uma lista ordenada."),
            ("Moda", "chart-bar", "A moda é o valor que mais se repete."),
            ("Amplitude", "arrow-expand", "A amplitude é a diferença entre o maior e o menor valor.")
        ]

        for nome, icone, explicacao in conceitos:
            btn = MDFillRoundFlatIconButton(
                text=nome,
                icon=icone,
                md_bg_color=(0.2, 0.6, 0.8, 1),
                text_color=(1, 1, 1, 1),
                on_release=lambda x, n=nome, e=explicacao: self.selecionar_conceito(n, e)
            )
            botoes.add_widget(btn)

        # ================== MONTAGEM FINAL ==================
        main_box.add_widget(self.card_explicacao)
        main_box.add_widget(self.card_interativo)
        main_box.add_widget(botoes)
        root.add_widget(main_box)

        # ================== TÍTULO E VOLTAR ==================
        titulo = MDLabel(
            text="Estatística - Representações",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H5",
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.98}
        )
        back_button = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={'x': 0, 'top': 0.98},
            on_release=lambda x: self.voltar("estatistica_tela")
        )

        root.add_widget(titulo)
        root.add_widget(back_button)
        self.add_widget(root)

        self.conceito_atual = None

    # ================== FUNÇÕES ==================
    def gerar_lista_aleatoria(self, instance):
        """Gera 10 valores aleatórios entre 1 e 100 e calcula automaticamente."""
        lista = [random.randint(1, 10) for _ in range(10)]
        self.input_valores.text = ", ".join(map(str, lista))
        # cálculo é feito automaticamente pelo bind do campo

    def selecionar_conceito(self, nome, explicacao):
        self.conceito_atual = nome
        self.label_titulo.text = f"Conceito: {nome}"
        self.label_explicacao.text = explicacao

        texto = self.input_valores.text.strip()
        if texto:  # já tem valores? recalcula automaticamente
            self.calcular_estatistica(self.input_valores, texto)
        else:
            self.label_resultado.text = "Digite valores ou gere uma lista para calcular."
            self.graph_area.clear_widgets()

    def calcular_estatistica(self, instance, texto):
        if not self.conceito_atual:
            self.label_resultado.text = "Selecione um conceito primeiro."
            return

        try:
            valores = [float(x.strip()) for x in texto.split(",") if x.strip()]
            if not valores:
                raise ValueError

            resultado = ""
            linha_valor = None  # <-- valor que será desenhado no gráfico

            if self.conceito_atual == "Média":
                media = np.mean(valores)
                resultado = f"Média = {media:.2f}"
                linha_valor = media

            elif self.conceito_atual == "Mediana":
                mediana = np.median(valores)
                resultado = f"Mediana = {mediana:.2f}"
                linha_valor = mediana

            elif self.conceito_atual == "Moda":
                valores_unicos, contagens = np.unique(valores, return_counts=True)
                moda = valores_unicos[np.argmax(contagens)]
                resultado = f"Moda = {moda:.2f}"
                linha_valor = moda

            elif self.conceito_atual == "Amplitude":
                amplitude = np.max(valores) - np.min(valores)
                resultado = f"Amplitude = {amplitude:.2f}"
                # aqui, a linha pode mostrar o valor máximo ou mínimo; vamos usar o máximo
                linha_valor = np.max(valores)

            self.label_resultado.text = f"Resultados: {resultado}"
            self.plotar_grafico(valores, linha_valor)  # <-- envia o valor da linha

        except ValueError:
            self.label_resultado.text = "Digite números válidos separados por vírgulas."


    def plotar_grafico(self, valores, linha_valor=None):
        self.graph_area.clear_widgets()

        fig, ax = plt.subplots()
        ax.bar(range(len(valores)), valores, color="#66b3ff")
        ax.set_title("Distribuição dos valores")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")

        # Calcula limite superior do eixo Y
        y_max = max(valores)
        if linha_valor is not None:
            y_max = max(y_max, linha_valor)
        ax.set_ylim(0, y_max * 1.30)

        # Desenha a linha horizontal, se houver valor
        if linha_valor is not None:
            ax.axhline(y=linha_valor, color='red', linestyle='--', linewidth=2)
            ax.text(
                0, linha_valor,
                f"{self.conceito_atual}: {linha_valor:.2f}",
                color='red', fontsize=10, va='bottom', ha='left'
            )

        self.graph_area.add_widget(FigureCanvasKivyAgg(fig))



    def voltar(self, tela_anterior):
        self.manager.current = tela_anterior