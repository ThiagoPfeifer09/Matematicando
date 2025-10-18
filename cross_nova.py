import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton
from kivymd.app import MDApp

# ---------- GERADOR DE CONTAS COM DIFICULDADE ----------
def gerar_conta(dificuldade="fundI", subnivel="basico"):
    if dificuldade == "fundI":  # Fundamental I
        ops = ["+", "-"]
        limites = {"basico": 10, "intermediario": 20, "avancado": 30}
        max_val = limites[subnivel]
        a = random.randint(1, max_val)
        b = random.randint(1, max_val)

    elif dificuldade == "fundII":  # Fundamental II
        ops = ["+", "-", "*", "/"]
        limites = {"basico": 30, "intermediario": 50, "avancado": 80}
        max_val = limites[subnivel]
        a = random.randint(1, max_val)
        b = random.randint(1, max_val)

    elif dificuldade == "medio":  # Ensino Médio
        ops = ["+", "-", "*", "/"]
        limites = {"basico": 80, "intermediario": 100, "avancado": 150}
        max_val = limites[subnivel]
        a = random.randint(1, max_val)
        b = random.randint(1, max_val)

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


def gerar_cruzadinha(dificuldade="fundI", subnivel="basico"):
    limites = {
        "fundI": (5, 7),
        "fundII": (8, 12),
        "medio": (12, 18)
    }

    min_contas, max_contas = limites.get(dificuldade, (3, 3))
    num_contas = random.randint(min_contas, max_contas)

    grid = {}
    contas = []

    conta = gerar_conta(dificuldade, subnivel)
    colocar_horizontal(grid, 0, 0, conta)
    contas.append(("H", 0, 0, conta))

    tentativas = 0
    while len(contas) < num_contas and tentativas < num_contas * 15:
        tentativas += 1
        conta = gerar_conta(dificuldade, subnivel)
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
        self.foreground_color = (0, 0, 0, 1)
        self.cursor_color = (0, 0, 0, 1)
        self.background_color = (0.9, 0.9, 0.9, 1)


class CruzadinhaWidget(GridLayout):
    def __init__(self, dificuldade="fundI", subnivel="basico", **kwargs):
        super().__init__(**kwargs)
        self.respostas = {}
        self.dificuldade = dificuldade
        self.subnivel = subnivel
        self.montar()

    def montar(self):
        self.clear_widgets()
        self.respostas.clear()

        grid, contas = gerar_cruzadinha(self.dificuldade, self.subnivel)

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

    def revelar_dica(self):
        if not self.respostas:
            return False

        posicoes = [pos for pos, (entrada, valor) in self.respostas.items() if entrada.text.strip() == ""]
        if not posicoes:
            return False

        x, y = random.choice(posicoes)
        entrada, valor = self.respostas.pop((x, y))
        entrada.text = valor
        entrada.readonly = True
        entrada.background_color = (0.6, 0.9, 1, 1)
        return True

    def get_total_celulas(self):
        return len(self.respostas)

    def get_celulas_vazias(self):
        return [pos for pos, (entrada, valor) in self.respostas.items() if entrada.text.strip() == ""]


