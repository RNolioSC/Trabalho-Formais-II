from Model.glc import *
import copy


class EliminarRaE:

    @staticmethod
    def eliminar_RaE(glc):

        # Verifica se tem recursão a esquerda direta/indireta
        rec_direta, rec_indireta = EliminarRaE.verificar_recursao(glc)
        if not(rec_direta or len(rec_indireta.values()) != 0):
            return glc, rec_direta, rec_indireta

        dict_glc = glc.get_dict_glc()
        new_dict_glc = copy.deepcopy(dict_glc)
        tmp_dict_glc = copy.deepcopy(new_dict_glc)
        rec_indireta_consulta = [simbolo for simbolos in rec_indireta.keys() for simbolo in rec_indireta[simbolos]]
        ordem = list(dict_glc.keys())

        for avanca in range(len(ordem)):
            for retrocede in range(avanca-1, -1, -1):
                # Substituição
                if ordem[retrocede] != ordem[avanca]:
                    for producoes in tmp_dict_glc[ordem[avanca]]:
                        if producoes[0] == ordem[retrocede]:
                            tmp_producao = producoes[1:]
                            conj_producoes = []
                            for producao_Aj in tmp_dict_glc[ordem[retrocede]]:
                                conj_producoes.append(producao_Aj + tmp_producao)
                            new_dict_glc[ordem[avanca]] += conj_producoes
                            new_dict_glc[ordem[avanca]].remove(producoes)

            if ordem[avanca] in rec_direta or ordem[avanca] in rec_indireta_consulta:
                novo_vn = ordem[avanca] + '98'
                new_dict_glc[novo_vn] = []
                tmp_dict_glc = copy.deepcopy(new_dict_glc)

                # Eliminação direta
                for producoes in tmp_dict_glc[ordem[avanca]]:
                    if producoes[0] == ordem[avanca]:
                        new_dict_glc[novo_vn].append(producoes[1:] + [novo_vn])
                    else:
                        new_dict_glc[ordem[avanca]].append(producoes + [novo_vn])
                    new_dict_glc[ordem[avanca]].remove(producoes)
                new_dict_glc[novo_vn] += [['&']]

            tmp_dict_glc = copy.deepcopy(new_dict_glc)

        new_glc = Glc(new_dict_glc, glc.get_simbolo_inicial())
        return new_glc, rec_direta, rec_indireta

    @staticmethod
    def verificar_recursao(glc):
        dict_glc = glc.get_dict_glc()
        rec_direta = []
        rec_indireta = {}

        for simbolos in dict_glc.keys():
            rec_indireta[simbolos] = []
            for producoes in dict_glc[simbolos]:
                if producoes[0] == simbolos:
                    rec_direta.append(simbolos)
                elif producoes[0] in list(dict_glc.keys()):
                    for prod_indiretas in dict_glc[producoes[0]]:
                        if prod_indiretas[0] == simbolos and producoes[0] not in rec_indireta[simbolos] and len(producoes) != 1:
                            rec_indireta[simbolos].append(producoes[0])
            if not rec_indireta[simbolos]:
                del rec_indireta[simbolos]

        return rec_direta, rec_indireta

#y = Glc({'S': [['a']], 'A': [['d']]}, 'S')
#x = Glc({'S': [['A', 'a'], ['S', 'b']], 'A': [['S', 'c'], ['d']]}, 'S')
#z = Glc({'S': [['S', 'a'], ['b']], 'A': [['S', 'c'], ['d']]}, 'S')
#print(EliminarRaE.eliminar_RaE(x)[0].get_dict_glc())
