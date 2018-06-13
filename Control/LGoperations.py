from Control.EliminarSimbolosInuteis import *

class LGoperations:

    @staticmethod
    def eh_vazia(glc):
        glc_ssi = EliminarSimbolosInuteis.eliminar_simbolos_inuteis(glc.get_dict_glc())

        if glc_ssi.get_dict_glc() == {}:
            return True
        else:
            return False

    @staticmethod
    def eh_finita(glc):
        dict_glc = EliminarSimbolosInuteis.eliminar_simbolos_inuteis(glc).get_dict_glc()
        if dict_glc == {}:
            return True
        ja_visitados = []
        novos_vn = [glc.get_simbolo_inicial()]
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

#x = Glc({'S': [['&'], ['A', 'ab']], 'A': [['a', 'A']], 'X':[['b','A']]}, 'S')
#print(LGoperations.eh_finita(x))