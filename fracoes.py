from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFloatingActionButton
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
import matplotlib.patches as patches
import math
import matplotlib.pyplot as plt
from fractions import Fraction
from PIL import Image as PILImage, ImageDraw, ImageFont
import os
from kivymd.uix.dialog import MDDialog
from kivy.uix.video import Video
import random
from kivy.core.text import LabelBase
LabelBase.register(name="ComicNeue", fn_regular="ComicNeue-Regular.ttf")


# =============================================================================
# CLASSE DE DEPENDÊNCIA (Botão customizado)
class CardBotao(MDRaisedButton):
    def __init__(self, texto, on_press_func, **kwargs):
        super().__init__(
            text=texto,
            on_release=lambda x: on_press_func(texto),
            size_hint=(1, 1),
            font_size="20sp",
            md_bg_color=random.choice([
                (1.0, 111/255, 64/255, 1),      # Laranja queimado vivo
                (0.36, 0.8, 0.96, 1),           # Azul claro brilhante
                (0.85, 0.53, 0.97, 1),          # Rosa roxo neon suave
                (0.59, 0.43, 0.91, 1),          # Roxo pastel vibrante
            ]),
            text_color=(1, 1, 1, 1),
            font_name="ComicNeue",
            elevation=6,
            **kwargs
        )
#= ============================================================================



