from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.label import MDIcon
import random
from kivymd.uix.screen import MDScreen
from kivy.uix.modalview import ModalView
from kivy.metrics import dp
from kivy.uix.video import Video
from kivy.core.window import Window
from kivy.uix.widget import Widget

# --- Paleta de Cores ---
COR_PRIMARIA = (0.2, 0.6, 0.8, 1)
COR_TEXTO = (0.1, 0.1, 0.1, 1)
COR_FUNDO_BOTAO = (0.85, 0.92, 1.0, 1)
COR_TEXTO_BOTAO = (0, 0, 0, 1)

# Cores para Dificuldades
COR_DIF_PRIMARIO = (0.4, 0.7, 0.9, 1)
COR_DIF_FUNDAMENTAL = (0.5, 0.5, 0.8, 1)
COR_DIF_MEDIO = (0.6, 0.3, 0.7, 1)

class CardBotao(MDCard):
    """Botão de resposta ajustado."""
    def __init__(self, texto, on_press_func, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.elevation = 3
        self.radius = [15]
        self.md_bg_color = COR_FUNDO_BOTAO
        self.texto = texto
        self.on_press_func = on_press_func
        self.padding = dp(5)
        self.ripple_behavior = True

        self.label = MDLabel(
            text=texto,
            halign="center",
            valign="center",
            font_style="H6",
            theme_text_color="Custom",
            text_color=COR_TEXTO_BOTAO,
            bold=True
        )
        self.add_widget(self.label)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.elevation = 1
            return super().on_touch_down(touch)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.elevation = 3
            self.on_press_func(self.texto, self)
            return True
        return super().on_touch_up(touch)


class AlgebraGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dificuldade = "fundamental"

        self.pergunta_atual = 1
        self.total_perguntas = 10
        self.acertos = 0
        self.erros = 0
        self.resposta_correta = None
        self.tempo_inicial = 30
        self.tempo_restante = 30
        self.timer_event = None
        self.tempo_total = 0
        self.tempo_total_event = None
        self.respondido = False

        # --- Layout Principal ---
        self.layout = FloatLayout()
        try:
            self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
            self.layout.add_widget(self.bg_image)
        except:
            Window.clearcolor = (0.92, 0.94, 0.96, 1)

        # --- Cabeçalho ---
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(60), padding=[dp(10), dp(5), dp(10), 0], spacing=dp(5), pos_hint={'top': 1})

        self.back_button = MDIconButton(
            icon='arrow-left',
            icon_size="32sp",
            on_release=self.voltar,
            theme_text_color="Custom",
            text_color=COR_TEXTO
        )
        header_layout.add_widget(self.back_button)
        header_layout.add_widget(MDLabel(text="Álgebra", font_style="H5", bold=True, theme_text_color="Custom", text_color=COR_TEXTO))

        self.help_button = MDIconButton(
            icon="play-circle",
            icon_size="36sp",
            theme_text_color="Custom",
            text_color=COR_PRIMARIA,
            on_release=self.mostrar_exemplo_animado
        )
        header_layout.add_widget(self.help_button)
        self.layout.add_widget(header_layout)

        # --- Container Central ---
        self.main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(20), dp(60), dp(20), dp(20)],
            size_hint=(1, 1)
        )

        # 1. Info Card (Aumentado levemente)
        self.info_card = MDCard(
            size_hint=(1, None),
            height=dp(100),
            elevation=2,
            radius=[15],
            padding=dp(12),
            orientation='vertical',
            md_bg_color=(1, 1, 1, 0.9)
        )

        # Linha Superior: Progresso e Placar com ÍCONES REAIS
        top_row = BoxLayout(size_hint_y=0.6, spacing=dp(10))

        self.progresso_label = MDLabel(
            text="1/10",
            halign="left",
            theme_text_color="Custom", text_color=COR_TEXTO,
            font_style="Subtitle1", bold=True,
            size_hint_x=0.4
        )

        # Box do Placar (Alinhado à direita)
        placar_box = BoxLayout(orientation='horizontal', size_hint_x=0.6, spacing=dp(5))

        # Ícone Acerto (Verde)
        icon_check = MDIcon(icon="check-circle", theme_text_color="Custom", text_color=(0.2, 0.7, 0.2, 1), font_size="22sp", pos_hint={'center_y': 0.5})
        self.acertos_label = MDLabel(text="0", font_style="Subtitle1", bold=True, theme_text_color="Custom", text_color=COR_TEXTO, size_hint_x=None, width=dp(30))

        # Ícone Erro (Vermelho)
        icon_close = MDIcon(icon="close-circle", theme_text_color="Custom", text_color=(0.8, 0.2, 0.2, 1), font_size="22sp", pos_hint={'center_y': 0.5})
        self.erros_label = MDLabel(text="0", font_style="Subtitle1", bold=True, theme_text_color="Custom", text_color=COR_TEXTO, size_hint_x=None, width=dp(30))

        placar_box.add_widget(Widget()) # Empurrar para direita
        placar_box.add_widget(icon_check)
        placar_box.add_widget(self.acertos_label)
        placar_box.add_widget(icon_close)
        placar_box.add_widget(self.erros_label)

        top_row.add_widget(self.progresso_label)
        top_row.add_widget(placar_box)
        self.info_card.add_widget(top_row)

        # Linha Inferior: Timer
        timer_box = BoxLayout(orientation='vertical', size_hint_y=0.4)
        self.timer_label = MDLabel(
            text="00:30", halign="center", font_style="H6",
            theme_text_color="Custom", text_color=COR_PRIMARIA, bold=True
        )
        self.progress_bar = MDProgressBar(value=100, max=100, size_hint_y=None, height=dp(6), color=COR_PRIMARIA)

        timer_box.add_widget(self.timer_label)
        timer_box.add_widget(self.progress_bar)
        self.info_card.add_widget(timer_box)

        self.main_layout.add_widget(self.info_card)


        # 2. Card da Equação (MAIOR DESTAQUE AGORA)
        self.equation_card = MDCard(
            size_hint=(1, 0.30), # Aumentado para 30% da tela vertical disponivel
            elevation=4,
            radius=[20],
            padding=dp(20),
            md_bg_color=COR_DIF_FUNDAMENTAL
        )
        self.equation_label = MDLabel(
            text="...",
            font_style="H3", # Fonte Maior
            halign="center", valign="center",
            theme_text_color="Custom", text_color=(1, 1, 1, 1),
            bold=True
        )
        self.equation_card.add_widget(self.equation_label)
        self.main_layout.add_widget(self.equation_card)


        # 3. Card de Feedback (Resposta)
        self.resposta_card = MDCard(
            size_hint=(0.95, 0.08),
            pos_hint={'center_x': 0.5},
            elevation=0,
            radius=[10],
            md_bg_color=(0, 0, 0, 0)
        )
        self.resposta_label = MDLabel(
            text="Encontre o valor de X",
            font_style="Subtitle1",
            halign="center", valign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )
        self.resposta_card.add_widget(self.resposta_label)
        self.main_layout.add_widget(self.resposta_card)


        # 4. Botões de Opções (MENORES E MAIS COMPACTOS)
        self.grid_botoes = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=0.30) # Reduzido para 30%

        self.botoes_row_1 = BoxLayout(spacing=dp(15)) # Mais espaçamento horizontal
        self.botoes_row_2 = BoxLayout(spacing=dp(15))

        self.grid_botoes.add_widget(self.botoes_row_1)
        self.grid_botoes.add_widget(self.botoes_row_2)
        self.main_layout.add_widget(self.grid_botoes)

        # Espaçador final para balancear
        self.main_layout.add_widget(Widget(size_hint_y=0.02))

        self.layout.add_widget(self.main_layout)
        self.add_widget(self.layout)

    def define_dificuldade(self, dificuldade):
        """Define a dificuldade e ajusta a cor do tema."""
        self.dificuldade = dificuldade.lower()
        if self.dificuldade == "primario":
            self.equation_card.md_bg_color = COR_DIF_PRIMARIO
        elif self.dificuldade == "medio":
            self.equation_card.md_bg_color = COR_DIF_MEDIO
        else:
            self.equation_card.md_bg_color = COR_DIF_FUNDAMENTAL
        (print
          (f"Álgebra configurada para: {self.dificuldade}"))

    def on_enter(self, *args):
        self.reiniciar_jogo()

    def on_leave(self, *args):
        self.parar_timers()

    def parar_timers(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        if self.tempo_total_event:
            self.tempo_total_event.cancel()
            self.tempo_total_event = None

    def reiniciar_jogo(self):
        self.pergunta_atual = 1
        self.acertos = 0
        self.erros = 0
        self.tempo_total = 0
        self.respondido = False

        self.acertos_label.text = "0"
        self.erros_label.text = "0"
        self.progresso_label.text = f"1/{self.total_perguntas}"

        self.resposta_label.text = "Encontre o valor de X"
        self.resposta_label.text_color = COR_TEXTO
        self.resposta_card.md_bg_color = (0,0,0,0)
        self.resposta_card.elevation = 0

        self.parar_timers()
        self.tempo_total_event = Clock.schedule_interval(self.atualizar_tempo_total, 1)

        self.gerar_equacao()

    def gerar_equacao(self):
        self.respondido = False

        self.resposta_label.text = "Qual é o valor de X?"
        self.resposta_label.text_color = (0, 0, 0, 1)
        self.resposta_card.md_bg_color = (0.95, 0.95, 0.95, 0) # Transparente até responder
        self.resposta_card.elevation = 0

        x = 0
        equacao_txt = ""

        if self.dificuldade == "primario":
            self.tempo_inicial = 45
            tipo = random.choice(['soma', 'sub'])
            x = random.randint(1, 10)
            outro = random.randint(1, 10)
            if tipo == 'soma':
                res = x + outro
                if random.random() > 0.5: equacao_txt = f"x + {outro} = {res}"
                else: equacao_txt = f"{outro} + x = {res}"
            else:
                res = x - outro
                if res < 0: x, outro = outro + random.randint(1, 10), x; res = x - outro
                equacao_txt = f"x - {outro} = {res}"

        elif self.dificuldade == "medio":
            self.tempo_inicial = 40
            tipo = random.choice(['var_lados', 'distributiva', 'quadratica'])
            if tipo == 'quadratica':
                x = random.randint(2, 12)
                c = x * x
                equacao_txt = f"x² - {c} = 0"
            elif tipo == 'distributiva':
                a, b, x = random.randint(2, 5), random.randint(1, 5), random.randint(1, 8)
                c = a * (x + b)
                equacao_txt = f"{a}(x + {b}) = {c}"
            else:
                x, a = random.randint(1, 10), random.randint(3, 8)
                c = random.randint(1, a-1)
                dif_coef = a - c
                res_lado_esq = dif_coef * x
                b = random.randint(1, 20)
                d = res_lado_esq + b
                equacao_txt = f"{a}x + {b} = {c}x + {d}"

        else:
            self.tempo_inicial = 30
            tipo = random.choice(['linear', 'divisao', 'simples'])
            if tipo == 'simples':
                a, b = random.randint(2, 9), random.randint(1, 20)
                res = a * b; x = b
                equacao_txt = f"{a}x = {res}"
            elif tipo == 'divisao':
                a, b = random.randint(2, 10), random.randint(2, 10)
                x = a * b
                equacao_txt = f"x ÷ {a} = {b}"
            else:
                a, x, b = random.randint(2, 6), random.randint(1, 10), random.randint(1, 15)
                c = a * x + b
                equacao_txt = f"{a}x + {b} = {c}"

        self.resposta_correta = x
        self.equation_label.text = equacao_txt

        opcoes = {x}
        while len(opcoes) < 4:
            fake = x + random.randint(-5, 5)
            if fake > 0 and fake != x: opcoes.add(fake)
            elif fake <= 0: opcoes.add(random.randint(1, 20))

        lista_opcoes = list(opcoes)
        random.shuffle(lista_opcoes)

        self.botoes_row_1.clear_widgets()
        self.botoes_row_2.clear_widgets()
        for i, val in enumerate(lista_opcoes):
            btn = CardBotao(str(val), self.verificar_resposta)
            if i < 2: self.botoes_row_1.add_widget(btn)
            else: self.botoes_row_2.add_widget(btn)

        self.reset_timer_visual()

    def reset_timer_visual(self):
        self.tempo_restante = self.tempo_inicial
        self.atualizar_label_timer()
        self.progress_bar.value = 100
        self.progress_bar.color = COR_PRIMARIA

        if self.timer_event: self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.atualizar_timer, 1)

    def atualizar_timer(self, dt):
        self.tempo_restante -= 1
        self.atualizar_label_timer()

        percent = (self.tempo_restante / self.tempo_inicial) * 100
        self.progress_bar.value = percent

        if percent < 30: self.progress_bar.color = (0.9, 0.3, 0.3, 1)
        elif percent < 60: self.progress_bar.color = (0.9, 0.8, 0.2, 1)

        if self.tempo_restante <= 0:
            self.processar_erro("Tempo esgotado!")

    def atualizar_label_timer(self):
        m, s = divmod(self.tempo_restante, 60)
        self.timer_label.text = f"{m:02}:{s:02}"

    def verificar_resposta(self, resposta_str, btn_widget):
        if self.respondido: return
        self.respondido = True

        if self.timer_event: self.timer_event.cancel()

        resp_int = int(resposta_str)
        self.resposta_card.elevation = 3

        if resp_int == self.resposta_correta:
            self.acertos += 1
            btn_widget.md_bg_color = (0.4, 0.9, 0.4, 1)
            self.resposta_label.text = "Correto!"
            self.resposta_label.text_color = (0, 0.5, 0, 1)
            self.resposta_card.md_bg_color = (0.8, 1, 0.8, 1)
        else:
            self.erros += 1
            btn_widget.md_bg_color = (1.0, 0.6, 0.6, 1)
            self.resposta_label.text = f"Errado! Era {self.resposta_correta}"
            self.resposta_label.text_color = (0.8, 0, 0, 1)
            self.resposta_card.md_bg_color = (1, 0.85, 0.85, 1)

        self.acertos_label.text = f"{self.acertos}"
        self.erros_label.text = f"{self.erros}"

        Clock.schedule_once(lambda dt: self.proxima_etapa(), 1.5)

    def processar_erro(self, msg):
        if self.respondido: return
        self.respondido = True

        self.erros += 1
        self.acertos_label.text = f"{self.acertos}"
        self.erros_label.text = f"{self.erros}"

        self.resposta_label.text = f"{msg} (Era {self.resposta_correta})"
        self.resposta_label.text_color = (0.8, 0, 0, 1)
        self.resposta_card.md_bg_color = (1, 0.85, 0.85, 1)
        self.resposta_card.elevation = 3

        Clock.schedule_once(lambda dt: self.proxima_etapa(), 2.0)

    def proxima_etapa(self):
        self.pergunta_atual += 1
        self.progresso_label.text = f"{self.pergunta_atual}/{self.total_perguntas}"

        if self.pergunta_atual > self.total_perguntas:
            self.encerrar_jogo()
        else:
            self.gerar_equacao()

    def atualizar_tempo_total(self, dt):
        self.tempo_total += dt

    def encerrar_jogo(self):
        self.parar_timers()
        m, s = divmod(int(self.tempo_total), 60)
        tempo_fmt = f"{m:02}:{s:02}"

        if self.manager.has_screen("fim_algebra"):
            screen = self.manager.get_screen("fim_algebra")
            screen.atualizar_stats(self.acertos, self.erros, tempo_fmt, self.dificuldade)
            self.manager.current = "fim_algebra"
        else:
            self.voltar(None)

    def voltar(self, instance):
        self.parar_timers()
        self.manager.current = "jogar"

    def mostrar_exemplo_animado(self, *args):
        if self.timer_event: self.timer_event.cancel()

        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))

        try:
            vid = Video(source='eq1.mp4', state='play', options={'eos': 'loop'})
            content.add_widget(vid)
        except:
            lbl = MDLabel(text="Vídeo não encontrado.\nDica: Isole o X!", halign="center")
            content.add_widget(lbl)

        btn_close = MDRaisedButton(
            text="FECHAR",
            pos_hint={'center_x': 0.5},
            md_bg_color=COR_PRIMARIA,
            text_color=(1,1,1,1)
        )
        content.add_widget(btn_close)

        modal = ModalView(size_hint=(0.9, 0.65), auto_dismiss=False, background_color=(0,0,0,0.6))
        modal.add_widget(content)

        def fechar(*args):
            modal.dismiss()
            if self.pergunta_atual <= self.total_perguntas:
                self.timer_event = Clock.schedule_interval(self.atualizar_timer, 1)

        btn_close.bind(on_release=fechar)
        modal.open()


