# sudoku_app.py

import random
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.behaviors import ButtonBehavior

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton


# ====================== LÓGICA DO SUDOKU ======================

class SudokuGenerator:
    def __init__(self):
        self.tabuleiro = [[0] * 9 for _ in range(9)]
        self.solucao = None

    def _e_valido(self, tabuleiro, num, pos):
        for j in range(9):
            if tabuleiro[pos[0]][j] == num and pos[1] != j:
                return False
        for i in range(9):
            if tabuleiro[i][pos[1]] == num and pos[0] != i:
                return False
        box_x, box_y = pos[1] // 3, pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if tabuleiro[i][j] == num and (i, j) != pos:
                    return False
        return True

    def _encontrar_vazio(self, tabuleiro):
        for i in range(9):
            for j in range(9):
                if tabuleiro[i][j] == 0:
                    return (i, j)
        return None

    def resolver(self, tabuleiro=None):
        if tabuleiro is None:
            tabuleiro = self.tabuleiro
        encontrar = self._encontrar_vazio(tabuleiro)
        if not encontrar:
            return True
        linha, coluna = encontrar
        numeros = list(range(1, 10))
        random.shuffle(numeros)
        for num in numeros:
            if self._e_valido(tabuleiro, num, (linha, coluna)):
                tabuleiro[linha][coluna] = num
                if self.resolver(tabuleiro):
                    return True
                tabuleiro[linha][coluna] = 0
        return False

    def gerar_tabuleiro(self, dificuldade="medio"):
        self.tabuleiro = [[0] * 9 for _ in range(9)]
        self._preencher_diagonal()
        self.resolver()
        self.solucao = [row[:] for row in self.tabuleiro]
        if "facil" in dificuldade:
            remocoes = 40
        elif "medio" in dificuldade:
            remocoes = 50
        else:
            remocoes = 60
        current_board = [row[:] for row in self.solucao]
        while remocoes > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if current_board[row][col] != 0:
                current_board[row][col] = 0
                remocoes -= 1
        self.tabuleiro = current_board
        return self.tabuleiro

    def _preencher_bloco(self, i, j):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for r in range(3):
            for c in range(3):
                self.tabuleiro[i + r][j + c] = nums.pop()

    def _preencher_diagonal(self):
        for i in range(0, 9, 3):
            self._preencher_bloco(i, i)

    def verificar_solucao_completa(self, tabuleiro):
        if self._encontrar_vazio(tabuleiro) is not None:
            return False
        if self.solucao is None:
            return False
        for i in range(9):
            for j in range(9):
                if tabuleiro[i][j] != self.solucao[i][j]:
                    return False
        return True


# ====================== WIDGET: CÉLULA ======================

