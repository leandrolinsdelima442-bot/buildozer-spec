import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Fundo preto para combinar com o estilo Pro
Window.clearcolor = (0, 0, 0, 1)

class SuperMatrizKarma(App):
    def build(self):
        self.loterias = self.gerar_jogos()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Seletor de Jogo (140 jogos e países como você pediu)
        self.spinner = Spinner(
            text="00001 - Brasil - Mega-Sena", 
            values=list(self.loterias.keys()), 
            size_hint_y=None, 
            height=50
        )
        self.spinner.bind(text=self.mudar_jogo)
        layout.add_widget(self.spinner)

        # Espaço para digitar os números
        self.grid_inputs = GridLayout(cols=10, size_hint_y=None, height=100, spacing=5)
        layout.add_widget(self.grid_inputs)
        self.inputs = []

        # Botão para calcular o Karma
        btn = Button(text="CALCULAR KARMA", size_hint_y=None, height=60, background_color=(0, 1, 0, 1))
        btn.bind(on_release=self.calcular)
        layout.add_widget(btn)

        # Área da Matriz Resultante
        scroll = ScrollView()
        self.grid_matriz = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.grid_matriz.bind(minimum_height=self.grid_matriz.setter('height'))
        scroll.add_widget(self.grid_matriz)
        layout.add_widget(scroll)
        self.labels_karma = []

        self.mudar_jogo(None, self.spinner.text)
        return layout

    def gerar_jogos(self):
        # Aqui simulamos a sua base de dados de 140 jogos/países
        base = {"00001 - Brasil - Mega-Sena": 6}
        paises = ["EUA", "França", "Japão", "Brasil", "Itália", "Portugal", "Angola"]
        for i in range(2, 141):
            base[f"{i:05d} - {random.choice(paises)} - Lotto"] = random.choice([5, 6, 15])
        return base

    def mudar_jogo(self, spinner, text):
        qtd = self.loterias[text]
        self.grid_inputs.clear_widgets()
        self.grid_matriz.clear_widgets()
        self.grid_matriz.cols = qtd + 1
        self.inputs = []
        self.labels_karma = []
        
        for _ in range(qtd):
            ti = TextInput(input_filter='int', halign='center', multiline=False)
            self.grid_inputs.add_widget(ti)
            self.inputs.append(ti)
            
        niveis = ["+2", "+1", "K0", "-1", "-2", "-3"]
        for r in range(6):
            self.grid_matriz.add_widget(Label(text=niveis[r], size_hint_y=None, height=40, color=(0,1,0,1)))
            for _ in range(qtd):
                lbl = Label(text="-", size_hint_y=None, height=40)
                self.grid_matriz.add_widget(lbl)
                self.labels_karma.append(lbl)

    def calcular(self, instance):
        try:
            dezenas = [int(ti.text) % 10 for ti in self.inputs if ti.text]
            if not dezenas: return
            ajs, qtd = [2, 1, 0, 9, 8, 7], len(dezenas)
            for r in range(6):
                for c in range(qtd):
                    res = (dezenas[c] + ajs[r]) % 10
                    self.labels_karma[(r * qtd) + c].text = str(res)
        except:
            pass

if __name__ == '__main__':
    SuperMatrizKarma().run()
