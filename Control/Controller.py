from View.View import *
from Model.glc import *
from Control.EliminarRaE import *
from Control.EliminarSimbolosInuteis import *
from Control.Fatoracao import *
from Control.LGoperations import *
from Control.GLCPropria import *

class Controller:

    def __init__(self):
        self.lista_operacoes = {}
        self.glc = None
        self.n_passos = 0

        self.view = View(self)


    def exec_operations(self, op):
        if op == 1:
            return LGoperations.eh_vazia(self.glc)
        if op == 2:
            return LGoperations.eh_finita(self.glc)
        if op == 3:
            return GLCPropria.glc_propria(self.glc)
        if op == 4:
            return Fatoracao.esta_fatorada(self.glc)
        if op == 5:
            return Fatoracao.eh_fatoravel(self.glc, self.n_passos)
        if op == 6:
            return EliminarRaE.eliminar_RaE(self.glc)
        if op == 7:
            pass
        if op == 8:
            pass
        if op == 9:
            pass


    # Salvar/Carregar arquivo
    def salvar_expressao(self, expressao):
        with open('Expressao.txt', 'w') as file:
            file.write(expressao.get("1.0", END))

    def carregar_expressao(self):
        with open('Expressao.txt', 'r') as file:
            return file.read()
    # -------------------------------

    # Sets
    def set_glc(self, input):
        self.glc = Glc(input.get("1.0", END).splitlines())
        self.lista_operacoes["GLC Inicial"] = self.glc

    def set_n_passos(self, n):
        self.n_passos = n
    # --------------------------------