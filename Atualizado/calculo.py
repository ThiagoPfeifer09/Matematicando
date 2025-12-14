from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.properties import StringProperty
import random

class calculoI(MDScreen):
    # Propriedade declarada para evitar erros no ScreenManager
    dificuldade = StringProperty("primario")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer = 0
        self.running = False
        self.modo = "normal"
        self.operacao = "Soma"
        self.rodadas = 5

        # Variáveis de Controle
        self.nivel_atual = 1
        self.nivel_max = 4
        self.nivel_selecionado = 1
        self.tudo_desbloqueado = False

        # Pontuação
        self.pontos_nivel = 0
        self.acertos_total = 0
        self.erros_total = 0

        # --- LAYOUT PRINCIPAL ---
        layout = FloatLayout()
        try:
            self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
            layout.add_widget(self.bg_image)
        except:
            pass

        # --- CABEÇALHO ---
        layout.add_widget(MDIconButton(
            icon="arrow-left",
            pos_hint={"x": 0.02, "top": 0.98},
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            on_release=self.ir_para_niveis
        ))

        layout.add_widget(Label(
            text="MATEMATICANDO",
            font_size="24sp",
            bold=True,
            color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.95}
        ))

        # ==========================================================
        # --- ÁREA DE ESTATÍSTICAS (CORRIGIDA - NÃO CORTA MAIS) ---
        # ==========================================================

        def criar_linha_stat(texto, y_pos, icon_name, icon_color):
            # AJUSTE: Empurrei mais para a direita (x: 0.05 e x: 0.12)
            icon = MDIcon(
                icon=icon_name,
                pos_hint={"center_x": 0.06, "center_y": y_pos},
                theme_text_color="Custom",
                text_color=icon_color,
                font_size="24sp"
            )
            lbl = Label(
                text=texto,
                font_size="15sp",
                bold=True,
                color=(0, 0, 0, 1),
                halign="left",
                # Garante que o texto comece depois do ícone sem cortar
                pos_hint={"x": 0.12, "center_y": y_pos},
                size_hint=(0.4, None),
                height=30
            )
            lbl.bind(size=lbl.setter('text_size'))
            return icon, lbl

        # Posicionamento Vertical das Stats
        self.icon_score, self.lbl_score_val = criar_linha_stat(
            "Pontos: 0", 0.88, "star", (0.9, 0.7, 0, 1)
        )
        layout.add_widget(self.icon_score)
        layout.add_widget(self.lbl_score_val)

        self.icon_acerto, self.lbl_acerto_val = criar_linha_stat(
            "Acertos: 0", 0.83, "check-circle", (0, 0.6, 0, 1)
        )
        layout.add_widget(self.icon_acerto)
        layout.add_widget(self.lbl_acerto_val)

        self.icon_erro, self.lbl_erro_val = criar_linha_stat(
            "Erros: 0", 0.78, "close-circle", (0.8, 0, 0, 1)
        )
        layout.add_widget(self.icon_erro)
        layout.add_widget(self.lbl_erro_val)

        # ==========================================================
        # --- ÁREA DA CONTA (POSICIONAMENTO E TAMANHO) ---
        # ==========================================================
        self.layout_conta = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            width=dp(240),
            height=dp(240),
            pos_hint={"center_x": 0.5, "center_y": 0.7}, #
            spacing=dp(2)
        )

        self.lbl_num1 = Label(
            text="",
            font_size="55sp",
            bold=True,
            color=(0,0,0,1),
            halign="right",
            valign="bottom",
            size_hint_y=0.45
        )
        self.lbl_num1.bind(size=self.lbl_num1.setter('text_size'))
        self.layout_conta.add_widget(self.lbl_num1)

        # 2. Operador e Último Número
        line_2_layout = BoxLayout(orientation='horizontal', size_hint_y=0.25)
        self.lbl_operador = Label(text="+", font_size="40sp", bold=True, color=(0,0,0,1), size_hint_x=0.3, halign="left", valign="center")
        self.lbl_operador.bind(size=self.lbl_operador.setter('text_size'))

        self.lbl_num2 = Label(text="", font_size="55sp", bold=True, color=(0,0,0,1), size_hint_x=0.7, halign="right", valign="center")
        self.lbl_num2.bind(size=self.lbl_num2.setter('text_size'))

        line_2_layout.add_widget(self.lbl_operador)
        line_2_layout.add_widget(self.lbl_num2)
        self.layout_conta.add_widget(line_2_layout)

        # 3. Linha Separadora
        self.linha_separadora = Widget(size_hint_y=None, height=dp(4))
        with self.linha_separadora.canvas:
            Color(0, 0, 0, 1)
            self.rect_linha = Rectangle(pos=self.linha_separadora.pos, size=self.linha_separadora.size)
            self.linha_separadora.bind(pos=self.atualiza_linha, size=self.atualiza_linha)
        self.layout_conta.add_widget(self.linha_separadora)

        # 4. Input e Botão OK
        input_row = BoxLayout(orientation='horizontal', size_hint_y=0.30, spacing=dp(5))

        self.answer_input = MDTextField(
            hint_text="?",
            halign="center",
            font_size="35sp",
            multiline=False,
            mode="rectangle",
            line_color_normal=(0,0,0,0), line_color_focus=(0,0,0,0),
            text_color_normal=(0,0,0,1), text_color_focus=(0,0,0,1),
            size_hint_x=0.65
        )
        self.answer_input.bind(text=self.check_responder_button)
        input_row.add_widget(self.answer_input)

        self.responder_button = MDRaisedButton(
            text="OK",
            size_hint=(0.35, 0.9),
            font_size="18sp",
            pos_hint={"center_y": 0.5},
            md_bg_color=(0, 0, 0.8, 1),
            text_color=(1, 1, 1, 1),
            elevation=2,
            on_release=self.verifica_resposta,
        )
        self.responder_button.disabled = True
        input_row.add_widget(self.responder_button)

        self.layout_conta.add_widget(input_row)
        layout.add_widget(self.layout_conta)

        # ==========================================================
        # --- TECLADO E NÍVEIS (MANTIDO CONFORME SUA APROVAÇÃO) ---
        # ==========================================================

        col_x_teclado = [0.15, 0.40, 0.65]
        col_x_nivel = 0.88

        base_y_teclado = 0.15
        gap_y = 0.08

        btn_num_size = (0.16, None)
        btn_num_height = dp(45)
        num_bg_color = (0.2, 0.6, 0.8, 1)

        rows_y = [
            base_y_teclado,
            base_y_teclado + gap_y,
            base_y_teclado + gap_y*2,
            base_y_teclado + gap_y*3,
            base_y_teclado + gap_y*4
        ]

        # 1. Label Nível
        layout.add_widget(Label(
            text="Nível",
            font_size="16sp", color=(0,0,0,1), bold=True,
            pos_hint={"center_x": col_x_nivel, "center_y": rows_y[4]}
        ))

        # 2. Botões de Nível
        self.nivel_botoes = {}
        nivel_cores = [(0, 0.6, 0, 1), (0, 0, 0.8, 1), (0.6, 0, 0.6, 1), (0.5, 0.5, 0.5, 1)]
        indices_visuais = [3, 2, 1, 0]

        for i, (level, color) in enumerate(zip(range(1, self.nivel_max + 1), nivel_cores)):
            row_idx = indices_visuais[i]
            btn = MDRaisedButton(
                text=f"{level}",
                size_hint=(0.12, None),
                height=btn_num_height,
                pos_hint={"center_x": col_x_nivel, "center_y": rows_y[row_idx]},
                text_color=(0, 0, 0, 1) if level != self.nivel_atual else (1,1,1,1),
                on_release=lambda _, lvl=level: self.inicia_nivel(lvl),
            )
            btn.original_color = color
            if level == self.nivel_atual:
                btn.disabled = False
                btn.md_bg_color = btn.original_color
                btn.text_color = (1, 1, 1, 1)
            else:
                btn.disabled = True
                btn.md_bg_color = (0.8, 0.8, 0.8, 1)
                btn.text_color = (0, 0, 0, 0.5)
            self.nivel_botoes[level] = btn
            layout.add_widget(btn)

        # 3. Teclado Numérico
        mapa_teclado = [
            (1, 0, 2), (2, 1, 2), (3, 2, 2),
            (4, 0, 3), (5, 1, 3), (6, 2, 3),
            (7, 0, 4), (8, 1, 4), (9, 2, 4),
            (0, 1, 1)
        ]

        for numero, col_idx, row_idx in mapa_teclado:
            layout.add_widget(MDRaisedButton(
                text=str(numero),
                size_hint=btn_num_size, height=btn_num_height,
                pos_hint={"center_x": col_x_teclado[col_idx], "center_y": rows_y[row_idx]},
                md_bg_color=num_bg_color, text_color=(0, 0, 0, 1), font_size="26sp",
                on_release=lambda _, nmb=numero: self.instancia_numero(nmb),
            ))

        # Botões Especiais
        layout.add_widget(MDRaisedButton(
            text="-", size_hint=btn_num_size, height=btn_num_height,
            pos_hint={"center_x": col_x_teclado[0], "center_y": rows_y[1]},
            md_bg_color=num_bg_color, text_color=(0, 0, 0, 1), font_size="28sp",
            on_release=self.minus_insert,
        ))
        layout.add_widget(MDRaisedButton(
            text=",", size_hint=btn_num_size, height=btn_num_height,
            pos_hint={"center_x": col_x_teclado[2], "center_y": rows_y[1]},
            md_bg_color=num_bg_color, text_color=(0, 0, 0, 1), font_size="28sp",
            on_release=self.point_insert,
        ))

        # Botões Ação
        layout.add_widget(MDRaisedButton(
            text="Apagar", size_hint=(0.20, None), height=dp(35),
            pos_hint={"center_x": col_x_teclado[0], "center_y": rows_y[0]},
            font_size="14sp", md_bg_color=(0.8, 0.4, 0.4, 1), text_color=(0, 0, 0, 1),
            on_release=self.apagar_numero,
        ))
        layout.add_widget(MDRaisedButton(
            text="Limpar", size_hint=(0.20, None), height=dp(35),
            pos_hint={"center_x": col_x_teclado[2], "center_y": rows_y[0]},
            font_size="14sp", md_bg_color=(0.8, 0.4, 0.4, 1), text_color=(0, 0, 0, 1),
            on_release=self.limpar_resposta,
        ))

        # --- TIMER E CONTROLES ---
        self.timer_label = Label(
            text="00:00:00", font_size="28sp", color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.08},
        )
        layout.add_widget(self.timer_label)

        control_buttons = [
            ("Parar", 0.30, self.pause_timer, (0.6, 0, 0.6, 1)),
            ("Reiniciar", 0.70, self.reset_timer, (0, 0, 0.8, 1)),
        ]
        for text, pos_x, callback, color in control_buttons:
            layout.add_widget(MDRaisedButton(
                text=text, size_hint=(0.25, None), height=dp(35), font_size="14sp",
                pos_hint={"center_x": pos_x, "center_y": 0.03},
                md_bg_color=color, text_color=(1, 1, 1, 1),
                on_release=callback,
            ))

        self.add_widget(layout)

    # --- MÉTODOS DE LÓGICA ---
    def confirma_rodadas(self, rodadas_value):
        if rodadas_value > 0: self.rodadas = rodadas_value
        else: self.rodadas = 5

    def escolha_modo(self, modo):
        self.modo = modo

    def atualiza_linha(self, instance, value):
        self.rect_linha.pos = instance.pos
        self.rect_linha.size = instance.size

    def atualizar_display_conta(self, texto_num1, texto_num2, operador_simbolo, eh_tres_termos=False):
        if eh_tres_termos:
            # AJUSTE: Fonte reduzida para 35sp quando houver 3 termos
            self.lbl_num1.font_size = "35sp"
            self.lbl_num1.text = texto_num1
        else:
            self.lbl_num1.font_size = "55sp"
            self.lbl_num1.text = texto_num1

        self.lbl_num2.text = texto_num2
        self.lbl_operador.text = operador_simbolo

    def minus_insert(self, instance):
        if len(self.answer_input.text) < 5: self.answer_input.text += "-"

    def point_insert(self, instance):
        if len(self.answer_input.text) < 5: self.answer_input.text += ","

    def check_responder_button(self, *args):
        if getattr(self, 'nivel_selecionado', None) and self.answer_input.text.strip():
            self.responder_button.disabled = False
            self.responder_button.md_bg_color = (0, 0, 0.8, 1)
        else:
            self.responder_button.disabled = True
            self.responder_button.md_bg_color = (0.5, 0.5, 0.5, 1)

    def instancia_numero(self, numero):
        if len(self.answer_input.text) < 5: self.answer_input.text += str(numero)

    def apagar_numero(self, instance):
        self.answer_input.text = self.answer_input.text[:-1]

    def limpar_resposta(self, instance):
        self.answer_input.text = ""

    def define_dificul(self, dificuldade):
        self.dificuldade = dificuldade
        self.nivel_atual = 1
        self.cria_questao()

    def inicia_nivel(self, level):
        if level != self.nivel_atual: return
        self.nivel_selecionado = level
        self.pontos_nivel = 0
        self.atualiza_labels_stats()
        self.answer_input.hint_text = "..."
        Clock.schedule_once(self.comecar_nivel, 1)

    def comecar_nivel(self, dt):
        self.answer_input.hint_text = "?"
        self.start_timer()
        self.cria_questao()

    def cria_questao(self):
        dificuldades_especificas = ["primario", "fundamental", "medio"]
        if self.dificuldade in dificuldades_especificas: self.cria_questaopersonalizada()
        elif self.modo == "normal": self.cria_questaonormal()
        else: self.cria_questaopersonalizada()

    def cria_questaonormal(self):
        min_v, max_v = 1, 10
        num1 = random.randint(min_v, max_v)
        num2 = random.randint(min_v, max_v or 1)
        self.montar_conta(num1, num2)

    def cria_questaopersonalizada(self):
        min_v, max_v = 1, 10
        if self.dificuldade == "primario": max_v = 20
        elif self.dificuldade == "fundamental": max_v = 100
        elif self.dificuldade == "medio": max_v = 999

        usar_3_termos = False
        if self.dificuldade == "medio" and self.nivel_atual >= 3: usar_3_termos = True
        elif self.dificuldade == "fundamental" and self.nivel_atual == 4: usar_3_termos = True

        n1 = random.randint(min_v, max_v)
        n2 = random.randint(min_v, max_v)
        n3 = None
        if usar_3_termos:
            n3 = random.randint(min_v, max_v)
            self.montar_conta(n1, n2, n3)
        else:
            self.montar_conta(n1, n2)

    def montar_conta(self, n1, n2, n3=None):
        simbolo = "+"
        op = self.operacao.capitalize() if self.operacao else "Soma"
        if op.startswith("Mult"): op = "Multiplicacao"
        if op.startswith("Div"): op = "Divisao"
        if op.startswith("Subt"): op = "Subtracao"

        if op == "Divisao" and n3 is not None: n3 = None

        if n3 is not None:
            if op == "Soma":
                self.answer = n1 + n2 + n3
                simbolo = "+"
            elif op == "Subtracao":
                if self.dificuldade != "medio":
                    vals = sorted([n1, n2, n3], reverse=True)
                    n1, n2, n3 = vals[0], vals[1], vals[2]
                self.answer = n1 - n2 - n3
                simbolo = "-"
            elif op == "Multiplicacao":
                if n1 > 12: n1 = random.randint(1, 10)
                if n2 > 12: n2 = random.randint(1, 10)
                if n3 > 12: n3 = random.randint(1, 10)
                self.answer = n1 * n2 * n3
                simbolo = "x"

            txt_num1 = f"{n1}\n{n2}"
            txt_num2 = str(n3)
            self.atualizar_display_conta(txt_num1, txt_num2, simbolo, eh_tres_termos=True)
        else:
            if op == "Soma":
                self.answer = n1 + n2
                simbolo = "+"
            elif op == "Subtracao":
                if self.dificuldade in ["primario", "fundamental"] and n2 > n1:
                    n1, n2 = n2, n1
                self.answer = n1 - n2
                simbolo = "-"
            elif op == "Multiplicacao":
                self.answer = n1 * n2
                simbolo = "x"
            elif op == "Divisao":
                if n2 == 0: n2 = 1
                n1 = n1 * n2
                self.answer = n1 // n2
                simbolo = "÷"
            self.atualizar_display_conta(str(n1), str(n2), simbolo, eh_tres_termos=False)

    def define_operacao(self, operacao):
        validas = ["soma", "subtracao", "multiplicacao", "divisao"]
        if operacao.lower() in validas: self.operacao = operacao.capitalize()

    def verifica_resposta(self, *args):
        user_answer = self.answer_input.text.replace(',', '.')
        try:
            val = float(user_answer)
            if abs(val - self.answer) < 0.01:
                self.acertos_total += 1
                self.pontos_nivel += 1
            else:
                self.erros_total += 1
                self.pontos_nivel = max(0, self.pontos_nivel - 1)
        except ValueError:
            self.answer_input.text = ""
            return

        self.answer_input.text = ""
        self.atualiza_labels_stats()

        meta_pontos = self.rodadas if self.rodadas > 0 else 5
        if self.pontos_nivel >= meta_pontos:
            self.pause_timer()
            if self.nivel_atual < self.nivel_max:
                btn_atual = self.nivel_botoes[self.nivel_atual]
                btn_atual.disabled = True
                btn_atual.md_bg_color = (0.8, 0.8, 0.8, 1)
                btn_atual.text_color = (0, 0, 0, 0.5)

                self.nivel_atual += 1
                self.pontos_nivel = 0

                next_btn = self.nivel_botoes[self.nivel_atual]
                next_btn.disabled = False
                next_btn.md_bg_color = next_btn.original_color
                next_btn.text_color = (1, 1, 1, 1)

                self.disparar_comemoracao()
                self.atualiza_labels_stats()
                Clock.schedule_once(lambda dt: self.inicia_nivel(self.nivel_atual), 2)
            else:
                self.ir_para_tela_fim_de_jogo()
        else:
            self.cria_questao()

    def atualiza_labels_stats(self):
        self.lbl_score_val.text = f"Pontos Nível: {self.pontos_nivel}"
        self.lbl_acerto_val.text = f"Acertos: {self.acertos_total}"
        self.lbl_erro_val.text = f"Erros: {self.erros_total}"

    def start_timer(self, *args):
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.att_timer, 1)

    def pause_timer(self, *args):
        self.running = False
        Clock.unschedule(self.att_timer)

    def reset_timer(self, *args):
        self.pause_timer()
        self.timer = 0
        self.timer_label.text = "00:00:00"

    def att_timer(self, dt):
        self.timer += 1
        m, s = divmod(self.timer, 60)
        h, m = divmod(m, 60)
        self.timer_label.text = f"{h:02}:{m:02}:{s:02}"

    def ir_para_niveis(self, instance):
        if self.manager.has_screen("escolha"): self.manager.current = "escolha"
        elif self.manager.has_screen("jogar"): self.manager.current = "jogar"
        else: print("Tela anterior não encontrada no Manager")

    def disparar_comemoracao(self):
        layout = self.children[0]
        try:
            for _ in range(25):
                b = Image(source='balao.png', size_hint=(None,None), size=(dp(random.randint(50,80)), dp(random.randint(50,80))), opacity=0.8)
                b.color = (random.random(), random.random(), random.random(), 1)
                b.x = random.uniform(0, self.width - b.width)
                b.y = -dp(100)
                layout.add_widget(b)
                anim = Animation(pos=(b.x + random.uniform(-dp(100), dp(100)), self.height + dp(50)), opacity=0, duration=random.uniform(2.5, 5.0), t='out_quad')
                anim.bind(on_complete=lambda a, w: layout.remove_widget(w))
                anim.start(b)
        except: pass

    def ir_para_tela_fim_de_jogo(self):
        if self.manager.has_screen("fim_de_jogo"):
            fim = self.manager.get_screen("fim_de_jogo")
            fim.atualizar_stats(self.timer_label.text, self.operacao, self.acertos_total + self.erros_total, self.acertos_total, self.erros_total, self.dificuldade)
            self.manager.current = "fim_de_jogo"

    def reiniciar_jogo(self):
        self.reset_timer()
        self.operacao = "Soma"
        self.pontos_nivel = 0
        self.acertos_total = 0
        self.erros_total = 0
        self.nivel_atual = 1
        self.nivel_selecionado = 1
        self.lbl_num1.text = ""
        self.lbl_num2.text = ""
        self.lbl_operador.text = ""
        self.answer_input.text = ""
        self.atualiza_labels_stats()
        for lvl, btn in self.nivel_botoes.items():
            if lvl == 1:
                btn.disabled = False
                btn.md_bg_color = btn.original_color
                btn.text_color = (1, 1, 1, 1)
            else:
                btn.disabled = True
                btn.md_bg_color = (0.8, 0.8, 0.8, 1)
                btn.text_color = (0, 0, 0, 0.5)
        self.responder_button.disabled = True

