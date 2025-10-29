from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.slider import MDSlider
from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton

# =================== TELA PRINCIPAL ÁLGEBRA ===================
class GrandezasTela(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Fundo
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        layout.add_widget(fundo)

        # Título
        self.title_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(self.title_label)
        self.digita_texto(self.title_label, "GRANDEZAS E MEDIDAS")

        # Botão voltar
        self.back_button = MDIconButton(
            icon='arrow-left',
            pos_hint={'x': 0, 'top': 1},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # cor branca
            on_release=lambda x: self.voltar("conteudos")
        )
        layout.add_widget(self.back_button)

        # Boneco
        boneco = Image(
            source="Boneco_Grandezas.png",
            size_hint=(0.47, 0.47),
            pos_hint={"center_x": 0.5, "center_y": 0.65}
        )
        layout.add_widget(boneco)

        # Botões principais
        btn_representacoes = self.create_card_button(
            "Representações",
            0.3, 0.35,
            lambda: self.ir_para("grandezas_representacoes")
        )
        btn_definicoes = self.create_card_button(
            "Definições",
            0.3, 0.2,
            lambda: self.ir_para("grandezas_definicoes")
        )

        layout.add_widget(btn_representacoes)
        layout.add_widget(btn_definicoes)
        self.add_widget(layout)

    # Funções auxiliares
    def digita_texto(self, label, texto, i=0):
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i + 1), 0.05)


    def create_card_button(self, text, x, y, callback):
        card = MDCard(
            size_hint=(0.4, 0.08),
            pos_hint={"x": x, "y": y},
            md_bg_color=(0.2, 0.2, 0.6, 0.85),
            radius=[20],
            elevation=10,
            ripple_behavior=True
        )
        label = MDLabel(
            text=text,
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size="18sp"
        )
        card.add_widget(label)
        card.bind(on_release=lambda *a: callback())
        return card


    def ir_para(self, tela_nome):
        self.manager.transition = SlideTransition(direction="left", duration=0.4)
        self.manager.current = tela_nome

    def voltar(self, tela_nome):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = tela_nome


