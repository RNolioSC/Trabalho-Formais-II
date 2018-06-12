class Glc:

    def __init__(self, text):
        self.estado_inicial = ""
        self.estados_finais = []
        self.dict_glc = self.text_to_dict(text)

    def text_to_dict(self, text_glc):
        for lines in text_glc:
            nt = ""
            contador = 0

            # Cria o não-terminal (nt)
            while lines[contador] != '-':
                nt += lines[contador]
                contador += 1

            # Pula "ponta da flecha". Ex: S -> a
            contador += 2

            # Cria as produções do nt
            self.dict_glc[nt] = [[]]

            simbolo = ''
            qtd_prod = 0
            while lines[contador] != "|":
                if lines[contador] != ' ':
                    simbolo += lines[contador]
                elif not simbolo:
                    if len(self.dict_glc) != qtd_prod+1:
                        self.dict_glc[nt].append([])

                    self.dict_glc[nt][qtd_prod].append(simbolo)
                    qtd_prod += 1


    def get_dict_gr(self):
        return self.dict_glc

    def get_estado_inicial(self):
        return self.estado_inicial

    def get_estados_finais(self):
        return self.estados_finais