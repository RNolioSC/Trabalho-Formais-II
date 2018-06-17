from Control.EliminarSimbolosInuteis import *

class LGoperations:

    @staticmethod
    def eh_vazia(glc):
        glc_ssi, nf, vi = EliminarSimbolosInuteis.eliminar_simbolos_inuteis(glc)

        if glc_ssi.get_dict_glc() == {}:
            return True, nf, vi
        else:
            return False, nf, vi

    @staticmethod
    def eh_finita(glc):
        new_glc,  nf, vi = EliminarSimbolosInuteis.eliminar_simbolos_inuteis(glc)
        dict_glc = new_glc.get_dict_glc()
        if dict_glc == {}:
            return True, nf, vi
        ja_visitados = []
        novos_vn = [glc.get_simbolo_inicial()]
        while novos_vn:
            vn = novos_vn.pop(0)
            ja_visitados.append(vn)
            for producoes in dict_glc[vn]:
                for simbolo in producoes:
                    if simbolo in ja_visitados:
                        return False, nf, vi
                    elif simbolo.isupper():
                        novos_vn.append(simbolo)
        return True, nf, vi
