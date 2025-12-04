# sudoku_app.py

import random
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog


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
        # Salva a solução completa para validação em tempo real
        self.solucao = [row[:] for row in self.tabuleiro]
        
        if "facil" in dificuldade:
            remocoes = 30
        elif "medio" in dificuldade:
            remocoes = 45
        else:
            remocoes = 55
            
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

    def verificar_vitoria(self, tabuleiro_atual):
        # Verifica se não há zeros e se tudo bate com a solução
        for i in range(9):
            for j in range(9):
                if tabuleiro_atual[i][j] == 0:
                    return False
                if tabuleiro_atual[i][j] != self.solucao[i][j]:
                    return False
        return True


# ====================== WIDGET: CÉLULA ======================

class CelulaSudoku(ButtonBehavior, MDLabel):
    def __init__(self, row, col, fixed, start_value=0, **kwargs):
        super().__init__(**kwargs)
        self.row, self.col, self.fixed, self.value = row, col, fixed, start_value
        self.halign, self.valign = 'center', 'middle'
        self.font_style, self.theme_text_color = 'H5', 'Custom'
        self.is_wrong = False # Novo estado para números errados
        
        # --- CORES DO TEMA CLARO ---
        self.bg_color_base = (1, 1, 1, 1)                # Branco
        self.bg_color_fixed = (0.9, 0.9, 0.9, 1)         # Cinza claro
        self.bg_color_selected = (0.6, 0.9, 1, 1)        # Azul claro
        self.bg_color_highlight = (0.85, 0.95, 0.85, 1)  # Verde suave
        self.bg_color_conflict = (1, 0.8, 0.8, 1)        # Fundo vermelho claro (erro)
        
        self.text_color_error = (0.8, 0, 0, 1)           # Texto Vermelho
        self.text_color_fixed = (0, 0, 0, 1)             # Preto
        self.text_color_input = (0.2, 0.2, 0.8, 1)       # Azul escuro (input usuário)
        
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

    def set_visual_state(self, is_selected=False, is_highlighted=False):
        """Atualiza a cor da célula baseada no estado atual."""
        # Define Cor de Fundo
        if is_selected:
            color = self.bg_color_selected
        elif self.is_wrong:
            color = self.bg_color_conflict
        elif is_highlighted:
            color = self.bg_color_highlight
        elif self.fixed:
            color = self.bg_color_fixed
        else:
            color = self.bg_color_base

        # Define Cor do Texto
        if self.is_wrong:
            text_color = self.text_color_error
        elif self.fixed:
            text_color = self.text_color_fixed
        else:
            text_color = self.text_color_input

        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.text_color = text_color
        self.current_bg_color = color

    def update_text(self):
        self.text = str(self.value) if self.value != 0 else ""

    def on_release(self):
        app_root = App.get_running_app().root
        if app_root:
            tela_sudoku = app_root.get_screen('sudoku')
            tela_sudoku.selecionar_celula(self.row, self.col)


# ====================== TELA: SUDOKU ======================