class TelaFimDeJogo(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "fim_de_jogo"
        layout = FloatLayout()
        try:
            self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
            layout.add_widget(self.bg_image)
        except:
            pass
        layout.add_widget(Label(text="Parabéns você concluiu o jogo!", font_size=50, bold=True, pos_hint={"center_x": 0.5, "center_y": 0.9}))
        self.nome_input = MDTextField(hint_text="Digite seu nome", pos_hint={"center_x": 0.5, "center_y": 0.78}, size_hint_x=0.6)
        layout.add_widget(self.nome_input)
        card = MDCard(size_hint=(0.6, 0.5), pos_hint={"center_x": 0.5, "center_y": 0.5}, md_bg_color=(0, 0, 0, 0.3), elevation=0, radius=[15, 15, 15, 15], padding=dp(20), spacing=dp(10))
        stats_layout = BoxLayout(orientation='vertical', spacing=dp(15))
        self.tempo_label = Label(text="Tempo: ", font_size=24)
        self.operacao_label = Label(text="Operação: ", font_size=24)
        self.rodadas_label = Label(text="Total de Questões: ", font_size=24)
        self.acertos_label = Label(text="Acertos: ", font_size=24)
        self.erros_label = Label(text="Erros: ", font_size=24)
        self.nivel_label = Label(text="Nível: ", font_size=24)
        stats_layout.add_widget(self.nivel_label)
        stats_layout.add_widget(self.tempo_label)
        stats_layout.add_widget(self.operacao_label)
        stats_layout.add_widget(self.rodadas_label)
        stats_layout.add_widget(self.acertos_label)
        stats_layout.add_widget(self.erros_label)
        card.add_widget(stats_layout)
        layout.add_widget(card)
        layout.add_widget(MDRaisedButton(text="Voltar ao Menu", font_size="24sp", pos_hint={"center_x": 0.5, "center_y": 0.15}, size_hint=(0.3, 0.1), on_release=self.enviar_dados_e_voltar))
        self.add_widget(layout)

    def atualizar_stats(self, tempo, operacao, rodadas, acertos, erros, nivel):
        self.tempo_label.text = f"Tempo Total: {tempo}"
        self.operacao_label.text = f"Operação: {operacao}"
        self.rodadas_label.text = f"Total de Questões: {rodadas}"
        self.acertos_label.text = f"Acertos Totais: {acertos}"
        self.erros_label.text = f"Erros Totais: {erros}"
        self.nivel_label.text = f"Nível: {nivel.capitalize()}"

    def enviar_dados_e_voltar(self, instance):
        nome = self.nome_input.text.strip()
        if not nome: return
        tempo = self.tempo_label.text.replace("Tempo Total: ", "")
        operacao = self.operacao_label.text.replace("Operação: ", "")
        rodadas = self.rodadas_label.text.replace("Total de Questões: ", "")
        acertos = self.acertos_label.text.replace("Acertos Totais: ", "")
        erros = self.erros_label.text.replace("Erros Totais: ", "")
        nivel = self.nivel_label.text.replace("Nível: ", "")
        try:
            from enviar_dados import enviar_resultado_googleforms
            enviar_resultado_googleforms(nome, tempo, operacao, rodadas, acertos, erros, nivel)
        except ImportError:
            print("Módulo de envio não encontrado")

        if self.manager.has_screen("inicial"):
            self.manager.current = "inicial"
        elif self.manager.has_screen("menu"):
            self.manager.current = "menu"
        else:
            self.manager.current = self.manager.screen_names[0]