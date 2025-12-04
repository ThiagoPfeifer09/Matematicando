import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout # Importante para centralizar
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

# KivyMD Imports
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu

# Ajuste para teclado
Window.softinput_mode = "below_target"

# ============================================================================
# 1. LÓGICA DO GERADOR (Otimizada para criar grids mais compactos)
# ============================================================================
def gerar_conta(dificuldade="fundI", subnivel="basico"):
    limites = {
        "fundI": {"basico": 10, "intermediario": 20, "avancado": 30},
        "fundII": {"basico": 30, "intermediario": 50, "avancado": 80},
        "medio": {"basico": 80, "intermediario": 100, "avancado": 150}
    }
    max_val = limites.get(dificuldade, {}).get(subnivel, 20)

    if dificuldade == "fundI": ops = ["+", "-"]
    else: ops = ["+", "-", "*", "/"]

    a = random.randint(1, max_val)
    b = random.randint(1, max_val)
    op = random.choice(ops)

    if op == "+": c = a + b
    elif op == "-":
        if b > a: a, b = b, a
        c = a - b
    elif op == "*": c = a * b
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

def gerar_cruzadinha(dificuldade="fundI", subnivel="basico"):
    # Quantidades de contas
    limites_qtd = {
        "fundI": (4, 5),
        "fundII": (5, 8),
        "medio": (8, 12) # Reduzi levemente o maximo para caber na tela sem scroll
    }

    min_c, max_c = limites_qtd.get(dificuldade, (4, 5))
    num_contas = random.randint(min_c, max_c)

    grid = {}
    contas = []

    # 1ª Conta centralizada
    conta = gerar_conta(dificuldade, subnivel)
    colocar_horizontal(grid, 0, 0, conta)
    contas.append(("H", 0, 0, conta))

    tentativas = 0
    # Tenta criar um grid mais "quadrado" para aproveitar melhor a tela
    while len(contas) < num_contas and tentativas < num_contas * 50:
        tentativas += 1
        conta = gerar_conta(dificuldade, subnivel)
        orientacao = random.choice(["H", "V"])

        if not contas: break
        _, x0, y0, conta_existente = random.choice(contas)

        conectado = False
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

# ============================================================================
# 2. CÉLULAS (Adaptáveis ao tamanho)
# ============================================================================
class CelulaFixa(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Não definimos size fixo aqui, será controlado pelo Grid
        self.font_size = "18sp" # Base, será atualizada
        self.bold = True
        self.color = (1, 1, 1, 1)

        with self.canvas.before:
            Color(0.2, 0.4, 0.7, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[4])
        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        # Atualiza fonte dinamicamente
        self.font_size = self.height * 0.5

class CelulaEntrada(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.input_filter = "int"
        self.halign = "center"
        self.padding_y = 0 # Será ajustado dinamicamente

        self.background_normal = ""
        self.background_active = ""
        self.background_color = (1, 1, 1, 1)
        self.foreground_color = (0, 0, 0, 1)

        with self.canvas.after:
            Color(0.6, 0.6, 0.6, 1)
            self.rect_border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 4), width=1)

        self.bind(pos=self.update_visuals, size=self.update_visuals)

    def update_visuals(self, *args):
        # Centraliza texto verticalmente
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
        # Atualiza borda
        self.rect_border.rounded_rectangle = (self.x, self.y, self.width, self.height, 4)
        # Atualiza tamanho da fonte baseado na altura da célula
        self.font_size = self.height * 0.5

    def set_status(self, status):
        if status == "correct": self.background_color = (0.7, 1, 0.7, 1)
        elif status == "wrong": self.background_color = (1, 0.7, 0.7, 1)
        elif status == "hint":  self.background_color = (0.6, 0.9, 1, 1)
        else: self.background_color = (1, 1, 1, 1)

