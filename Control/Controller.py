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
            resultado, nf, vi = LGoperations.eh_vazia(self.glc)
            self.lista_operacoes["Conjuntos gerados"] = [nf, vi]
            return resultado
        if op == 2:
            resultado, nf, vi = LGoperations.eh_finita(self.glc)
            self.lista_operacoes["Conjuntos gerados"] = [nf, vi]
            return resultado
        if op == 3:
            glc_propria, ne, n, nf, vi = GLCPropria.glc_propria(self.glc)
            self.lista_operacoes["Conjuntos gerados"] = [nf, vi, ne, n]
            self.lista_operacoes["GLC Final"] = glc_propria
            return glc_propria
        if op == 4:
            return Fatoracao.esta_fatorada(self.glc)
        if op == 5:
            glc, _ = Fatoracao.eh_fatoravel(self.glc, self.n_passos)
            self.lista_operacoes["GLC Final"] = glc
            return glc
        if op == 6:
            glc, rd, ri = EliminarRaE.eliminar_RaE(self.glc)
            self.lista_operacoes["Tipo de recursão"] = [rd, ri]
            self.lista_operacoes["GLC Final"] = glc
            return glc
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

    # Sets e Gets
    def get_lista_operacoes(self):
        return self.lista_operacoes

    def set_lista_operacoes(self, list_op):
        self.lista_operacoes = {}

    def set_glc(self, input):
        self.glc = Glc(input.get("1.0", END).splitlines(), input.get("1.0", END).split('-')[0].replace(' ', ''))
        self.lista_operacoes["GLC Inicial"] = self.glc

    def set_glc_existente(self, glc):
        self.glc = glc

    def set_n_passos(self, n):
        self.n_passos = n
    # --------------------------------