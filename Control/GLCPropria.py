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
        dict_glc = {}

        # Verifica cada producao e add producoes novas conforme alg especificado em aula
        # Enquanto eh add novas producoes, a nova glc eh criada sem &
        for simbolo in dict_glc:
            producoes_validas = []
            dict_glc[simbolo] = []
            for producoes in dict_glc[simbolo]:
                for elemento in producoes:
                    if elemento in ne:
                        producoes_validas.append(GLCPropria.gera_producoes_validas(producoes, ne))
                        break
                if '&' not in producoes:
                    dict_glc[simbolo].append(producoes)
            dict_glc[simbolo] += producoes_validas

        new_glc = Glc(dict_glc, glc.get_simbolo_inicial())

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
        list(itertools.permutations(producoes, len(producoes)))
        

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


x = Glc({'S': [['&'], ['A', 'ab']], 'A': [['a', 'S']], 'X': [['b', 'A']]}, 'S')
print(GLCPropria.construir_NE(x))