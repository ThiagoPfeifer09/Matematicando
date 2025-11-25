from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.metrics import dp
import random
from kivy.uix.image import Image
from kivymd.uix.button import MDIconButton
from kivy.app import App
from kivymd.uix.textfield import MDTextField


class calculoI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer = 0
        self.running = False
        self.modo = "normal"
        self.operacao = "Soma"  # Operação padrão
        self.rodadas = 0  # Número total de rodadas
        self.rodada_atual = 0  # Rodada atual
        self.nivel_atual = 1  # Nível atual
        self.resp_correta = 0  # Contador de acertos
        self.resp_correta_total = 0
        self.resp_errada = 0  # Contador de erros
        self.resp_errada_total = 0
        self.dialog = None
        self.nivel_selecionado = self.nivel_atual
        self.nivel_max = 4  # Total de níveis
        self.dificuldade = "primario"  # Padrão para primário (mais fácil)
        self.tudo_desbloqueado = False  # Indica se tudo está desbloqueado

        # Layout principal
        layout = FloatLayout()
        self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.bg_image)



        # Título
        layout.add_widget(Label(text="MATEMATICANDO", font_size=40, bold=True,
                                pos_hint={"center_x": 0.5, "center_y": 0.95}))

        self.question_label = Label(
            text="Escolha um nível para começar!",
            height=50,
            size_hint=(0.4, None),
            font_size="30sp",
            pos_hint={"center_x": 0.5, "center_y": 0.8875},
        )
        layout.add_widget(self.question_label)

        self.answer_input = MDTextField(
            hint_text="Digite a resposta",
            size_hint=(1, 1),
            halign="center",
            font_size="36sp",
            line_color_normal=(1, 1, 1, 0.3),
            line_color_focus=(1, 1, 1, 0.8),
            mode="rectangle",
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            multiline=False,
        )

        card = MDCard(
            size_hint=(0.5, None),
            height=100,
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            md_bg_color=(0, 0, 0, 0.2),
            elevation=0,
            radius=[10, 10, 10, 10],
        )
        card_layout = BoxLayout(orientation="vertical", padding=10, spacing=5)
        card_layout.add_widget(self.answer_input)
        card.add_widget(card_layout)
        layout.add_widget(card)

        self.score_label = Label(
            text="Pontuação: 0/",
            font_size="24sp",
            pos_hint={"center_x": 0.375, "center_y": 0.7},
        )
        layout.add_widget(self.score_label)

        #Botão de responder
        self.responder_button = MDRaisedButton(
            text="Responder",
            size_hint=(0.05, 0.04),
            font_size="24sp",
            pos_hint={"center_x": 0.75, "center_y": 0.6},
            md_bg_color=(0, 0, 0.8, 1),
            text_color=(1, 1, 1, 1),
            on_release=self.verifica_resposta,
        )
        self.responder_button.disabled = True  # Começa desativado
        layout.add_widget(self.responder_button)

        self.answer_input.bind(text=self.check_responder_button)

        layout.add_widget(
            Label(
                text="Níveis:",
                font_size=35,
                pos_hint={"center_x": 0.75, "center_y": 0.5},
            )
        )

        # Botão de voltar (Retorna para o nível a tela de selecionar os níveis)
        layout.add_widget(
            MDRaisedButton(
                text="Voltar",
                size_hint=(0.035, 0.04),
                pos_hint={"center_x": 0.12, "center_y": 0.6},
                font_size="14sp",
                md_bg_color=(0.5, 0.5, 0.5, 1),
                text_color=(1, 1, 1, 1),
                on_release=self.ir_para_niveis,
            )
        )

        self.nivel_botoes = {}
        self.numero_botoes_esquerda = {}
        self.numero_botoes_centro = {}
        self.numero_botoes_direita = {}
        nivel_cores = [(0, 0.6, 0, 1), (0, 0, 0.8, 1), (0.6, 0, 0.6, 1), (0.5, 0.5, 0.5, 1)]

        for level, pos_y, color in zip(range(1, self.nivel_max + 1), [0.425, 0.35, 0.275, 0.2], nivel_cores):
            btn = MDRaisedButton(
                text=f"Nível {level}",
                size_hint=(0.07, 0.04),
                font_size="18sp",
                pos_hint={"center_x": 0.75, "center_y": pos_y},
                text_color=(1, 1, 1, 1),
                on_release=lambda _, lvl=level: self.inicia_nivel(lvl),
            )
            btn.original_color = color  # Salva a cor original

            if level == self.nivel_atual:
                btn.disabled = False
                btn.md_bg_color = btn.original_color
            else:
                btn.disabled = True
                btn.md_bg_color = (0.7, 0.7, 0.7, 1)  # Cinza

            self.nivel_botoes[level] = btn
            layout.add_widget(btn)

        valores_esquerda = [1,4,7]
        valores_centro = [0,2,5,8]
        valores_direita = [3,6,9]

        for numberl, pos_y, color in zip(valores_esquerda, [0.3, 0.4, 0.5], nivel_cores):
            btn = MDRaisedButton(
                text=f"{numberl}",
                size_hint=(0.035, 0.04),
                pos_hint={"center_x": 0.12, "center_y": pos_y},
                md_bg_color=(0.2, 0.6, 0.8, 1),
                text_color=(1, 1, 1, 1),
                font_size="24sp",
                on_release=lambda _, nmb=numberl: self.instancia_numero(nmb),
            )
            self.numero_botoes_esquerda[numberl] = btn
            layout.add_widget(btn)

        for numberc, pos_y, color in zip(valores_centro, [0.2, 0.3, 0.4,0.5], nivel_cores):
            btn = MDRaisedButton(
                text=f"{numberc}",
                size_hint=(0.035, 0.04),
                pos_hint={"center_x": 0.3, "center_y": pos_y},
                md_bg_color=(0.2, 0.6, 0.8, 1),
                text_color=(1, 1, 1, 1),
                font_size="24sp",
                on_release=lambda _, nmb=numberc: self.instancia_numero(nmb),
            )
            self.numero_botoes_centro[numberc] = btn
            layout.add_widget(btn)

        for numberr, pos_y, color in zip(valores_direita, [0.3, 0.4, 0.5], nivel_cores):
            btn = MDRaisedButton(
                text=f"{numberr}",
                size_hint=(0.035, 0.04),
                pos_hint={"center_x": 0.5, "center_y": pos_y},
                md_bg_color=(0.2, 0.6, 0.8, 1),
                text_color=(1, 1, 1, 1),
                font_size="24sp",
                on_release=lambda _, nmb=numberr: self.instancia_numero(nmb),
            )
            self.numero_botoes_direita[numberc] = btn
            layout.add_widget(btn)

        botao_apagar = MDRaisedButton(
            text="Apagar",
            size_hint=(0.035, 0.04),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            font_size="14sp",
            md_bg_color=(0.2, 0.6, 0.8, 1),
            text_color=(1, 1, 1, 1),
            on_release=self.apagar_numero,
        )
        layout.add_widget(botao_apagar)

        limpar_button = MDRaisedButton(
            text="Limpar",
            size_hint=(0.035, 0.04),
            pos_hint={"center_x": 0.3, "center_y": 0.6},
            md_bg_color=(0.2, 0.6, 0.8, 1),
            text_color=(1, 1, 1, 1),
            font_size="14sp",
            on_release=self.limpar_resposta,
        )
        layout.add_widget(limpar_button)

        minus_button = MDRaisedButton(
            text="-",
            size_hint=(0.035, 0.04),
            pos_hint={"center_x": 0.12, "center_y": 0.2},
            md_bg_color=(0.2, 0.6, 0.8, 1),
            text_color=(1, 1, 1, 1),
            font_size="24sp",
            on_release=self.minus_insert,
        )
        layout.add_widget(minus_button)

        point_button = MDRaisedButton(
            text=",",
            size_hint=(0.035, 0.04),
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            md_bg_color=(0.2, 0.6, 0.8, 1),
            text_color=(1, 1, 1, 1),
            font_size="24sp",
            on_release=self.point_insert,
        )
        layout.add_widget(point_button)


        self.timer_label = Label(
            text="00:00:00",
            font_size=80,
            pos_hint={"center_x": 0.5, "center_y": 0.125},
        )
        layout.add_widget(self.timer_label)

        control_buttons = [
            ("Parar", 0.25, self.pause_timer, (0.6, 0, 0.6, 1)),
            ("Reiniciar", 0.75, self.reset_timer, (0, 0, 0.8, 1)),
        ]

        for text, pos_x, callback, color in control_buttons:
            layout.add_widget(
                MDRaisedButton(
                    text=text,
                    size_hint=(0.2, 0.05),
                    font_size="24sp",
                    pos_hint={"center_x": pos_x, "center_y": 0.05},
                    md_bg_color=color,
                    text_color=(1, 1, 1, 1),
                    on_release=callback,
                )
            )

        #Clock.schedule_once(self.iniciar_nivel_automaticamente, 0.5)

        self.add_widget(layout)

    def minus_insert(self, instance):
        self.answer_input.text += "-"

    def point_insert(self, instance):
        self.answer_input.text += ","

    def check_responder_button(self, *args):
        if getattr(self, 'nivel_selecionado', None) and self.answer_input.text.strip():
            self.responder_button.disabled = False
            self.responder_button.md_bg_color = (0.2, 0.6, 0.8, 1)  # Azul normal quando ativo
        else:
            self.responder_button.disabled = True
            self.responder_button.md_bg_color = (0.5, 0.5, 0.5, 1)  # Cinza quando desativado

    def instancia_numero(self, numero):
        self.answer_input.text += str(numero)

    def apagar_numero(self, instance):
        self.answer_input.text = self.answer_input.text[:-1]

    def limpar_resposta(self, instance):
        self.answer_input.text = ""

    def define_dificul(self, dificuldade):
        self.dificuldade = dificuldade
        self.nivel_atual = 1
        self.cria_questao()

    def confirma_rodadas(self, rodadas_value):
        if rodadas_value > 0:
            self.rodadas = rodadas_value
        else:
            print("Erro ao iniciar jogo: Valor inválido de rodadas.")

    def inicia_nivel(self, level):
        if level != self.nivel_atual:
            return
        self.nivel_selecionado = level
        self.rodada_atual = 0
        self.question_label.text = f"Iniciando nível {level}..."

        Clock.schedule_once(self.comecar_nivel, 1)

    def comecar_nivel(self, dt):
        self.start_timer()
        self.cria_questao()

    def escolha_modo(self,modo):
        self.modo = modo

    def cria_questao(self):
        if self.modo == "normal":
            self.cria_questaonormal()
        else:
            self.cria_questaopersonalizada()

    def cria_questaonormal(self):
        def gerar_operacao(num1, num2):
            op = self.operacao.lower()
            if op == "soma":
                return f"{num1} + {num2}", num1 + num2
            elif op == "subtracao":
                return f"{num1} - {num2}", num1 - num2
            elif op == "multiplicacao":
                return f"{num1} x {num2}", num1 * num2
            elif op == "divisao":
                num2 = num2 if num2 != 0 else 1
                num1 = num1 * num2
                return f"{num1} ÷ {num2}", num1 // num2
            else:
                raise ValueError(f"Operação inválida: {self.operacao}")


        rodada = self.rodada_atual

        # Define intervalo de números com base na rodada e no total de rodadas
        if self.rodadas == 3:
            if rodada == 0:
                min_value, max_value = 1, 10
            elif rodada == 1:
                min_value, max_value = 5, 10
            elif rodada == 2:
                min_value, max_value = 5, 15
            else:
                min_value, max_value = 1, 15

        elif self.rodadas == 6:
            if rodada in [0, 3]:
                min_value, max_value = 1, 10
            elif rodada in [1, 4]:
                min_value, max_value = 5, 10
            elif rodada in [2, 5]:
                min_value, max_value = 5, 15
            else:
                min_value, max_value = 1, 15

        elif self.rodadas == 10:
            if rodada in [0, 1, 4, 7]:
                min_value, max_value = 1, 10
            elif rodada in [2, 5, 8]:
                min_value, max_value = 5, 10
            elif rodada in [3, 6, 9]:
                min_value, max_value = 5, 15
            else:
                min_value, max_value = 1, 15

        else:
            min_value, max_value = 1, 10

        num1 = random.randint(min_value, max_value)
        num2 = random.randint(min_value, max_value or 1)
        self.question, self.answer = gerar_operacao(num1, num2)
        self.question_label.text = self.question

    def define_operacao(self, operacao):
        operacoes_validas = ["soma", "subtracao", "multiplicacao", "divisao"]
        if operacao in operacoes_validas:
            self.operacao = operacao.capitalize()
        else:
            print(f"Operação inválida recebida: {operacao}")



    def cria_questaopersonalizada(self):
        if self.dificuldade == "primario":
            min_value = 1
            max_value = 10  # Números até 10 (mais simples)
        elif self.dificuldade == "fundamental":
            min_value = 0
            max_value = 50  # Números até 50 (médio)
        else:  # Ensino Médio
            min_value = -100
            max_value = 100  # Números até 100 (difícil)

        num1 = random.randint(min_value, max_value)
        num2 = random.randint(min_value, max_value)

        if self.operacao == "Soma":
            self.question = f"{num1} + {num2}"
            self.answer = num1 + num2
        elif self.operacao == "Subt":
            self.question = f"{num1} - {num2}"
            self.answer = num1 - num2
        elif self.operacao == "Mult":
            self.question = f"{num1} x {num2}"
            self.answer = num1 * num2
        elif self.operacao == "Div":
            num1 = num1 * num2  # Garante que a divisão será exata
            self.question = f"{num1} ÷ {num2}"
            self.answer = num1 // num2

        self.question_label.text = self.question

    def verifica_resposta(self, *args):
        user_answer = self.answer_input.text.replace(',', '.')
        try:
            if float(user_answer) == self.answer:
                self.resp_correta += 1
                self.resp_correta_total += 1
            else:
                self.resp_errada += 1
                self.resp_errada_total += 1
        except ValueError:
            self.resp_errada += 1
            self.resp_errada_total += 1
            self.question_label.text = "Insira um número válido!"
            self.answer_input.text = ""
            return

        self.answer_input.text = ""

        # Atualiza score
        score_atual = self.resp_correta - self.resp_errada
        self.score_label.text = f"Pontuação: {score_atual}/{self.rodadas}"

        # Verifica se o score mínimo necessário foi atingido
        if score_atual >= self.rodadas:
            self.pause_timer()

            if self.nivel_atual < self.nivel_max:
                self.nivel_atual += 1
                next_button = self.nivel_botoes[self.nivel_atual]
                next_button.disabled = False
                next_button.md_bg_color = next_button.original_color
                self.question_label.text = f"Nível {self.nivel_atual} desbloqueado!"
                self.disparar_comemoracao()

                # Zera contadores para o novo nível
                self.resp_correta = 0
                self.resp_errada = 0
                self.rodada_atual = 0

                Clock.schedule_once(lambda dt: self.inicia_nivel(self.nivel_atual), 2)
            else:
                self.pause_timer()
                self.ir_para_tela_fim_de_jogo()

        else:
            # Ainda não passou, continua gerando questões
            self.rodada_atual += 1
            self.cria_questao()


    def start_timer(self, *args):
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.att_timer, 1)

    def pause_timer(self, *args):
        self.running = False
        Clock.unschedule(self.att_timer)

    def reset_timer(self, *args):
        self.running = False
        Clock.unschedule(self.att_timer)
        self.timer = 0
        self.timer_label.text = "00:00:00"

    def att_timer(self, dt):
        self.timer += 1
        minutes, seconds = divmod(self.timer, 60)
        hours, minutes = divmod(minutes, 60)
        self.timer_label.text = f"{hours:02}:{minutes:02}:{seconds:02}"

    def ir_para_niveis(self, instance):
        self.manager.current = "jogar"


    def disparar_comemoracao(self):
        layout_principal = self.children[0]
        num_baloes = 25

        for _ in range(num_baloes):
            balao = Image(
                source='balao.png',
                size_hint=(None, None),
                size=(dp(random.randint(50, 80)), dp(random.randint(50, 80))),
                opacity=0.8
            )

            balao.color = (
                random.uniform(0.5, 1.0),
                random.uniform(0.5, 1.0),
                random.uniform(0.5, 1.0),
                1
            )

            balao.x = random.uniform(0, self.width - balao.width)
            balao.y = -dp(100)

            layout_principal.add_widget(balao)

            duracao = random.uniform(2.5, 5.0)
            fim_x = balao.x + random.uniform(-dp(100), dp(100))
            fim_y = self.height + dp(50)

            anim = Animation(
                pos=(fim_x, fim_y),
                opacity=0,
                duration=duracao,
                t='out_quad'
            )

            anim.bind(on_complete=self.remover_widget)
            anim.start(balao)

    def remover_widget(self, animation, widget):
        # Acessa o layout principal para remover o widget
        layout_principal = self.children[0]
        layout_principal.remove_widget(widget)

    def ir_para_tela_fim_de_jogo(self):
        tempo_total = self.timer_label.text
        operacao = self.operacao
        rodadas_total = self.resp_correta_total + self.resp_errada_total
        acertos = self.resp_correta_total
        erros = self.resp_errada_total
        nivel = self.dificuldade  # já está salvo como 'primario', 'fundamental' ou 'medio'

        fim_screen = self.manager.get_screen("fim_de_jogo")
        fim_screen.atualizar_stats(tempo_total, operacao, rodadas_total, acertos, erros, nivel)
        self.manager.current = "fim_de_jogo"

    def reiniciar_jogo(self):
        self.timer = 0
        self.running = False
        self.operacao = "Soma"
        self.rodadas = 0
        self.rodada_atual = 0
        self.nivel_atual = 1
        self.resp_correta = 0
        self.resp_correta_total = 0
        self.resp_errada = 0
        self.resp_errada_total = 0
        self.dificuldade = "primario"
        self.nivel_selecionado = self.nivel_atual
        self.tudo_desbloqueado = False
        self.timer_label.text = "00:00:00"
        self.question_label.text = "Escolha um nível para começar!"
        self.answer_input.text = ""
        self.score_label.text = "Pontuação: 0/"

        for level, botao in self.nivel_botoes.items():
            if level == self.nivel_atual:
                botao.disabled = False
                botao.md_bg_color = botao.original_color
            else:
                botao.disabled = True
                botao.md_bg_color = (0.7, 0.7, 0.7, 1)  # cinza

        self.responder_button.disabled = True


