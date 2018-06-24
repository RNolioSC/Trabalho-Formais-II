
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
                    if ciclo[0] != caminhos[0][0]:  # ex: S->C->C, pega somente C
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
    def follow(gram, first):
        glc = gram.get_dict_glc()
        simbolo_inicial = gram.get_simbolo_inicial()

        # passo 1
        follow = {simbolo_inicial: ['$']}
        for vn in glc:
            if vn != simbolo_inicial:
                follow[vn] = []

        prods_n = {}  # todas as producoes de tamanho > 1
        prods_1 = {}  # todas as producoes, de tamanho 1, somente Vns; e as pendentes

        # separamos as prods simples das demais
        for vn in glc:
            prods_1[vn] = []
            prods_n[vn] = []
            for prod_temp in glc[vn]:
                if len(prod_temp) > 1:
                    prods_n[vn].append(prod_temp)
                else:
                    if prod_temp[0] in glc:
                        prods_1[vn].append(prod_temp)

        # passo 2:
        while prods_n:
            for vn in prods_n:
                prods_n_new = []
                formas_sent = prods_n[vn]
                for form_sent in formas_sent:  # ex: lado direito de S->aB
                    if len(form_sent) == 1:
                        if form_sent[0] not in glc:  # eh um vt
                            continue
                        else:  # ex: S->A
                            if form_sent[0] != vn:  # para nao adicionar S->S
                                prods_1[form_sent[0]].append(vn)

                    else:  # forma sentencial de tamanho >1
                        if form_sent[0] not in glc:  # eh um vt, ex: S->aB, avaliando a
                            prods_n_new.append(form_sent[1:])
                            continue

                        else:  # eh um vn, ex: S->Ab, avaliando A
                            if form_sent[1] not in glc:  # o proximo simbolo eh um vt
                                if form_sent[1] not in follow[form_sent[0]]:
                                    follow[form_sent[0]].append(form_sent[1])
                                    if len(form_sent) > 2:
                                        prods_n_new.append(form_sent[2:])

                            else:  # o proximo simbolo eh um vn
                                first_temp = first[form_sent[1]]
                                for n in first_temp:
                                    if n != '&':
                                        if n not in follow[form_sent[0]]:
                                            follow[form_sent[0]].append(n)
                                if '&' in first_temp:
                                    # ex: S->ABc, avaliando A, com & in first(B), adicionamos S->Ac para ser processado
                                    nova_prod = [form_sent[0]]
                                    if len(form_sent) > 2:
                                        for j in form_sent[2:]:
                                            nova_prod.append(j)
                                    prods_n_new.append(nova_prod)

                                # falta processar o resto da forma sentencial
                                prods_n_new.append(form_sent[1:])

                # atualizando a lista
                prods_n[vn] = prods_n_new
            # se nao tiverem mais formas sentenciais, deletar do dicionario ex: {'S': []}
            vns_temp = list(prods_n.keys())
            for m in vns_temp:
                if not prods_n[m]:
                    del prods_n[m]
                    
        # passo 3
        while prods_1:
            vns_temp = list(prods_1.keys())
            for m in vns_temp:
                if not prods_1[m]:
                    del prods_1[m]
            for vn in prods_1:

                prods_1_new = []
                pendencias = prods_1[vn]
                for pend in pendencias:
                    for i in follow[pend]:
                        if i not in follow[vn]:
                            follow[vn].append(i)
                    if pend not in prods_1:
                        continue
                    for j in prods_1[pend]:
                        if j not in prods_1_new and j != vn:  # para evitar {'S':['S']}
                            prods_1_new.append(j)
                prods_1[vn] = prods_1_new
        return follow
