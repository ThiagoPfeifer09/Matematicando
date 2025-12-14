from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFloatingActionButton
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.video import Video
from kivy.metrics import dp
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from fractions import Fraction
from PIL import Image as PILImage, ImageDraw
import random
import math

# Cores Globais
COR_AZUL_DEST = "#1E90FF"  # DodgerBlue
COR_FUNDO_GRAF = "#F5F5F5" # WhiteSmoke
COR_BORDAS = "black"

# =============================================================================
# CARD DE RESPOSTA (BOTÃO)
# =============================================================================
class OpcaoCard(MDCard):
    def __init__(self, texto, on_press_func, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.elevation = 3
        self.radius = [12]
        self.ripple_behavior = True
        self.md_bg_color = (1, 1, 1, 1)
        self.padding = dp(5)
        self.on_press_func = on_press_func
        self.texto_resposta = texto

        box = BoxLayout(orientation='vertical')
        lbl = MDLabel(
            text=texto, halign="center", valign="center",
            font_style="H4", theme_text_color="Custom", # Aumentei a fonte para H4 para ficar legível
            text_color=(0.2, 0.2, 0.2, 1), bold=True
        )
        box.add_widget(lbl)
        self.add_widget(box)

    def on_release(self):
        self.on_press_func(self.texto_resposta)

# =============================================================================
# TELA PRINCIPAL DO JOGO DE FRAÇÕES
# =============================================================================
class FracoesGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "fracoes_info"

        # Variáveis de Estado
        self.pergunta_atual = 1
        self.total_perguntas = 10
        self.acertos = 0
        self.erros = 0
        self.resposta_correta = ""
        self.dificuldade = "Primario"
        self.timer_event = None
        self.tempo_total = 20
        self.tempo_restante = 20

        # Layout Base
        self.layout = FloatLayout()
        self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg_image)

        # Botão Voltar
        self.back_button = MDIconButton(
            icon='arrow-left',
            pos_hint={'x': 0.02, 'top': 0.98},
            theme_text_color="Custom",
            text_color=(0,0,0,1),
            on_release=self.voltar
        )
        self.layout.add_widget(self.back_button)

        # Container Principal
        # AJUSTE 1: Aumentei o padding TOP para dp(90) para descer o conteúdo e não bater no botão
        self.main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=[dp(20), dp(90), dp(20), dp(10)],
            size_hint=(1, 1)
        )

        # 1. BARRA DE STATUS (HUD)
        # AJUSTE 2: Diminuí a largura e centralizei para não encostar no botão Ajuda
        self.hud_card = MDCard(
            size_hint=(0.9, None), # 90% da largura
            pos_hint={"center_x": 0.5}, # Centralizado
            height=dp(50),
            radius=[15],
            elevation=4,
            md_bg_color=(1, 1, 1, 0.95),
            padding=[dp(10), dp(5), dp(10), dp(5)]
        )

        hud_box = MDBoxLayout(orientation="horizontal", spacing=dp(15))

        self.lbl_num_quest = self._criar_item_hud(hud_box, "help-circle-outline", "1/10", (0, 0, 0, 1))
        self.lbl_acertos = self._criar_item_hud(hud_box, "check-circle", "0", (0, 0.7, 0, 1))
        self.lbl_erros = self._criar_item_hud(hud_box, "close-circle", "0", (0.8, 0, 0, 1))

        self.hud_card.add_widget(hud_box)
        self.main_layout.add_widget(self.hud_card)

        # 2. BARRA DE TIMER
        self.progress_timer = MDProgressBar(
            value=100,
            color=(1, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(4),
            opacity=0
        )
        self.main_layout.add_widget(self.progress_timer)

        # 3. CARD DO GRÁFICO
        self.question_card = MDCard(
            size_hint=(0.95, 0.35),
            pos_hint={"center_x": 0.5},
            elevation=2,
            radius=[20],
            padding=dp(8),
            md_bg_color=(1, 1, 1, 0.95)
        )
        self.pie_chart_image = Image(allow_stretch=True, keep_ratio=True)
        self.question_card.add_widget(self.pie_chart_image)
        self.main_layout.add_widget(self.question_card)

        # 4. CARD DO ENUNCIADO
        self.card_enunciado = MDCard(
            size_hint=(1, None),
            height=dp(50),
            radius=[10],
            elevation=0,
            md_bg_color=(1, 1, 1, 0)
        )
        self.lbl_enunciado = MDLabel(
            text="Qual fração representa a parte AZUL?",
            halign="center",
            valign="center",
            bold=True,
            theme_text_color="Primary",
            font_style="Subtitle1"
        )
        self.card_enunciado.add_widget(self.lbl_enunciado)
        self.main_layout.add_widget(self.card_enunciado)

        # 5. BOTÕES DE RESPOSTA
        self.grid_botoes = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=0.28
        )
        self.linha1 = BoxLayout(spacing=dp(10))
        self.linha2 = BoxLayout(spacing=dp(10))
        self.grid_botoes.add_widget(self.linha1)
        self.grid_botoes.add_widget(self.linha2)

        self.main_layout.add_widget(self.grid_botoes)

        # Botão Ajuda
        self.help_button = MDFloatingActionButton(
            icon="help",
            pos_hint={'right': 0.95, 'top': 0.98},
            md_bg_color=(1, 0.6, 0, 1),
            on_release=self.mostrar_exemplo_animado,
            elevation=4,
            icon_size=dp(24)
        )
        self.layout.add_widget(self.help_button)

        self.layout.add_widget(self.main_layout)
        self.add_widget(self.layout)

    def _criar_item_hud(self, layout_pai, icon, text, color):
        box = MDBoxLayout(orientation="horizontal", spacing=dp(5), adaptive_width=True)
        box.add_widget(MDIconButton(
            icon=icon, icon_size=dp(20), theme_text_color="Custom", text_color=color,
            size_hint=(None, None), size=(dp(24), dp(24))
        ))
        lbl = MDLabel(
            text=text, theme_text_color="Custom", text_color=color, bold=True,
            font_style="Subtitle2", adaptive_width=True, valign="center"
        )
        box.add_widget(lbl)
        layout_pai.add_widget(box)
        return lbl

    # =========================================================================
    # LÓGICA DO JOGO
    # =========================================================================
    def definir_dificuldade(self, dificuldade):
        self.dificuldade = dificuldade

    def on_pre_enter(self, *args):
        self.reiniciar_jogo()

    def on_leave(self, *args):
        self.parar_timer()

    def reiniciar_jogo(self):
        self.pergunta_atual = 1
        self.acertos = 0
        self.erros = 0
        self.gerar_pergunta()

    def atualizar_hud(self):
        self.lbl_num_quest.text = f"{self.pergunta_atual}/{self.total_perguntas}"
        self.lbl_acertos.text = str(self.acertos)
        self.lbl_erros.text = str(self.erros)

    def gerar_pergunta(self):
        self.atualizar_hud()

        self.card_enunciado.md_bg_color = (0, 0, 0, 0)
        self.lbl_enunciado.theme_text_color = "Primary"
        self.lbl_enunciado.text_color = (0,0,0,1)

        self.parar_timer()
        if self.dificuldade in ["Medio", "Fundamental"]:
            self.progress_timer.opacity = 1
            self.tempo_total = 20 if self.dificuldade == "Medio" else 25
            self.tempo_restante = self.tempo_total
            self.progress_timer.value = 100
            self.timer_event = Clock.schedule_interval(self.atualizar_timer, 1)
        else:
            self.progress_timer.opacity = 0

        if self.dificuldade == "Primario":
            self.gerar_primario()
        elif self.dificuldade == "Medio":
            self.gerar_medio()
        else:
            self.gerar_fundamental()

    def atualizar_timer(self, dt):
        self.tempo_restante -= 1
        pct = (self.tempo_restante / self.tempo_total) * 100
        self.progress_timer.value = pct

        if self.tempo_restante <= 0:
            self.verificar_resposta(None)

    def parar_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

    # --- GERADORES ---
    # --- GERADORES COM DIVERSIFICAÇÃO ---
    def gerar_primario(self):
        self.lbl_enunciado.text = "Qual fração representa a parte AZUL?"

        # Gera o denominador
        d = random.randint(2, 6)

        # Gera numerador
        n = random.randint(1, d)

        # --- LÓGICA DE DIVERSIFICAÇÃO ---
        # Se o numerador for igual ao denominador (ex: 3/3),
        # jogamos um dado. Temos 80% de chance de FORÇAR ele a mudar.
        # Isso diminui drasticamente a quantidade de "pizzas inteiras".
        if n == d and d > 1:
            if random.random() < 0.80: # 80% de chance de trocar
                n = random.randint(1, d - 1)
        # --------------------------------

        self.resposta_correta = f"{n}/{d}"

        if random.choice(["pizza", "barra"]) == "pizza":
            img = self.criar_grafico_pizza(n, d)
        else:
            img = self.criar_grafico_barra(n, d)

        self.pie_chart_image.source = img
        self.pie_chart_image.reload()

        self.gerar_alternativas(n, d)

    def gerar_medio(self):
        self.lbl_enunciado.text = "Qual fração representa a parte AZUL?"

        # Aumentei um pouco o range para dar mais variedade visual
        d = random.randint(4, 10)
        n = random.randint(1, d)

        # --- LÓGICA DE DIVERSIFICAÇÃO ---
        # Mesma regra: evita excesso de frações inteiras (ex: 8/8)
        if n == d and d > 1:
            if random.random() < 0.80:
                n = random.randint(1, d - 1)
        # --------------------------------

        self.resposta_correta = f"{n}/{d}"

        # Hexágonos são legais, vamos aumentar a chance deles aparecerem no médio (60%)
        if random.random() < 0.6:
            img = self.criar_grafico_hexagonos(n, d)
        else:
            img = self.criar_grafico_pizza(n, d)

        self.pie_chart_image.source = img
        self.pie_chart_image.reload()

        self.gerar_alternativas(n, d)


    def gerar_fundamental(self):
        operacoes = ['+', '-', '*', '/']
        op = random.choice(operacoes)
        d1 = random.randint(2, 6); n1 = random.randint(1, d1); f1 = Fraction(n1, d1)
        d2 = random.randint(2, 6); n2 = random.randint(1, d2); f2 = Fraction(n2, d2)

        if op == '+': res = f1 + f2
        elif op == '-':
            if f1 < f2: f1, f2 = f2, f1
            res = f1 - f2
        elif op == '*': res = f1 * f2
        elif op == '/': res = f1 / f2

        # No fundamental, como é cálculo, a simplificação é aceitável, mas
        # para manter consistência, vamos pegar o numerador/denominador do resultado
        self.resposta_correta = f"{res.numerator}/{res.denominator}"
        self.lbl_enunciado.text = f"Quanto é:  {f1}  {op}  {f2} ?"

        self.gerar_imagem_operacao(f1, f2, op)
        self.gerar_alternativas(res.numerator, res.denominator)

    # --- AUXILIARES GRÁFICOS ---
    def criar_grafico_pizza(self, n, d, nome='grafico_pizza.png'):
        fig, ax = plt.subplots(figsize=(4, 4))
        cores = [COR_AZUL_DEST if i < n else COR_FUNDO_GRAF for i in range(d)]
        ax.pie([1]*d, colors=cores, startangle=90, counterclock=False, wedgeprops={"edgecolor": COR_BORDAS, 'linewidth': 2})
        plt.subplots_adjust(0,0,1,1); plt.axis('off'); plt.savefig(nome, transparent=True, dpi=90); plt.close(fig)
        return nome

    def criar_grafico_barra(self, n, d):
        fig, ax = plt.subplots(figsize=(6, 2))
        for i in range(d):
            c = COR_AZUL_DEST if i < n else COR_FUNDO_GRAF
            ax.barh(0, 1, left=i, height=0.8, color=c, edgecolor=COR_BORDAS, linewidth=2)
        ax.set_xlim(0, d); ax.axis('off'); plt.savefig('grafico_barra.png', transparent=True, dpi=90, bbox_inches='tight'); plt.close(fig)
        return 'grafico_barra.png'

    def criar_grafico_hexagonos(self, n, d):
        # Layout automático em grade
        cols = math.ceil(math.sqrt(d))
        rows = math.ceil(d / cols)

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.set_aspect('equal')

        count = 0
        for row in range(rows):
            for col in range(cols):
                if count >= d: break

                # Ajuste de espaçamento (1.5 e sqrt(3) são geometria hexagonal)
                x = col * 1.5
                y = -row * math.sqrt(3) - (math.sqrt(3)/2 if col % 2 else 0)

                c = COR_AZUL_DEST if count < n else COR_FUNDO_GRAF

                # CORREÇÃO AQUI: Passar 'numVertices' e 'radius' nomeados explicitamente
                poly = patches.RegularPolygon(
                    (x, y),
                    numVertices=6,
                    radius=1,
                    orientation=math.radians(30),
                    facecolor=c,
                    edgecolor=COR_BORDAS,
                    linewidth=2
                )
                ax.add_patch(poly)
                count += 1

        ax.autoscale_view()
        ax.axis('off')

        nome_arquivo = 'grafico_hex.png'
        plt.savefig(nome_arquivo, transparent=True, dpi=90, bbox_inches='tight')
        plt.close(fig)
        return nome_arquivo

    def gerar_imagem_operacao(self, f1, f2, op):
        img1 = self.criar_grafico_pizza(f1.numerator, f1.denominator, 'fra1.png')
        img2 = self.criar_grafico_pizza(f2.numerator, f2.denominator, 'fra2.png')
        try:
            p1 = PILImage.open(img1); p2 = PILImage.open(img2)
            w_op = 60; h = max(p1.height, p2.height)
            i_op = PILImage.new("RGBA", (w_op, h), (0,0,0,0)); draw = ImageDraw.Draw(i_op)
            draw.text((20, h//2-15), op, fill="black", font_size=30)
            comb = PILImage.new("RGBA", (p1.width+w_op+p2.width, h), (0,0,0,0))
            comb.paste(p1,(0,0)); comb.paste(i_op,(p1.width,0)); comb.paste(p2,(p1.width+w_op,0))
            comb.save("grafico_op.png"); self.pie_chart_image.source = "grafico_op.png"; self.pie_chart_image.reload()
        except: pass

    # --- CORREÇÃO DA GERAÇÃO DE ALTERNATIVAS ---
    def gerar_alternativas(self, num_correto, den_correto):
        # Cria a resposta correta como string exata (ex: "3/3")
        str_correta = f"{num_correto}/{den_correto}"
        opcoes = {str_correta}

        while len(opcoes) < 4:
            # Gera denominadores e numeradores aleatórios
            d_fake = random.randint(2, 10)
            n_fake = random.randint(1, d_fake) # Garante que o numerador não ultrapasse se for pizza simples

            # Se for nível fundamental (operações), pode ter frações impróprias, então relaxamos
            if self.dificuldade == "Fundamental":
                n_fake = random.randint(1, 15)

            str_fake = f"{n_fake}/{d_fake}"

            # Evita duplicatas de string
            if str_fake != str_correta:
                opcoes.add(str_fake)

        lista = list(opcoes)
        random.shuffle(lista)

        self.linha1.clear_widgets(); self.linha2.clear_widgets()
        self.linha1.add_widget(OpcaoCard(lista[0], self.verificar_resposta))
        self.linha1.add_widget(OpcaoCard(lista[1], self.verificar_resposta))
        self.linha2.add_widget(OpcaoCard(lista[2], self.verificar_resposta))
        self.linha2.add_widget(OpcaoCard(lista[3], self.verificar_resposta))

    # =========================================================================
    # VERIFICAÇÃO
    # =========================================================================
    def verificar_resposta(self, resposta):
        self.parar_timer()

        if resposta is None:
            acertou = False
            self.lbl_enunciado.text = f"Tempo Esgotado! Era {self.resposta_correta}"
        elif resposta == self.resposta_correta:
            acertou = True
            self.lbl_enunciado.text = "Acertou! Muito bem!"
        else:
            acertou = False
            self.lbl_enunciado.text = f"Errou! Era {self.resposta_correta}"

        if acertou:
            self.acertos += 1
            self.card_enunciado.md_bg_color = (0.7, 1, 0.7, 1)
            self.lbl_enunciado.theme_text_color = "Custom"
            self.lbl_enunciado.text_color = (0, 0.4, 0, 1)
        else:
            self.erros += 1
            self.card_enunciado.md_bg_color = (1, 0.7, 0.7, 1)
            self.lbl_enunciado.theme_text_color = "Custom"
            self.lbl_enunciado.text_color = (0.6, 0, 0, 1)

        self.atualizar_hud()
        self.pergunta_atual += 1

        if self.pergunta_atual > self.total_perguntas:
            Clock.schedule_once(lambda dt: self.encerrar_jogo(), 2)
        else:
            Clock.schedule_once(lambda dt: self.gerar_pergunta(), 2)

    def encerrar_jogo(self):
        if self.manager.has_screen("fim_fracoes"):
            tela = self.manager.get_screen("fim_fracoes")
            tela.atualizar_stats(self.acertos, self.erros, "Frações")
            self.manager.current = "fim_fracoes"
        else:
            self.voltar(None)

    def voltar(self, instance):
        self.parar_timer()
        self.manager.current = "jogar"

    def mostrar_exemplo_animado(self, *args):
        # Código do vídeo
        pass

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


    def atualizar_stats(self, acertos, erros, nome_jogo):
        self.acertos_label.text = f"✅ Acertos: {acertos}"
        self.erros_label.text = f"❌ Erros: {erros}"
        self.jogo_label.text = f"📊 Jogo: {nome_jogo}"

    def voltar_menu(self, instance):
        self.manager.current = "jogar"
