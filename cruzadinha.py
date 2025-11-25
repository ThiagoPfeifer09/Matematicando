import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle


# ---------- GERADOR DE CONTAS COM DIFICULDADE ----------
def gerar_conta(dificuldade="fundI"):
    if dificuldade == "fundI":  # Fundamental I
        ops = ["+", "-"]
        a = random.randint(1, 20)
        b = random.randint(1, 20)

    elif dificuldade == "fundII":  # Fundamental II
        ops = ["+", "-", "*", "/"]
        a = random.randint(1, 50)
        b = random.randint(1, 50)

    elif dificuldade == "medio":  # Ensino Médio
        ops = ["+", "-", "*", "/"]
        a = random.randint(1, 100)
        b = random.randint(1, 100)

    op = random.choice(ops)

    if op == "+":
        c = a + b
    elif op == "-":
        if b > a:
            a, b = b, a
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
        if (x+i, y) in grid and grid[(x+i, y)] != ch:
            return False
    for i, ch in enumerate(conta):
        grid[(x+i, y)] = ch
    return True


def colocar_vertical(grid, x, y, conta):
    for i, ch in enumerate(conta):
        if (x, y+i) in grid and grid[(x, y+i)] != ch:
            return False
    for i, ch in enumerate(conta):
        grid[(x, y+i)] = ch
    return True


def gerar_cruzadinha(num_contas=6, dificuldade="fundI"):
    grid = {}
    contas = []

    conta = gerar_conta(dificuldade)
    colocar_horizontal(grid, 0, 0, conta)
    contas.append(("H", 0, 0, conta))

    tentativas = 0
    while len(contas) < num_contas and tentativas < num_contas*15:
        tentativas += 1
        conta = gerar_conta(dificuldade)
        orientacao = random.choice(["H", "V"])
        _, x0, y0, conta_existente = random.choice(contas)

        conectado = False
        for i, ch1 in enumerate(conta):
            for j, ch2 in enumerate(conta_existente):
                if ch1 == ch2:
                    if orientacao == "H":
                        x = x0 + j - i
                        y = y0
                        if colocar_horizontal(grid, x, y, conta):
                            contas.append(("H", x, y, conta))
                            conectado = True
                            break
                    else:
                        x = x0
                        y = y0 + j - i
                        if colocar_vertical(grid, x, y, conta):
                            contas.append(("V", x, y, conta))
                            conectado = True
                            break
            if conectado:
                break

    return grid, contas


# ---------- CÉLULAS ESTILIZADAS ----------
class CelulaFixa(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (44, 44)
        self.font_size = 22
        self.bold = True
        self.color = (1, 1, 1, 1)
        with self.canvas.before:
            Color(0.2, 0.4, 0.6, 0.9)  # azul
            self.bg = RoundedRectangle(size=self.size, pos=self.pos, radius=[8])
        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size



class CelulaEntrada(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (44, 44)
        self.font_size = 22
        self.multiline = False
        self.input_filter = "int"  # só aceita números

        # Aparência
        self.foreground_color = (0, 0, 0, 1)   # texto preto
        self.cursor_color = (0, 0, 0, 1)       # cursor preto
        self.background_color = (0.9, 0.9, 0.9, 1)  # fundo cinza claro


# ---------- WIDGET CRUZADINHA ----------
class CruzadinhaWidget(GridLayout):
    def __init__(self, dificuldade="fundI", **kwargs):
        super().__init__(**kwargs)
        self.respostas = {}
        self.dificuldade = dificuldade
        self.montar()

    def montar(self):
        self.clear_widgets()
        self.respostas.clear()

        grid, contas = gerar_cruzadinha(6, self.dificuldade)

        xs = [x for (x, y) in grid.keys()]
        ys = [y for (x, y) in grid.keys()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        self.cols = (max_x - min_x + 1)
        self.rows = (max_y - min_y + 1)
        self.spacing = 2
        self.padding = 10

        fixos = set()
        for orient, x0, y0, conta in contas:
            numeros = [i for i, ch in enumerate(conta) if ch.isdigit()]
            if len(numeros) >= 2:
                escolhidos = random.sample(numeros, 2)
                for idx in escolhidos:
                    if orient == "H":
                        fixos.add((x0+idx, y0))
                    else:
                        fixos.add((x0, y0+idx))

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
                    self.add_widget(Widget(size_hint=(None, None), size=(44, 44)))

        self.size_hint = (None, None)
        self.width = self.cols * 46
        self.height = self.rows * 46

    def verificar(self):
        acertos = 0
        for (x, y), (entrada, valor) in self.respostas.items():
            if entrada.text.strip() == valor:
                entrada.background_color = (0, 1, 0, 0.4)  # verde
                acertos += 1
            else:
                entrada.background_color = (1, 0, 0, 0.4)  # vermelho
        return acertos, len(self.respostas)


# ---------- TELA PRINCIPAL ----------
class CruzadinhaScreen(Screen):
    def __init__(self, dificuldade, **kwargs):
        super().__init__(**kwargs)
        self.dificuldade = dificuldade

        layout_principal = FloatLayout()

        fundo = Image(
            source="fundoapp.png",
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False   # pode simplesmente remover essa linha
        )
        layout_principal.add_widget(fundo)

        conteudo = BoxLayout(orientation="vertical", spacing=10, padding=10)
        layout_principal.add_widget(conteudo)

        topo = BoxLayout(size_hint=(1, 0.12), padding=10)
        topo.add_widget(Label(text="✦ Complete a Cruzadinha Matemática ✦",
                              font_size=28, color=(1, 1, 1, 1), bold=True))
        conteudo.add_widget(topo)

        meio = AnchorLayout(size_hint=(1, 0.7))
        self.cruzadinha = CruzadinhaWidget(dificuldade=self.dificuldade)
        meio.add_widget(self.cruzadinha)
        conteudo.add_widget(meio)

        base = BoxLayout(size_hint=(1, 0.18), spacing=15, padding=15)

        botao_verificar = Button(text="✅ Verificar", font_size=20,
                                 background_normal="",
                                 background_color=(0.2, 0.8, 0.2, 1),
                                 color=(1, 1, 1, 1),
                                 border=(20, 20, 20, 20))
        botao_verificar.bind(on_release=self.verificar)

        botao_novo = Button(text="🔄 Nova Cruzadinha", font_size=20,
                            background_normal="",
                            background_color=(0.2, 0.4, 0.9, 1),
                            color=(1, 1, 1, 1),
                            border=(20, 20, 20, 20))
        botao_novo.bind(on_release=self.nova_cruzadinha)

        self.resultado = Label(text="", font_size=20, color=(1, 1, 1, 1))

        base.add_widget(botao_verificar)
        base.add_widget(botao_novo)
        base.add_widget(self.resultado)

        conteudo.add_widget(base)
        self.add_widget(layout_principal)

    def verificar(self, *args):
        acertos, total = self.cruzadinha.verificar()
        self.resultado.text = f"Acertos: {acertos}/{total}"

    def nova_cruzadinha(self, *args):
        self.cruzadinha.montar()
        self.resultado.text = ""

