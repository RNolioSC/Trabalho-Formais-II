from tkinter import messagebox
from tkinter import *
from Control.Controller import *
from Model.glc import *
from tkinter.simpledialog import askstring

class View:

    # Controle
    operacao = None
    controller = None

    def __init__(self, controller):
        # Cria frame raiz
        self.root = Tk()
        self.root.title('T1 de Formais')
        self.root.geometry('{}x{}'.format(900, 380))

        # Create frames principais
        self.frame_top = Frame(self.root, width=900, height=30, pady=3)
        self.frame_esq = Frame(self.root, width=270, height=50, pady=3)
        self.frame_centro = Frame(self.root, width=300, height=50, pady=3)
        self.frame_dir = Frame(self.root, width=240, height=50, pady=3, padx=7)

        # Layout dos containers principais
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Colocar frames na tela
        self.frame_top.grid(row=0, columnspan=3, sticky="ew")
        self.frame_esq.grid(row=1, column =0, sticky="nsw")
        self.frame_centro.grid(row=1, column = 1, sticky="ns")
        self.frame_dir.grid(row=1, column = 2,sticky="nse")

        # Criar widgets frames da esquerda
        self.frame_esq.grid_rowconfigure(0, weight=1)
        self.frame_esq.grid_columnconfigure(1, weight=1)

        self.top_frame_esq = Frame(self.frame_esq, width=266, height=50)
        self.btn_frame_esq = Frame(self.frame_esq, width=266, height=70)

        self.top_frame_esq.grid(row=0, column=0, sticky="nsew")
        self.btn_frame_esq.grid(row=1, column=0, sticky="nsew")

        self.create_widgets_left_frame()

        # Criar widgets frames do centro
        self.frame_centro.grid_rowconfigure(1, weight=1)
        self.frame_centro.grid_columnconfigure(0, weight=1)

        self.top_frame_centro = Frame(self.frame_centro, width=266, height=230)

        self.top_frame_centro.grid(row=0, column=0, sticky="nsew")

        self.top_frame_centro.grid_rowconfigure(1, weight=1)
        self.top_frame_centro.grid_columnconfigure(0, weight=1)

        self.input = Text(self.top_frame_centro, bg='white', width=32, height=21)
        self.input.grid(row=0, column=0, sticky="we")

        # Criar widgets frames da direita
        self.frame_dir.grid_rowconfigure(1, weight=1)
        self.frame_dir.grid_columnconfigure(0, weight=1)

        self.lista_operacoes = Listbox(self.frame_dir, width=40, height=9)
        self.lista_operacoes.grid(row=16, column=0, columnspan=12, rowspan=16, sticky='wsne', pady=3)

        self.output_glc = Text(self.frame_dir, bg='white', width=35, height=12)
        self.output_glc.grid(row=0, column=2, columnspan=3, sticky="ew")

        # Criar widgets frame do topo
        self.frame_top.grid_rowconfigure(1, weight=1)
        self.frame_top.grid_columnconfigure(0, weight=1)

        opcoes = Label(self.frame_top, text="Escolha uma das opções abaixo:")
        input = Label(self.frame_top, text="Input:")
        output = Label(self.frame_top, text="Output:")

        opcoes.grid(row=0, column=0, sticky="w")
        input.grid(row=0, column=0)
        output.grid(row=0, columnspan=1, sticky="e")

        self.controller = controller

        self.root.mainloop()

    def create_widgets_left_frame(self):
        self.top_frame_esq.grid_rowconfigure(15, weight=1)
        self.top_frame_esq.grid_columnconfigure(1, weight=1)

        lg = LabelFrame(self.top_frame_esq, text='2 - L(G)')
        vazia = Radiobutton(lg, text="É vazia?", variable="Operacao", value=1, tristatevalue=0, command=lambda: self.set_operacao(1))
        finita = Radiobutton(lg, text="É finita?", variable="Operacao", value=2, tristatevalue=0, command=lambda: self.set_operacao(2))

        conversao = LabelFrame(self.top_frame_esq, text='3 - Conversão')
        conversaoPropria = Radiobutton(conversao, text="GLC para GLC Própria", variable="Operacao", value=3, tristatevalue=0, command=lambda: self.set_operacao(3))

        fatoracao = LabelFrame(self.top_frame_esq, text='4 - Fatoração de G')
        estaFatorada = Radiobutton(fatoracao, text="Está fatorada?", variable="Operacao", value=4, tristatevalue=0, command=lambda: self.set_operacao(4))
        ehFatoravel = Radiobutton(fatoracao, text="É fatorável?", variable="Operacao", value=5, tristatevalue=0, command=lambda: self.set_operacao(5))

        recAesq = LabelFrame(self.top_frame_esq, text='5 - Recursão a Esquerda')
        verificar = Radiobutton(recAesq, text="Verificar RaE", variable="Operacao", value=6, tristatevalue=0, command=lambda: self.set_operacao(6))

        analiseSintatica = LabelFrame(self.top_frame_esq, text='6 - Análise Sintática')
        first = Radiobutton(analiseSintatica, text="First", variable="Operacao", value=7, tristatevalue=0, command=lambda: self.set_operacao(7))
        follow = Radiobutton(analiseSintatica, text="Follow", variable="Operacao", value=8, tristatevalue=0, command=lambda: self.set_operacao(8))
        firstNT = Radiobutton(analiseSintatica, text="First-NT", variable="Operacao", value=9, tristatevalue=0, command=lambda: self.set_operacao(9))

        btn_continue = Button(self.btn_frame_esq, text="CONTINUAR", command=self.exibir_resultados)
        btn_salvar = Button(self.btn_frame_esq,  text="SALVAR EXPRESSÃO", command=self.salvar_expressao)
        btn_carregar = Button(self.btn_frame_esq,  text="CARREGAR EXPRESSÃO", command=self.carregar_expressao)

        lg.grid(row=0, column=0, columnspan=3, sticky='we')
        vazia.grid(row=1, column=0, sticky='w')
        finita.grid(row=2, column=0, sticky='w')

        conversao.grid(row=3, column=0, columnspan=3, sticky='wne')
        conversaoPropria.grid(row=4, column=0, sticky='w')

        fatoracao.grid(row=5, column=0, columnspan=3, sticky='we')
        estaFatorada.grid(row=6, column=0, sticky='w')
        ehFatoravel.grid(row=7, column=0, sticky='w')

        recAesq.grid(row=8, column=0, columnspan=3, sticky='we')
        verificar.grid(row=9, column=0, sticky='w')

        analiseSintatica.grid(row=10, column=0, columnspan=3, sticky='wesn')
        first.grid(row=11, column=0, sticky='w')
        follow.grid(row=12, column=0, sticky='w')
        firstNT.grid(row=13, column=0, sticky='w')

        btn_continue.grid(row=0, column=0)
        btn_salvar.grid(row=0, column=1)
        btn_carregar.grid(row=0, column=2)

    # Salvar uma expressão em disco
    def salvar_expressao(self):
        self.controller.salvar_expressao(self.input)

    # Carregar uma expressão em disco
    def carregar_expressao(self):
        self.input.delete("1.0", END)
        self.input.insert(INSERT, self.controller.carregar_expressao())
        self.input.delete("end-1c", END)

    # Executar a operacao selecionada e exibe os resultados
    def exibir_resultados(self):
        #try:
        self.clear_all()
        self.controller.set_glc(self.input)
        if self.operacao == 5:
            n_passos = askstring('Número de passos', 'Insira a quantidade de passos')
            self.controller.set_n_passos(int(n_passos))

        self.resultados = self.controller.exec_operations(self.operacao)

        if self.operacao in [7, 8, 9]:
            opcao_escolhida = ('First' if self.operacao == 7 else 'Follow') if self.operacao != 9 else 'First NT'
            for keys in self.resultados:
                self.output_glc.insert(END, opcao_escolhida+' (' + keys + ') : ' + ' - '.join(list(set(self.resultados[keys]))) + '\n')
        elif self.operacao == 5:
            if not self.resultados:
                messagebox.showinfo("Resultado da operação", "Foi possível fatorar a gramática em " + n_passos +" ou menos passos")
            else:
                messagebox.showinfo("Resultado da operação", "Não foi possível fatorar a gramática em " + n_passos + " passos")
                self.output_glc.insert(END, "Vns NÃO Fatoradas: " + " - ".join(self.resultados))
        elif self.operacao not in [1, 2, 4, 6]:
            self.formata_glc(self.output_glc, self.resultados)
        else:
            if self.operacao == 1:
                msg = "A gramática gera L(G) vazia" if self.resultados else "A gramática gera L(G) não vazia"
            if self.operacao == 2:
                msg = "A gramática gera L(G) finita" if self.resultados else "A gramática gera L(G) infinita"
            if self.operacao == 4:
                msg = "A gramática está fatorada" if self.resultados else "A gramática não está fatorada"
            if self.operacao == 6:
                recursao = self.controller.lista_operacoes["Tipo de recursão"]
                result = False if recursao[0] or recursao[1] else True
                msg = "Não há recursão à esquerda" if result else "A recursão à esquerda foi removida"
            messagebox.showinfo("Resultado da operação", msg)

        lista_operacao = self.controller.get_lista_operacoes()
        self.lista_operacoes.delete(0, END)
        for keys in lista_operacao.keys():
            self.lista_operacoes.insert(END, keys)

        self.lista_operacoes.bind("<Double-1>", self.formata_lista_operacoes)
        self.output_glc.bind("<Button-3>", self.formata_saida_entrada)
        #except Exception:
        #   messagebox.showinfo("ERRO!", "Um erro inesperado ocorreu! Por favor, revise sua gramática.")

    def formata_saida_entrada(self, event):
        select = self.lista_operacoes.curselection()

        try:
            opcao_escolhida = self.lista_operacoes.get(select[0])
        except IndexError:
            opcao_escolhida = 'GLC Inicial'

        result = self.controller.get_lista_operacoes()[opcao_escolhida]

        self.controller.set_glc_existente(result)
        self.input.delete("1.0", END)
        self.formata_glc(self.input, result)

    def formata_lista_operacoes(self, event):
        select = self.lista_operacoes.curselection()
        opcao_escolhida = self.lista_operacoes.get(select[0])
        result = self.controller.get_lista_operacoes()[opcao_escolhida]

        self.output_glc.delete("1.0", END)
        if opcao_escolhida == 'Conjuntos gerados':
            tipo_conjunto = ['Nf: ', 'Vi: ', 'Ne: ', 'Na: ']
            count = 0
            for conjunto in result:
                linha = tipo_conjunto[count]
                linha += (', '.join(conjunto) if conjunto else 'Não há') + '\n'
                self.output_glc.insert(END, linha)
                count += 1
        elif opcao_escolhida == 'Tipo de recursão':
            output = ' - '.join(result[0])
            self.output_glc.insert(END, 'Recursão direta: ' + (output if result[0] else 'Não há') +'\n')

            list_itens = []
            for item in result[1].values():
                list_itens += item
            output = ' - '.join(list_itens)

            self.output_glc.insert(END, 'Recursão indireta: ' + (output if result[1] else 'Não há'))
        elif opcao_escolhida == 'First' or opcao_escolhida == 'Follow' or opcao_escolhida == 'First NT':
            for keys in result:
                self.output_glc.insert(END, opcao_escolhida+' (' + keys + ') : ' + ' - '.join(result[keys]) + '\n')
        elif opcao_escolhida == 'Vns Não Fatoradas':
            self.output_glc.insert(END, 'Vns não fatoradas: ' + '-'.join(result))
        else:
            self.formata_glc(self.output_glc, result)

    def formata_glc(self, field_text, glc):
        try:
            dict_glc = glc.get_dict_glc()
        except AttributeError:
            messagebox.showinfo("Ação bloqueada", "Não é uma GLC!")
            return

        output = ''
        if dict_glc != {} and glc.get_simbolo_inicial() in list(dict_glc.keys()):
            # Seta simbolo inicial como primeiro simbolo
            output += glc.get_simbolo_inicial() + '-> '
            for producoes in dict_glc[glc.get_simbolo_inicial()]:
                for simbolo in producoes:
                    output += simbolo + ' '
                output += '| '
            output = output[:-2]
            field_text.insert(END, output)

            # Seta os demais simbolos
            for simbolos in dict_glc.keys():
                if simbolos != glc.get_simbolo_inicial():
                    output = ''
                    output += simbolos + '-> '
                    for producoes in dict_glc[simbolos]:
                        for simbolo in producoes:
                            output += simbolo + ' '
                        output += '| '
                    output = '\n' + output[:-2]
                    field_text.insert(END, output)
        else:
            field_text.insert(END, glc.get_simbolo_inicial() + '->')

    # Limpa o campo de texto
    def clear_all(self):
        self.output_glc.delete("1.0", END)
        self.controller.set_lista_operacoes({})

    # Armazena a operação selecionada
    def set_operacao(self, op):
        self.operacao = op