# =============================================================================
# CLASSE PRINCIPAL DO JOGO DE FRAÇÕES
# =============================================================================
class FracoesGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "fracoes"
        self.pergunta_atual = 1
        self.total_perguntas = 10
        self.acertos = 0
        self.erros = 0
        self.resposta_correta = ""

        self.layout = FloatLayout()
        self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg_image)

        self.back_button = MDIconButton(icon='arrow-left', pos_hint={'x': 0, 'top': 1},on_release=self.voltar)
        self.layout.add_widget(self.back_button)

        self.main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(30), dp(20), dp(30), dp(20)],
            size_hint=(1, 1)
        )

        self.top_layout = BoxLayout(size_hint_y=None, height=dp(40))

        self.progresso_label = MDLabel(
            font_size=dp(14),  # tamanho menor
            halign="left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_name="ComicNeue"
        )

        self.placar_label = MDLabel(
            font_size=dp(14),  # tamanho menor
            halign="right",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_name="ComicNeue"
        )

        self.top_layout.add_widget(self.progresso_label)
        self.top_layout.add_widget(self.placar_label)
        self.main_layout.add_widget(self.top_layout)

        self.question_card = MDCard(
            size_hint=(1, 0.45),
            elevation=8,
            radius=[30],
            padding=dp(10),
            md_bg_color=(0.85, 0.53, 0.97, 1)

        )
        self.pie_chart_image = Image(allow_stretch=True)
        self.question_card.add_widget(self.pie_chart_image)
        self.main_layout.add_widget(self.question_card)

        self.resposta_card = MDCard(
            size_hint=(1, 0.15),
            elevation=10,
            radius=[25],
            md_bg_color=(0.36, 0.8, 0.96, 1)
        )
        self.resposta_label = MDLabel(
            text="Qual é a fração?",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(53/255, 79/255, 117/255, 1),
            font_name="ComicNeue"
        )
        self.resposta_card.add_widget(self.resposta_label)
        self.main_layout.add_widget(self.resposta_card)

        self.botoes_layout_1 = BoxLayout(spacing=dp(12), size_hint_y=None, height=dp(60))
        self.botoes_layout_2 = BoxLayout(spacing=dp(12), size_hint_y=None, height=dp(60))
        self.main_layout.add_widget(self.botoes_layout_1)
        self.main_layout.add_widget(self.botoes_layout_2)

        self.help_button = MDFloatingActionButton(
            icon="play-circle-outline",
            pos_hint={'right': 0.55, 'top': 0.985},
            on_release=self.mostrar_exemplo_animado
        )
        self.layout.add_widget(self.help_button)

        self.layout.add_widget(self.main_layout)
        self.add_widget(self.layout)
        self.representacoes = ["pizza", "barra", "hexagono"]
        self.dificuldade = "Primario"


    def definir_dificuldade(self, dificuldade):
        self.dificuldade = dificuldade

    def on_pre_enter(self, *args):
        print(f"[DEBUG on_pre_enter] Dificuldade: {self.dificuldade}")
        self.reiniciar_jogo()


    def reiniciar_jogo(self):
        self.pergunta_atual = 1
        self.acertos = 0
        self.erros = 0
        self.gerar_pergunta()

    def criar_grafico_pizza(self, numerador, denominador, nome_arquivo='grafico_pizza.png'):
        fig, ax = plt.subplots()
        fatias = [1] * denominador
        cores = ['skyblue' if i < numerador else 'lightgray' for i in range(denominador)]
        wedges, _ = ax.pie(fatias, colors=cores, startangle=90, counterclock=False)
        for w in wedges:
            w.set_edgecolor('black')
        ax.set_aspect('equal')
        plt.axis('off')
        plt.savefig(nome_arquivo, transparent=True)
        plt.close(fig)
        return nome_arquivo

    def criar_grafico_barra(self, numerador, denominador):
        fig, ax = plt.subplots(figsize=(6, 1))
        for i in range(denominador):
            cor = 'saddlebrown' if i < numerador else 'lightgray'
            ax.barh(0, 1, left=i, height=1, color=cor, edgecolor='black')
        ax.set_xlim(0, denominador)
        ax.axis('off')
        caminho_imagem = 'grafico_barra.png'
        plt.savefig(caminho_imagem, transparent=True)
        plt.close(fig)
        return caminho_imagem


    def criar_grafico_hexagonos(self, numerador, denominador):
        cols = math.ceil(math.sqrt(denominador))
        rows = math.ceil(denominador / cols)

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.set_aspect('equal')
        hex_size = 1

        count = 0
        for row in range(rows):
            for col in range(cols):
                if count >= denominador:
                    break
                x = col * 1.5 * hex_size
                y = row * math.sqrt(3) * hex_size + (math.sqrt(3)/2 * hex_size if col % 2 == 1 else 0)
                color = 'deepskyblue' if count < numerador else 'lightgray'
                hex = patches.RegularPolygon(
                    (x, y), numVertices=6, radius=hex_size,
                    orientation=math.radians(30), facecolor=color, edgecolor='black'
                )
                ax.add_patch(hex)
                count += 1

        ax.set_xlim(-1, cols * 1.5)
        ax.set_ylim(-1, rows * math.sqrt(3) + 1)
        ax.axis('off')
        caminho_imagem = 'grafico_hexagono.png'
        plt.savefig(caminho_imagem, transparent=True)
        plt.close(fig)
        return caminho_imagem

    def gerar_pergunta(self):
        print(f"[DEBUG] Dificuldade atual: {self.dificuldade}")
        if self.dificuldade == "Primário":
            self.gerar_pergunta_primario()
        elif self.dificuldade == "Fundamental":
            self.gerar_pergunta_fundamental()
        else:
            print("[ERRO] Dificuldade não reconhecida!")


    def gerar_pergunta_fundamental(self):
        self.placar_label.text = f"Acertos: {self.acertos}  Erros: {self.erros}"
        self.progresso_label.text = f"Pergunta: {self.pergunta_atual}/{self.total_perguntas}"
        self.resposta_card.md_bg_color = App.get_running_app().theme_cls.bg_dark

        operacoes = ['+', '-', '*', '/']
        op = random.choice(operacoes)

        # Frações aleatórias
        d1 = random.randint(2, 8)
        n1 = random.randint(1, d1)
        f1 = Fraction(n1, d1)

        d2 = random.randint(2, 8)
        n2 = random.randint(1, d2)
        f2 = Fraction(n2, d2)

        # Calcula resultado
        if op == '+':
            resultado = f1 + f2
        elif op == '-':
            resultado = f1 - f2 if f1 > f2 else f2 - f1
            if f1 < f2:
                f1, f2 = f2, f1
        elif op == '*':
            resultado = f1 * f2
        elif op == '/':
            resultado = f1 / f2

        self.resposta_correta = f"{resultado.numerator}/{resultado.denominator}"
        self.resposta_label.text = f"Quanto é {f1} {op} {f2}?"

        # Gera imagens com nomes distintos
        img1 = self.criar_grafico_pizza(f1.numerator, f1.denominator, nome_arquivo='fra1.png')
        img2 = self.criar_grafico_pizza(f2.numerator, f2.denominator, nome_arquivo='fra2.png')

        # Renderiza o operador como imagem
        img1_pil = PILImage.open(img1)
        img2_pil = PILImage.open(img2)
        operador_img = PILImage.new("RGBA", (60, img1_pil.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(operador_img)

        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()

        bbox = font.getbbox(op)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((60 - text_w) // 2, (img1_pil.height - text_h) // 2), op, fill="black", font=font)

        # Junta as 3 imagens
        largura_total = img1_pil.width + operador_img.width + img2_pil.width
        altura = max(img1_pil.height, img2_pil.height)
        combinada = PILImage.new("RGBA", (largura_total, altura), (255, 255, 255, 0))
        combinada.paste(img1_pil, (0, 0), img1_pil)
        combinada.paste(operador_img, (img1_pil.width, 0), operador_img)
        combinada.paste(img2_pil, (img1_pil.width + operador_img.width, 0), img2_pil)

        caminho_combinado = "grafico_operacao.png"
        combinada.save(caminho_combinado)

        self.pie_chart_image.source = caminho_combinado
        self.pie_chart_image.reload()

        # Gera alternativas
        opcoes = {self.resposta_correta}
        while len(opcoes) < 4:
            fake = resultado + Fraction(random.choice([-2, -1, 1, 2]), random.randint(1, 8))
            fracao_fake = f"{fake.numerator}/{fake.denominator}"
            if fracao_fake != self.resposta_correta and fake > 0:
                opcoes.add(fracao_fake)

        opcoes_list = list(opcoes)
        random.shuffle(opcoes_list)

        self.botoes_layout_1.clear_widgets()
        self.botoes_layout_2.clear_widgets()
        botoes = [CardBotao(texto=op, on_press_func=self.verificar_resposta) for op in opcoes_list]
        self.botoes_layout_1.add_widget(botoes[0])
        self.botoes_layout_1.add_widget(botoes[1])
        self.botoes_layout_2.add_widget(botoes[2])
        self.botoes_layout_2.add_widget(botoes[3])

    def gerar_pergunta_primario(self):
        self.placar_label.text = f"Acertos: {self.acertos}  Erros: {self.erros}"
        self.progresso_label.text = f"Pergunta: {self.pergunta_atual}/{self.total_perguntas}"
        self.resposta_label.text = "Qual é a fração?"
        self.resposta_card.md_bg_color = App.get_running_app().theme_cls.bg_dark

        denominador = random.randint(2, 6)
        numerador = random.randint(1, denominador)
        self.resposta_correta = f"{numerador}/{denominador}"

        tipo_grafico = random.choice(self.representacoes)
        if tipo_grafico == "pizza":
            caminho_imagem = self.criar_grafico_pizza(numerador, denominador)
        elif tipo_grafico == "barra":
            caminho_imagem = self.criar_grafico_barra(numerador, denominador)
        elif tipo_grafico == "hexagono":
            caminho_imagem = self.criar_grafico_hexagonos(numerador, denominador)

        self.pie_chart_image.source = caminho_imagem
        self.pie_chart_image.reload()

        opcoes = {self.resposta_correta}
        while len(opcoes) < 4:
            d_errado = random.randint(2, 6)
            n_errado = random.randint(1, d_errado)
            fracao_errada = f"{n_errado}/{d_errado}"
            opcoes.add(fracao_errada)
        opcoes_list = list(opcoes)
        random.shuffle(opcoes_list)

        self.botoes_layout_1.clear_widgets()
        self.botoes_layout_2.clear_widgets()
        botoes = [CardBotao(texto=op, on_press_func=self.verificar_resposta) for op in opcoes_list]
        self.botoes_layout_1.add_widget(botoes[0])
        self.botoes_layout_1.add_widget(botoes[1])
        self.botoes_layout_2.add_widget(botoes[2])
        self.botoes_layout_2.add_widget(botoes[3])


    def verificar_resposta(self, valor_str):
        if valor_str == self.resposta_correta:
            self.acertos += 1
            self.resposta_label.text = "Acertou! ✔️"
            self.resposta_card.md_bg_color = (0.2, 0.8, 0.2, 1)
        else:
            self.erros += 1
            self.resposta_label.text = f"Errou! Era {self.resposta_correta} ❌"
            self.resposta_card.md_bg_color = (0.9, 0.3, 0.3, 1)
        self.placar_label.text = f"Acertos: {self.acertos}  Erros: {self.erros}"
        self.pergunta_atual += 1
        if self.pergunta_atual > self.total_perguntas:
            Clock.schedule_once(lambda dt: self.encerrar_jogo(), 1.5)
        else:
            Clock.schedule_once(lambda dt: self.gerar_pergunta(), 1.5)

    def encerrar_jogo(self):
        fim_screen = self.manager.get_screen("fim_fracoes")
        fim_screen.atualizar_stats(self.acertos, self.erros, "Frações")
        self.manager.current = "fim_fracoes"

    def voltar(self, instance):
        self.manager.current = "jogar"

    def mostrar_exemplo_animado(self, *args):
        # Caminho do vídeo de exemplo

        # Cria o layout do vídeo
        video_widget = Video(
            source='SomaFracoesTexto.mp4',
            state='play',
            allow_stretch=True,
            keep_ratio=True,
            volume=1.0,
            size_hint=(1, 1)
        )

        # Envolve o vídeo em um BoxLayout para exibição
        video_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(500), dp(350)))
        video_layout.add_widget(video_widget)

        dialog = MDDialog(
            title="Exemplo de Frações",
            type="custom",
            content_cls=video_layout,
            buttons=[
                MDRaisedButton(
                    text="FECHAR",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
            width=dp(520)
        )

        dialog.bind(on_dismiss=lambda x: setattr(video_widget, 'state', 'stop'))
        dialog.open()


# =============================================================================
# TELA DE FIM DE JOGO PARA FRAÇÕES
# =============================================================================
class TelaFimFracoes(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "fim_fracoes"
        layout = FloatLayout()

        self.bg_image = Image(
            source='fundoapp.png',
            allow_stretch=True,
            keep_ratio=False
        )
        layout.add_widget(self.bg_image)

        self.title_label = MDLabel(
            text="Fim de Jogo!",
            font_style="H3",
            halign="center",
            pos_hint={"center_x": 0.5, "top": 0.9},
            theme_text_color="Custom"
        )
        layout.add_widget(self.title_label)

        self.card_stats = MDCard(
            size_hint=(0.8, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            elevation=10,
            padding=dp(25),
            radius=[20],
            orientation="vertical",
            spacing=dp(15)
        )
        self.acertos_label = MDLabel(
            font_style="H6",
            halign="center"
        )

        self.erros_label = MDLabel(
            font_style="H6",
            halign="center"
        )

        self.jogo_label = MDLabel(
            font_style="H6",
            halign="center"
        )

        self.card_stats.add_widget(self.acertos_label); self.card_stats.add_widget(self.erros_label); self.card_stats.add_widget(self.jogo_label)
        layout.add_widget(self.card_stats)

        self.menu_button = MDRaisedButton(
            text="Voltar ao Menu",
            font_size="18sp",
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            size_hint=(0.6, 0.08),
            on_release=self.voltar_menu
        )
        layout.add_widget(self.menu_button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        theme = App.get_running_app().theme_cls
        self.bg_image.source = "escuro.png" if theme.theme_style == "Dark" else "fundoapp.png"
        self.title_label.color = (1,1,1,1) if theme.theme_style == "Dark" else (0,0,0,1)
        self.card_stats.md_bg_color = theme.bg_dark
        for label in self.card_stats.children:
            if hasattr(label, 'color'): label.color = theme.text_color
        self.menu_button.md_bg_color = theme.primary_color
        self.menu_button.theme_text_color = "ContrastParentBackground"

    def atualizar_stats(self, acertos, erros, nome_jogo):
        self.acertos_label.text = f"✅ Acertos: {acertos}"
        self.erros_label.text = f"❌ Erros: {erros}"
        self.jogo_label.text = f"📊 Jogo: {nome_jogo}"

    def voltar_menu(self, instance):
        self.manager.current = "jogar"
