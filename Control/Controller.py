from View.View import *
from Model.glc import *
from Control.EliminarRaE import *
from Control.EliminarSimbolosInuteis import *
from Control.Fatoracao import *
from Control.LGoperations import *
from Control.GLCPropria import *
from Control.FirstFollow import *

class Controller:

    # TODO Executar o algoritmo da gramática própria antes de executar a RaE
    # TODO Expandir tamanho dos input/output
    # TODO Add exceções onde necessário

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
            glc_propria, glc_e_livre, glc_sem_ciclo, ne, n, nf, vi = GLCPropria.glc_propria(self.glc)
            self.lista_operacoes["GLC &-livre"] = glc_e_livre
            self.lista_operacoes["GLC Sem Ciclos"] = glc_sem_ciclo
            self.lista_operacoes["Conjuntos gerados"] = [nf, vi, ne, n]
            self.lista_operacoes["GLC Final"] = glc_propria
            return glc_propria
        if op == 4:
            esta_fatorada, first, vn_nao_fatorada = Fatoracao.esta_fatorada(self.glc)
            self.lista_operacoes["First"] = first
            if vn_nao_fatorada:
                self.lista_operacoes["Vns Não Fatoradas"] = vn_nao_fatorada
            return esta_fatorada
        if op == 5:
            eh_fatoravel, glc = Fatoracao.eh_fatoravel(self.glc, self.n_passos)
            self.lista_operacoes["GLC Final"] = glc
            return glc
        if op == 6:
            glc, rd, ri = EliminarRaE.eliminar_RaE(self.glc)
            self.lista_operacoes["Tipo de recursão"] = [rd, ri]
            self.lista_operacoes["GLC Final"] = glc
            return glc
        if op == 7:
            first = FirstFollow.first(self.glc)
            self.lista_operacoes["First"] = first
            return first
        if op == 8:
            first = FirstFollow.first(self.glc)
            self.lista_operacoes["First"] = first
            follow = FirstFollow.follow(self.glc, first)
            self.lista_operacoes["Follow"] = follow
            return follow
        if op == 9:
            first = FirstFollow.first(self.glc)
            self.lista_operacoes["First"] = first


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