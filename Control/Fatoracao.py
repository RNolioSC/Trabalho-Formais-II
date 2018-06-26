from Model.glc import *
from Control.FirstFollow import *
from Control.EliminarRaE import *
import copy

class Fatoracao:

    @staticmethod
    def eh_fatoravel(glc, n_passos):
        glc, rec_direta, rec_indireta, glc_propria, glc_fertil, glc_e_livre, glc_sem_ciclos, ne, n, nf, vi = EliminarRaE.eliminar_RaE(glc)

        dict_glc = glc.get_dict_glc()
        new_dict_glc = copy.deepcopy(dict_glc)

        for i in range(0, n_passos):
            esta_fatorada, first, vn_nao_fatorada = Fatoracao.esta_fatorada(Glc(new_dict_glc, glc.get_simbolo_inicial()))

            if esta_fatorada or not vn_nao_fatorada:
                return True, Glc(new_dict_glc, glc.get_simbolo_inicial()), None, glc, rec_direta, rec_indireta, glc_propria, glc_fertil, glc_e_livre, glc_sem_ciclos, ne, n, nf, vi
            else:
                # Atualiza old dict
                dict_glc = copy.deepcopy(new_dict_glc)

                # A cada passo, se fatora uma vn
                vn = vn_nao_fatorada.pop(0)

                # Verifica as vts duplicadas (que precisam ser fatoradas)
                vt_duplicada = set([x for x in first[vn] if first[vn].count(x) > 1])

                # Encontro as producoes que iniciam com o mesmo simbolo
                new_dict_glc[vn] = []
                producoes_para_fatorar = []
                for producoes in dict_glc[vn]:
                    if producoes[0] in vt_duplicada:
                        producoes_para_fatorar.append(producoes)
                    elif producoes[0].isupper():
                        for vt in first[producoes[0]]:
                            if vt in vt_duplicada and producoes not in producoes_para_fatorar:
                                producoes_para_fatorar.append(producoes)
                    else:
                        new_dict_glc[vn].append(producoes)

                # Derivacoes sucessivas até ser possível fatorar diretamente
                tmp_list = producoes_para_fatorar.copy()
                while Fatoracao.eh_possivel_fatoracao_direta(first, vn, vt_duplicada, producoes_para_fatorar):
                    for producoes in producoes_para_fatorar:
                        if producoes[0].isupper():
                            vn_indireto, resto_producao = producoes[0][:1], producoes[1:]
                            for producao in dict_glc[vn_indireto[0]]:
                                nova_producao = producao + resto_producao
                                tmp_list.append(nova_producao)
                            tmp_list.remove(producoes)
                    producoes_para_fatorar = tmp_list.copy()

                # Fatoracao direta
                novo_simbolo = vn+'1'
                for vt in vt_duplicada:
                    new_dict_glc[novo_simbolo] = []
                    for producoes in producoes_para_fatorar:
                        if producoes[0] == vt:
                            nova_producao = producoes[1:] if len(producoes) > 1 else ['&']
                            new_dict_glc[novo_simbolo].append(nova_producao)
                    new_dict_glc[vn].append([vt, novo_simbolo])
                    novo_simbolo += '1'

        new_glc = Glc(new_dict_glc, glc.get_simbolo_inicial())
        esta_fatorada, first, vn_nao_fatorada = Fatoracao.esta_fatorada(new_glc)

        return (True, new_glc, None, glc, rec_direta, rec_indireta, glc_propria, glc_fertil, glc_e_livre, glc_sem_ciclos, ne, n, nf, vi) if esta_fatorada else (False, new_glc, vn_nao_fatorada, glc, rec_direta, rec_indireta, glc_propria, glc_fertil, glc_e_livre, glc_sem_ciclos, ne, n, nf, vi)

    @staticmethod
    def eh_possivel_fatoracao_direta(first, vn, vt_duplicada, producoes_para_fatorar):
        existe_vt_indireto = False
        for vt in vt_duplicada:
            count_vt = first[vn].count(vt)
            count = 0
            for producoes in producoes_para_fatorar:
                if producoes[0] == vt:
                    count += 1
            if count_vt != count:
                existe_vt_indireto = True
        return existe_vt_indireto

    @staticmethod
    def esta_fatorada(glc):
        first = FirstFollow.first(glc)
        vn_nao_fatorada = []
        for keys in first:
            if len(first[keys]) != len(set(first[keys])):
                vn_nao_fatorada.append(keys)

        return (True, first, None) if not vn_nao_fatorada else (False, first, vn_nao_fatorada)


# first = {'S': ['a', 'a', 'a'], 'X': ['z', 'a', 'a'], 'Y': ['a', 'a']}
#y = Glc({'S': [['a', 'S', 'b'], ['A', 'C']], 'A': [['a', 'A', 'b'], ['a', 'D'], ['b', 'E']], 'C': [['c', 'C'], ['&']], 'D': [['a', 'D'], ['&']], 'E': [['b', 'E'], ['&']]}, 'S')
#y = Glc({'S': [['a', 'S'], ['X']], 'X': [['Y'], ['z']], 'Y': [['a', 'Y'], ['a']]}, 'S')
#print(Fatoracao.eh_fatoravel(y, 2))