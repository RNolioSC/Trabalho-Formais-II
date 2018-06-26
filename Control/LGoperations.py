from Control.EliminarSimbolosInuteis import *
from Control.GLCPropria import *

class LGoperations:

    @staticmethod
    def eh_vazia(glc):
        glc_ssi, glc_ferteis, nf, vi = EliminarSimbolosInuteis.eliminar_simbolos_inuteis(glc)

        if glc_ssi.get_dict_glc() == {}:
            return True, nf, vi, glc_ssi, glc_ferteis
        else:
            return False, nf, vi, glc_ssi, glc_ferteis

    @staticmethod
    def eh_finita(glc):
        glc_sem_ciclo, na = GLCPropria.remove_ciclos(glc)

        glc_sem_inuteis, glc_ferteis, nf, vi = EliminarSimbolosInuteis.eliminar_simbolos_inuteis(glc_sem_ciclo)

        dict_glc = glc_sem_inuteis.get_dict_glc()

        if dict_glc == {}:
            return True, nf, vi, na, glc_sem_inuteis, glc_sem_ciclo, glc_ferteis

        ja_visitados = []
        novos_vn = [glc.get_simbolo_inicial()]
        while novos_vn:
            vn = novos_vn.pop(0)
            ja_visitados.append(vn)
            for producoes in dict_glc[vn]:
                for simbolo in producoes:
                    if simbolo in ja_visitados:
                        return False, nf, vi, na, glc_sem_inuteis, glc_sem_ciclo, glc_ferteis
                    elif simbolo.isupper():
                        novos_vn.append(simbolo)
        return True, nf, vi, na, glc_sem_inuteis, glc_sem_ciclo, glc_ferteis
