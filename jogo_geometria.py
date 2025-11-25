# game_geometria.py
# Tela de jogo "Formas em Ação!" - Geometria Plana
# Sem .kv — tudo em Python (Kivy + KivyMD)
#
# Requisitos: kivy, kivymd

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

import random
import math
from functools import partial


class GameGeometriaScreen(MDScreen):
    """
    Tela de jogo de Geometria Plana (círculo, quadrado, retângulo, trapézio).
    Para usar no seu ScreenManager faça:
        from game_geometria import GameGeometriaScreen
        sm.add_widget(GameGeometriaScreen(name='game_geometria'))
    """

    pontos = NumericProperty(0)
    vidas = NumericProperty(3)
    estrelas = NumericProperty(0)
    combo = NumericProperty(0)
    tempo_restante = NumericProperty(0)
    timer_ativo = BooleanProperty(False)

    feedback_text = StringProperty("")
    pergunta_text = StringProperty("")
    dica_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout base: fundo + main
        bg = Image(source="fundoapp.png", allow_stretch=True, keep_ratio=False)
        self.add_widget(bg)

        self.main = MDBoxLayout(orientation="vertical", padding=dp(12), spacing=dp(12))
        self.add_widget(self.main)

        # Top bar (voltar + título + pontuação)
        top = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(60))
        self.main.add_widget(top)

        self.btn_back = MDIconButton(icon="arrow-left", on_release=self._voltar)
        top.add_widget(self.btn_back)

        self.title_label = MDLabel(text="Formas em Ação! — Geometria Plana",
                                   font_style="H6",
                                   halign="left",
                                   valign="middle")
        top.add_widget(self.title_label)

        right_top = MDBoxLayout(orientation="horizontal", size_hint_x=None, width=dp(220))
        top.add_widget(right_top)

        self.pontos_lbl = MDLabel(text="Pontos: 0", halign="right")
        right_top.add_widget(self.pontos_lbl)

        self.vidas_lbl = MDLabel(text="V: 3", halign="center", size_hint_x=None, width=dp(80))
        right_top.add_widget(self.vidas_lbl)

        # Área do jogo: card com pergunta + entrada + ações
        area = MDBoxLayout(orientation="horizontal", spacing=dp(12))
        self.main.add_widget(area)

        # Card esquerdo: pergunta e inputs
        self.card = MDCard(radius=[16], padding=dp(16), size_hint=(0.68, 1), elevation=8)
        area.add_widget(self.card)

        card_layout = MDBoxLayout(orientation="vertical", spacing=dp(12))
        self.card.add_widget(card_layout)

        self.pergunta_label = MDLabel(text="", halign="center", font_style="H5")
        card_layout.add_widget(self.pergunta_label)

        # Hint / dica
        self.dica_label = MDLabel(text="", halign="center", theme_text_color="Secondary")
        card_layout.add_widget(self.dica_label)

        # Campo de resposta
        self.input_resposta = MDTextField(hint_text="Digite a resposta (ex: 12.5)", size_hint_x=0.8,
                                          pos_hint={"center_x": 0.5})
        card_layout.add_widget(self.input_resposta)

        # Botões de múltipla escolha (usado para perguntas de fórmulas)
        self.mc_grid = MDGridLayout(cols=1, size_hint_y=None)
        card_layout.add_widget(self.mc_grid)

        # Ações: confirmar / pular
        action_row = MDBoxLayout(orientation="horizontal", spacing=dp(12), size_hint_y=None, height=dp(48))
        card_layout.add_widget(action_row)

        self.btn_confirm = MDRaisedButton(text="Confirmar", on_release=self.on_confirm)
        action_row.add_widget(self.btn_confirm)

        self.btn_skip = MDRectangleFlatButton(text="Pular (-1 vida)", on_release=self.on_skip)
        action_row.add_widget(self.btn_skip)

        # Feedback rápido
        self.feedback_label = MDLabel(text="", halign="center", theme_text_color="Custom")
        card_layout.add_widget(self.feedback_label)

        # Card direito: status, timer, modo
        side = MDCard(radius=[16], padding=dp(12), size_hint=(0.32, 1), elevation=6)
        area.add_widget(side)

        side_layout = MDBoxLayout(orientation="vertical", spacing=dp(8))
        side.add_widget(side_layout)

        self.progress = MDProgressBar(value=0)
        side_layout.add_widget(self.progress)

        self.timer_label = MDLabel(text="Tempo: --", halign="center")
        side_layout.add_widget(self.timer_label)

        # Modo timer toggle (simples: liga/desliga)
        self.timer_toggle_btn = MDRaisedButton(text="Ativar Timer (10s)", on_release=self.toggle_timer)
        side_layout.add_widget(self.timer_toggle_btn)

        # Pontuação/Combo/Estrelas
        self.pontos_widget = MDLabel(text="Pontos: 0", halign="center")
        side_layout.add_widget(self.pontos_widget)

        self.combo_widget = MDLabel(text="Combo: 0", halign="center")
        side_layout.add_widget(self.combo_widget)

        self.estrelas_widget = MDLabel(text="Estrelas: 0", halign="center")
        side_layout.add_widget(self.estrelas_widget)

        # Rodapé: instruções e botão iniciar/reiniciar
        footer = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(64), spacing=dp(12))
        self.main.add_widget(footer)

        instr = MDLabel(text="Formas: Círculo | Quadrado | Retângulo | Trapézio",
                        halign="left", size_hint_x=0.8)
        footer.add_widget(instr)

        self.btn_start = MDRaisedButton(text="Iniciar Jogo", on_release=self.start_game)
        footer.add_widget(self.btn_start)

        # Estado do jogo
        self.current_question = None
        self._timer_event = None
        self.question_time_limit = 10  # default

        # Preparar primeiras renderizações
        self._render_ui_initial()

    # ---------------------------
    # UI helpers
    # ---------------------------
    def _render_ui_initial(self):
        self.update_status_widgets()
        self.pergunta_label.text = "Pressione INICIAR para começar"
        self.dica_label.text = ""
        self.feedback_label.text = ""
        self.input_resposta.text = ""
        self.mc_grid.clear_widgets()
        self.progress.value = 0
        self.timer_label.text = "Tempo: --"

    def update_status_widgets(self):
        self.pontos_lbl.text = f"Pontos: {self.pontos}"
        self.pontos_widget.text = f"Pontos: {self.pontos}"
        self.vidas_lbl.text = "Vida: " + str(self.vidas)
        self.combo_widget.text = f"Combo: {self.combo}"
        self.estrelas_widget.text = f"Estrelas: {self.estrelas}"

    # ---------------------------
    # Game controls
    # ---------------------------
    def _voltar(self, *l):
        # se você tiver ScreenManager, voltar para a tela inicial:
        if self.manager:
            self.manager.current = "inicial"
        else:
            print("Voltar pressionado (sem ScreenManager)")

    def toggle_timer(self, *l):
        self.timer_ativo = not self.timer_ativo
        if self.timer_ativo:
            self.timer_label.text = f"Tempo: {self.question_time_limit}s"
            self.timer_toggle_btn.text = f"Timer: {self.question_time_limit}s (ON)"
        else:
            self.timer_label.text = "Tempo: --"
            self.timer_toggle_btn.text = "Ativar Timer (10s)"

    def start_game(self, *l):
        # reset
        self.pontos = 0
        self.vidas = 3
        self.estrelas = 0
        self.combo = 0
        self.update_status_widgets()
        self._next_question()

    def on_confirm(self, *l):
        if not self.current_question:
            return
        # se houver opções MC, usar aquele fluxo
        if self.current_question.get("type") == "mc":
            # coletar resposta selecionada (já salva no current_question['selected'])
            selected = self.current_question.get("selected", None)
            if selected is None:
                self._show_feedback("Escolha uma opção.", bad=True)
                return
            answer = selected
        else:
            text = self.input_resposta.text.strip()
            if text == "":
                self._show_feedback("Digite uma resposta.", bad=True)
                return
            # aceitar vírgula decimal
            text = text.replace(",", ".")
            try:
                answer = float(text)
            except Exception:
                self._show_feedback("Resposta numérica inválida.", bad=True)
                return

        self._evaluate_answer(answer)

    def on_skip(self, *l):
        # perder 1 vida, pular pergunta
        self.vidas = max(0, self.vidas - 1)
        self.combo = 0
        self.update_status_widgets()
        self._show_feedback("Pulou! -1 vida.", bad=True)
        if self.vidas <= 0:
            self._game_over()
            return
        self._next_question()

    # ---------------------------
    # Question generation
    # ---------------------------
    def _next_question(self, *l):
        # cancelar timer anterior
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None

        shape = random.choice(["circulo", "quadrado", "retangulo", "trapezio"])
        q = None
        if shape == "circulo":
            q = self._gerar_circulo()
        elif shape == "quadrado":
            q = self._gerar_quadrado()
        elif shape == "retangulo":
            q = self._gerar_retangulo()
        else:
            q = self._gerar_trapezio()

        self.current_question = q
        self._render_question(q)

        # iniciar timer se ligado
        if self.timer_ativo:
            self.tempo_restante = self.question_time_limit
            self.progress.max = self.question_time_limit
            self.progress.value = 0
            self._timer_event = Clock.schedule_interval(self._tick_timer, 1)

    def _tick_timer(self, dt):
        self.tempo_restante -= 1
        if self.tempo_restante < 0:
            # tempo esgotou
            if self._timer_event:
                self._timer_event.cancel()
                self._timer_event = None
            self._show_feedback("Tempo esgotou! -1 vida", bad=True)
            self.vidas = max(0, self.vidas - 1)
            self.combo = 0
            self.update_status_widgets()
            if self.vidas <= 0:
                self._game_over()
                return
            Clock.schedule_once(lambda dt: self._next_question(), 1.0)
            return
        # atualizar UI
        self.progress.value = self.question_time_limit - self.tempo_restante
        self.timer_label.text = f"Tempo: {int(self.tempo_restante)}s"

    # ---------------------------
    # Render question
    # ---------------------------
    def _render_question(self, q):
        # q: dict com keys: text, answer, type ('num' ou 'mc'), extras...
        self.input_resposta.text = ""
        self.mc_grid.clear_widgets()
        self.feedback_label.text = ""
        self.pergunta_label.text = q["text"]
        self.dica_label.text = q.get("hint", "")

        if q["type"] == "mc":
            # criar botões de opção
            opts = q["options"]
            self.current_question["selected"] = None
            self.mc_grid.cols = 1
            self.mc_grid.size_hint_y = None
            self.mc_grid.height = dp(48) * len(opts)
            for idx, opt in enumerate(opts):
                b = MDRectangleFlatButton(text=str(opt),
                                          on_release=partial(self._mc_select, idx))
                # armazenar texto no botão
                b.option_index = idx
                self.mc_grid.add_widget(b)
        else:
            # campo numérico: foco
            pass

    def _mc_select(self, idx, btn):
        # btn is the button instance that called this via partial
        # mark selection visually
        for w in list(self.mc_grid.children):
            try:
                w.md_bg_color = (0, 0, 0, 0)
            except Exception:
                pass
        btn.md_bg_color = get_color_from_hex("#444444")
        # store selected option value
        opt_value = self.current_question["options"][idx]
        self.current_question["selected"] = opt_value

    # ---------------------------
    # Evaluate answer
    # ---------------------------
    def _evaluate_answer(self, given):
        q = self.current_question
        correct = False
        # numeric compare with tolerance
        if q["type"] == "num":
            expected = q["answer"]
            # expected can be float; allow small tolerance relative
            tol = 1e-2 if abs(expected) < 100 else 1e-1
            if abs(float(given) - float(expected)) <= tol:
                correct = True
        elif q["type"] == "mc":
            if str(given) == str(q["answer"]):
                correct = True

        if correct:
            self.pontos += 10
            # bônus por velocidade
            if self.timer_ativo and self.tempo_restante > (self.question_time_limit / 2):
                self.pontos += 5
            self.combo += 1
            self._show_feedback("Correto! +10", bad=False)
            # estrelas a cada 5 acertos seguidos
            if self.combo > 0 and (self.combo % 5) == 0:
                self.estrelas += 1
                self._show_feedback(f"Combo {self.combo}! Estrela ganha ⭐", bad=False)
        else:
            self.vidas = max(0, self.vidas - 1)
            self.combo = 0
            self._show_feedback(f"Errado! Resposta correta: {q['answer']}", bad=True)

        self.update_status_widgets()

        if self.vidas <= 0:
            self._game_over()
            return

        # próxima pergunta em 0.8s
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None

        Clock.schedule_once(lambda dt: self._next_question(), 0.8)

    # ---------------------------
    # Feedback helpers
    # ---------------------------
    def _show_feedback(self, text, bad=False):
        self.feedback_label.text = text
        if bad:
            self.feedback_label.theme_text_color = "Error"
        else:
            self.feedback_label.theme_text_color = "Custom"
            self.feedback_label.text_color = get_color_from_hex("#b2ff59")  # suave verde
        # reset color after a while
        Clock.schedule_once(lambda dt: self._clear_feedback(), 2.0)

    def _clear_feedback(self):
        self.feedback_label.text = ""
        # reset to default color (let MD decide)
        self.feedback_label.text_color = (1, 1, 1, 1)

    # ---------------------------
    # Game over / end
    # ---------------------------
    def _game_over(self):
        # cancelar timers
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None

        dialog = MDDialog(title="Fim de Jogo",
                          text=f"Você chegou a 0 vidas.\nPontos: {self.pontos}\nEstrelas: {self.estrelas}",
                          size_hint=(0.8, None),
                          buttons=[
                              MDRaisedButton(text="Reiniciar", on_release=self._dialog_reiniciar),
                              MDRectangleFlatButton(text="Sair", on_release=self._dialog_sair)
                          ])
        dialog.open()

    def _dialog_reiniciar(self, *l):
        l[0].parent.parent.dismiss()  # fecha dialog
        self.start_game()

    def _dialog_sair(self, *l):
        l[0].parent.parent.dismiss()
        # volta para tela inicial se existir
        if self.manager:
            self.manager.current = "inicial"

    # ---------------------------
    # Shape question generators
    # ---------------------------
    def _gerar_circulo(self):
        r = random.randint(2, 20)
        tipo = random.choice(["area", "perimetro", "comparar"])
        if tipo == "area":
            val = math.pi * r * r
            text = f"Calcule a área do círculo de raio {r} cm. (Use unidades cm²)"
            return {"type": "num", "text": text, "answer": round(val, 2), "hint": "Use π ≈ 3.1416"}
        elif tipo == "perimetro":
            val = 2 * math.pi * r
            text = f"Calcule o perímetro (circunferência) do círculo de raio {r} cm."
            return {"type": "num", "text": text, "answer": round(val, 2), "hint": "Perímetro = 2πr"}
        else:
            # comparar com quadrado de lado r
            area_circ = math.pi * r * r
            area_quad = r * r
            text = f"Qual forma tem maior área: círculo com raio {r} cm, ou quadrado de lado {r} cm?"
            winner = "Círculo" if area_circ > area_quad else "Quadrado"
            options = ["Círculo", "Quadrado"]
            return {"type": "mc", "text": text, "options": options, "answer": winner,
                    "hint": "Compare as áreas (círculo: πr² ; quadrado: lado²)"}

    def _gerar_quadrado(self):
        a = random.randint(2, 30)
        tipo = random.choice(["area", "perimetro", "identificar_form"])
        if tipo == "area":
            val = a * a
            text = f"Calcule a área do quadrado de lado {a} cm."
            return {"type": "num", "text": text, "answer": float(val), "hint": "Área = lado²"}
        elif tipo == "perimetro":
            val = 4 * a
            text = f"Calcule o perímetro do quadrado de lado {a} cm."
            return {"type": "num", "text": text, "answer": float(val), "hint": "Perímetro = 4 × lado"}
        else:
            text = "Qual é a fórmula da área do quadrado?"
            options = ["lado²", "2 × lado", "lado × altura"]
            return {"type": "mc", "text": text, "options": options, "answer": "lado²",
                    "hint": ""}

    def _gerar_retangulo(self):
        b = random.randint(3, 30)
        h = random.randint(2, 20)
        tipo = random.choice(["area", "perimetro", "comparar"])
        if tipo == "area":
            val = b * h
            text = f"Calcule a área do retângulo base {b} cm e altura {h} cm."
            return {"type": "num", "text": text, "answer": float(val), "hint": "Área = base × altura"}
        elif tipo == "perimetro":
            val = 2 * (b + h)
            text = f"Calcule o perímetro do retângulo base {b} cm e altura {h} cm."
            return {"type": "num", "text": text, "answer": float(val), "hint": "Perímetro = 2(b + h)"}
        else:
            # comparação entre retângulo e quadrado com lado = min(b,h)
            lado = min(b, h)
            area_rect = b * h
            area_quad = lado * lado
            winner = "Retângulo" if area_rect > area_quad else "Quadrado"
            text = f"Entre retângulo ({b}×{h}) e quadrado de lado {lado}, qual tem maior área?"
            options = ["Retângulo", "Quadrado"]
            return {"type": "mc", "text": text, "options": options, "answer": winner, "hint": ""}

    def _gerar_trapezio(self):
        B = random.randint(6, 30)
        b = random.randint(2, B - 1)
        h = random.randint(2, 20)
        tipo = random.choice(["area", "perimetro"])
        if tipo == "area":
            val = ((B + b) * h) / 2.0
            text = f"Calcule a área do trapézio com bases {B} cm e {b} cm, altura {h} cm."
            return {"type": "num", "text": text, "answer": round(val, 2), "hint": "Área = ((B + b) × h) / 2"}
        else:
            # para perímetro precisamos de lados oblíquos: simplificar pedindo soma das bases + lados iguais (aprox)
            # aqui pedimos apenas soma das bases + 2*l (onde l é dado) para simplificar
            l = random.randint(3, 20)
            val = B + b + 2 * l
            text = f"Calcule o perímetro aproximado do trapézio com bases {B} cm, {b} cm e lados iguais de {l} cm."
            return {"type": "num", "text": text, "answer": float(val),
                    "hint": "Perímetro = B + b + lado1 + lado2 (aqui lados iguais)"}

# Para testar a tela isoladamente
if __name__ == "__main__":
    class TestApp(MDApp):
        def build(self):
            self.theme_cls.theme_style = "Dark"
            screen = GameGeometriaScreen()
            return screen

    TestApp().run()
