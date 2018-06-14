from Model.glc import *

class EliminarRaE:

    @staticmethod
    def eliminar_RaE(glc):

        # Verifica se tem recursão a esquerda direta/indireta
        # rec_direta será a ordem
        rec_direta, rec_indireta = EliminarRaE.verificar_recursao(glc)
        if not(rec_direta and rec_indireta.values()):
            return False

        dict_glc = glc.get_dict_glc()

        for avanca in range(len(rec_direta)):
            print(avanca)
            for retrocede in range(avanca, 0, -1):
                print(retrocede)
                print("--")


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
                    rec_indireta[simbolos].append(producoes[0])

        return rec_direta, rec_indireta



y = Glc({'S': [['a']], 'A': [['d']]}, 'S')
x = Glc({'S': [['A', 'a'], ['S', 'b']], 'A': [['S', 'c'], ['d']]}, 'S')
print(EliminarRaE.eliminar_RaE(x))