class TelaFimDeJogo(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "fim_de_jogo"

        layout = FloatLayout()
        self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.bg_image)

        layout.add_widget(Label(
            text="Parabéns você concluiu o jogo!",
            font_size=50,
            bold=True,
            pos_hint={"center_x": 0.5, "center_y": 0.9}
        ))

        # Campo para digitar o nome
        self.nome_input = MDTextField(
            hint_text="Digite seu nome",
            pos_hint={"center_x": 0.5, "center_y": 0.78},
            size_hint_x=0.6
        )
        layout.add_widget(self.nome_input)

        card = MDCard(
            size_hint=(0.6, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=(0, 0, 0, 0.3),
            elevation=0,
            radius=[15, 15, 15, 15],
            padding=dp(20),
            spacing=dp(10)
        )
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

        layout.add_widget(MDRaisedButton(
            text="Voltar ao Menu",
            font_size="24sp",
            pos_hint={"center_x": 0.5, "center_y": 0.15},
            size_hint=(0.3, 0.1),
            on_release=self.enviar_dados_e_voltar
        ))

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
        if not nome:
            print("⚠️ Nome não preenchido.")
            return

        # Recuperar os dados dos labels
        tempo = self.tempo_label.text.replace("Tempo Total: ", "")
        operacao = self.operacao_label.text.replace("Operação: ", "")
        rodadas = self.rodadas_label.text.replace("Total de Questões: ", "")
        acertos = self.acertos_label.text.replace("Acertos Totais: ", "")
        erros = self.erros_label.text.replace("Erros Totais: ", "")
        nivel = self.nivel_label.text.replace("Nível: ", "")

        # Enviar para o formulário
        from enviar_dados import enviar_resultado_googleforms
        enviar_resultado_googleforms(nome, tempo, operacao, rodadas, acertos, erros, nivel)

        self.manager.current = "inicial"
