
class FirstFollow:
    @staticmethod
    def first(glc):

        vn = list(glc.keys())
        first = {}
        first_pendencias = {}  # {A: [B,C]}, A recebe first de B e de C
        #first_pendentes = []  # Vns que possuem alguma pendencia #TODO: eh necessario? nao basta checar first_pendencias?
        for a in vn:
            first_a = []
            first_a_pendentes = []  # eg: se S->AB|C, [[A, B],[C]] entra neste conjunto

        # parte 1
            producoes_a = glc[a]  # retorna o lado direito das producoes #eg: [ [a , S], [X, A] ]

            for i in producoes_a:  # eg: [a, S]
                print(a, "->", i)
                if i[0] not in vn:  # eh um vt  # eg: a
                    if i[0] not in first_a:
                        first_a.append(i[0])

                    # else: (i[0] in first_a) ja esta no first, nao modificamos

        # parte 2 e 3
                else:  # eh um vn  #eg: [X, A]
                    first_a_pendentes.append(i)
            print("first ", a, ": ", first_a, "; pend: ", first_a_pendentes)

            # depois de ver todas as prods deste estado
            #if first_a_pendentes: TODO: list
            #    first_pendentes.append(a)  # este estado tem pendencias
            # else:  # nao temos nada pendente neste vn

            if first_a_pendentes:  # se existir alguma pendencia:
                first_pendencias[a] = first_a_pendentes

            first[a] = first_a  # adicionamos o first deste estado no dicionario

        # TODO: somente para testes, remover depois
        print('fin: first: ', first, ' pendentes: ', first_pendencias)
        tst_first_prontos = []
        for i in vn:
            if i not in first_pendencias:
                tst_first_prontos.append(i)
        print('pendentes: ', list(first_pendencias.keys()), ' prontos: ', tst_first_prontos)



        # resolvendo pendentes:
        count = 0  # TODO: para testes
        while first_pendencias:  # enquanto houver algum vn com pendencias #TODO list
            print('\nprox passo:')
            ocorreramModificacoes = False  # usamos este flag pra detectar deadlocks
            first_pendencias_novas = {}
            vns_pendentes = list(first_pendencias.keys())
            for a in vns_pendentes: #first_pendencias: #TODO list
                #print('estado: ', a)
                first_a_temp = first[a]
                first_a_pendencias_novas = []
                for pendencia in first_pendencias[a]:  # para cada pendencia de vn, formato [A, B]
                    print('pendencia: ', a, ' :', pendencia)

                    #for vs_producao in pendencia:
                    if pendencia[0] not in vn:  # eh um vt
                        print('para ', pendencia[0], 'adicionamos ao first de ', a)
                        if pendencia[0] not in first_a_temp:
                            first_a_temp.append(pendencia[0])
                        ocorreramModificacoes = True
                    else:  # eh um vn
                        if pendencia[0] in first_pendencias: #todo list
                            print('pular')
                            first_a_pendencias_novas = first_pendencias[a]
                            continue
                        first_vns_producao = first[pendencia[0]]  # ex: para A->BC, A recebe first de B = [a,b,c,...]
                        ocorreramModificacoes = True
                        for i in first_vns_producao:  # para cada elemento do first_vns_producao
                            print('para ', i, ' de ', pendencia[0], ' de ', pendencia)
                            if i not in first_a_temp and i != '&':  # este simbolo ainda nao esta no first, e nao eh &
                                first_a_temp.append(i)
                                print('adicionamos ao first de ', a, ': ', i)
                        if '&' in first_vns_producao:
                            if len(pendencia) > 1:  # ex: para A->BC, se '&' in B:
                                first_a_pendencias_novas.append(pendencia[1:])  # checamos o resto da producao
                            else:  # ex: para A->B, se '&' in B, entao incluir & em first de A
                                if '&' not in first_a_temp:
                                    first_a_temp.append('&')
                                # deletar esta pendencia
                                first_a_pendencias_novas.remove(pendencia)

                # atualizando globalmente
                del first[a]
                first[a] = first_a_temp
                del first_pendencias[a]
                if first_a_pendencias_novas:  # se ainda tiver pendencias
                    first_pendencias[a] = first_a_pendencias_novas
                #else:  # este vn nao tem mais nada pendente
                    #first_pendentes.remove(a)

            print('fin: first: ', first, ' pendentes: ', first_pendencias)
            tst_first_prontos = []
            for i in vn:
                if i not in first_pendencias:
                    tst_first_prontos.append(i)
            print('pendentes: ', list(first_pendencias.keys()), ' prontos: ', tst_first_prontos, 'ocorreu modificao: ', ocorreramModificacoes)
            count = count + 1 #TODO: testes?
            if not ocorreramModificacoes:
                print('\nloop!!!')
                first_pendencias = FirstFollow.encontrar_1_ciclo(first, first_pendencias)
                # TODO: pode ser que ao corrigir um ciclo, um vn esteja pronto. verificar isto.
                #for k in first_pendentes:
                #    try:
                #        _ = first_pendencias[k]
                #    except KeyError:
                #        first_pendentes.remove(k)

                    #if not first_pendencias[k]:
                    #    first_pendentes.remove(k)

                print('fin: first: ', first, ' pendentes: ', first_pendencias)
                tst_first_prontos = []
                for i in vn:
                    if i not in first_pendencias:
                        tst_first_prontos.append(i)
                print('pendentes: ', list(first_pendencias.keys()), ' prontos: ', tst_first_prontos, 'ocorreu modificao: ',
                      ocorreramModificacoes)

                #print(first)
                #break  # TODO: para testes, na vdd vai continuar executando o loop
            if count==10: # TODO: para testes, count iteracoes
                break

        return first

    @staticmethod
    def encontrar_1_ciclo(first, first_pendencias):
        print('\nCICLO\n')
        caminhos_pendentes = {}  # armazena quais caminhos ainda nao visitamos, usamos para backtrack, destruimos
        for i in first_pendencias:
            caminhos_pendentes[i] = first_pendencias[i]
        ciclo = []
        prods_envolvidas = {}

        vn = list(caminhos_pendentes.keys())[0]  # primeiro vn com pendencias
        print('1ro vn c pend', vn)
        ciclo.append(vn)
        count = 0
        while True: #count<5:  # True
            count = count+1 #TODO: para teste
            caminhos = caminhos_pendentes[vn]  # [[AB],[Ac]]
            del caminhos_pendentes[vn]
            prods_envolvidas[vn] = caminhos[0]  # usamos esta producao no ciclo # TODO: e se trocarmos de caminho? sobreescreve. Pode ser problema?
            print('prods do ciclo: ', prods_envolvidas)

            if len(caminhos) > 1:  # se existirem outros caminhos a seguir
                caminhos_pendentes[vn] = caminhos[1:]
                print('cam pend: ', caminhos_pendentes)

            if caminhos[0][0] in ciclo:  # encontramos o ciclo
                print('encontramos o ciclo: ', ciclo, caminhos[0][0])
                #while True:
                    #if ciclo[0] != caminhos[0][0]:  # TODO: eh realmente necessario?
                    #    ciclo.remove(0)
                    #else:
                    #    break
                first_pendencias = FirstFollow.corrige_1_ciclo(first, first_pendencias, prods_envolvidas, ciclo)
                # TODO: estamos modificando o first e pendenc corretos? parece que sim, fazer testes
                return first_pendencias
            else:
                ciclo.append(caminhos[0][0])
                vn = caminhos[0][0]

    @staticmethod
    def corrige_1_ciclo(first, first_pendencias, prods_envolvidas, ciclo):
        # TODO: estamos modificando o first e pendenc corretos?

        print('\nCORRIGINDO\n')

        # fazemos a uniao de todos os firsts dos elementos do ciclo
        first_uniao = []
        for vn in ciclo:
            first_vn = first[vn]  # TODO: lol
            for k in first_vn:
                if k not in first_uniao:
                    first_uniao.append(k)
        print('uniao de fs de ', ciclo, ' = ', first_uniao)

        # adicionando a uniao aos conjuntos first de todos os vn envolvidos
        for vn in ciclo:
            first_temp = first[vn]
            del first[vn]
            for m in first_uniao:
                if m not in first_temp:
                    first_temp.append(m)

            first[vn] = first_temp
            print('modificado o f de ', vn, 'para', first_temp)

        # removemos as prods do ciclo das pendentes
        for i in prods_envolvidas:  # para cada key, cada prod a ser removida
            print('para ', i)
            prod_a_remover = []
            pend_temp = first_pendencias[i]
            del first_pendencias[i]
            for j in pend_temp:
                if j == prods_envolvidas[i]:  # encontramos a prod a ser removida das pendentes
                    prod_a_remover = j
            pend_temp.remove(prod_a_remover)
            print('removido: ', prod_a_remover)

            # se & pertence ao first:
            if '&' in first[i] and len(prod_a_remover) > 1:  # ex: A->BC, se B->&, add C como pendente
                pend_temp.append(prod_a_remover[1:])
                print('adicionado: ', prod_a_remover[1:], ' em pend_temp de ', i)
            # else: ex: A->BC, mas nao tem B->&, entao nao fazemos nada.
            if pend_temp:
                first_pendencias[i] = pend_temp

        return first_pendencias

    @staticmethod
    def follow(glc):
        return True
