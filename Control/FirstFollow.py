
class FirstFollow:
    @staticmethod
    def first(gram):
        glc = gram.get_dict_glc()
        vn = list(glc.keys())
        first = {}
        first_pendencias = {}  # formato: {A: [B,C]} ;  A recebe first de B e de C
        for a in vn:
            first_a = []
            first_a_pendentes = []  # eg: se S->AB|C, [[A, B],[C]] entra neste conjunto

        # parte 1
            producoes_a = glc[a]  # retorna o lado direito das producoes #eg: [ [a , S], [X, A] ]

            for i in producoes_a:  # eg: [a, S]
                if i[0] not in vn:  # eh um vt  # eg: a
                    first_a.append(i[0])

        # parte 2 e 3
                else:  # eh um vn  #eg: [X, A]
                    first_a_pendentes.append(i)
            if first_a_pendentes:  # se existir alguma pendencia:
                first_pendencias[a] = first_a_pendentes
            first[a] = first_a  # adicionamos o first deste estado no dicionario

        while first_pendencias:  # enquanto houver algum vn com pendencias
            ocorreram_modificacoes = False  # usamos este flag pra detectar deadlocks
            vns_pendentes = list(first_pendencias.keys())
            for a in vns_pendentes:
                first_a_temp = first[a]
                first_a_pendencias_novas = []
                for pendencia in first_pendencias[a]:  # para cada pendencia de vn, formato [A, B]

                    if pendencia[0] not in vn:  # eh um vt
                        first_a_temp.append(pendencia[0])
                        ocorreram_modificacoes = True
                    else:  # eh um vn
                        if pendencia[0] in first_pendencias:  # pulamos
                            first_a_pendencias_novas.append(pendencia)
                            continue
                        first_vns_producao = first[pendencia[0]]  # ex: para A->BC, A recebe first de B = [a,b,c,...]
                        ocorreram_modificacoes = True
                        for i in first_vns_producao:  # para cada elemento do first_vns_producao
                            if i != '&':
                                first_a_temp.append(i)
                        if '&' in first_vns_producao:
                            if len(pendencia) > 1:  # ex: para A->BC, se '&' in B:
                                first_a_pendencias_novas.append(pendencia[1:])  # checamos o resto da producao
                            else:  # ex: para A->B, se '&' in B, entao incluir & em first de A
                                first_a_temp.append('&')

                # atualizando globalmente
                del first_pendencias[a]
                if first_a_pendencias_novas:  # se ainda tiver pendencias
                    first_pendencias[a] = first_a_pendencias_novas
                    # else:  # este vn nao tem mais nada pendente

            if not ocorreram_modificacoes:  # entao encontramos um ciclo
                first_pendencias = FirstFollow.encontrar_1_ciclo(first, first_pendencias)

        return first

    @staticmethod
    def encontrar_1_ciclo(first, first_pendencias):
        caminhos_pendentes = {}  # armazena quais caminhos ainda nao visitamos, usamos para backtrack, destruimos
        for i in first_pendencias:
            caminhos_pendentes[i] = first_pendencias[i]
        ciclo = []
        prods_envolvidas = {}

        vn = list(caminhos_pendentes.keys())[0]  # primeiro vn com pendencias
        ciclo.append(vn)
        while True:
            caminhos = caminhos_pendentes[vn]  # [[AB],[Ac]]
            del caminhos_pendentes[vn]
            prods_envolvidas[vn] = caminhos[0]

            if len(caminhos) > 1:  # se existirem outros caminhos a seguir
                caminhos_pendentes[vn] = caminhos[1:]

            if caminhos[0][0] in ciclo:  # encontramos o ciclo
                while True:
                    if ciclo[0] != caminhos[0][0]:  # eh necessario, ex: S->C->C, deve pegar somente C
                        ciclo.pop(0)
                    else:
                        break
                first_pendencias = FirstFollow.corrige_1_ciclo(first, first_pendencias, prods_envolvidas, ciclo)
                return first_pendencias
            else:
                ciclo.append(caminhos[0][0])
                vn = caminhos[0][0]

    @staticmethod
    def corrige_1_ciclo(first, first_pendencias, prods_envolvidas, ciclo):
        # fazemos a uniao de todos os firsts dos elementos do ciclo
        first_uniao = []
        for vn in ciclo:
            for k in first[vn]:
                first_uniao.append(k)

        # adicionando a uniao aos conjuntos first de todos os vn envolvidos
        for vn in ciclo:
            first_temp = first[vn]
            del first[vn]
            for m in first_uniao:
                first_temp.append(m)
            first[vn] = first_temp

        # removemos as prods do ciclo das pendentes
        for i in prods_envolvidas:  # para cada key, cada prod a ser removida
            if i not in ciclo:  # para nao remover as producoes que nao estiverem de facto no ciclo
                continue
            prod_a_remover = []
            pend_temp = first_pendencias[i]
            del first_pendencias[i]
            for j in pend_temp:
                if j == prods_envolvidas[i]:  # encontramos a prod a ser removida das pendentes
                    prod_a_remover = j
            pend_temp.remove(prod_a_remover)

            # se & pertence ao first:
            if '&' in first[prod_a_remover[0]] and len(prod_a_remover) > 1:  # ex: A->BC, se B->&, add C como pendente
                pend_temp.append(prod_a_remover[1:])
            # else: ex: A->BC, mas nao tem B->&, entao nao fazemos nada.
            if pend_temp:
                first_pendencias[i] = pend_temp

        return first_pendencias

    @staticmethod
    def follow(gram, simbolo_inicial, first):
        return first
