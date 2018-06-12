class Glc:

    def __init__(self, text):
        self.simbolo_inicial = ""
        self.dict_glc = self.text_to_dict(text)
        print(self.dict_glc)

    def text_to_dict(self, text_glc):
        new_dict_glc = {}
        self.simbolo_inicial = text_glc[0][0]
        for lines in text_glc:
            nt = ""
            contador = 0

            # Cria o não-terminal (nt)
            while lines[contador] != '-':
                if lines[contador] != ' ':
                    nt += lines[contador]
                contador += 1

            # Pula "ponta da flecha". Ex: S -> a
            contador += 2

            # Cria as produções do nt
            new_dict_glc[nt] = []
            lista_prod = []

            while contador < len(lines):
                if lines[contador] != '|':
                    simbolo = ''

                    while contador < len(lines):
                        if lines[contador] != ' ':
                            simbolo += lines[contador]
                            contador += 1
                        else:
                            break

                    if simbolo != '':
                        lista_prod.append(simbolo)
                    if contador == len(lines):
                        new_dict_glc[nt].append(lista_prod)
                else:
                    new_dict_glc[nt].append(lista_prod)
                    lista_prod = []

                contador += 1

        return new_dict_glc


    def get_dict_gr(self):
        return self.dict_glc

    def get_estado_inicial(self):
        return self.simbolo_inicial