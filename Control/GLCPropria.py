from Control.EliminarSimbolosInuteis import *
from string import punctuation
import itertools

class GLCPropria:

    @staticmethod
    def glc_propria(glc):
        glc_e_livre, ne = GLCPropria.e_livre(glc) if GLCPropria.construir_NE(glc) else (glc, [])
        glc_sem_ciclos, n = GLCPropria.remove_ciclos(glc_e_livre) if GLCPropria.verifica_ciclos(glc_e_livre) else (glc_e_livre, [])
        glc_propria, glc_fertil, nf, vi = EliminarSimbolosInuteis.eliminar_simbolos_inuteis(glc_sem_ciclos)

        return glc_propria, glc_fertil, glc_e_livre, glc_sem_ciclos, ne, n, nf, vi

    @staticmethod
    def e_livre(glc):
        ne = GLCPropria.construir_NE(glc)

        # Se já é e_livre retorna a própria glc
        if not ne:
            return glc

        dict_glc = glc.get_dict_glc()
        new_dict_glc = {}

        # Verifica cada producao e add producoes novas conforme alg especificado em aula
        # Enquanto eh add novas producoes, a nova glc eh criada sem &
        for simbolo in dict_glc:
            producoes_validas = []
            new_dict_glc[simbolo] = []
            for producoes in dict_glc[simbolo]:
                for elemento in producoes:
                    if elemento in ne:
                        producoes_validas.append(GLCPropria.gera_producoes_validas(producoes, ne))
                        break
                if '&' not in producoes:
                    new_dict_glc[simbolo].append(producoes)
            if producoes_validas:
                for producoes in producoes_validas[0]:
                    if producoes not in new_dict_glc[simbolo]:
                        new_dict_glc[simbolo].append(producoes)

        new_glc = Glc(new_dict_glc, glc.get_simbolo_inicial())

        if glc.get_simbolo_inicial() in ne:
            novo_simbolo = glc.get_simbolo_inicial() + '1'
            new_glc.get_dict_glc()[novo_simbolo] = [[glc.get_simbolo_inicial()], ['&']]
            new_glc.set_simbolo_inicial(novo_simbolo)

        return new_glc, ne

    @staticmethod
    def remove_ciclos(glc):
        if not GLCPropria.verifica_ciclos(glc):
            return glc, None

        dict_glc = glc.get_dict_glc()
        new_dict_glc = {}

        # Dicionário N{S,A.....,X} = lista de producoes simples
        tmp_N = {}

        # Add prod simples diretas relacionadas ao simbolo
        for simbolo in dict_glc.keys():
            tmp_N[simbolo] = []
            new_dict_glc[simbolo] = []
            for producoes in dict_glc[simbolo]:
                if len(producoes) == 1 and not(producoes[0].islower() or producoes[0] in punctuation):
                    tmp_N[simbolo].append(producoes[0])
                else:
                    new_dict_glc[simbolo].append(producoes)

        # Add prod simples indiretas relacionadas ao simbolo
        N = {}
        while len(N.values()) != len(tmp_N.values()):
            N = tmp_N

            for simbolo in N.keys():
                for prod_simples in N[simbolo]:
                    for prod in N[prod_simples]:
                        if prod not in N[simbolo]:
                            tmp_N[simbolo].append(prod)

        tmp_dict_glc = copy.deepcopy(new_dict_glc)

        for simbolos in N:
            for prod_simples in N[simbolos]:
                if simbolos != prod_simples:
                    for prod in tmp_dict_glc[prod_simples]:
                        if prod not in new_dict_glc[simbolos]:
                            new_dict_glc[simbolos] += [prod]

        new_glc = Glc(new_dict_glc, glc.get_simbolo_inicial())

        return new_glc, N

    '''
        Métodos auxiliares
    '''

    @staticmethod
    def gera_producoes_validas(producoes, ne):
        # Simbolos obrigatorios em todas as producoes
        complemento_ne = [simbolo for simbolo in producoes if simbolo not in ne]

        producoes_validas = []
        producoes_geradas = []

        # Gero combinacoes de producoes a partir da producao dada
        for i in range(len(producoes)+1):
            producoes_geradas += list(itertools.combinations(producoes, i))

        '''
            Se não há simbolos obrigatórios, então faz combinação todos com todos (add todas as producoes geradas).
            Se há, verifica se todos os simbolos obrigatórios estão em todas as produções geradas, add só aquelas que
            passam nesse critério
        '''
        if not complemento_ne:
            producoes_validas = [list(simbolo) for simbolo in producoes_geradas]
            producoes_validas.pop(0)
        else:
            for producoes in producoes_geradas:
                prod = list(producoes)
                if len(prod) >= len(complemento_ne):
                    if len(prod) == len(complemento_ne) and complemento_ne == prod:
                        producoes_validas.append(prod)
                    else:
                        nao_add = False
                        for simbolo in complemento_ne:
                            if simbolo not in prod:
                                nao_add = True
                        if not nao_add:
                            producoes_validas.append(prod)

        return producoes_validas[:-1]

    @staticmethod
    def construir_NE(glc):
        dict_glc = glc.get_dict_glc()
        ne = None
        tmp_ne = []
        permite_e = True

        while ne != tmp_ne:
            ne = tmp_ne
            for simbolo in dict_glc.keys():
                for producoes in dict_glc[simbolo]:
                    if simbolo not in tmp_ne:
                        if '&' in producoes:
                            tmp_ne.append(simbolo)
                        for elemento in producoes:
                            if (elemento.islower() or elemento in punctuation) and elemento not in ne:
                                permite_e = False
                                break
                            elif len(producoes) == 1 and elemento not in ne:
                                permite_e = False
                                break
                            elif elemento.isupper() and elemento not in ne:
                                permite_e = False
                                break
                        if permite_e:
                            tmp_ne.append(simbolo)
                    permite_e = True

        return ne

    @staticmethod
    def verifica_ciclos(glc):
        dict_glc = glc.get_dict_glc()
        ja_visitados = []
        novos_simbolos = [glc.get_simbolo_inicial()]
        while novos_simbolos:
            simbolo = novos_simbolos.pop(0)
            for producoes in dict_glc[simbolo]:
                if len(producoes) == 1 and not(producoes[0].islower() or producoes[0] in punctuation):
                    if producoes[0] in ja_visitados:
                        return True
                    ja_visitados.append(producoes[0])
                    novos_simbolos.append(producoes[0])
        return False


#x_ciclo = Glc({'S': [['A', 'ab'], ['A']], 'A': [['a', 'S', 'X'], ['X']], 'X': [['S']]}, 'S')
#print(GLCPropria.construir_NE(x_ciclo))
#print(x_ciclo.get_dict_glc())
#x = GLCPropria.e_livre(x_ciclo)[0]
#print(x.get_dict_glc())
#x = GLCPropria.remove_ciclos(x)[0]
#print(x.get_dict_glc())
#x = EliminarSimbolosInuteis.eliminar_simbolos_inuteis(x)[0]
#print(x.get_dict_glc())