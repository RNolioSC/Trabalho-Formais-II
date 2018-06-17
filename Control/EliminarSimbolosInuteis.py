from Model.glc import *
from string import punctuation
import copy


class EliminarSimbolosInuteis:

    @staticmethod
    def eliminar_simbolos_inuteis(glc):
        glc_ferteis, Nf = EliminarSimbolosInuteis.eliminar_inferteis(glc)

        # Verifica se não foi eliminado todas as produções
        if glc_ferteis.get_dict_glc() == {}:
            return glc_ferteis, Nf, []

        glc_alcancaveis, Vi = EliminarSimbolosInuteis.eliminar_inalcancaveis(glc_ferteis)

        return glc_alcancaveis, Nf, Vi

    @staticmethod
    def eliminar_inferteis(glc):
        dict_gr = glc.get_dict_glc()
        new_dict_glc = copy.deepcopy(dict_gr)

        # Conjunto N
        N = None
        tmp_N = []

        while N != tmp_N:
            N = tmp_N.copy()
            for vn in dict_gr.keys():
                for producoes in dict_gr[vn]:
                    for simbolo in producoes:
                        if (simbolo.islower() or simbolo in punctuation) and len(producoes) == 1 or simbolo in N:
                            if vn not in tmp_N:
                                tmp_N.append(vn)

        # Simbolos para eliminar
        dead_symbols = [vn for vn in dict_gr.keys() if vn not in N]

        # Eliminando produções com não terminais inférteis
        pos_para_eliminar = []
        for simbolo in dead_symbols:
            for vn in dict_gr.keys():
                if vn not in dead_symbols:
                    for pos_producoes in range(len(dict_gr[vn])):
                        if simbolo in dict_gr[vn][pos_producoes]:
                            pos_para_eliminar.append(pos_producoes)
                    for pos in pos_para_eliminar:
                        del new_dict_glc[vn][pos]
                    pos_para_eliminar = []
            del new_dict_glc[simbolo]

        return Glc(new_dict_glc, glc.get_simbolo_inicial()), N

    @staticmethod
    def eliminar_inalcancaveis(glc):
        dict_glc = glc.get_dict_glc()
        new_dict_glc = {}

        # Conjunto N
        N = None
        tmp_N = [glc.get_simbolo_inicial()]

        while N != tmp_N:
            N = tmp_N.copy()
            for simbolo in N:
                if not simbolo.islower() and simbolo not in punctuation:
                    for producoes in dict_glc[simbolo]:
                        for char in producoes:
                            if char not in tmp_N:
                                tmp_N.append(char)

        for simbolo in N:
            if not simbolo.islower() and simbolo not in punctuation:
                new_dict_glc[simbolo] = dict_glc[simbolo]

        return Glc(new_dict_glc, glc.get_simbolo_inicial()), N