# =================== TELA DEFINIÇÕES ===================
class DefinicoesGrandezas(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Fundo
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        layout.add_widget(fundo)

        # Título
        self.title_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        layout.add_widget(self.title_label)
        self.digita_texto(self.title_label, "DEFINIÇÕES GEOMETRIA")

        # Lista de imagens (uma para cada operação)
        imagens = [
            "quadrado.jpeg",
            "triangulo.jpeg",
            "circulo.jpeg",
            "retangulo.jpeg"
        ]

        pos_y = [0.68, 0.68, 0.30, 0.30]
        pos_x = [0.26, 0.74, 0.26, 0.74]

        for i, img in enumerate(imagens):
            card = MDCard(
                size_hint=(0.45, 0.32),
                pos_hint={"center_x": pos_x[i], "center_y": pos_y[i]},
                radius=[20],
                elevation=10,
                orientation="vertical"
            )

            # Imagem dentro do card
            card.add_widget(Image(
                source=img,
                allow_stretch=True,
                keep_ratio=False
            ))

            layout.add_widget(card)

        # Botão voltar
        btn_voltar = MDCard(
            size_hint=(0.18, 0.06),
            pos_hint={"x": 0.05, "y": 0.05},
            md_bg_color=(0.2, 0.2, 0.6, 0.85),
            radius=[20],
            elevation=10,
            ripple_behavior=True
        )
        btn_voltar.add_widget(MDLabel(
            text="Voltar",
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        ))
        btn_voltar.on_release = lambda *a: self.voltar()
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def digita_texto(self, label, texto, i=0):
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i+1), 0.05)

    def voltar(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "grandezas_tela"





class GrandezasRepresentacoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = FloatLayout()

        # ================== FUNDO ==================
        fundo = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        root.add_widget(fundo)

        # ================== LAYOUT PRINCIPAL ==================
        main_box = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=[20, 80, 20, 20],
            size_hint=(1, 0.9),
            pos_hint={"center_x": 0.5, "center_y": 0.45}
        )

        # ================== CARD EXPLICATIVO (com passo a passo didático) ==================
        self.card_explicacao = MDCard(
            orientation="vertical",
            size_hint=(1, 0.35),
            elevation=10,
            radius=[25],
            md_bg_color=(1, 1, 1, 0.9),
            padding=20,
            spacing=10
        )

        self.label_titulo = MDLabel(
            text="Selecione uma grandeza e veja suas representações e conversões:",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="Subtitle1"
        )
        self.label_detalhe = MDLabel(
            text="",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="Body1"
        )
        self.label_passo_a_passo = MDLabel(
            text="[i]O passo a passo das conversões aparecerá aqui automaticamente.[/i]",
            halign="left",
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            font_style="Body1",
            markup=True
        )

        self.card_explicacao.add_widget(self.label_titulo)
        self.card_explicacao.add_widget(self.label_detalhe)
        self.card_explicacao.add_widget(self.label_passo_a_passo)

        # ================== CARD INTERATIVO (CENTRAL) ==================
        interativo_box = BoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint=(1, 0.45)
        )

        # --- CARD ESQUERDA (IMAGEM + TEXTO EXPLICATIVO) ---
        self.card_imagem = MDCard(
            orientation="vertical",
            size_hint=(0.5, 1),
            radius=[25],
            elevation=10,
            md_bg_color=(1, 1, 1, 0.9),
            padding=15,
            spacing=10
        )
        self.imagem_representacao = Image(
            source="",
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 0.8)
        )
        self.label_explicacao_figura = MDLabel(
            text="Selecione uma grandeza para ver uma ilustração e entender melhor o conceito.",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="Body2"
        )
        self.card_imagem.add_widget(self.imagem_representacao)
        self.card_imagem.add_widget(self.label_explicacao_figura)

        # --- CARD DIREITA (INTERAÇÃO) ---
        self.card_interativo = MDCard(
            orientation="vertical",
            size_hint=(0.5, 1),
            radius=[25],
            elevation=10,
            md_bg_color=(1, 1, 1, 0.9),
            padding=20,
            spacing=10
        )

        self.label_input = MDLabel(
            text="Digite ou escolha um valor para converter:",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )

        self.input_valor = MDTextField(
            hint_text="Ex: 5",
            mode="rectangle",
            helper_text="Valor a converter",
            helper_text_mode="on_focus",
            size_hint_x=0.7
        )
        self.input_valor.bind(text=self.atualizar_conversao)

        self.slider_valor = MDSlider(
            min=0,
            max=100,
            value=10,
            step=1,
            size_hint_x=0.9
        )
        self.slider_valor.bind(value=self.atualizar_slider)

        self.label_resultados = MDLabel(
            text="Resultados: —",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="Body1"
        )

        self.card_interativo.add_widget(self.label_input)
        self.card_interativo.add_widget(self.input_valor)
        self.card_interativo.add_widget(self.slider_valor)
        self.card_interativo.add_widget(self.label_resultados)

        interativo_box.add_widget(self.card_imagem)
        interativo_box.add_widget(self.card_interativo)

        # ================== BOTÕES ==================
        botoes_box = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(1, 0.2)
        )
        grandezas = [
            ("Comprimento", "regua.png", "O comprimento mede distâncias, como metros e quilômetros."),
            ("Massa", "balanca.png", "A massa indica a quantidade de matéria em um corpo, medida em kg ou g."),
            ("Tempo", "relogio.png", "O tempo é medido em segundos, minutos e horas."),
            ("Volume", "jarra.png", "O volume indica a capacidade de um recipiente, medida em litros."),
            ("Temperatura", "termometro.png", "A temperatura mede o grau de calor de um corpo, em °C, °F ou K.")
        ]

        for nome, img, explicacao in grandezas:
            btn = MDFillRoundFlatIconButton(
                text=nome,
                icon="information",
                md_bg_color=(0.2, 0.4, 0.7, 1),
                text_color=(1, 1, 1, 1),
                on_release=lambda x, n=nome, i=img, e=explicacao: self.selecionar_grandeza(n, i, e)
            )
            botoes_box.add_widget(btn)

        # ================== MONTAGEM FINAL ==================
        main_box.add_widget(self.card_explicacao)
        main_box.add_widget(interativo_box)
        main_box.add_widget(botoes_box)
        root.add_widget(main_box)

        # ================== TÍTULO E VOLTAR ==================
        titulo = MDLabel(
            text="📏 Grandezas e Representações",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H5",
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.98}
        )
        back_button = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={'x': 0, 'top': 0.98},
            on_release=lambda x: self.voltar("grandezas_tela")
        )
        root.add_widget(titulo)
        root.add_widget(back_button)

        self.add_widget(root)

        # ================== VARIÁVEIS DE CONTROLE ==================
        self.grandeza_atual = None


    # ======================================================
    # FUNÇÕES DE AÇÃO
    # ======================================================
    def selecionar_grandeza(self, nome, imagem, explicacao):
        self.grandeza_atual = nome
        self.imagem_representacao.source = imagem
        self.label_explicacao_figura.text = explicacao

        # Texto introdutório e fórmula base
        if nome == "Comprimento":
            self.label_detalhe.text = "1 metro = 100 centímetros"
        elif nome == "Massa":
            self.label_detalhe.text = "1 quilograma = 1000 gramas"
        elif nome == "Tempo":
            self.label_detalhe.text = "1 hora = 60 minutos"
        elif nome == "Volume":
            self.label_detalhe.text = "1 litro = 1000 mililitros"
        elif nome == "Temperatura":
            self.label_detalhe.text = "Conversões: °C ↔ °F ↔ K"
        else:
            self.label_detalhe.text = ""

        self.label_titulo.text = f"Grandeza: {nome}"
        self.label_resultados.text = "Resultados: —"
        self.label_passo_a_passo.text = "[i]Digite um valor para ver o passo a passo da conversão.[/i]"


        # ================== FUNÇÃO: QUANDO O SLIDER MUDA ==================
    def atualizar_slider(self, instance, value):
        self.input_valor.text = str(int(value))
        self.calcular_resultados(value)

    # ================== FUNÇÃO: QUANDO O TEXTO MUDA ==================
    def atualizar_conversao(self, instance, text):
        try:
            valor = float(text)
            self.slider_valor.value = valor
            self.calcular_resultados(valor)
        except ValueError:
            self.label_resultados.text = "Resultados: —"
            self.label_passo_a_passo.text = "[i]Digite um valor válido.[/i]"


    # ================== FUNÇÃO: CALCULAR E MOSTRAR O PASSO A PASSO ==================
    def calcular_resultados(self, valor):
        if not self.grandeza_atual:
            self.label_resultados.text = "Resultados: —"
            self.label_passo_a_passo.text = "[i]Selecione uma grandeza primeiro.[/i]"
            return

        g = self.grandeza_atual

        if g == "Comprimento":
            cm = valor * 100
            self.label_resultados.text = f"Resultados: {valor} m = {cm:.0f} cm"
            self.label_passo_a_passo.text = (
                f"[b]Passo a passo:[/b]\n"
                f"1️⃣ Sabemos que 1 metro tem 100 centímetros.\n"
                f"2️⃣ Para converter metros em centímetros, multiplicamos por 100.\n"
                f"3️⃣ {valor} × 100 = {cm:.0f} cm.\n"
                f"✅ Portanto, {valor} m = {cm:.0f} cm."
            )

        elif g == "Massa":
            g_total = valor * 1000
            self.label_resultados.text = f"Resultados: {valor} kg = {g_total:.0f} g"
            self.label_passo_a_passo.text = (
                f"[b]Passo a passo:[/b]\n"
                f"1️⃣ 1 quilograma tem 1000 gramas.\n"
                f"2️⃣ Para transformar quilogramas em gramas, multiplicamos por 1000.\n"
                f"3️⃣ {valor} × 1000 = {g_total:.0f} g.\n"
                f"✅ Portanto, {valor} kg = {g_total:.0f} g."
            )

        elif g == "Tempo":
            minutos = valor * 60
            self.label_resultados.text = f"Resultados: {valor} h = {minutos:.0f} min"
            self.label_passo_a_passo.text = (
                f"[b]Passo a passo:[/b]\n"
                f"1️⃣ 1 hora tem 60 minutos.\n"
                f"2️⃣ Para converter horas em minutos, multiplicamos por 60.\n"
                f"3️⃣ {valor} × 60 = {minutos:.0f} min.\n"
                f"✅ Portanto, {valor} h = {minutos:.0f} min."
            )

        elif g == "Volume":
            ml = valor * 1000
            self.label_resultados.text = f"Resultados: {valor} L = {ml:.0f} mL"
            self.label_passo_a_passo.text = (
                f"[b]Passo a passo:[/b]\n"
                f"1️⃣ 1 litro tem 1000 mililitros.\n"
                f"2️⃣ Para converter litros em mililitros, multiplicamos por 1000.\n"
                f"3️⃣ {valor} × 1000 = {ml:.0f} mL.\n"
                f"✅ Portanto, {valor} L = {ml:.0f} mL."
            )

        elif g == "Temperatura":
            fahrenheit = valor * 9 / 5 + 32
            kelvin = valor + 273.15
            self.label_resultados.text = f"Resultados: {valor} °C = {fahrenheit:.1f} °F | {kelvin:.2f} K"
            self.label_passo_a_passo.text = (
                f"[b]Passo a passo:[/b]\n"
                f"1️⃣ Para converter °C → °F, usamos a fórmula: (°C × 9/5) + 32.\n"
                f"2️⃣ Para °C → K, somamos 273.15.\n"
                f"3️⃣ {valor} × 9/5 + 32 = {fahrenheit:.1f} °F.\n"
                f"4️⃣ {valor} + 273.15 = {kelvin:.2f} K.\n"
                f"✅ Portanto, {valor} °C = {fahrenheit:.1f} °F e {kelvin:.2f} K."
            )

    def voltar(self, tela_anterior):
        self.manager.current = tela_anterior