from Control.EliminarSimbolosInuteis import *
from string import punctuation
import itertools

class GLCPropria:

    @staticmethod
    def glc_propria(glc):
        glc_e_livre = GLCPropria.e_livre(glc)
        new_glc = GLCPropria.remove_ciclos(glc_e_livre) if GLCPropria.verifica_ciclos(glc_e_livre) else glc_e_livre
        glc_propria = EliminarSimbolosInuteis.eliminar_simbolos_inuteis(new_glc)

        return glc_propria

    @staticmethod
    def e_livre(glc):
        ne = GLCPropria.construir_NE(glc)
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
                new_dict_glc[simbolo] += producoes_validas[0]

        new_glc = Glc(new_dict_glc, glc.get_simbolo_inicial())

        # Verifica se estado inicial em NE
        if glc.get_simbolo_inicial() in ne:
            dict_glc['S99'] = [[glc.get_simbolo_inicial()], ['&']]
            new_glc.set_simbolo_inicial('S99')

        return new_glc, ne

    @staticmethod
    def remove_ciclos(glc):
        pass

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
                        if permite_e:
                            tmp_ne.append(simbolo)
                    permite_e = True

        return ne

    @staticmethod
    def verifica_ciclos(glc):
        pass


x = Glc({'S': [['&'], ['A', 'ab']], 'A': [['a', 'S', 'X']], 'X': [['S']]}, 'S')
#print(GLCPropria.construir_NE(x))
GLCPropria.e_livre(x)
#print(GLCPropria.gera_producoes_validas(['a', 'S', 'X'], ['S', 'X']))