class TelaSudoku(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'sudoku'
        self.generator = SudokuGenerator()
        self.cells, self.tabuleiro_logico = {}, None
        self.celula_selecionada = None
        
        # Estados do Jogo
        self.dificuldade = "medio"
        self.erros = 0
        self.max_erros = 3
        self.tempo_segundos = 0
        self.timer_event = None
        self.dialog = None
        
        self._build_ui()

    def _build_ui(self):
        layout = FloatLayout()
        
        # --- MUDANÇA NO FUNDO ---
        # Tenta carregar a imagem de fundo azul
        try:
            bg = Image(source='fundoapp.png', allow_stretch=True,
                       keep_ratio=False, size_hint=(1, 1),
                       pos_hint={'x': 0, 'y': 0}, fit_mode='fill')
            layout.add_widget(bg)
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo: {e}")
            # Fallback para fundo sólido se a imagem falhar
            with layout.canvas.before:
                Color(0.98, 0.98, 0.98, 1)
                Rectangle(pos=layout.pos, size=layout.size)
        # ------------------------
        
        # ================= CABEÇALHO (Stats) =================
        header_layout = GridLayout(cols=3, size_hint=(0.9, 0.08), 
                                   pos_hint={'center_x': 0.5, 'top': 0.98}, spacing=dp(10))
        
        # 1. Erros (Texto um pouco mais escuro para contraste com o azul)
        self.lbl_erros = MDLabel(text="Erros: 0/3", halign="center", theme_text_color="Custom", text_color=(0.2, 0.2, 0.2, 1))
        
        # 2. Tempo
        self.lbl_tempo = MDLabel(text="00:00", halign="center", font_style="H6", theme_text_color="Custom", text_color=(0.1, 0.1, 0.1, 1))
        
        # 3. Botão Pause
        btn_pause = MDIconButton(icon="pause", on_release=self.pausar_jogo, 
                                 theme_text_color="Custom", text_color=(0.1, 0.1, 0.1, 1), pos_hint={'center_x': 0.5})
        
        header_layout.add_widget(self.lbl_erros)
        header_layout.add_widget(self.lbl_tempo)
        header_layout.add_widget(btn_pause)
        
        layout.add_widget(header_layout)
        # ====================================================

        # Grade 9x9
        self.grade_9x9 = GridLayout(cols=9, rows=9, spacing=dp(2),
                                    size_hint=(0.92, 0.55),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.6})
        
        self.grade_9x9.bind(pos=self.desenhar_linhas_grade, size=self.desenhar_linhas_grade)
        layout.add_widget(self.grade_9x9)
        
        # Teclado Numérico
        teclado = self._criar_teclado()
        layout.add_widget(teclado)
        
        self.add_widget(layout)

    def desenhar_linhas_grade(self, *args):
        grid = self.grade_9x9
        grid.canvas.after.clear()
        with grid.canvas.after:
            w, h = grid.width, grid.height
            x, y = grid.x, grid.y
            espessura = dp(2.5)

            # Linhas Verticais Amarelas
            Color(1.0, 0.8, 0.0, 1.0)
            Line(points=[x + w/3, y, x + w/3, y + h], width=espessura, cap='square')
            Line(points=[x + 2*w/3, y, x + 2*w/3, y + h], width=espessura, cap='square')
            
            # Linhas Horizontais Vermelhas
            Color(1.0, 0.2, 0.2, 1.0)
            Line(points=[x, y + h/3, x + w, y + h/3], width=espessura, cap='square')
            Line(points=[x, y + 2*h/3, x + w, y + 2*h/3], width=espessura, cap='square')
            
            Color(0, 0, 0, 1)
            Line(rectangle=(x, y, w, h), width=dp(2))

    def _criar_teclado(self):
        teclado_layout = GridLayout(
            cols=1, rows=2,
            size_hint=(0.9, 0.18),
            pos_hint={'center_x': 0.5, 'center_y': 0.15},
            spacing=dp(8)
        )
        linha_superior = GridLayout(cols=5, spacing=dp(8))
        
        # --- BOTÕES NUMÉRICOS (Branco com texto Preto) ---
        for i in range(1, 6):
            btn = MDRaisedButton(text=str(i), size_hint=(1, 1), elevation=2,
                                 md_bg_color=(1, 1, 1, 1),           # Fundo BRANCO
                                 theme_text_color="Custom",          # Habilita cor customizada
                                 text_color=(0, 0, 0, 1),            # Texto PRETO
                                 on_release=lambda btn, n=i: self.inserir_numero(n))
            linha_superior.add_widget(btn)

        linha_inferior = GridLayout(cols=5, spacing=dp(8))
        for i in range(6, 10):
            btn = MDRaisedButton(text=str(i), size_hint=(1, 1), elevation=2,
                                 md_bg_color=(1, 1, 1, 1),           # Fundo BRANCO
                                 theme_text_color="Custom",          # Habilita cor customizada
                                 text_color=(0, 0, 0, 1),            # Texto PRETO
                                 on_release=lambda btn, n=i: self.inserir_numero(n))
            linha_inferior.add_widget(btn)
            
        # --- BOTÃO X (Vermelho com texto Preto) ---
        btn_x = MDRaisedButton(text="X", size_hint=(1, 1), elevation=2, 
                               md_bg_color=(0.8, 0.2, 0.2, 1),       # Fundo VERMELHO
                               theme_text_color="Custom",            # Habilita cor customizada
                               text_color=(0, 0, 0, 1),              # Texto PRETO
                               on_release=lambda btn: self.inserir_numero(0))
        linha_inferior.add_widget(btn_x)

        teclado_layout.add_widget(linha_superior)
        teclado_layout.add_widget(linha_inferior)
        return teclado_layout

    # ================= LOGICA DO JOGO =================

    def on_enter(self, *args):
        Thread(target=self.iniciar_novo_jogo).start()

    def iniciar_novo_jogo(self):
        # Resetar variaveis
        self.erros = 0
        self.tempo_segundos = 0
        self.stop_timer()
        
        self.tabuleiro_logico = self.generator.gerar_tabuleiro(self.dificuldade)
        
        # Atualiza UI na thread principal
        Clock.schedule_once(self._montar_grade, 0)
        Clock.schedule_once(self.start_timer, 0) # Inicia timer

    def _montar_grade(self, dt):
        self.grade_9x9.clear_widgets()
        self.cells.clear()
        self.lbl_erros.text = f"Erros: 0/{self.max_erros}"
        self.lbl_erros.theme_text_color = "Custom"
        
        for r in range(9):
            for c in range(9):
                valor = self.tabuleiro_logico[r][c]
                cell = CelulaSudoku(r, c, valor != 0, valor)
                self.grade_9x9.add_widget(cell)
                self.cells[(r, c)] = cell
        Clock.schedule_once(self.desenhar_linhas_grade, 0.1)

    # --- TIMER ---
    def start_timer(self, dt=None):
        self.stop_timer()
        self.timer_event = Clock.schedule_interval(self.atualizar_tempo, 1)

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

    def atualizar_tempo(self, dt):
        self.tempo_segundos += 1
        m, s = divmod(self.tempo_segundos, 60)
        self.lbl_tempo.text = f"{m:02d}:{s:02d}"

    # --- PAUSE ---
    def pausar_jogo(self, instance):
        self.stop_timer()
        if not self.dialog:
            self.dialog = MDDialog(
                title="Jogo Pausado",
                text="O jogo está parado. Deseja continuar?",
                buttons=[
                    MDFlatButton(text="SAIR", on_release=self.voltar),
                    MDFlatButton(text="CONTINUAR", on_release=self.retomar_jogo)
                ],
                auto_dismiss=False
            )
        self.dialog.open()

    def retomar_jogo(self, inst):
        self.dialog.dismiss()
        self.dialog = None
        self.start_timer()

    # --- INPUT E ERROS ---
    def selecionar_celula(self, row, col):
        self.celula_selecionada = (row, col)
        block_r = row // 3
        block_c = col // 3
        
        for (r, c), cell in self.cells.items():
            is_selected = (r == row and c == col)
            in_cross = (r == row) or (c == col)
            in_block = (r // 3 == block_r and c // 3 == block_c)
            is_highlighted = (in_cross or in_block) and not is_selected
            
            cell.set_visual_state(is_selected=is_selected, is_highlighted=is_highlighted)

    def inserir_numero(self, num):
        if not self.celula_selecionada:
            return
        r, c = self.celula_selecionada
        cell = self.cells[(r, c)]
        
        if cell.fixed:
            return
            
        # Apagar número (X)
        if num == 0:
            self.tabuleiro_logico[r][c] = 0
            cell.value = 0
            cell.is_wrong = False
            cell.update_text()
            cell.set_visual_state(is_selected=True) # Re-renderiza cor
            return

        # Validação em Tempo Real
        valor_correto = self.generator.solucao[r][c]
        
        if num == valor_correto:
            # Acertou
            self.tabuleiro_logico[r][c] = num
            cell.value = num
            cell.is_wrong = False
            cell.update_text()
            cell.set_visual_state(is_selected=True)
            
            # Verifica Vitória
            if self.generator.verificar_vitoria(self.tabuleiro_logico):
                self.game_finished(win=True)
        else:
            # Errou
            self.erros += 1
            self.lbl_erros.text = f"Erros: {self.erros}/{self.max_erros}"
            self.lbl_erros.theme_text_color = "Error" # Muda cor do texto para vermelho momentaneamente
            
            cell.value = num
            cell.is_wrong = True
            cell.update_text()
            cell.set_visual_state(is_selected=True)
            
            # Verifica Derrota
            if self.erros >= self.max_erros:
                self.game_finished(win=False)

    def game_finished(self, win):
        self.stop_timer()
        titulo = "Parabéns!" if win else "Game Over"
        msg = f"Você completou o Sudoku em {self.lbl_tempo.text}!" if win else "Você atingiu o limite de 3 erros."
        
        self.dialog = MDDialog(
            title=titulo,
            text=msg,
            buttons=[
                MDFlatButton(text="SAIR", on_release=self.voltar),
                MDFlatButton(text="NOVO JOGO", on_release=self.reiniciar)
            ],
            auto_dismiss=False
        )
        self.dialog.open()

    def reiniciar(self, inst):
        self.dialog.dismiss()
        self.dialog = None
        Thread(target=self.iniciar_novo_jogo).start()

    def voltar(self, *args):
        if self.dialog:
            self.dialog.dismiss()
        if self.manager:
            self.manager.transition = SlideTransition(direction="right", duration=0.4)
            self.manager.current = "inicial"