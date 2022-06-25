import os
os.system('cls')
from tkinter import * #módulo para interface gráfica
from tkinter import ttk # o ttk amplia as funções do tkinter
from tkinter import messagebox #módulo para mensagens de confirmação e erro
from PIL import Image, ImageTk #módulo para adcionar imagem
from tkinter import filedialog #módulo para buscar arquivo no PC
import sqlite3 #módulo para banco de dados

class Funcs_cadastro_cliente():
    def limpa_tela(self):
        self.ed_matricula.delete(0, END)
        self.ed_nome.delete(0, END)
        self.ed_email.delete(0, END)
        self.ed_nascimento.delete(0, END)
        self.cb_sexo.set('')
        self.ed_cpf.delete(0, END)
        self.ed_telefone.delete(0, END)
        self.ed_cep.delete(0, END)
        self.ed_logradouro.delete(0, END)
        self.ed_complemento.delete(0, END)
        self.ed_bairro.delete(0, END)
        self.ed_cidade.delete(0, END)
        self.cb_plano.set('')
        self.lb_preço.config(text='')
        self.lb_cpf_erro.config(text='')
        self.lb_imagem.config(image='')
        self.fln = ('')

    def limpa_imagem(self): 
        self.lb_imagem.config(image='')  
        self.fln = ('')

    def conecta_bd(self):
        self.conn = sqlite3.connect("cliente.db")
        self.cursor = self.conn.cursor(); print('Conectando ao Banco de Dados...')
    
    def desconecta_bd(self):

        self.conn.close(); print("Desconectando do Banco de Dados.")

    def montaTabelas(self): # cria tabelas dentro do banco de dados
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                matricula INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_cliente VARCHAR(40),
                email VARCHAR(40),
                nascimento VARCHAR(40),
                sexo VARCHAR(15),
                cpf VARCHAR(25),
                telefone VARCHAR(25),
                cep VARCHAR(25),
                logradouro VARCHAR(40),
                complemento VARCHAR(40),
                bairro VARCHAR(25),
                cidade VARCHAR(25),
                plano VARCHAR(25),
                valor VARCHAR(25),
                imagem_perfil VARCHAR(100)    
              
            ); """)

        self.conn.commit(); print("Banco de Dados criado!")
        self.desconecta_bd()

    def variaveis(self):
        self.matricula = self.ed_matricula.get()
        self.nome = self.ed_nome.get()
        self.email = self.ed_email.get()
        self.nascimento = self.ed_nascimento.get()
        self.sexo = self.cb_sexo.get()
        self.cpf = self.ed_cpf.get()
        self.telefone = self.ed_telefone.get()
        self.cep = self.ed_cep.get()
        self.logradouro = self.ed_logradouro.get()
        self.complemento = self.ed_complemento.get()
        self.bairro = self.ed_bairro.get()
        self.cidade = self.ed_cidade.get()
        self.plano =self.cb_plano.get()
        self.valor = self.lb_preço["text"]
        self.imagem = self.fln

    def cadastrar_cliente(self): # adiciona os valores ao banco de dados digitados na tela
        self.variaveis()
        self.conecta_bd() # conecta ao banco de dados
        self.cursor.execute(""" INSERT INTO clientes(nome_cliente, email, nascimento, sexo, cpf, telefone, cep, logradouro, complemento, bairro, cidade, plano, valor, imagem_perfil)
         VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,? ,?)""",
         ( self.nome, self.email, self.nascimento, self.sexo, self.cpf, self.telefone, self.cep, self.logradouro, self.complemento,self.bairro, self.cidade, self.plano, self.valor, self.imagem))
        self.conn.commit() # validar os dados
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT matricula, nome_cliente, email, nascimento, sexo, cpf, telefone, cep, logradouro, complemento, bairro, cidade, plano, valor, imagem_perfil FROM clientes 
        ORDER BY matricula; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def clique_duplo(self, event):    
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14,col15 = self.listaCli.item(n, 'values')
            self.ed_matricula.insert(END, col1)
            self.ed_nome.insert(END, col2)
            self.ed_email.insert(END, col3)
            self.ed_nascimento.insert(END, col4)
            self.cb_sexo.insert(END, col5)
            self.ed_cpf.insert(END, col6)
            self.ed_telefone.insert(END, col7)
            self.ed_cep.insert(END, col8)
            self.ed_logradouro.insert(END, col9)
            self.ed_complemento.insert(END, col10)
            self.ed_bairro.insert(END, col11)
            self.ed_cidade.insert(END, col12)
            self.cb_plano.insert(END, col13)
            self.lb_preço.config(text= col14)
            #Exibição imagem na interface(repeti a função showimage, mas coloquei para fln recelber a coluna 15 da treeview):
            self.fln = col15
            self.img = Image.open(self.fln)
            self.resized = self.img.resize((200,266), Image.ANTIALIAS)
            self.nova_img= ImageTk.PhotoImage(self.resized)
            self.lb_imagem.configure(image=self.nova_img)
            self.lb_imagem.image = self.nova_img  
            self.lb_imagem.config(END, image= self.nova_img)

            
    def deletar_cliente(self):
        self.variaveis() 
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE matricula = ? """, (self.matricula,) )
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def update_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, email = ?, nascimento = ?, sexo = ?, cpf = ?, telefone = ?, cep = ?, logradouro = ?, complemento = ?, bairro = ?, cidade = ?, plano = ?, valor = ?, imagem_perfil = ?
                                WHERE matricula = ? """, (self.nome, self.email, self.nascimento, self.sexo, self.cpf, self.telefone, self.cep, self.logradouro, self.complemento, self.bairro, self.cidade, self.plano, self.valor, self.imagem, self.matricula))
        self.conn.commit()                        
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def buscar_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        self.ed_nome.insert(END, '%')
        nome= self.ed_nome.get()
        self.cursor.execute(
            """ SELECT matricula, nome_cliente, email, nascimento, sexo, cpf, telefone, cep, logradouro, complemento, bairro, cidade, plano, valor, imagem_perfil FROM clientes 
            WHERE nome_cliente LIKE "%s" ORDER BY nome_cliente ASC """ % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("",END, values=i)
        self.limpa_tela()    
        self.desconecta_bd()

    def refresh_lista(self): #Atualiza lista após buscar alguem cadastrado:
        self.variaveis()
        self.conecta_bd()                       
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def showimage(self):
        self.fln = filedialog.askopenfilename(initialdir= os.getcwd(), title= "Select Image File", filetypes=(("JPG File", "*.jpg"),("PNG File", "*.png"),("All files", "*.*")))
        self.img = Image.open(self.fln)
        self.resized = self.img.resize((200,266), Image.ANTIALIAS)
        self.nova_img= ImageTk.PhotoImage(self.resized)
        self.lb_imagem.configure(image=self.nova_img)
        self.lb_imagem.image = self.nova_img
        
class App(Funcs_cadastro_cliente):
    def __init__(self):
        self.root = Tk()
        self.style = ttk.Style()
        self.tela()
        self.frames_de_tela()
        self.Widgets_aba1()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        self.root.mainloop()
    
    def tela(self):
        self.root.title("Cadastro Academia LocBoy")
        self.root.configure(background= '#155569')
        self.root.geometry('700x800')  
        self.root.resizable(True, True)  
        self.root.maxsize(width= 840, height=960)
        self.root.minsize(width= 700, height=800)
      
    def frames_de_tela (self):  
        #Frame Cadastro Clientes:
        self.frame_1 = Frame(self.root, bd = 4, bg = 'lightgrey', 
                                        highlightbackground= 'black', highlightthickness=1)
        self.frame_1.place(relx= 0.02, rely=0.025, relwidth=0.96, relheight=0.96)

        #Abas:
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1= Frame(self.abas)
        self.aba2= Frame(self.abas)
        self.aba3= Frame(self.abas)
         
    def Widgets_aba1 (self):

        self.aba1.configure(background= 'lightgrey')
        self.aba2.configure(background= 'lightgrey')
        self.aba3.configure(background= 'lightgrey')

        self.abas.add(self.aba1, text="Cadastro Cliente")
        self.abas.add(self.aba2, text="Cadastro Funcionário")
        self.abas.add(self.aba3, text="Cadastro Convidado")

        self.abas.place(relx= 0,rely=0,  relwidth=1, relheight=1)

        #Botões:
        self.bt_limpar = Button(self.aba1, text= "Limpar", font=('verdana', '9'), command= self.limpa_tela )
        self.bt_limpar.place(relx= 0.025,rely=0.005,  relwidth=0.1, relheight= 0.035)   

        self.bt_buscar = Button(self.aba1, text= "Buscar", font=('verdana', '9'), command=self.buscar_cliente)
        self.bt_buscar.place(relx= 0.125, rely=0.005, relwidth=0.1, relheight= 0.035) 

        self.bt_refresh = Button(self.aba1, text= "Atualizar", font=('verdana', '9'), command=self.refresh_lista)
        self.bt_refresh.place(relx= 0.225, rely=0.005, relwidth=0.1, relheight= 0.035)

        self.bt_novo = Button(self.aba1, text= "Novo", font=('verdana', '9'), command=self.validar_cadastro)
        self.bt_novo.place(relx= 0.625, rely=0.005, relwidth=0.15, relheight= 0.035) 

        self.bt_alterar = Button(self.aba1, text= "Alterar", font=('verdana', '9'), command=self.validar_update_cadastro)
        self.bt_alterar.place(relx= 0.775, rely=0.005, relwidth=0.1, relheight= 0.035)

        self.bt_apagar = Button(self.aba1, text= "Excluir", font=('verdana', '9'), command=self.validar_exclusao)
        self.bt_apagar.place(relx= 0.875, rely=0.005, relwidth=0.1, relheight= 0.035)

        self.bt_imagem = Button(self.aba1, text= "Procurar Foto", font=('verdana', '9'), command=self.showimage)
        self.bt_imagem.place(relx= 0.655, rely=0.42, relwidth=0.18, relheight= 0.035)

        self.bt_limpar_imagem = Button(self.aba1, text= "Limpar Foto", font=('verdana', '9'), command=self.limpa_imagem)
        self.bt_limpar_imagem.place(relx= 0.655, rely=0.46, relwidth=0.18, relheight= 0.035)


        #Widgets da aba1:
        #1-Matrícula;
        self.lb_matricula = Label(self.aba1, text= 'Matrícula:', bg='lightgrey')
        self.lb_matricula.place(relx=0.025, rely=0.05)

        self.ed_matricula = Entry(self.aba1, bd=2)
        self.ed_matricula.place(relx=0.125, rely=0.05, relwidth= 0.1)
        #2-Nome;
        self.lb_nome = Label(self.aba1, text= 'Nome:', bg='lightgrey')
        self.lb_nome.place(relx=0.025, rely=0.095)

        self.ed_nome = Entry(self.aba1, bd=2)
        self.ed_nome.place(relx=0.125, rely=0.095, relwidth= 0.3)

        #3-Email;
        self.lb_email = Label(self.aba1, text= 'E-mail:', bg='lightgrey')
        self.lb_email.place(relx=0.025, rely=0.14)

        self.ed_email = Entry(self.aba1, bd=2)
        self.ed_email.place(relx=0.125, rely=0.14, relwidth= 0.3)

        #4-Data de nascimento;
        self.lb_nascimento = Label(self.aba1, text= 'Data de Nascimento:', bg='lightgrey')
        self.lb_nascimento.place(relx=0.025, rely=0.185)

        self.ed_nascimento = Entry(self.aba1, bd=2)
        self.ed_nascimento.place(relx=0.23, rely=0.185, relwidth= 0.195)

        #5-Sexo;
        self.lb_sexo = Label(self.aba1, text= 'Sexo:', bg='lightgrey')
        self.lb_sexo.place(relx=0.025, rely=0.23)

        self.lista_sexo=['Masculino', 'Feminino']
        self.cb_sexo= ttk.Combobox(self.aba1, values= self.lista_sexo)
        self.cb_sexo.place(relx=0.125, rely=0.23, relwidth=0.3, relheight=0.03)

        #6-CPF;
        self.lb_cpf = Label(self.aba1, text= 'CPF:', bg='lightgrey')
        self.lb_cpf.place(relx=0.025, rely=0.275)
        self.lb_cpf_erro = Label(self.aba1, text= '', bg='lightgrey')
        self.lb_cpf_erro.place(relx=0.43, rely=0.275)

        self.ed_cpf = Entry(self.aba1, bd=2)
        self.ed_cpf.place(relx=0.125, rely=0.275, relwidth= 0.3)

        #7-Telefone;
        self.lb_telefone = Label(self.aba1, text= 'Telefone:', bg='lightgrey')
        self.lb_telefone.place(relx=0.025, rely=0.32)
        
        self.ed_telefone= Entry(self.aba1, bd=2)
        self.ed_telefone.place(relx=0.125, rely=0.32, relwidth= 0.3)

        #8-CEP;
        self.lb_cep = Label(self.aba1, text= 'CEP:', bg='lightgrey')
        self.lb_cep.place(relx=0.025, rely=0.365)

        self.ed_cep = Entry(self.aba1, bd=2)
        self.ed_cep.place(relx=0.125, rely=0.365, relwidth= 0.3)

        #10-Logradouro;
        self.lb_logradouro = Label(self.aba1, text= 'Logradouro:', bg='lightgrey')
        self.lb_logradouro.place(relx=0.025, rely=0.41)

        self.ed_logradouro = Entry(self.aba1, bd=2)
        self.ed_logradouro.place(relx=0.16, rely=0.41, relwidth= 0.265)

        #11-Complemento;
        self.lb_complemento = Label(self.aba1, text= 'Complemento:', bg='lightgrey')
        self.lb_complemento.place(relx=0.025, rely=0.455)

        self.ed_complemento = Entry(self.aba1, bd=2)
        self.ed_complemento.place(relx=0.18, rely=0.455, relwidth= 0.245)

        #12-Bairro;
        self.lb_bairro = Label(self.aba1, text= 'Bairro:', bg='lightgrey')
        self.lb_bairro.place(relx=0.025, rely=0.50)

        self.ed_bairro = Entry(self.aba1, bd=2)
        self.ed_bairro.place(relx=0.125, rely=0.50, relwidth= 0.3)

        #13-Cidade;
        self.lb_cidade = Label(self.aba1, text= 'Cidade:', bg='lightgrey')
        self.lb_cidade.place(relx=0.025, rely=0.545)

        self.ed_cidade = Entry(self.aba1, bd=2)
        self.ed_cidade.place(relx=0.125, rely=0.545, relwidth= 0.3)
        
        #14-Plano;
        self.lb_plano = Label(self.aba1, text= 'Tipo de Plano:', bg='lightgrey')
        self.lb_plano.place(relx=0.025, rely=0.59)

        self.lista_plano=['Básico', 'Médio','Completo']
        self.cb_plano= ttk.Combobox(self.aba1, values= self.lista_plano)
        self.cb_plano.place(relx=0.175, rely=0.59, relwidth=0.25, relheight=0.03)
        self.cb_plano.bind('<<ComboboxSelected>>', self.valores)#Ação quando selecionado um item no combobox
       
        #15-Mensalidade;
        self.lb_plano = Label(self.aba1, text= 'Mensalidade:', bg='lightgrey')
        self.lb_plano.place(relx=0.025, rely=0.635)
        self.lb_preço = Label(self.aba1, text= '', bg='lightgrey', fg= 'blue' , font=(50))
        self.lb_preço.place(relx=0.165, rely=0.635)

        #16-Imagem;
        self.lb_imagem = Label(self.aba1, text= 'Foto JPG ou PNG', bg='#b0b0b0')
        self.lb_imagem.place(relx=0.625, rely=0.095, relwidth= 0.24, relheight= 0.3)
        
        #17 Lista de matriculados :
        self.listaCli = ttk.Treeview(self.aba1, height= 3, column=('col1', 'col2','col3','col4','col5','col6','col7','col8','col9','col10','col11','col12','col13','col14','col15'))
        self.listaCli.heading('#0', text='')
        self.listaCli.heading('#1', text='Matrícula')
        self.listaCli.heading('#2', text='Nome')
        self.listaCli.heading('#3', text='E-mail')
        self.listaCli.heading('#4', text='Nascimento')
        self.listaCli.heading('#5', text='Sexo')
        self.listaCli.heading('#6', text='CPF')
        self.listaCli.heading('#7', text='Telefone')
        self.listaCli.heading('#8', text='CEP')
        self.listaCli.heading('#9', text='Logradouro')
        self.listaCli.heading('#10', text='Complemento')
        self.listaCli.heading('#11', text='Bairro')
        self.listaCli.heading('#12', text='Cidade')
        self.listaCli.heading('#13', text='Plano')
        self.listaCli.heading('#14', text='Mensalidade')
        self.listaCli.heading('#15', text='Foto')
        
        

        self.listaCli.column('#0', width=20, minwidth= 20)
        self.listaCli.column('#1', width=60, minwidth= 80)
        self.listaCli.column('#2', width=100, minwidth= 220)
        self.listaCli.column('#3', width=60, minwidth= 150)
        self.listaCli.column('#4', width=60, minwidth= 100)
        self.listaCli.column('#5', width=60, minwidth= 100)
        self.listaCli.column('#6', width=60, minwidth= 100)
        self.listaCli.column('#7', width=60, minwidth= 100)
        self.listaCli.column('#8', width=60, minwidth= 100)
        self.listaCli.column('#9', width=60, minwidth= 200)
        self.listaCli.column('#10', width=60, minwidth= 120)
        self.listaCli.column('#11', width=60, minwidth= 100)
        self.listaCli.column('#12', width=60, minwidth= 100)
        self.listaCli.column('#13', width=60, minwidth= 100)
        self.listaCli.column('#14', width=60, minwidth= 100)
        self.listaCli.column('#15', width=60, minwidth= 250)
      
       

        self.listaCli.place(relx=0.005, rely=0.7, relwidth= 1, relheight=0.3)
        
        #18 Scrollbar Vertical:
        self.scrollistaV = ttk.Scrollbar(self.aba1, orient= 'vertical', command= self.listaCli.yview)
        self.listaCli['yscrollcommand'] = self.scrollistaV.set
        self.scrollistaV.place(relx=0.975, rely=0.7, relwidth= 0.025, relheight=0.275)

        #19 Scrollbar Horizontal:
        self.scrollistaH = ttk.Scrollbar(self.aba1, orient= 'horizontal', command= self.listaCli.xview)
        self.listaCli['xscrollcommand'] = self.scrollistaH.set
        self.scrollistaH.place(relx=0.005, rely=0.975, relwidth= 1, relheight=0.025)
        
        #selecionar tipo de tema (alt, clam, default):
        self.style.theme_use('alt')
        
        #Estilizando tema fo Treeview selecionada:
        self.style.configure('Treeview', background='white', foreground='black',rowheight='25', fieldbackground= 'white', bd=1)
        self.style.map('Treeview', background=[('selected', 'green')])
        self.listaCli.bind("<Double-1>", self.clique_duplo)

    def valores(self, event):
        #Função para adicionar valor da mensalidade ao escolher um plano na label self.lb_preço:
        self.valor = self.cb_plano.get()
        if self.valor == self.lista_plano[0]:
            self.lb_preço['text'] = ('R$ 70,00')
        elif self.valor == self.lista_plano[1]:
            self.lb_preço['text'] = ('R$ 90,00')
        elif self.valor == self.lista_plano[2]:
            self.lb_preço['text'] = ('R$ 120,00')

    def validar_cadastro(self):
        cpf=self.ed_cpf.get()
        validacpf = bool
        digitos = []

        #extrair os dígitos do CPF
        if cpf.isdigit() == True:
            for digito in str(cpf):
                digitos.append(int(digito))

            if len(digitos)!= 11:
                validacpf = False

            elif digitos[0] == digitos[1] == digitos[2] == digitos[3] == digitos[4] == digitos[5] == digitos[6] == digitos[7] == digitos[8] ==digitos[9] == digitos[10]:
                validacpf = False
            else:
                soma1 = digitos[0]*10 + digitos[1]*9 + digitos[2]*8 + digitos[3]*7 + digitos[4]*6 + digitos[5]*5 + digitos[6]*4 + digitos[7]*3 + digitos[8]*2
                resto1 = (soma1 * 10) % 11

                if resto1 == 10:
                    resto1 = 0

                soma2 = digitos[0]*11 + digitos[1]*10 + digitos[2]*9 + digitos[3]*8 + digitos[4]*7 + digitos[5]*6 + digitos[6]*5 + digitos[7]*4 + digitos[8]*3 + digitos[9]*2
                resto2 = (soma2 * 10) % 11

                if resto2 == 10:
                    resto2 = 0

                if resto1 == digitos[9] and resto2 == digitos[10]:
                    validacpf = True
                else:
                    validacpf = False
        else:
            validacpf = False

        self.confirmar_cadastro =  messagebox.askyesno('Cadastrar cliente','Deseja confirmar cadastro?')

        if validacpf == True and self.confirmar_cadastro == True: 
            self.cadastrar_cliente()
            self.yes_alterar_1 =messagebox.showwarning("Cadastrar cliente", "Cadastro efetuado com sucesso!")

        elif validacpf == True and self.confirmar_cadastro == False:
            self.no_alterar_1 =messagebox.showwarning("Cadastrar cliente", "Cadastro cancelado!")

        elif validacpf == False: 
            self.erro_cadastro_1 = messagebox.showerror('Erro de cadastro', 'Erro: CPF inválido!')

    def validar_update_cadastro(self):
        cpf=self.ed_cpf.get()
        validacpf = bool
        digitos = []

        #extrair os dígitos do CPF
        if cpf.isdigit() == True:
            for digito in str(cpf):
                digitos.append(int(digito))

            if len(digitos)!= 11:
                validacpf = False

            elif digitos[0] == digitos[1] == digitos[2] == digitos[3] == digitos[4] == digitos[5] == digitos[6] == digitos[7] == digitos[8] ==digitos[9] == digitos[10]:
                validacpf = False
            else:
                soma1 = digitos[0]*10 + digitos[1]*9 + digitos[2]*8 + digitos[3]*7 + digitos[4]*6 + digitos[5]*5 + digitos[6]*4 + digitos[7]*3 + digitos[8]*2
                resto1 = (soma1 * 10) % 11

                if resto1 == 10:
                    resto1 = 0

                soma2 = digitos[0]*11 + digitos[1]*10 + digitos[2]*9 + digitos[3]*8 + digitos[4]*7 + digitos[5]*6 + digitos[6]*5 + digitos[7]*4 + digitos[8]*3 + digitos[9]*2
                resto2 = (soma2 * 10) % 11

                if resto2 == 10:
                    resto2 = 0

                if resto1 == digitos[9] and resto2 == digitos[10]:
                    validacpf = True
                else:
                    validacpf = False
        else:
            validacpf = False

        self.confirmar_alterar =  messagebox.askyesno('Alterar dados cliente','Deseja confirmar alteração de cadastro?')

        if validacpf == True and self.confirmar_alterar == True: 
            self.update_cliente()
            self.yes_alterar =messagebox.showwarning("Alterar dados cliente", "Alteração de cadastro confirmada!")

        elif validacpf == True and self.confirmar_alterar == False:
            self.no_alterar =messagebox.showwarning("Alterar dados cliente", "Alteração de cadastro cancelada!")

        elif validacpf == False: 
            self.erro_cadastro = messagebox.showerror('Erro de cadastro', 'Erro: CPF inválido!')

    def validar_exclusao(self):

        self.confirmar_exclusao =  messagebox.askyesno('Excluir cliente','Deseja confirmar exclusão do cliente?')

        if self.confirmar_exclusao == True: 
            self.deletar_cliente()
            self.yes_excluir =messagebox.showwarning("Excluir cliente", "Cliente excluído com sucesso!")

    def Menus(self):
        menubar = Menu(self.frame_1)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        '''filemenu3 = Menu(menubar)'''

        def Quit() : self.root.destroy()

        menubar.add_cascade(label = "Opções", menu= filemenu)
        menubar.add_cascade(label = "Ajuda", menu= filemenu2)
        '''menubar.add_cascade(label = "Organizar clientes por:", menu= filemenu3)'''

        filemenu.add_command(label="Sair", command= Quit)
        filemenu2.add_command(label= "Instruções de uso", command=self.janela_instrucoes)
        '''filemenu3.add_command(label= "Matrícula", command=self.organizar_cod)
        filemenu3.add_command(label= "Nome", command=self.organizar_nome)
   
    def organizar_nome(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes 
        ORDER BY nome_cliente ASC; """) # cod, nome_cliente, telefone, cidade
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def organizar_cod(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes 
        ORDER BY cod; """) # cod, nome_cliente, telefone, cidade
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd() '''   

    def janela_instrucoes(self):  
  
        self.Janela_2 = Toplevel()
        self.Janela_2.title('Nova Janela')
        self.Janela_2.configure(background= '#155569')
        self.Janela_2.geometry('800x400')
        self.Janela_2.resizable(False, True )
        self.Janela_2.transient(self.root)
        self.Janela_2.focus_force()
        self.Janela_2.grab_set()
       
        #Label com instruções:
        self.lb_instrucoes = Label(self.Janela_2, text= 
        '''Instruções de uso:

        1- Para cadastrar novo cliente informe os dados nos campos e aperte o botão 'Cadastrar';
        2- O campo 'Matrícula' não deve ser preenchido na hora do cadastro;
        3- Para limpar todos os campos de preenchimento clique em 'Limpar';
        4- Para alterar dados do cliente dê duplo em seu nome na lista de cadatro e depois selecione o botão 'Alterar';
        5- Para apagar cadastro de cliente dê duplo em seu nome na lista na lista de cadastro e depois selecione o botão 'Apagar';
        6- Para buscar um cliente digite na secção "Nome" o nome da pessoa que deseja encontrar.
        7- Para mudar ordem de organização da lista va no menu superior e escolha uma das opções sugeridas.
        ''', bg='lightgrey', justify= LEFT, anchor='n')
        self.lb_instrucoes.place(relx=0.02, rely=0.02,relwidth=0.96, relheight=0.96)
        
        
App()