# ---------- TELA PRINCIPAL ----------
class CruzadinhaScreen(Screen):
    def __init__(self, dificuldade, **kwargs):
        super().__init__(**kwargs)
        self.dificuldade = dificuldade
        self.subnivel = "basico"
        self.dicas_usadas = 0
        self.dicas_max = 0
        self.pontuacao = 0  # <<< sistema de pontos

        layout_principal = FloatLayout()

        # FUNDO
        fundo = Image(source="fundoapp.png", size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        layout_principal.add_widget(fundo)

        conteudo = BoxLayout(orientation="vertical", spacing=10, padding=10)
        layout_principal.add_widget(conteudo)

        # TOPO
        topo = BoxLayout(size_hint=(1, 0.12), padding=10, spacing=15)
        topo.add_widget(Label(
            text="Complete a Cruzadinha Matemática",
            font_size=28, color=(1, 1, 1, 1), bold=True
        ))

        # DROPDOWN SUBNÍVEL
        self.subnivel_button = MDRaisedButton(
            text="Básico", size_hint=(None, None), size=("160dp", "48dp"),
            md_bg_color=(1.0, 111/255, 64/255, 1)
        )
        menu_items = [
            {"viewclass": "OneLineListItem", "text": "Básico", "on_release": lambda x="Básico": self.set_subnivel(x)},
            {"viewclass": "OneLineListItem", "text": "Intermediário", "on_release": lambda x="Intermediário": self.set_subnivel(x)},
            {"viewclass": "OneLineListItem", "text": "Avançado", "on_release": lambda x="Avançado": self.set_subnivel(x)},
        ]
        self.menu = MDDropdownMenu(caller=self.subnivel_button, items=menu_items, width_mult=4)
        self.subnivel_button.bind(on_release=lambda x: self.menu.open())
        topo.add_widget(self.subnivel_button)

        conteudo.add_widget(topo)

        # MEIO
        meio = AnchorLayout(size_hint=(1, 0.7))
        self.cruzadinha = CruzadinhaWidget(dificuldade=self.dificuldade, subnivel=self.subnivel)
        meio.add_widget(self.cruzadinha)
        conteudo.add_widget(meio)

        # BASE
        base = BoxLayout(size_hint=(1, 0.18), spacing=15, padding=15)

        # Botão verificar
        botao_verificar = MDRaisedButton(
            text="Verificar", md_bg_color=(0.59, 0.43, 0.91, 1),
            text_color=(1, 1, 1, 1), font_size=20
        )
        botao_verificar.bind(on_release=self.verificar)

        # Botão nova cruzadinha
        botao_novo = MDRaisedButton(
            text="Nova Cruzadinha", md_bg_color=(0.36, 0.8, 0.96, 1),
            text_color=(1, 1, 1, 1), font_size=20
        )
        botao_novo.bind(on_release=self.nova_cruzadinha)

        # Botão de dica
        botao_dica = MDRaisedButton(
            text="Dica 💡", md_bg_color=(1, 0.76, 0.03, 1),
            text_color=(0, 0, 0, 1), font_size=20
        )
        botao_dica.bind(on_release=self.usar_dica)

        # Labels de status
        self.resultado = Label(text="", font_size=20, color=(1, 1, 1, 1))
        self.dicas_label = Label(text="Dicas: 0", font_size=18, color=(1, 1, 1, 1))
        self.pontuacao_label = Label(text="Pontuação: 0", font_size=20, color=(1, 1, 1, 1))  # <<< NOVO

        # Adiciona botões na base
        base.add_widget(botao_verificar)
        base.add_widget(botao_novo)
        base.add_widget(botao_dica)
        base.add_widget(self.dicas_label)
        base.add_widget(self.resultado)
        base.add_widget(self.pontuacao_label)  # <<< NOVO

        conteudo.add_widget(base)
        self.add_widget(layout_principal)

        # Inicializa dicas
        self.nova_cruzadinha()

    def set_subnivel(self, text):
        self.subnivel_button.text = text
        self.menu.dismiss()
        mapa = {"Básico": "basico", "Intermediário": "intermediario", "Avançado": "avancado"}
        self.subnivel = mapa[text]
        self.nova_cruzadinha()

    def verificar(self, *args):
        acertos, total = self.cruzadinha.verificar()
        self.resultado.text = f"Acertos: {acertos}/{total}"

        # Atualiza pontuação
        pontos_ganhos = acertos * 10
        pontos_perdidos = (total - acertos) * 5
        self.pontuacao += pontos_ganhos - pontos_perdidos
        if self.pontuacao < 0:
            self.pontuacao = 0
        self.atualizar_pontuacao()

    def nova_cruzadinha(self, *args):
        self.cruzadinha.dificuldade = self.dificuldade
        self.cruzadinha.subnivel = self.subnivel
        self.cruzadinha.montar()

        total_celulas = self.cruzadinha.get_total_celulas()
        self.dicas_usadas = 0
        self.dicas_max = max(0, total_celulas // 2) if total_celulas > 1 else 0
        self.resultado.text = ""
        self.atualizar_dicas_label()

    def usar_dica(self, *args):
        if self.dicas_usadas >= self.dicas_max:
            self.resultado.text = "Sem dicas restantes!"
            return

        revelado = self.cruzadinha.revelar_dica()
        if revelado:
            self.dicas_usadas += 1
            self.resultado.text = "Dica usada!"
            # Desconta pontos por usar dica
            self.pontuacao -= 5
            if self.pontuacao < 0:
                self.pontuacao = 0
            self.atualizar_pontuacao()
        else:
            self.resultado.text = "Nenhuma célula disponível."

        self.atualizar_dicas_label()

    def atualizar_dicas_label(self):
        self.dicas_label.text = f"Dicas restantes: {self.dicas_max - self.dicas_usadas}"

    def atualizar_pontuacao(self):
        self.pontuacao_label.text = f"Pontuação: {self.pontuacao}"