class CelulaSudoku(ButtonBehavior, MDLabel):
    def __init__(self, row, col, fixed, start_value=0, **kwargs):
        super().__init__(**kwargs)
        self.row, self.col, self.fixed, self.value = row, col, fixed, start_value
        self.halign, self.valign = 'center', 'middle'
        self.font_style, self.theme_text_color = 'H5', 'Custom'
        self.bg_color_base = (0.1, 0.1, 0.1, 1)
        self.bg_color_fixed = (0.2, 0.2, 0.2, 1)
        self.bg_color_selected = (0.3, 0.3, 0.5, 1)
        self.bg_color_conflict = (0.5, 0.1, 0.1, 1)
        self.text_color_error = (1, 0.1, 0.1, 1)
        self.text_color_fixed = (1, 1, 0.2, 1)
        self.text_color_input = (1, 1, 1, 1)
        self.current_bg_color = self.bg_color_fixed if self.fixed else self.bg_color_base
        self.text_color = self.text_color_fixed if self.fixed else self.text_color_input
        self.text = str(self.value) if self.value != 0 else ""
        with self.canvas.before:
            Color(*self.current_bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        if hasattr(self, 'rect'):
            self.rect.pos, self.rect.size = self.pos, self.size

    def set_visual_state(self, is_selected=False, is_conflict=False):
        if is_selected:
            color = self.bg_color_selected
        elif self.fixed:
            color = self.bg_color_fixed
        elif is_conflict:
            color = self.bg_color_conflict
        else:
            color = self.bg_color_base
        if self.fixed:
            text_color = self.text_color_fixed
        elif is_conflict:
            text_color = self.text_color_error
        else:
            text_color = self.text_color_input
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.text_color = text_color
        self.current_bg_color = color

    def update_text(self):
        self.text = str(self.value) if self.value != 0 else ""

    def on_release(self):
        if not self.fixed:
            app_root = App.get_running_app().root
            tela_sudoku = app_root.get_screen('sudoku')
            tela_sudoku.selecionar_celula(self.row, self.col)


# ====================== TELA: SUDOKU ======================

class TelaSudoku(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'sudoku'
        self.generator = SudokuGenerator()
        self.cells, self.tabuleiro_logico = {}, None
        self.celula_selecionada, self.dificuldade = None, "medio"
        self._build_ui()

    def _build_ui(self):
        layout = FloatLayout()
        layout.add_widget(Image(source='fundoapp.png', allow_stretch=True,
                                keep_ratio=False, size_hint=(1, 1),
                                pos_hint={'x': 0, 'y': 0}, fit_mode='fill'))
        layout.add_widget(MDLabel(text="SUDOKU MATEMÁTICO", halign="center",
                                  font_style="H3", pos_hint={"center_x": 0.5, "top": 0.95},
                                  theme_text_color="Custom", text_color=(1, 0.95, 0.8, 1)))
        self.grade_9x9 = GridLayout(cols=9, rows=9, spacing=dp(1),
                                    size_hint=(0.9, 0.65),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.55})
        layout.add_widget(self.grade_9x9)
        teclado = self._criar_teclado()
        layout.add_widget(teclado)
        back_btn = MDIconButton(icon='arrow-left', pos_hint={'x': 0, 'top': 1},
                                on_release=self.voltar)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def _criar_teclado(self):
        # Layout principal do teclado (duas linhas)
        teclado_layout = GridLayout(
            cols=1,
            rows=2,
            size_hint=(0.9, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            spacing=dp(5)
        )

        # Primeira linha com números 1 a 5
        linha_superior = GridLayout(cols=5, spacing=dp(5))
        for i in range(1, 6):
            linha_superior.add_widget(MDRaisedButton(
                text=str(i),
                on_release=lambda btn, n=i: self.inserir_numero(n)
            ))

        # Segunda linha com números 6 a 9 e o X
        linha_inferior = GridLayout(cols=5, spacing=dp(5))
        for i in range(6, 10):
            linha_inferior.add_widget(MDRaisedButton(
                text=str(i),
                on_release=lambda btn, n=i: self.inserir_numero(n)
            ))
        linha_inferior.add_widget(MDRaisedButton(
            text="X",
            on_release=lambda btn: self.inserir_numero(0),
            md_bg_color=(0.6, 0.1, 0.1, 1)
        ))

        teclado_layout.add_widget(linha_superior)
        teclado_layout.add_widget(linha_inferior)
        return teclado_layout


    def on_enter(self, *args):
        # roda em thread para não travar a UI
        Thread(target=self.iniciar_novo_jogo).start()

    def iniciar_novo_jogo(self):
        self.tabuleiro_logico = self.generator.gerar_tabuleiro(self.dificuldade)
        Clock.schedule_once(self._montar_grade, 0)

    def _montar_grade(self, dt):
        self.grade_9x9.clear_widgets()
        self.cells.clear()
        for r in range(9):
            for c in range(9):
                valor = self.tabuleiro_logico[r][c]
                cell = CelulaSudoku(r, c, valor != 0, valor)
                self.grade_9x9.add_widget(cell)
                self.cells[(r, c)] = cell

    def selecionar_celula(self, row, col):
        self.celula_selecionada = (row, col)
        for cell in self.cells.values():
            cell.set_visual_state(is_selected=False)
        self.cells[(row, col)].set_visual_state(is_selected=True)

    def inserir_numero(self, num):
        if not self.celula_selecionada:
            return
        r, c = self.celula_selecionada
        cell = self.cells[(r, c)]
        if cell.fixed:
            return
        self.tabuleiro_logico[r][c] = num
        cell.value = num
        cell.update_text()
        if self.generator.verificar_solucao_completa(self.tabuleiro_logico):
            print("🎉 Sudoku completo!")
            self.voltar()

    def voltar(self, *args):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "inicial"
