from View.View import *
from Model.glc import *

class Controller:

    def __init__(self):
        self.lista_operacoes = {}

        self.view = View(self)


    # Salvar/Carregar arquivo
    def salvar_expressao(self, expressao):
        with open('Expressao.txt', 'w') as file:
            file.write(expressao.get("1.0", END))

    def carregar_expressao(self):
        with open('Expressao.txt', 'r') as file:
            return file.read()
    # -------------------------------

    # Guarda GLC
    def set_glc(self, input):
        new_glc = Glc(input.get("1.0", END).splitlines())
        self.lista_operacoes["GLC Inicial"] = new_glc
    # --------------------------------