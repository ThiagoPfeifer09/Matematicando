from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDRectangleFlatButton
from kivymd.uix.slider import MDSlider
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.boxlayout import MDBoxLayout

# ---------- Utilitários ----------
class ThemeManagerMixin:
    def setup_background_and_theme_button(self, layout):
        # adiciona background (reaproveitável por telas filhas)
        self.bg_image = Image(source='fundoapp.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.bg_image)


# Botão-imagem: combina ButtonBehavior + Image
class ImageButton(ButtonBehavior, Image):
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        # restringe área clicável (10% de margem)
        x, y = touch.pos
        if (self.x + self.width * 0.1 < x < self.right - self.width * 0.1 and
                self.y + self.height * 0.1 < y < self.top - self.height * 0.1):
            # deixa ButtonBehavior tratar o evento (método herdado)
            return super(ImageButton, self).on_touch_down(touch)
        return False


# Botão-card: MDCard que responde como botão
class CardButton(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout()
        botao = MDFlatButton(
            text="Abrir Jogo",
            on_release=lambda x: print("Card clicado!")
        )
        layout.add_widget(botao)
        self.add_widget(layout)


# ---------- Tela Inicial ----------
class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.setup_background(layout)

        # Título (card)
        self.title_card = MDCard(
            orientation="vertical",
            size_hint=(0.85, None),
            height=110,
            md_bg_color=(60 / 255, 20 / 255, 100 / 255, 0.65),
            radius=[24],
            elevation=12,
            padding=[20, 10, 20, 10],
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        # note: para alinhamento vertical perfeito, setei text_size no label
        self.title_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 0.95, 0.8, 1),
            font_style="H4",
        )
        self.title_card.add_widget(self.title_label)
        layout.add_widget(self.title_card)
        self.digita_texto(self.title_label, "MATEMATICANDO")

        # Botão JOGAR (imagem)
        botao_jogar = ImageButton(
            source="jogar.png",
            size_hint=(None, None),
            size=(400, 180),
            allow_stretch=False,
            keep_ratio=True,
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        botao_jogar.bind(on_release=lambda *a: self.acao_jogar())
        layout.add_widget(botao_jogar)

        # Botão CONTEÚDOS
        botao_conteudos = ImageButton(
            source="conteudos.png",
            size_hint=(None, None),
            size=(400, 180),
            allow_stretch=False,
            keep_ratio=True,
            pos_hint={"center_x": 0.5, "center_y": 0.35},
        )
        botao_conteudos.bind(on_release=lambda *a: self.acao_conteudos())
        layout.add_widget(botao_conteudos)

        # Botão CONFIGURAÇÕES (engrenagem)
        self.settings_button = MDIconButton(
            icon="cog",
            theme_text_color="Custom",
            pos_hint={"right": 0.98, "top": 0.98},
        )
        self.settings_button.bind(on_release=self.abrir_tela_config)
        layout.add_widget(self.settings_button)

        self.add_widget(layout)

    def setup_background(self, layout):
        background = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        layout.add_widget(background)

    def digita_texto(self, label, texto, i=0):
        # implementação segura do "typewriter"
        if i <= len(texto):
            label.text = texto[:i]
            Clock.schedule_once(lambda dt: self.digita_texto(label, texto, i + 1), 0.05)

    # Ações
    def acao_jogar(self):
        if self.manager:
            self.manager.current = "seleciona"

    def acao_conteudos(self):
        if self.manager:
            self.manager.current = "conteudos"

    def abrir_tela_config(self, *args):
        if self.manager:
            self.manager.current = "config"


# ---------- Seleciona Nível ----------
class Seleciona_Nivel(Screen, ThemeManagerMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.setup_background_and_theme_button(layout)

        title = MDLabel(
            text="Selecione o nível dos jogos que deseja:",
            halign="center",
            font_style="H6",
            size_hint=(0.8, None),
            height=30,
            pos_hint={"center_x": 0.5, "top": 0.9},
            theme_text_color="Custom",
            text_color=(1, 0.8, 0, 1),
        )
        layout.add_widget(title)
        self.animate_title(title)

        btn_primario = ImageButton(
            source="primario.png",
            size_hint=(0.55, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.68},
        )
        btn_primario.bind(on_release=lambda *args: self.ir_para_jogar_p())
        layout.add_widget(btn_primario)

        btn_fundamental = ImageButton(
            source="fundamental.png",
            size_hint=(0.55, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        btn_fundamental.bind(on_release=lambda *args: self.ir_para_jogar_f())
        layout.add_widget(btn_fundamental)

        btn_medio = ImageButton(
            source="medio.png",
            size_hint=(0.55, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.32},
        )
        btn_medio.bind(on_release=lambda *args: self.ir_para_jogar())
        layout.add_widget(btn_medio)

        back_button = MDIconButton(icon='cog', pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_release=self.voltar)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def animate_title(self, label):
        anim = Animation(opacity=0.7, duration=1) + Animation(opacity=1, duration=1)
        anim.repeat = True
        anim.start(label)

    def create_card_button(self, text, center_y, callback, color, width=0.3):
        # agora usando CardButton (ButtonBehavior + MDCard)
        card = CardButton(
            size_hint=(width, 0.1),
            pos_hint={"center_x": 0.5, "center_y": center_y},
            md_bg_color=color,
            radius=[20],
            elevation=10,
        )
        label = MDLabel(
            text=text,
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size="20sp"
        )
        card.add_widget(label)
        card.bind(on_release=lambda *a: callback())
        return card

    def ir_para_jogar_p(self):
        if self.manager:
            self.manager.transition = SlideTransition(direction="left", duration=0.4)
            self.manager.current = "inicial"

    def ir_para_jogar_f(self):
        if self.manager:
            self.manager.transition = SlideTransition(direction="left", duration=0.4)
            self.manager.current = "inicial"

    def ir_para_jogar(self):
        if self.manager:
            self.manager.transition = SlideTransition(direction="left", duration=0.4)
            self.manager.current = "inicial"

    def voltar(self, instance):
        if self.manager:
            self.manager.transition = SlideTransition(direction="right", duration=0.4)
            self.manager.current = "inicial"


# ---------- Tela Conteúdos ----------
class TelaConteudos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Fundo
        background = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        layout.add_widget(background)

        topicos = [
            ("Operações", "inicial", "novo_Operacoes.png"),
            ("Álgebra", "inicial", "novo_Algebra.png"),
            ("Geometria", "inicial", "novo_Geometria.png"),
            ("Grandezas e Medidas", "inicial", "novo_Grandezas.png"),
            ("Probabilidade e Estatística", "inicial", "novo_Estatistica.png"),
        ]

        for i, (nome, tela, img) in enumerate(topicos):
            btn_img = ImageButton(
                source=img,
                size_hint=(0.4, 0.18),
                pos_hint={"center_x": 0.5, "center_y": 0.8 - i * 0.15},
                allow_stretch=True,
                keep_ratio=True,
            )
            # capture 'tela' via default arg
            btn_img.bind(on_release=lambda x, t=tela: self.abrir_topico(t))
            layout.add_widget(btn_img)

        voltar_btn = MDRaisedButton(
            text="Voltar",
            size_hint=(0.3, 0.08),
            pos_hint={"center_x": 0.5, "y": 0.05},
            md_bg_color=(0.7, 0.1, 0.2, 1),
        )
        voltar_btn.bind(on_release=lambda *a: setattr(self.manager, "current", "inicial"))
        layout.add_widget(voltar_btn)

        self.add_widget(layout)

    def abrir_topico(self, nome_tela):
        if nome_tela in self.manager.screen_names:
            self.manager.current = nome_tela
        else:
            print(f"⚠️ Tela '{nome_tela}' ainda não foi criada.")


# ---------- Tela Configurações ----------
class TelaConfiguracoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        background = Image(
            source="fundoapp.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        layout.add_widget(background)

        card = MDCard(
            orientation="vertical",
            size_hint=(0.85, 0.78),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[25],
            md_bg_color=(0.22, 0.08, 0.43, 0.9),
            padding=[30, 40, 30, 40],
            spacing=25,
            elevation=18,
        )

        conteudo = MDBoxLayout(orientation="vertical", spacing=25)

        titulo = MDLabel(
            text="CONFIGURAÇÕES",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.96, 0.92, 1, 1),
            font_style="H5",
        )
        conteudo.add_widget(titulo)

        linha_som = MDBoxLayout(orientation="horizontal", spacing=15, adaptive_height=True)
        linha_som.add_widget(MDLabel(
            text="Som ativado",
            halign="left",
            theme_text_color="Custom",
            text_color=(0.8, 0.85, 1, 1),
        ))
        self.switch_som = MDSwitch(active=True)
        linha_som.add_widget(self.switch_som)
        conteudo.add_widget(linha_som)

        self.label_volume = MDLabel(
            text=f"Volume: 75",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.5, 0.9, 1, 1),
            font_style="Subtitle1",
        )
        conteudo.add_widget(self.label_volume)

        self.slider_volume = MDSlider(min=0, max=100, value=75)
        self.slider_volume.bind(value=self.atualizar_volume)
        conteudo.add_widget(self.slider_volume)

        botao_reportar = MDRectangleFlatButton(
            text="Reportar erro",
            pos_hint={"center_x": 0.5},
        )
        botao_reportar.bind(on_release=lambda *a: self.animar_botao(botao_reportar))
        conteudo.add_widget(botao_reportar)

        botao_dev = MDRectangleFlatButton(
            text="Ver desenvolvedores",
            pos_hint={"center_x": 0.5},
        )
        botao_dev.bind(on_release=lambda *a: self.animar_botao(botao_dev))
        conteudo.add_widget(botao_dev)

        botao_voltar = MDRectangleFlatButton(
            text="Voltar",
            pos_hint={"center_x": 0.5},
        )
        botao_voltar.bind(on_release=lambda *a: self.voltar_tela_inicial())
        conteudo.add_widget(botao_voltar)

        card.add_widget(conteudo)
        layout.add_widget(card)
        self.add_widget(layout)

    def atualizar_volume(self, instance, value):
        self.label_volume.text = f"Volume: {int(value)}"

    def animar_botao(self, botao):
        anim = Animation(opacity=0.6, duration=0.1) + Animation(opacity=1, duration=0.1)
        anim.start(botao)

    def voltar_tela_inicial(self):
        if self.manager:
            self.manager.current = "inicial"


# ---------- Montador de GUI / App de teste ----------
class AppGUI:
    def build_gui(self):
        sm = ScreenManager()
        sm.add_widget(TelaInicial(name="inicial"))
        sm.add_widget(Seleciona_Nivel(name="seleciona"))
        sm.add_widget(TelaConteudos(name="conteudos"))
        sm.add_widget(TelaConfiguracoes(name="config"))
        return sm

from kivymd.app import MDApp
# Opcional: App para testar diretamente este arquivo
class DemoApp(MDApp):
    def build(self):
        gui = AppGUI()
        return gui.build_gui()


if __name__ == "__main__":
    DemoApp().run()
