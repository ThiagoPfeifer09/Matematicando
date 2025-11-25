from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDIconButton
import random
from kivymd.uix.screen import MDScreen
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivy.uix.video import Video

CORES_BOTOES = [
    (1.0, 111/255, 64/255, 1),      # Laranja queimado vivo
    (0.36, 0.8, 0.96, 1),           # Azul claro brilhante
    (0.85, 0.53, 0.97, 1),          # Rosa roxo neon suave
    (0.59, 0.43, 0.91, 1),          # Roxo pastel vibrante
]

class CardBotao(MDCard):
    def __init__(self, texto, on_press_func, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = dp(60)
        self.elevation = 10
        self.radius = [20]
        self.md_bg_color = random.choice(CORES_BOTOES)
        self.texto = texto
        self.on_press_func = on_press_func
        self.padding = dp(10)
        self.ripple_behavior = True

        self.label = MDLabel(
            text=texto,
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.add_widget(self.label)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.on_press_func(self.texto)
            return True
        return super().on_touch_down(touch)


class AlgebraGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pergunta_atual = 1
        self.total_perguntas = 10
        self.acertos = 0
        self.erros = 0
        self.resposta_correta = None
        self.tempo_inicial = 30
        self.tempo_restante = 30
        self.timer_event = None

        self.layout = FloatLayout()
        self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg_image)

        self.back_button = MDIconButton(
            icon='arrow-left',
            pos_hint={'x': 0, 'top': 1},
            on_release=self.voltar,
            theme_text_color="Custom"
        )
        self.layout.add_widget(self.back_button)


        self.main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(25),
            size_hint=(1, 1)
        )

        self.top_layout = BoxLayout(size_hint_y=None, height=dp(40))
        self.progresso_label = MDLabel(
            text="Pergunta: 1/10",
            halign="left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size=dp(14)  # tamanho menor
        )

        self.placar_label = MDLabel(
            text="Acertos: 0  Erros: 0",
            halign="right",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size=dp(14)  # mesmo tamanho
        )
        self.top_layout.add_widget(self.progresso_label)
        self.top_layout.add_widget(self.placar_label)
        self.main_layout.add_widget(self.top_layout)

        self.timer_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(50))
        self.timer_label = MDLabel(
            text="Tempo: 00:30",
            halign="center",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1)
        )
        self.progress_bar = MDProgressBar(value=100, max=100)
        self.timer_layout.add_widget(self.timer_label)
        self.timer_layout.add_widget(self.progress_bar)
        self.main_layout.add_widget(self.timer_layout)

        self.equation_card = MDCard(
            size_hint=(1, 0.2),
            elevation=10,
            radius=[20],
            padding=dp(20),
            md_bg_color=(0.36, 0.8, 0.96, 1)
        )

        self.equation_label = MDLabel(
            text="2x = 24 - 14",
            font_style="H4",
            halign="center",
            theme_text_color="Custom",
            text_color=(53/255, 79/255, 117/255, 1)
        )
        self.equation_card.add_widget(self.equation_label)
        self.main_layout.add_widget(self.equation_card)

        self.resposta_card = MDCard(
            size_hint=(1, 0.15),
            elevation=6,
            padding=dp(15),
            radius=[15],
            md_bg_color=(0.85, 0.8, 1, 0.3)
        )

        self.resposta_label = MDLabel(
            text="x = _____",
            font_style="H5",
            halign="center",
            theme_text_color="Custom",
            text_color=(1,1,1,1)
        )
        self.resposta_card.add_widget(self.resposta_label)
        self.main_layout.add_widget(self.resposta_card)

        self.botoes_layout_1 = BoxLayout(spacing=dp(12), size_hint_y=None, height=dp(60))
        self.botoes_layout_2 = BoxLayout(spacing=dp(12), size_hint_y=None, height=dp(60))
        self.main_layout.add_widget(self.botoes_layout_1)
        self.main_layout.add_widget(self.botoes_layout_2)

        self.tempo_total = 0
        self.tempo_total_event = None
        self.dificuldade = "Fundamental"

        self.help_button = MDFloatingActionButton(
            icon="play-circle-outline",
            pos_hint={'right': 0.55, 'top': 0.97},
            on_release=self.mostrar_exemplo_animado
        )
        self.layout.add_widget(self.help_button)

        self.layout.add_widget(self.main_layout)
        self.add_widget(self.layout)


    def on_enter(self, *args):
        """Inicia o jogo e o timer apenas quando a tela entrar."""
        print("[DEBUG] Entrou na tela, iniciando jogo e timer.")
        self.reiniciar_jogo()

    def on_leave(self, *args):
        """Cancela todos os timers quando sair da tela."""
        print("[DEBUG] Saiu da tela, cancelando timers.")
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
        self.placar_label.text = f"Acertos: {self.acertos}  Erros: {self.erros}"

        # Garante que o layout principal está limpo e é reconstruído
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.top_layout)
        self.main_layout.add_widget(self.timer_layout)
        self.main_layout.add_widget(self.equation_card)
        self.main_layout.add_widget(self.resposta_card)
        self.main_layout.add_widget(self.botoes_layout_1)
        self.main_layout.add_widget(self.botoes_layout_2)

        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        if self.tempo_total_event:
            self.tempo_total_event.cancel()

        self.tempo_total_event = Clock.schedule_interval(self.atualizar_tempo_total, 1)
        Clock.schedule_once(lambda dt: self.gerar_equacao(), 0.3)

    def gerar_equacao(self):
        modelo = random.choice(["ax=b-c", "x+b=c", "x-b=c", "x/a=b", "ax+b=c", "a(x+b)=c"])
        def vd(facil, medio):
            return self.valor_por_dificuldade(facil, medio)

        if modelo == "ax=b-c":
            a = vd((1, 3), (2, 5))
            b = vd((10, 20), (20, 40))
            c = vd((1, b - 1), (1, b - 1))
            x = (b - c) // a
            self.equation_label.text = f"{a}x = {b} - {c}"
        elif modelo == "x+b=c":
            x = vd((1, 10), (5, 20))
            b = vd((1, 5), (5, 10))
            c = x + b
            self.equation_label.text = f"x + {b} = {c}"
        elif modelo == "x-b=c":
            x = vd((5, 15), (10, 30))
            b = vd((1, 4), (1, 9))
            c = x - b
            self.equation_label.text = f"x - {b} = {c}"
        elif modelo == "x/a=b":
            b = vd((1, 5), (2, 10))
            a = vd((1, 3), (1, 5))
            x = a * b
            self.equation_label.text = f"x ÷ {a} = {b}"
        elif modelo == "ax+b=c":
            a = vd((1, 2), (2, 5))
            x = vd((1, 5), (5, 10))
            b = vd((1, 5), (5, 10))
            c = a * x + b
            self.equation_label.text = f"{a}x + {b} = {c}"
        elif modelo == "a(x+b)=c":
            a = vd((1, 2), (2, 5))
            x = vd((1, 3), (3, 7))
            b = vd((1, 3), (3, 7))
            c = a * (x + b)
            self.equation_label.text = f"{a}(x + {b}) = {c}"

        self.resposta_correta = x
        self.resposta_label.text = "x = _____"

        # Gera opções
        opcoes = [x]
        while len(opcoes) < 4:
            fake = random.randint(x - 3, x + 3)
            if fake != x and fake not in opcoes and fake >= 0:
                opcoes.append(fake)
        random.shuffle(opcoes)

        # Limpa e adiciona os botões
        self.botoes_layout_1.clear_widgets()
        self.botoes_layout_2.clear_widgets()

        for i, valor in enumerate(opcoes):
            btn = CardBotao(
                texto=str(valor),
                on_press_func=self.verificar_resposta
            )
            if i < 2:
                self.botoes_layout_1.add_widget(btn)
            else:
                self.botoes_layout_2.add_widget(btn)

        # Reset do cronômetro e barra
        self.tempo_restante = self.tempo_inicial
        minutos, segundos = divmod(self.tempo_restante, 60)
        self.timer_label.text = f"Tempo: {minutos:02}:{segundos:02}"
        self.progress_bar.value = 100
        self.progress_bar.color = (0, 1, 0, 1)

        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        self.timer_event = Clock.schedule_interval(self.atualizar_timer, 1)

        # Atualiza progresso
        self.progresso_label.text = f"Pergunta: {self.pergunta_atual}/{self.total_perguntas}"

    def verificar_resposta(self, resposta_str):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        try:
            resposta_selecionada = int(resposta_str)
        except ValueError:
            resposta_selecionada = None

        if resposta_selecionada == self.resposta_correta:
            self.acertos += 1
            self.resposta_label.text = "Acertou! ✔️"
            self.resposta_card.md_bg_color = (0.2, 0.8, 0.2, 1)
        else:
            self.erros += 1
            self.resposta_label.text = f"Errou! ❌ (Era {self.resposta_correta})"
            self.resposta_card.md_bg_color = (0.9, 0.3, 0.3, 1)

        self.placar_label.text = f"Acertos: {self.acertos}  Erros: {self.erros}"
        self.pergunta_atual += 1

        if self.pergunta_atual > self.total_perguntas:
            Clock.schedule_once(lambda dt: self.encerrar_jogo(), 1.5)
        else:
            Clock.schedule_once(lambda dt: self.gerar_equacao(), 1.5)


    def contar_erro_por_tempo(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        self.erros += 1
        self.resposta_label.text = f"Tempo esgotado! ❌"
        self.resposta_card.md_bg_color = (0.9, 0.3, 0.3, 1)
        self.placar_label.text = f"Acertos: {self.acertos}  Erros: {self.erros}"
        self.pergunta_atual += 1

        if self.pergunta_atual > self.total_perguntas:
            Clock.schedule_once(lambda dt: self.encerrar_jogo(), 1.5)
        else:
            Clock.schedule_once(lambda dt: self.gerar_equacao(), 1.5)



    def encerrar_jogo(self):
        if self.tempo_total_event:
            self.tempo_total_event.cancel()

        minutos, segundos = divmod(int(self.tempo_total), 60)
        tempo_formatado = f"{minutos:02}:{segundos:02}"


        fim_screen = self.manager.get_screen("fim_algebra")
        fim_screen.atualizar_stats(
            acertos=self.acertos,
            erros=self.erros,
            tempo_total=tempo_formatado,
            dificuldade=self.dificuldade
        )
        self.manager.current = "fim_algebra"

    def atualizar_timer(self, dt):
        self.tempo_restante -= dt
        if self.tempo_restante < 0: self.tempo_restante = 0
        minutos, segundos = divmod(int(self.tempo_restante), 60)
        self.timer_label.text = f"Tempo: {minutos:02}:{segundos:02}"

        if self.tempo_inicial > 0:
            percentual = (self.tempo_restante / self.tempo_inicial) * 100
        else:
            percentual = 0
        self.progress_bar.value = percentual

        if self.tempo_restante <= 5: self.progress_bar.color = [1, 0, 0, 1]
        elif percentual <= 50: self.progress_bar.color = [1, 1, 0, 1]
        else: self.progress_bar.color = [0, 1, 0, 1]
        print(f"[DEBUG] Tempo restante: {self.tempo_restante}")

        if self.tempo_restante == 0: self.contar_erro_por_tempo()

    def atualizar_tempo_total(self, dt):
        self.tempo_total += dt

    def definir_dificuldade(self, dificuldade):
        self.dificuldade = dificuldade

    def _calcular_tempo_da_pergunta(self):
        """Calcula o tempo para a pergunta atual com base na dificuldade e em degraus."""
        if self.dificuldade.lower() == "medio":
            # Lógica de tempo em degraus para o nível Médio
            pergunta = self.pergunta_atual

            if pergunta >= 10:
                # Na pergunta 10, o tempo é de 10 segundos
                return 10
            elif pergunta >= 8:
                # Nas perguntas 8 e 9, o tempo é de 15 segundos
                return 15
            elif pergunta >= 5:
                # Nas perguntas 5, 6 e 7, o tempo é de 20 segundos
                return 20
            else:
                # Nas perguntas 1 a 4, o tempo é de 25 segundos
                return 25
        else:
            # Dificuldade Fundamental continua com tempo fixo
            return 30

    def valor_por_dificuldade(self, facil_range, medio_range):
        if self.dificuldade.lower() == "fundamental": return random.randint(*facil_range)
        else: return random.randint(*medio_range)

    def voltar(self, instance):
        if self.timer_event: self.timer_event.cancel()
        if self.tempo_total_event: self.tempo_total_event.cancel()
        self.manager.current = "jogar" # Assumindo que a tela de menu se chama 'jogar'

    def _resume_game_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        self.timer_event = Clock.schedule_interval(self.atualizar_timer, 1)

    def mostrar_exemplo_animado(self, *args):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        video_widget = Video(
            source="eq1.mp4",
            state='play',
            allow_stretch=True,
            keep_ratio=True,
            volume=0,
            size_hint=(1, None),
            height=dp(300)
        )
        layout.add_widget(video_widget)

        modal = ModalView(
            size_hint=(None, None),
            size=(dp(520), dp(400)),
            auto_dismiss=False
        )
        modal.add_widget(layout)

        def fechar_modal(*_):
            modal.dismiss()
            # Após o fechamento, aguarde 0.1s e então pare o vídeo e retome o cronômetro
            Clock.schedule_once(lambda dt: (
                setattr(video_widget, 'state', 'stop'),
                self._resume_game_timer()
            ), 0.1)

        btn_fechar = MDRaisedButton(
            text="FECHAR",
            pos_hint={'center_x': 0.5},
            on_release=fechar_modal
        )
        layout.add_widget(btn_fechar)

        modal.open()


class TelaFimAlgebra(MDScreen):
    """Tela de final de jogo, mostrando as estatísticas."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "fim_algebra"

        layout = FloatLayout()
        self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.bg_image)

        # Título
        self.title_label = MDLabel(
            text="Fim de Jogo!",
            font_style="H3",
            halign="center",
            pos_hint={"center_x": 0.5, "top": 0.9},
            theme_text_color="Custom"
        )
        layout.add_widget(self.title_label)

        # Card de estatísticas
        self.card_stats = MDCard(
            size_hint=(0.8, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            elevation=10,
            padding=dp(25),
            radius=[20],
            orientation="vertical",
            spacing=dp(15)
        )

        self.acertos_label = MDLabel(text="Acertos: ", font_style="H6", halign="center")
        self.erros_label = MDLabel(text="Erros: ", font_style="H6", halign="center")
        self.tempo_label = MDLabel(text="Tempo Total: ", font_style="H6", halign="center")
        self.dificuldade_label = MDLabel(text="Dificuldade: ", font_style="H6", halign="center")

        self.card_stats.add_widget(self.acertos_label)
        self.card_stats.add_widget(self.erros_label)
        self.card_stats.add_widget(self.tempo_label)
        self.card_stats.add_widget(self.dificuldade_label)
        layout.add_widget(self.card_stats)

        # Botão para voltar ao menu
        self.menu_button = MDRaisedButton(
            text="Voltar ao Menu",
            font_size="18sp",
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            size_hint=(0.6, 0.08),
            on_release=self.voltar_menu
        )
        layout.add_widget(self.menu_button)
        self.add_widget(layout)


    def atualizar_stats(self, acertos, erros, tempo_total, dificuldade):
        self.acertos_label.text = f"✅ Acertos: {acertos}"
        self.erros_label.text = f"❌ Erros: {erros}"
        self.tempo_label.text = f"⏱️ Tempo Total: {tempo_total}"
        self.dificuldade_label.text = f"📊 Dificuldade: {dificuldade.capitalize()}"

    def voltar_menu(self, instance):
        self.manager.current = "jogar_p"