# ============================================================================
# 3. WIDGET CRUZADINHA (Grid Dinâmico)
# ============================================================================
class CruzadinhaWidget(GridLayout):
    def __init__(self, dificuldade="fundI", subnivel="basico", **kwargs):
        super().__init__(**kwargs)
        self.respostas = {}
        self.dificuldade = dificuldade
        self.subnivel = subnivel
        # O segredo: size_hint None para podermos controlar o tamanho exato,
        # mas vamos atualizar esse tamanho baseado no pai.
        self.size_hint = (None, None)
        self.spacing = dp(2)
        # Sem padding interno para aproveitar espaço
        self.padding = 0

        # Gera o grid lógico
        self.montar_logica()

    def montar_logica(self):
        self.clear_widgets()
        self.respostas.clear()

        grid, contas = gerar_cruzadinha(self.dificuldade, self.subnivel)
        if not grid:
            self.montar_logica()
            return

        xs = [x for x, y in grid.keys()]
        ys = [y for x, y in grid.keys()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        self.cols = (max_x - min_x + 1)
        self.rows = (max_y - min_y + 1)

        # Lógica de Fixos (Um escondido, o resto fixo)
        fixos = set()
        for orient, x0, y0, conta in contas:
            idx_op, idx_eq = 1, 3
            indices_A, indices_B, indices_C = [0], [2], [4]
            escolha = random.choice(['hide_A', 'hide_B', 'hide_C'])

            indices_para_fixar = [idx_op, idx_eq]
            if escolha == 'hide_A':
                indices_para_fixar.extend(indices_B + indices_C)
            elif escolha == 'hide_B':
                indices_para_fixar.extend(indices_A + indices_C)
            else:
                indices_para_fixar.extend(indices_A + indices_B)

            for idx in indices_para_fixar:
                if orient == "H": fixos.add((x0 + idx, y0))
                else: fixos.add((x0, y0 + idx))

        # Adiciona Widgets (ainda sem tamanho definido)
        for y in range(max_y, min_y-1, -1):
            for x in range(min_x, max_x+1):
                if (x, y) in grid:
                    valor = grid[(x, y)]
                    if valor.isdigit() and (x, y) not in fixos:
                        entrada = CelulaEntrada()
                        self.respostas[(x, y)] = (entrada, valor)
                        self.add_widget(entrada)
                    else:
                        self.add_widget(CelulaFixa(text=valor))
                else:
                    # Widget vazio transparente
                    self.add_widget(Widget())

    def atualizar_tamanho_celulas(self, layout_disponivel_size):
        """
        Esta função é chamada pela tela para redimensionar as células
        para caberem exatamente no espaço disponível (w, h).
        """
        w_disp, h_disp = layout_disponivel_size

        # Margem de segurança
        w_disp -= dp(20)
        h_disp -= dp(20)

        # Calcula o tamanho máximo possível da célula (quadrada)
        tamanho_w = w_disp / self.cols
        tamanho_h = h_disp / self.rows

        # Pega o menor para garantir que cabe em ambos os eixos
        tamanho_final = min(tamanho_w, tamanho_h)

        # Limita para não ficar gigante em grids pequenos (ex: 2x2)
        tamanho_final = min(tamanho_final, dp(65))

        # Aplica ao Grid
        self.col_default_width = tamanho_final
        self.row_default_height = tamanho_final
        self.col_force_default = True
        self.row_force_default = True

        # Atualiza o tamanho do próprio widget
        self.width = self.cols * (tamanho_final + self.spacing[0])
        self.height = self.rows * (tamanho_final + self.spacing[1])

    def verificar(self):
        acertos = 0
        total = len(self.respostas)
        for (x, y), (entrada, valor) in self.respostas.items():
            if entrada.text.strip() == valor:
                entrada.set_status("correct")
                acertos += 1
            elif entrada.text.strip() == "":
                entrada.set_status("normal")
            else:
                entrada.set_status("wrong")
        return acertos, total

    def revelar_dica(self):
        vazias = [pos for pos, (ent, val) in self.respostas.items() if ent.text.strip() == ""]
        if not vazias: return False
        x, y = random.choice(vazias)
        entrada, valor = self.respostas[(x, y)]
        entrada.text = valor
        entrada.readonly = True
        entrada.set_status("hint")
        return True

    def get_total_celulas(self):
        return len(self.respostas)

# ============================================================================
# 4. TELA PRINCIPAL (Sem ScrollView, Layout Ajustado)
# ============================================================================
class CruzadinhaScreen(Screen):
    def __init__(self, dificuldade, **kwargs):
        super().__init__(**kwargs)
        self.dificuldade = dificuldade
        self.subnivel = "basico"
        self.dicas_usadas = 0
        self.dicas_max = 0
        self.pontuacao = 0

        layout = FloatLayout()

        # 1. Fundo
        fundo = Image(source="fundoapp.png", allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        layout.add_widget(fundo)

        # 2. Cabeçalho (Fixo Topo - 12% da tela)
        header = MDCard(
            size_hint=(1, 0.12),
            pos_hint={"top": 1},
            md_bg_color=(1, 1, 1, 0.85),
            elevation=2,
            radius=[0, 0, 20, 20],
            padding=[dp(5), 0]
        )

        btn_back = MDIconButton(
            icon="arrow-left",
            pos_hint={"center_y": 0.5},
            on_release=lambda x: self.voltar()
        )

        box_titulos = BoxLayout(orientation="vertical", pos_hint={"center_y": 0.5}, spacing=dp(2))
        lbl_title = MDLabel(
            text="CRUZADINHA",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_name="BungeeShade",
            font_size="22sp",
            bold=True
        )

        self.btn_nivel = MDRaisedButton(
            text="Nível: Básico",
            md_bg_color=(1, 0.5, 0, 1),
            size_hint=(None, None),
            height=dp(28),
            font_size="14sp",
            pos_hint={"center_x": 0.5}
        )
        self.menu_nivel = self.criar_menu_nivel()
        self.btn_nivel.bind(on_release=lambda x: self.menu_nivel.open())

        box_titulos.add_widget(lbl_title)

        header.add_widget(btn_back)
        header.add_widget(box_titulos)
        header.add_widget(self.btn_nivel)
        layout.add_widget(header)

        # 3. Área Central (AnchorLayout para centralizar o Grid)
        # Ocupa o espaço entre o Header (0.12) e o Footer (0.15) -> Aprox 0.73
        self.area_central = AnchorLayout(
            anchor_x='center', anchor_y='center',
            size_hint=(1, 0.73),
            pos_hint={"top": 0.88}
        )

        self.cruzadinha = CruzadinhaWidget(dificuldade=self.dificuldade, subnivel=self.subnivel)
        self.area_central.add_widget(self.cruzadinha)
        layout.add_widget(self.area_central)

        # 4. Painel Inferior (Footer - 15% da tela)
        panel = MDCard(
            size_hint=(0.96, 0.14),
            pos_hint={"center_x": 0.5, "y": 0.01},
            md_bg_color=(1, 1, 1, 0.95),
            radius=[20],
            elevation=4,
            padding=dp(10),
            spacing=dp(5)
        )

        status_box = BoxLayout(orientation="vertical", size_hint_x=0.35)
        self.lbl_pontos = MDLabel(text="Pts: 0", font_style="Caption", bold=True)
        self.lbl_dicas = MDLabel(text="Dicas: 0", font_style="Caption")
        self.lbl_info = MDLabel(text="Jogar!", font_style="Overline", theme_text_color="Custom", text_color=(0,0.5,0,1))

        status_box.add_widget(self.lbl_pontos)
        status_box.add_widget(self.lbl_dicas)
        status_box.add_widget(self.lbl_info)
        panel.add_widget(status_box)

        btns_box = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_x=0.65)

        btn_dica = MDIconButton(
            icon="lightbulb", md_bg_color=(1, 0.8, 0, 1), theme_text_color="Custom", text_color=(0,0,0,1),
            on_release=self.usar_dica
        )

        btn_novo = MDIconButton(
            icon="refresh", md_bg_color=(0.2, 0.6, 0.8, 1), theme_text_color="Custom", text_color=(1,1,1,1),
            on_release=self.nova_cruzadinha
        )

        btn_check = MDRaisedButton(
            text="OK", md_bg_color=(0.2, 0.7, 0.3, 1), text_color=(1,1,1,1),
            size_hint_x=1, # Ocupa o resto
            on_release=self.verificar
        )

        btns_box.add_widget(btn_dica)
        btns_box.add_widget(btn_novo)
        btns_box.add_widget(btn_check)
        panel.add_widget(btns_box)

        layout.add_widget(panel)
        self.add_widget(layout)

        # Inicia jogo e agenda ajuste de tamanho
        self.nova_cruzadinha()
        # Bind para quando a tela mudar de tamanho (rotação ou init)
        self.area_central.bind(size=self.ajustar_tamanho_grid)

    def criar_menu_nivel(self):
        items = [
            {"viewclass": "OneLineListItem", "text": "Básico", "on_release": lambda x="Básico": self.set_subnivel(x)},
            {"viewclass": "OneLineListItem", "text": "Intermediário", "on_release": lambda x="Intermediário": self.set_subnivel(x)},
            {"viewclass": "OneLineListItem", "text": "Avançado", "on_release": lambda x="Avançado": self.set_subnivel(x)},
        ]
        return MDDropdownMenu(caller=self.btn_nivel, items=items, width_mult=3)

    def set_subnivel(self, text):
        self.btn_nivel.text = f"Nível: {text}"
        self.menu_nivel.dismiss()
        mapa = {"Básico": "basico", "Intermediário": "intermediario", "Avançado": "avancado"}
        self.subnivel = mapa[text]
        self.nova_cruzadinha()

    def verificar(self, *args):
        acertos, total = self.cruzadinha.verificar()
        if acertos == total and total > 0:
            self.lbl_info.text = "PARABÉNS!"
            self.pontuacao += 50
        else:
            self.lbl_info.text = f"Acertos: {acertos}/{total}"
        self.atualizar_labels()

    def nova_cruzadinha(self, *args):
        self.cruzadinha.dificuldade = self.dificuldade
        self.cruzadinha.subnivel = self.subnivel
        self.cruzadinha.montar_logica()

        # Ajusta o tamanho visual assim que montar
        Clock.schedule_once(lambda dt: self.ajustar_tamanho_grid(), 0.1)

        total = self.cruzadinha.get_total_celulas()
        self.dicas_max = max(1, total // 3)
        self.dicas_usadas = 0
        self.lbl_info.text = "Novo Jogo"
        self.atualizar_labels()

    def ajustar_tamanho_grid(self, *args):
        # Pega o tamanho real disponível no AnchorLayout
        w, h = self.area_central.size
        # Manda o grid se recalcular para caber aí
        self.cruzadinha.atualizar_tamanho_celulas((w, h))

    def usar_dica(self, *args):
        if self.dicas_usadas >= self.dicas_max:
            self.lbl_info.text = "Sem dicas!"
            return
        if self.cruzadinha.revelar_dica():
            self.dicas_usadas += 1
            self.pontuacao = max(0, self.pontuacao - 5)
            self.lbl_info.text = "Dica usada"
            self.atualizar_labels()

    def atualizar_labels(self):
        self.lbl_pontos.text = f"Pts: {self.pontuacao}"
        self.lbl_dicas.text = f"Dicas: {self.dicas_max - self.dicas_usadas}"

    def voltar(self):
        if self.manager:
            self.manager.current = "jogar"