import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
# KivyMD Imports
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton, MDIconButton
from kivymd.uix.card import MDCard

# Ajuste para o teclado não cobrir o jogo
Window.softinput_mode = "below_target"

# ---------- LÓGICA DO GERADOR (Mantida igual) ----------
def gerar_conta(dificuldade="fundI"):
    if dificuldade == "fundI":
        ops = ["+", "-"]
        a = random.randint(1, 20)
        b = random.randint(1, 20)
    elif dificuldade == "fundII":
        ops = ["+", "-", "*", "/"]
        a = random.randint(1, 50)
        b = random.randint(1, 50)
    elif dificuldade == "medio":
        ops = ["+", "-", "*", "/"]
        a = random.randint(1, 100)
        b = random.randint(1, 100)

    op = random.choice(ops)

    if op == "+":
        c = a + b
    elif op == "-":
        if b > a: a, b = b, a
        c = a - b
    elif op == "*":
        c = a * b
    elif op == "/":
        b = random.randint(1, 10)
        c = random.randint(1, 10)
        a = b * c

    return [str(a), op, str(b), "=", str(c)]

def colocar_horizontal(grid, x, y, conta):
    for i, ch in enumerate(conta):
        if (x+i, y) in grid and grid[(x+i, y)] != ch: return False
    for i, ch in enumerate(conta): grid[(x+i, y)] = ch
    return True

def colocar_vertical(grid, x, y, conta):
    for i, ch in enumerate(conta):
        if (x, y+i) in grid and grid[(x, y+i)] != ch: return False
    for i, ch in enumerate(conta): grid[(x, y+i)] = ch
    return True

def gerar_cruzadinha(num_contas=6, dificuldade="fundI"):
    grid = {}
    contas = []

    # Primeira conta no centro (ou 0,0)
    conta = gerar_conta(dificuldade)
    colocar_horizontal(grid, 0, 0, conta)
    contas.append(("H", 0, 0, conta))

    tentativas = 0
    while len(contas) < num_contas and tentativas < num_contas*20:
        tentativas += 1
        conta = gerar_conta(dificuldade)
        orientacao = random.choice(["H", "V"])

        if not contas: break
        _, x0, y0, conta_existente = random.choice(contas)

        conectado = False
        # Tenta conectar a nova conta em algum caractere da conta existente
        for i, ch1 in enumerate(conta):
            for j, ch2 in enumerate(conta_existente):
                if ch1 == ch2:
                    if orientacao == "H":
                        x = x0 + j - i; y = y0
                        if colocar_horizontal(grid, x, y, conta):
                            contas.append(("H", x, y, conta))
                            conectado = True
                    else:
                        x = x0; y = y0 + j - i
                        if colocar_vertical(grid, x, y, conta):
                            contas.append(("V", x, y, conta))
                            conectado = True
                    if conectado: break
            if conectado: break
    return grid, contas

# ---------- CÉLULAS ----------

class CelulaFixa(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(50), dp(50)) # Tamanho fixo maior
        self.font_size = "20sp"
        self.bold = True
        self.color = (1, 1, 1, 1)

        with self.canvas.before:
            Color(0.2, 0.4, 0.7, 1)  # Azul mais bonito
            self.bg = RoundedRectangle(size=self.size, pos=self.pos, radius=[6])

        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

class CelulaEntrada(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(50), dp(50))
        self.font_size = "24sp"
        self.multiline = False
        self.input_filter = "int"
        self.halign = "center"
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]

        # Estilo visual
        self.background_normal = ""
        self.background_active = ""
        self.background_color = (1, 1, 1, 1) # Fundo branco
        self.foreground_color = (0, 0, 0, 1) # Texto preto
        self.cursor_color = (0, 0, 0, 1)

        # Borda simples usando canvas
        with self.canvas.after:
            Color(0.7, 0.7, 0.7, 1)
            self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 6), width=1)

        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 6)

    def set_status(self, status):
        """Muda a cor baseado no acerto/erro"""
        if status == "correct":
            self.background_color = (0.7, 1, 0.7, 1) # Verde claro
        elif status == "wrong":
            self.background_color = (1, 0.7, 0.7, 1) # Vermelho claro
        else:
            self.background_color = (1, 1, 1, 1)

