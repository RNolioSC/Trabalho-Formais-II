from View.View import *
from Model.glc import *
from Control.EliminarRaE import *
from Control.EliminarSimbolosInuteis import *
from Control.Fatoracao import *
from Control.LGoperations import *
from Control.GLCPropria import *
from Control.FirstFollow import *

class Controller:

    # TODO MSG para avisar se possui ou não RaE

    def __init__(self):
        self.lista_operacoes = {}
        self.glc = None
        self.n_passos = 0

        self.view = View(self)


    def exec_operations(self, op):
        if op == 1:
            print(self.glc.get_dict_glc())
            resultado, nf, vi, glc_ssi, glc_ferteis = LGoperations.eh_vazia(self.glc)
            self.lista_operacoes["GLC Fértil"] = glc_ferteis
            self.lista_operacoes["GLC Final"] = glc_ssi
            self.lista_operacoes["Conjuntos gerados"] = [nf, vi]
            return resultado
        if op == 2:
            resultado, nf, vi, na, glc_sem_inuteis, glc_sem_ciclo, glc_ferteis = LGoperations.eh_finita(self.glc)
            self.lista_operacoes["GLC Fértil"] = glc_ferteis
            self.lista_operacoes["GLC Sem Ciclos"] = glc_sem_ciclo
            self.lista_operacoes["GLC Final"] = glc_sem_inuteis
            self.lista_operacoes["Conjuntos gerados"] = [nf, vi, [], na]
            return resultado
        if op == 3:
            glc_propria, glc_fertil, glc_e_livre, glc_sem_ciclo, ne, n, nf, vi = GLCPropria.glc_propria(self.glc)
            self.lista_operacoes["GLC &-livre"] = glc_e_livre
            self.lista_operacoes["GLC Sem Ciclos"] = glc_sem_ciclo
            self.lista_operacoes["GLC Fértil"] = glc_fertil
            self.lista_operacoes["GLC Final"] = glc_propria
            self.lista_operacoes["Conjuntos gerados"] = [nf, vi, ne, n]
            return glc_propria
        if op == 4:
            esta_fatorada, first, vn_nao_fatorada = Fatoracao.esta_fatorada(self.glc)
            self.lista_operacoes["First"] = first
            if vn_nao_fatorada:
                self.lista_operacoes["Vns Não Fatoradas"] = vn_nao_fatorada
            return esta_fatorada
        if op == 5:
            eh_fatoravel, glc, vn_nao_fatorada = Fatoracao.eh_fatoravel(self.glc, self.n_passos)
            self.lista_operacoes["GLC Final"] = glc
            if vn_nao_fatorada:
                self.lista_operacoes["Vns Não Fatoradas"] = vn_nao_fatorada
            return vn_nao_fatorada
        if op == 6:
            glc, rd, ri, glc_propria, glc_fertil, glc_e_livre, glc_sem_ciclos, ne, na, nf, vi = EliminarRaE.eliminar_RaE(self.glc)
            self.lista_operacoes["GLC &-livre"] = glc_e_livre
            self.lista_operacoes["GLC Sem Ciclos"] = glc_sem_ciclos
            self.lista_operacoes["GLC Fértil"] = glc_fertil
            self.lista_operacoes["GLC Própria"] = glc_propria
            self.lista_operacoes["GLC Final"] = glc
            self.lista_operacoes["Conjuntos gerados"] = [nf, vi, ne, na]
            self.lista_operacoes["Tipo de recursão"] = [rd, ri]
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
            first_nt = FirstFollow.first_nt(self.glc, first)
            self.lista_operacoes["First NT"] = first_nt
            return first_nt

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
        self.lista_operacoes = list_op

    def set_glc(self, input):
        self.glc = Glc(input.get("1.0", END).splitlines(), input.get("1.0", END).split('-')[0].replace(' ', ''))
        self.lista_operacoes["GLC Inicial"] = self.glc

    def set_glc_existente(self, glc):
        self.glc = glc

    def set_n_passos(self, n):
        self.n_passos = n
    # --------------------------------