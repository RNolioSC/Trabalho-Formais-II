from string import punctuation
import copy

class EliminarSimbolosInuteis:

    @staticmethod
    def eliminar_inferteis(glc):
        dict_gr = glc.get_dict_gr()
        new_dict_gr = copy.deepcopy(dict_gr)

        # Conjunto N
        N = None
        tmp_N = []

        while N != tmp_N:
            N = tmp_N
            for vn in dict_gr.keys():
                for producoes in dict_gr[vn]:
                    for simbolo in producoes:
                        if (simbolo.islower() or simbolo in punctuation) and len(producoes) == 1 or simbolo in N:
                            if vn not in N:
                                tmp_N.append(vn)

        # Simbolos para eliminar
        dead_symbols = [simbolo for vn in dict_gr.keys() if vn not in N]

        # Eliminando produções com não terminais inférteis
        pos_para_eliminar = []
        for simbolo in dead_symbols:
            for vn in dict_gr.keys():
                for pos_producoes in range(len(dict_gr[vn])):
                    if simbolo in dict_gr[vn][pos_producoes]:
                        pos_para_eliminar.append(pos_producoes)
                for pos in pos_para_eliminar:
                    del new_dict_gr[vn][pos]
                pos_para_eliminar = []
            del new_dict_gr[simbolo]

        return new_dict_gr, N

    @staticmethod
    def eliminar_inalcancaveis(dict_gr):
        #dict_gr = glc.get_dict_gr()
        new_dict_gr = {}

        # Conjunto N
        N = None
        #tmp_N = [glc.get_estado_inicial()]
        tmp_N = ['S']

        while N != tmp_N:
            N = tmp_N
            for simbolo in N:
                if not simbolo.islower() and simbolo not in punctuation:
                    for producoes in dict_gr[simbolo]:
                        for char in producoes:
                            if char not in tmp_N:
                                tmp_N.append(char)

        for simbolo in N:
            if not simbolo.islower() and simbolo not in punctuation:
                new_dict_gr[simbolo] = dict_gr[simbolo]

        return new_dict_gr, N


EliminarSimbolosInuteis.eliminar_inalcancaveis({'S': [['&'], ['A', 'ab']], 'A': [['a', 'A']], 'X':[['b','X']]})