# ---------- WIDGET CRUZADINHA (GRID) ----------
class CruzadinhaWidget(GridLayout):
    def __init__(self, dificuldade="fundI", **kwargs):
        super().__init__(**kwargs)
        self.respostas = {}
        self.dificuldade = dificuldade
        # Configurações essenciais para ScrollView funcionar
        self.size_hint = (None, None)
        self.spacing = dp(4)
        self.padding = dp(20)
        self.montar()

    def montar(self):
        self.clear_widgets()
        self.respostas.clear()

        # Gera e normaliza coordenadas
        grid, contas = gerar_cruzadinha(7, self.dificuldade)

        if not grid: # Segurança caso falhe
            self.montar()
            return

        xs = [x for x, y in grid.keys()]
        ys = [y for x, y in grid.keys()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        self.cols = (max_x - min_x + 1)
        self.rows = (max_y - min_y + 1)

        # Calcula tamanho total do grid
        cell_size = dp(50) # Tamanho base da célula
        self.width = self.cols * (cell_size + self.spacing[0]) + self.padding[0]*2
        self.height = self.rows * (cell_size + self.spacing[1]) + self.padding[1]*2

        # Lógica de células vazias para completar a cruzadinha
        fixos = set()
        for orient, x0, y0, conta in contas:
            numeros = [i for i, ch in enumerate(conta) if ch.isdigit()]
            if len(numeros) >= 2:
                # Escolhe alguns números para ficarem fixos (dicas)
                qtd_dicas = 2 if len(numeros) > 3 else 1
                escolhidos = random.sample(numeros, qtd_dicas)
                for idx in escolhidos:
                    if orient == "H": fixos.add((x0+idx, y0))
                    else: fixos.add((x0, y0+idx))

        # Preenche o Grid (Kivy preenche de baixo para cima, esquerda para direita se não invertido)
        # Vamos inverter o range Y para desenhar de cima para baixo visualmente
        for y in range(max_y, min_y-1, -1):
            for x in range(min_x, max_x+1):
                if (x, y) in grid:
                    valor = grid[(x, y)]
                    if valor.isdigit() and (x, y) not in fixos:
                        # Campo de entrada
                        entrada = CelulaEntrada()
                        self.respostas[(x, y)] = (entrada, valor)
                        self.add_widget(entrada)
                    else:
                        # Célula fixa (operadores, igual, ou dicas)
                        self.add_widget(CelulaFixa(text=valor))
                else:
                    # Espaço vazio transparente
                    self.add_widget(Widget(size_hint=(None, None), size=(cell_size, cell_size)))

    def verificar(self):
        acertos = 0
        total = len(self.respostas)
        if total == 0: return 0, 0

        for (x, y), (entrada, valor) in self.respostas.items():
            texto = entrada.text.strip()
            if texto == valor:
                entrada.set_status("correct")
                acertos += 1
            elif texto == "":
                entrada.set_status("normal")
            else:
                entrada.set_status("wrong")
        return acertos, total

# ---------- TELA DO JOGO ----------
class CruzadinhaScreen(Screen):
    def __init__(self, dificuldade="fundI", **kwargs):
        super().__init__(**kwargs)
        self.dificuldade = dificuldade
        layout = FloatLayout()

        # 1. Fundo
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        layout.add_widget(fundo)

        # 2. Cabeçalho (Fixo)
        header = MDCard(
            size_hint=(1, None),
            height=dp(70),
            pos_hint={"top": 1},
            md_bg_color=(1, 1, 1, 0.8),
            elevation=2,
            radius=[0, 0, 20, 20],
            padding=[dp(10), 0]
        )

        # Botão Voltar
        btn_back = MDIconButton(
            icon="arrow-left",
            pos_hint={"center_y": 0.5},
            on_release=lambda x: self.voltar("jogar")
        )

        # Título
        lbl_title = MDLabel(
            text="CRUZADINHA",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_size="26sp",
            pos_hint={"center_y": 0.5}
        )
        # Dummy para centralizar
        dummy = Widget(size_hint_x=None, width=dp(48))

        header.add_widget(btn_back)
        header.add_widget(lbl_title)
        header.add_widget(dummy)
        layout.add_widget(header)

        # 3. Área de Scroll (Cruzadinha)
        # O ScrollView permite que a cruzadinha seja maior que a tela
        self.scroll = ScrollView(
            size_hint=(1, 0.75),
            pos_hint={"center_x": 0.5, "center_y": 0.52}
        )
        self.cruzadinha = CruzadinhaWidget(dificuldade=self.dificuldade)
        # Centraliza o grid dentro do scroll se for menor que a tela
        self.cruzadinha.bind(minimum_height=self.cruzadinha.setter('height'))
        self.cruzadinha.bind(minimum_width=self.cruzadinha.setter('width'))

        self.scroll.add_widget(self.cruzadinha)
        layout.add_widget(self.scroll)

        # 4. Painel de Controle (Fixo na Base)
        panel = MDCard(
            size_hint=(0.95, None),
            height=dp(80),
            pos_hint={"center_x": 0.5, "y": 0.02},
            md_bg_color=(1, 1, 1, 0.95),
            radius=[20],
            elevation=4,
            padding=dp(10),
            spacing=dp(10)
        )

        # Info de Acertos
        self.lbl_info = MDLabel(
            text="Preencha os campos",
            halign="center",
            font_style="Caption",
            size_hint_x=0.4
        )

        # Botão Verificar
        btn_check = MDFillRoundFlatButton(
            text="VERIFICAR",
            font_name="Roboto", # Fonte padrão legível
            md_bg_color=(0.2, 0.7, 0.3, 1), # Verde
            on_release=self.acao_verificar,
            size_hint_x=0.3
        )

        # Botão Nova
        btn_new = MDIconButton(
            icon="refresh",
            icon_size="32sp",
            theme_text_color="Custom",
            text_color=(0.2, 0.4, 0.9, 1),
            on_release=self.acao_nova,
            pos_hint={"center_y": 0.5}
        )

        panel.add_widget(btn_new)
        panel.add_widget(self.lbl_info)
        panel.add_widget(btn_check)

        layout.add_widget(panel)
        self.add_widget(layout)

    def acao_verificar(self, instance):
        acertos, total = self.cruzadinha.verificar()
        if acertos == total and total > 0:
            self.lbl_info.text = "PARABÉNS! COMPLETOU!"
            self.lbl_info.theme_text_color = "Custom"
            self.lbl_info.text_color = (0, 0.6, 0, 1)
        else:
            self.lbl_info.text = f"Acertos: {acertos} / {total}"
            self.lbl_info.theme_text_color = "Custom"
            self.lbl_info.text_color = (0, 0, 0, 1)

    def acao_nova(self, instance):
        self.cruzadinha.montar()
        self.lbl_info.text = "Novo Jogo Gerado"
        self.lbl_info.text_color = (0, 0, 0, 1)
        # Reseta a posição do scroll para o centro (opcional)
        self.scroll.scroll_x = 0.5
        self.scroll.scroll_y = 0.5

    def voltar(self, tela_nome):
        self.manager.current = "jogar" # Ajuste para o nome da tela de menu de jogos