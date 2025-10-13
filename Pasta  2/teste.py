from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivy.uix.behaviors import ButtonBehavior

# --- Botão de imagem básico ---
class ImageButton(ButtonBehavior, Image):
    pass


# --- Tela inicial ---
class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.setup_background(layout)

        # --- Título ---
        self.title_card = MDCard(
            orientation="vertical",
            size_hint=(0.85, None),
            height=110,
            md_bg_color=(60/255, 20/255, 100/255, 0.65),
            radius=[24],
            elevation=12,
            padding=[20, 10, 20, 10],
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        self.title_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 0.95, 0.8, 1),
            font_style="H4",
            valign="middle",
        )
        self.title_card.add_widget(self.title_label)
        layout.add_widget(self.title_card)
        self.digita_texto(self.title_label, "MATEMATICANDO")

        # --- Botão JOGAR ---
        botao_jogar = ImageButton(
            source="jogar.png",
            size_hint=(0.55, 0.25),
            on_release=lambda *a: self.acao_jogar(),
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )
        layout.add_widget(botao_jogar)

        # --- Botão CONTEÚDOS ---
        botao_conteudos = ImageButton(
            source="conteudos.png",
            size_hint=(0.75, 0.55),
            on_release=lambda *a: self.acao_conteudos(),
            pos_hint={"center_x": 0.5, "center_y": 0.35}
        )
        layout.add_widget(botao_conteudos)

        # --- Botão CONFIGURAÇÕES (engrenagem) ---
        self.settings_button = MDIconButton(
            icon="cog",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={"right": 0.98, "top": 0.98},
            on_release=self.abrir_menu_config
        )
        layout.add_widget(self.settings_button)

        self.add_widget(layout)

        # --- Menu dropdown ---
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Desenvolvedores",
                "on_release": lambda: self.mostrar_dev(),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Música: Ligar/Desligar",
                "on_release": lambda: self.toggle_musica(),
            },
        ]
        self.menu = MDDropdownMenu(
            caller=self.settings_button,
            items=menu_items,
            width_mult=4,
        )

    def setup_background(self, layout):
        background = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        layout.add_widget(background)

    def digita_texto(self, label, texto, i=0):
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i+1), 0.05)

    # --- Ações ---
    def acao_jogar(self):
        print("👉 Ir para tela de seleção de jogos")

    def acao_conteudos(self):
        self.manager.current = "conteudos"

    def mostrar_dev(self):
        print("👨‍💻 Mostrar tela de desenvolvedores")
        self.menu.dismiss()

    def toggle_musica(self):
        print("🎵 Alternar música ON/OFF")
        self.menu.dismiss()

    def abrir_menu_config(self, *args):
        self.menu.open()

# --- Tela de Conteúdos ---
class TelaConteudos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        background = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        layout.add_widget(background)

        # Lista de tópicos com suas telas correspondentes
        topicos = [
            ("Operações", "meia_tela"),     # já criada
            ("Álgebra", "algebra_tela"),    # você cria depois
            ("Geometria", "geometria_tela"),
            ("Grandezas e Medidas", "grandezas_tela"),
            ("Probabilidade e Estatística", "estatistica_tela"),
        ]

        # Criar botões
        for i, (nome, tela) in enumerate(topicos):
            btn = MDRaisedButton(
                text=nome,
                size_hint=(0.6, 0.1),
                pos_hint={"center_x": 0.5, "center_y": 0.8 - i*0.15},
                md_bg_color=(0.3, 0.2, 0.6, 1),
                text_color=(1, 1, 1, 1),
                on_release=lambda x, t=tela: self.abrir_topico(t)
            )
            layout.add_widget(btn)

        # Botão voltar
        voltar_btn = MDRaisedButton(
            text="Voltar",
            size_hint=(0.3, 0.08),
            pos_hint={"center_x": 0.5, "y": 0.05},
            md_bg_color=(0.7, 0.1, 0.2, 1),
            text_color=(1, 1, 1, 1),
            on_release=lambda *a: setattr(self.manager, "current", "inicio")
        )
        layout.add_widget(voltar_btn)

        self.add_widget(layout)

    def abrir_topico(self, nome_tela):
        if nome_tela in self.manager.screen_names:
            self.manager.current = nome_tela
        else:
            print(f"⚠️ Tela '{nome_tela}' ainda não foi criada.")

from meia_tela import MeiaTela, TelaRepresentacoes, DefinicoesTela
from meia_algebra import AlgebraTela, AlgebraRepresentacoes, AlgebraDefinicoes
# --- App base ---
class MobileApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TelaInicial(name="inicio"))
        sm.add_widget(TelaConteudos(name="conteudos"))
        sm.add_widget(MeiaTela(name="meia_tela"))
        sm.add_widget(TelaRepresentacoes(name="representacoes"))
        sm.add_widget(DefinicoesTela(name="definicoes"))
        sm.add_widget(AlgebraTela(name="algebra_tela"))
        sm.add_widget(AlgebraRepresentacoes(name="algebra_representacoes"))
        sm.add_widget(AlgebraDefinicoes(name="algebra_definicoes"))
        return sm


if __name__ == "__main__":
    MobileApp().run()
