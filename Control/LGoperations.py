from Control.EliminarSimbolosInuteis import *
from Model.glc import *

class LGoperations:

    @staticmethod
    def eh_vazia(glc):
        glc_ssi = LGoperations.eliminar_simbolos_inuteis(glc.get_dict_glc())

        if glc_ssi.get_dict_glc() == {}:
            return True
        else:
            return False

    @staticmethod
    def eh_finita(glc):
        dict_glc = LGoperations.eliminar_simbolos_inuteis(glc).get_dict_glc()
        if dict_glc == {}:
            return True
        ja_visitados = []
        novos_vn = [glc.get_estado_inicial()]
        while novos_vn:
            vn = novos_vn.pop(0)
            ja_visitados.append(vn)
            for producoes in dict_glc[vn]:
                for simbolo in producoes:
                    if simbolo in ja_visitados:
                        return False
                    elif simbolo.isupper():
                        novos_vn.append(simbolo)
        return True

    # TODO Remover futuramente ?
    @staticmethod
    def eliminar_simbolos_inuteis(glc):
        new_dict_gr, _ = EliminarSimbolosInuteis.eliminar_inferteis(glc)
        glc_ferteis = Glc(new_dict_gr, glc.get_estado_inicial())
        new_dict_gr, _ = EliminarSimbolosInuteis.eliminar_inalcancaveis(glc_ferteis)
        glc_alcancaveis = Glc(new_dict_gr, glc.get_estado_inicial())

        return glc_alcancaveis

# x = Glc({'S': [['&'], ['A', 'ab']], 'A': [['a', 'A']], 'X':[['b','A']]}, 'S')
# print(LGoperations.eh_finita(x))