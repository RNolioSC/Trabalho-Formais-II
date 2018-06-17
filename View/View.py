from tkinter import messagebox
from tkinter import *
from Control.Controller import *
from Model.glc import *

class View:

    # Controle
    operacao = None
    controller = None

    def __init__(self, controller):
        # Cria frame raiz
        self.root = Tk()
        self.root.title('T1 de Formais')
        self.root.geometry('{}x{}'.format(800, 380))

        # Create frames principais
        self.frame_top = Frame(self.root, width=800, height=30, pady=3)
        self.frame_esq = Frame(self.root, width=270, height=50, pady=3)
        self.frame_centro = Frame(self.root, width=266, height=50, pady=3)
        self.frame_dir = Frame(self.root, width=267, height=50, pady=3, padx=10)

        # Layout dos containers principais
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Colocar frames na tela
        self.frame_top.grid(row=0, sticky="ew")
        self.frame_esq.grid(row=1, sticky="nsw")
        self.frame_centro.grid(row=1, sticky="ns")
        self.frame_dir.grid(row=1, sticky="nse")

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

        self.input = Text(self.top_frame_centro, bg='white', width=30, height=21)
        self.input.grid(row=0, column=0, sticky="ew")

        # Criar widgets frames da direita
        self.frame_dir.grid_rowconfigure(1, weight=1)
        self.frame_dir.grid_columnconfigure(0, weight=1)

        self.lista_operacoes = Listbox(self.frame_dir, width=40, height=7)
        self.lista_operacoes.grid(row=16, column=0, columnspan=12, rowspan=16, sticky='wse', pady=3)

        self.output_glc = Text(self.frame_dir, bg='white', width=30, height=15)
        self.output_glc.grid(row=0, column=2, columnspan=3, sticky="ew")

        # Criar widgets frame do topo
        self.frame_top.grid_rowconfigure(1, weight=1)
        self.frame_top.grid_columnconfigure(0, weight=1)

        opcoes = Label(self.frame_top, text="Escolha uma das opções abaixo:")
        input = Label(self.frame_top, text="Input:")
        output = Label(self.frame_top, text="Output:")

        opcoes.grid(row=0, column=0, sticky="w")
        input.grid(row=0, column=0)
        output.grid(row=0, column=1, sticky="e")

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

        btn_continue = Button(self.btn_frame_esq, text="Continuar", command=self.exibir_resultados)
        btn_salvar = Button(self.btn_frame_esq, text="Salvar Expressão", command=self.salvar_expressao)
        btn_carregar = Button(self.btn_frame_esq, text="Carregar Expressão", command=self.carregar_expressao)

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
        self.clear_all()
        self.controller.set_glc(self.input)
        if self.operacao == 5:
            self.controller.set_n_passos(5) # TODO criar uma var pra receber esse cara (Um messagebox, mais fácil)

        self.resultados = self.controller.exec_operations(self.operacao)

        if self.operacao not in [1, 2, 4]:
            self.formata_glc(self.resultados)
        else:
            if self.operacao == 1:
                msg = "A gramática gera L(G) vazia" if self.resultados else "A gramática gera L(G) não vazia"
            if self.operacao == 2:
                msg = "A gramática gera L(G) finita" if self.resultados else "A gramática gera L(G) infinita"
            if self.operacao == 4:
                msg = "A gramática está fatorada" if self.resultados else "A gramática não está fatorada"
            messagebox.showinfo("Resultado da operação", msg)

        lista_operacao = self.controller.get_lista_operacoes()
        self.lista_operacoes.delete(0, END)
        for keys in lista_operacao.keys():
            self.lista_operacoes.insert(END, keys)

        self.lista_operacoes.bind("<Double-1>", self.formata_lista_operacoes)

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
                linha += str(conjunto) + '\n'
                self.output_glc.insert(END, linha)
                count += 1
        else:
            self.formata_glc(result)

    def formata_glc(self, glc):
        dict_glc = glc.get_dict_glc()

        output = ''

        # Seta simbolo inicial como primeiro simbolo
        output += glc.get_simbolo_inicial() + '-> '
        for producoes in dict_glc[glc.get_simbolo_inicial()]:
            for simbolo in producoes:
                output += simbolo + ' '
            output += '| '
        output = output[:-2]
        self.output_glc.insert(END, output)

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
                self.output_glc.insert(END, output)

    # Limpa o campo de texto
    def clear_all(self):
        self.output_glc.delete("1.0", END)
        self.controller.set_lista_operacoes({})

    # Armazena a operação selecionada
    def set_operacao(self, op):
        self.operacao = op