class TelaFimAlgebra(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        try:
            bg = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
            layout.add_widget(bg)
        except: pass

        card = MDCard(
            size_hint=(0.85, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            elevation=8,
            radius=[25],
            orientation='vertical',
            padding=dp(25),
            spacing=dp(15),
            md_bg_color=(0.95, 0.95, 0.98, 1)
        )

        self.titulo_lbl = MDLabel(
            text="FIM DE JOGO!",
            halign="center",
            font_style="H4",
            bold=True,
            theme_text_color="Custom",
            text_color=COR_PRIMARIA
        )

        self.resumo_box = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=0.6)

        self.acertos_lbl = MDLabel(text="Acertos: 0", halign="center", font_style="Subtitle1", theme_text_color="Custom", text_color=COR_TEXTO)
        self.erros_lbl = MDLabel(text="Erros: 0", halign="center", font_style="Subtitle1", theme_text_color="Custom", text_color=COR_TEXTO)
        self.tempo_lbl = MDLabel(text="Tempo: 00:00", halign="center", font_style="Subtitle1", theme_text_color="Custom", text_color=COR_TEXTO)
        self.nivel_lbl = MDLabel(text="Nível: -", halign="center", font_style="Subtitle2", theme_text_color="Hint")

        self.resumo_box.add_widget(self.acertos_lbl)
        self.resumo_box.add_widget(self.erros_lbl)
        self.resumo_box.add_widget(self.tempo_lbl)
        self.resumo_box.add_widget(self.nivel_lbl)

        btn_voltar = MDRaisedButton(
            text="MENU PRINCIPAL",
            size_hint_x=0.9,
            pos_hint={'center_x': 0.5},
            md_bg_color=COR_PRIMARIA,
            text_color=(1,1,1,1),
            on_release=self.voltar_menu
        )

        card.add_widget(self.titulo_lbl)
        card.add_widget(self.resumo_box)
        card.add_widget(Widget())
        card.add_widget(btn_voltar)

        layout.add_widget(card)
        self.add_widget(layout)

    def atualizar_stats(self, acertos, erros, tempo, dificuldade):
        self.acertos_lbl.text = f"Acertos: {acertos}"
        self.erros_lbl.text = f"Erros: {erros}"
        self.tempo_lbl.text = f"Tempo: {tempo}"
        self.nivel_lbl.text = f"Nível: {dificuldade.upper()}"

        if acertos >= 8:
            self.titulo_lbl.text = "EXCELENTE!"
            self.titulo_lbl.text_color = (0.2, 0.7, 0.2, 1)
        elif acertos >= 5:
            self.titulo_lbl.text = "MUITO BEM!"
            self.titulo_lbl.text_color = (1.0, 0.7, 0.2, 1)
        else:
            self.titulo_lbl.text = "PRATIQUE MAIS!"
            self.titulo_lbl.text_color = (0.5, 0.3, 0.7, 1)

    def voltar_menu(self, instance):
        self.manager.current = "jogar"