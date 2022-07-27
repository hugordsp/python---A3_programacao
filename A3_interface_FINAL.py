import os
os.system('cls')
from tkinter import * #módulo para interface gráfica
from tkinter import ttk # o ttk amplia as funções do tkinter
from tkinter import messagebox #módulo para mensagens de confirmação e erro
from PIL import Image, ImageTk #módulo para adcionar imagem
from tkinter import filedialog #módulo para buscar arquivo no PC
from tkcalendar import Calendar, DateEntry #módulo para calendário tkinter
from datetime import datetime #módulo para calendário python
import sqlite3 #módulo para banco de dados


################           INSTRUÇÕES NECESSÁRIAS PARA INICIAR         ###############
# NECESSÁRIO INSTALAR TODAS AS BIBLIOTECAS ACIMA!
# PARA EXECUTAR O PROGRAMA NO SEU COMPUTADOR, SERÁ NECESSÁRIO ALTERAR O CAMINHO DO DIRETÓRIO DAS IMAGENS PARA UMA PASTA NO SEU COMPUTADOR:
# (SUGESTÃO: UTILIZE A PASTA "FOTOS.PERFIL" PRESENTE NO ARQUIVO .ZIP)
# LINHAS 64, 289, 515, 876, 1071, 1266 -> REFERENCIAR A FOTO PADRÃO (LOGO ACADEMIA LOCBOY)
# LINHAS 175, 176 -> REFERENCIAR UMA FOTO QUALQUER (SUGESTÃO NOMEAR A FOTO "LOGO.PNG" - TEM QUE SER DIFERENTE DA ANTERIOR)
# LINHAS 400, 401 -> REFERENCIAR UMA FOTO QUALQUER (SUGESTÃO NOMEAR A FOTO "LOGO1.PNG" - TEM QUE SER DIFERENTE DAS ANTERIORES)
# LINHAS 626, 627 -> REFERENCIAR UMA FOTO QUALQUER (SUGESTÃO NOMEAR A FOTO "LOGO2.PNG" - TEM QUE SER DIFERENTE DAS ANTERIORES)

class Funcs_cadastro_cliente():

    def adicionar_imagem(self):
        global get_image
        get_image = filedialog.askopenfilenames()
        if get_image != "":
            self.foto = Image.open(get_image[0])
            self.foto_resize = self.foto.resize(((182, 182)),Image.Palette.ADAPTIVE)
            self.foto = ImageTk.PhotoImage(self.foto_resize)
            self.frame_foto = Label(self.frame_moldura)
            self.frame_foto.place(relx=0,rely=0,relheight=1,relwidth=1)
            self.lb_foto = Label(self.frame_foto,image=self.foto)
            self.lb_foto.place(rely=0,relx=0,relheight=1,relwidth=1)

    def convert_image_into_binary(self,filename):
        with open(filename, 'rb') as file:
            foto = file.read()
        return foto
        
    def converter_de_binário_para_foto(self, fotobn, diretório_retornado):
        with open(diretório_retornado, 'wb') as dir_retornado:
            dir_retornado.write(fotobn)       
        
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
        self.frame_moldura.destroy()
        

        self.fln = ("C:/Users/Hugo Rodrigues/OneDrive - Anima Holding/ADS/PROGRAMAÇÃO DE SOLUÇÕES COMPUTACIONAIS/EXERCÍCIOS/A3/fotos_perfil/Locboy.png")
        self.img = Image.open(self.fln)
        self.resized = self.img.resize((183,183), Image.LANCZOS)
        self.nova_img= ImageTk.PhotoImage(self.resized)
        self.frame_moldura = Label(self.aba1, image=self.nova_img)
        self.frame_moldura.place(relx=0.625,rely=0.14,height=182,width=182)
 
    def conecta_bd(self):
        self.conn = sqlite3.connect("locboy.db")
        self.cursor = self.conn.cursor(); print('Conectando ao Banco de Dados...')

    def desconecta_bd(self):
        self.conn.close(); print("Desconectando do Banco de Dados.")

    def montaTabelas(self): # cria tabelas dentro do banco de dados
        self.conecta_bd()
        # Criar Tabela
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
                foto Blob     
              
            );        
        """)
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
        self.imagem = self.frame_moldura["image"]
        
        
    def cadastrar_cliente(self): # adiciona os valores ao banco de dados digitados na tela
        self.variaveis()
        self.conecta_bd() # conecta ao banco de dados

        for image in get_image:
            self.insert_photo = self.convert_image_into_binary(image)

        self.cursor.execute(""" INSERT INTO clientes(nome_cliente, email, nascimento, sexo, cpf, telefone, cep, logradouro, complemento, bairro, cidade, plano, valor, foto)
         VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,? , ?)""",
         (self.nome, self.email, self.nascimento, self.sexo, self.cpf, self.telefone, self.cep, self.logradouro, self.complemento,self.bairro, self.cidade, self.plano, self.valor, self.insert_photo))
        self.conn.commit() # validar os dados
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT matricula, nome_cliente, email, nascimento, sexo, cpf, telefone, cep, logradouro, complemento, bairro, cidade, plano, valor, foto FROM clientes 
        ORDER BY matricula; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def clique_duplo(self, event):    
        self.limpa_tela()
        self.listaCli.selection()
        
        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15 = self.listaCli.item(n, 'values')
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
            self.conecta_bd()
            self.cursor.execute(
                f"SELECT foto FROM clientes WHERE matricula = (?)",(col1,))
            self.insert_photo = self.cursor.fetchone()
            self.cursor.close()
            self.desconecta_bd()   
            #converter para binario
            self.converter_de_binário_para_foto(
            
            self.insert_photo[0], "C:/Users/Hugo Rodrigues/OneDrive - Anima Holding/ADS/PROGRAMAÇÃO DE SOLUÇÕES COMPUTACIONAIS/EXERCÍCIOS/A3/fotos_perfil/logo.png")
            self.foto_recuperada = Image.open("C:/Users/Hugo Rodrigues/OneDrive - Anima Holding/ADS/PROGRAMAÇÃO DE SOLUÇÕES COMPUTACIONAIS/EXERCÍCIOS/A3/fotos_perfil/logo.png")
            self.foto_resize = self.foto_recuperada.resize(((182, 182)),Image.Palette.ADAPTIVE)
            self.foto_recuperada = ImageTk.PhotoImage(self.foto_resize)
            
            self.lb_foto = Label(self.frame_moldura,image=self.foto_recuperada)
            self.lb_foto.place(x=0,y=0,relwidth=1,relheight=1)
            
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

        for image in get_image:
            self.insert_photo = self.convert_image_into_binary(image)

        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, email = ?, nascimento = ?, sexo = ?, cpf = ?, telefone = ?, cep = ?, logradouro = ?, complemento = ?, bairro = ?, cidade = ?, plano = ?, valor = ?, foto = ? 
                                WHERE matricula = ? """, (self.nome, self.email, self.nascimento, self.sexo, self.cpf, self.telefone, self.cep, self.logradouro, self.complemento, self.bairro, self.cidade, self.plano, self.valor, self.insert_photo, self.matricula))
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
            """ SELECT matricula, nome_cliente, email, nascimento, sexo, cpf, telefone, cep, logradouro, complemento, bairro, cidade, plano, valor FROM clientes 
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


    def calendar_Frame(self):
        self.janela_3 = Toplevel()
        self.janela_3.title("Calendario")
        self.janela_3.configure(background= '#155569')
        self.janela_3.geometry('390x300')  
        self.janela_3.resizable(False, False)  
        self.calendario_1 = Calendar(self.janela_3, fg="gray75", bg="blue", font=("verdana", '9', 'bold'), locale='pt_br')
        self.calendario_1.place(relx=0.1, rely=0.1)
        self.inserirData = Button(self.janela_3, text= "Inserir Data", font=('verdana', '9'), command= self.printCalendar)
        self.inserirData.place(relx=0.35, rely=0.85, relheight=0.1, relwidth=0.3)

    def printCalendar (self):
        dataEntry = self.calendario_1.get_date()
        self.janela_3.destroy()
        self.ed_nascimento.delete(0, END)
        self.ed_nascimento.insert(END, dataEntry)
        self.inserirData.destroy()   

class Funcs_cadastro_funcionario():

    def adicionar_imagem_funcionario(self):
        global get_image_func
        get_image_func = filedialog.askopenfilenames()
        print(get_image_func[0])
        if get_image_func != "":
            self.foto_funcionario = Image.open(get_image_func[0])
            self.foto_funcionario_resize = self.foto_funcionario.resize(((182, 182)),Image.Palette.ADAPTIVE)
            self.foto_funcionario = ImageTk.PhotoImage(self.foto_funcionario_resize)
            self.frame_foto_funcionario = Label(self.frame_moldura_funcionario)
            self.frame_foto_funcionario.place(relx=0,rely=0,relheight=1,relwidth=1)
            self.lb_foto_funcionario = Label(self.frame_foto_funcionario,image=self.foto_funcionario)
            self.lb_foto_funcionario.place(rely=0,relx=0,relheight=1,relwidth=1)

    def convert_image_into_binary_func(self,filename):
        with open(filename, 'rb') as file:
            foto_funcionario = file.read()
        return foto_funcionario
        
    def converter_de_binário_para_foto_func(self, fotobn, diretório_retornado):
        with open(diretório_retornado, 'wb') as dir_retornado_func:
            dir_retornado_func.write(fotobn)       
        
    def limpa_tela_funcionario(self):
        self.ed_matricula_funcionario.delete(0, END)
        self.ed_nome_funcionario.delete(0, END)
        self.ed_email_funcionario.delete(0, END)
        self.ed_nascimento_funcionario.delete(0, END)
        self.cb_sexo_funcionario.set('')
        self.ed_cpf_funcionario.delete(0, END)
        self.ed_telefone_funcionario.delete(0, END)
        self.ed_cep_funcionario.delete(0, END)
        self.ed_logradouro_funcionario.delete(0, END)
        self.ed_complemento_funcionario.delete(0, END)
        self.ed_bairro_funcionario.delete(0, END)
        self.ed_cidade_funcionario.delete(0, END)
        self.cb_cargo_funcionario.set('')
        self.lb_valor_salario_funcionario.config(text='')
        self.lb_cpf_funcionario_erro.config(text='')
        self.frame_moldura_funcionario.destroy()
        

        self.fln_funcionario = ("C:/Users/Hugo Rodrigues/OneDrive - Anima Holding/ADS/PROGRAMAÇÃO DE SOLUÇÕES COMPUTACIONAIS/EXERCÍCIOS/A3/fotos_perfil/Locboy.png")
        self.img_funcionario = Image.open(self.fln_funcionario)
        self.resized_funcionario = self.img_funcionario.resize((183,183), Image.LANCZOS)
        self.nova_img_funcionario= ImageTk.PhotoImage(self.resized_funcionario)
        self.frame_moldura_funcionario = Label(self.aba2, image=self.nova_img_funcionario)
        self.frame_moldura_funcionario.place(relx=0.625,rely=0.14,height=182,width=182)
 
    def conecta_bd_func(self):
        self.conn_func = sqlite3.connect("locboy.db")
        self.cursor_func = self.conn_func.cursor(); print('Conectando ao Banco de Dados...')

    def desconecta_bd_func(self):
        self.conn_func.close(); print("Desconectando do Banco de Dados.")

    def montaTabelas_func(self): # cria tabelas dentro do banco de dados
        self.conecta_bd_func()
        # Criar Tabela
        self.cursor_func.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios(
                matricula_func INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_func VARCHAR(40),
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
                cargo VARCHAR(25),
                salario VARCHAR(25),
                foto_func Blob     
              
            );        
        """)
        self.conn_func.commit(); print("Banco de Dados criado!")
        self.desconecta_bd_func()

    def variaveis_funcionario(self):
        self.matricula_funcionario = self.ed_matricula_funcionario.get()
        self.nome_funcionario = self.ed_nome_funcionario.get()
        self.email_funcionario = self.ed_email_funcionario.get()
        self.nascimento_funcionario = self.ed_nascimento_funcionario.get()
        self.sexo_funcionario = self.cb_sexo_funcionario.get()
        self.cpf_funcionario = self.ed_cpf_funcionario.get()
        self.telefone_funcionario = self.ed_telefone_funcionario.get()
        self.cep_funcionario = self.ed_cep_funcionario.get()
        self.logradouro_funcionario = self.ed_logradouro_funcionario.get()
        self.complemento_funcionario = self.ed_complemento_funcionario.get()
        self.bairro_funcionario = self.ed_bairro_funcionario.get()
        self.cidade_funcionario = self.ed_cidade_funcionario.get()
        self.cargo_funcionario =self.cb_cargo_funcionario.get()
        self.salario_funcionario = self.lb_valor_salario_funcionario["text"]
        self.imagem_funcionario = self.frame_moldura_funcionario["image"]
        
        
    def cadastrar_funcionario(self): # adiciona os valores ao banco de dados digitados na tela
        self.variaveis_funcionario()
        self.conecta_bd_func() # conecta ao banco de dados

        for image in get_image_func:
            self.insert_photo_funcionario = self.convert_image_into_binary_func(image)

        self.cursor_func.execute(""" INSERT INTO funcionarios(nome_func, email, nascimento, sexo, cpf, telefone, cep, logradouro, complemento, bairro, cidade, cargo, salario, foto_func)
         VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,? , ?)""",
         (self.nome_funcionario, self.email_funcionario, self.nascimento_funcionario, self.sexo_funcionario, self.cpf_funcionario, self.telefone_funcionario, self.cep_funcionario, self.logradouro_funcionario, self.complemento_funcionario, self.bairro_funcionario, self.cidade_funcionario, self.cargo_funcionario, self.salario_funcionario, self.insert_photo_funcionario))
        self.conn_func.commit() # validar os dados
        self.desconecta_bd_func()
        self.select_lista_funcionario()
        self.limpa_tela_funcionario()

    def select_lista_funcionario(self):
        self.listaFunc.delete(*self.listaFunc.get_children())
        self.conecta_bd_func()
        lista_func = self.cursor_func.execute(""" SELECT matricula_func, nome_func, email, nascimento, sexo, cpf, telefone, cep, logradouro, complemento, bairro, cidade, cargo, salario, foto_func FROM funcionarios 
        ORDER BY matricula_func; """)
        for i in lista_func:
            self.listaFunc.insert("", END, values=i)
        self.desconecta_bd_func()

    def clique_duplo_func(self, event):    
        self.limpa_tela_funcionario()
        self.listaFunc.selection()
        
        for i in self.listaFunc.selection():
            col1_func, col2_func, col3_func, col4_func, col5_func, col6_func, col7_func, col8_func, col9_func, col10_func, col11_func, col12_func, col13_func, col14_func, col15_func = self.listaFunc.item(i, 'values')
            self.ed_matricula_funcionario.insert(END, col1_func)
            self.ed_nome_funcionario.insert(END, col2_func)
            self.ed_email_funcionario.insert(END, col3_func)
            self.ed_nascimento_funcionario.insert(END, col4_func)
            self.cb_sexo_funcionario.insert(END, col5_func)
            self.ed_cpf_funcionario.insert(END, col6_func)
            self.ed_telefone_funcionario.insert(END, col7_func)
            self.ed_cep_funcionario.insert(END, col8_func)
            self.ed_logradouro_funcionario.insert(END, col9_func)
            self.ed_complemento_funcionario.insert(END, col10_func)
            self.ed_bairro_funcionario.insert(END, col11_func)
            self.ed_cidade_funcionario.insert(END, col12_func)
            self.cb_cargo_funcionario.insert(END, col13_func)
            self.lb_valor_salario_funcionario.config(text= col14_func)
            self.conecta_bd_func()
            self.cursor_func.execute(
                f"SELECT foto_func FROM funcionarios WHERE matricula_func = (?)",(col1_func,))
            self.insert_photo_funcionario = self.cursor_func.fetchone()
            self.cursor_func.close()
            self.desconecta_bd_func()   
            #converter para binario
            self.converter_de_binário_para_foto_func(
            
            self.insert_photo_funcionario[0], "C:/Users/Hugo Rodrigues/OneDrive - Anima Holding/ADS/PROGRAMAÇÃO DE SOLUÇÕES COMPUTACIONAIS/EXERCÍCIOS/A3/fotos_perfil/logo1.png")
            self.foto_funcionario_recuperada = Image.open("C:/Users/Hugo Rodrigues/OneDrive - Anima Holding/ADS/PROGRAMAÇÃO DE SOLUÇÕES COMPUTACIONAIS/EXERCÍCIOS/A3/fotos_perfil/logo1.png")
            self.foto_funcionario_resize = self.foto_funcionario_recuperada.resize(((182, 182)),Image.Palette.ADAPTIVE)
            self.foto_funcionario_recuperada = ImageTk.PhotoImage(self.foto_funcionario_resize)
            
            self.lb_foto_funcionario = Label(self.frame_moldura_funcionario,image=self.foto_funcionario_recuperada)
            self.lb_foto_funcionario.place(x=0,y=0,relwidth=1,relheight=1)

            
    def deletar_funcionario(self):
        self.variaveis_funcionario() 
        self.conecta_bd_func()
        self.cursor_func.execute("""DELETE FROM funcionarios WHERE matricula_func = ? """, (self.matricula_funcionario,) )
        self.conn_func.commit()
        self.desconecta_bd_func()
        self.limpa_tela_funcionario()
        self.select_lista_funcionario()

    def update_funcionario(self):
        self.variaveis_funcionario()
        self.desconecta_bd_func()
        self.conecta_bd_func()

        for image in get_image_func:
            self.insert_photo_funcionario = self.convert_image_into_binary_func(image)

        self.cursor_func.execute(""" UPDATE funcionarios SET nome_func = ?, email = ?, nascimento = ?, sexo = ?, cpf = ?, telefone = ?, cep = ?, logradouro = ?, complemento = ?, bairro = ?, cidade = ?, cargo = ?, salario = ?, foto_func = ? 
                                WHERE matricula_func = ? """, (self.nome_funcionario, self.email_funcionario, self.nascimento_funcionario, self.sexo_funcionario, self.cpf_funcionario, self.telefone_funcionario, self.cep_funcionario, self.logradouro_funcionario, self.complemento_funcionario, self.bairro_funcionario, self.cidade_funcionario, self.cargo_funcionario, self.salario_funcionario, self.insert_photo_funcionario, self.matricula_funcionario))
        self.conn_func.commit()                        
        self.desconecta_bd_func()
        self.select_lista_funcionario()
        self.limpa_tela_funcionario()

    def buscar_funcionario(self):
        self.conecta_bd_func()
        self.listaFunc.delete(*self.listaFunc.get_children())
        self.ed_nome_funcionario.insert(END, '%')
        nome_funcionario= self.ed_nome_funcionario.get()
        self.cursor_func.execute(
            """ SELECT matricula_func, nome_func, email, nascimento, sexo, cpf, telefone, cep, logradouro, complemento, bairro, cidade, cargo, salario FROM funcionarios 
            WHERE nome_func LIKE "%s" ORDER BY nome_func ASC """ % nome_funcionario)
        buscanomeFunc = self.cursor_func.fetchall()
        for j in buscanomeFunc:
            self.listaFunc.insert("",END, values=j)
        self.limpa_tela_funcionario()    
        self.desconecta_bd_func()

    def refresh_lista_funcionarios(self): #Atualiza lista após buscar alguem cadastrado:
        self.variaveis_funcionario()
        self.conecta_bd_func()                       
        self.desconecta_bd_func()
        self.select_lista_funcionario()
        self.limpa_tela_funcionario()

    def calendar_Frame_funcionario(self):
        self.janela_4 = Toplevel()
        self.janela_4.title("Calendario")
        self.janela_4.configure(background= '#155569')
        self.janela_4.geometry('390x300')  
        self.janela_4.resizable(False, False) 
        self.calendario_2 = Calendar(self.janela_4, fg="gray75", bg="blue", font=("verdana", '9', 'bold'), locale='pt_br')
        self.calendario_2.place(relx=0.1, rely=0.1)
        self.inserirData_func = Button(self.janela_4, text= "Inserir Data", font=('verdana', '9'), command= self.printCalendar_funcionario)
        self.inserirData_func.place(relx=0.35, rely=0.85, relheight=0.1, relwidth=0.3)

    def printCalendar_funcionario (self):
        dataEntry_func = self.calendario_2.get_date()
        self.janela_4.destroy()
        self.ed_nascimento_funcionario.delete(0, END)
        self.ed_nascimento_funcionario.insert(END, dataEntry_func)
        self.inserirData_func.destroy()

class Funcs_cadastro_convidado():

    def adicionar_imagem_convidado(self):
        global get_image_conv
        get_image_conv = filedialog.askopenfilenames()
        print(get_image_conv[0])
        if get_image_conv != "":
            self.foto_convidado = Image.open(get_image_conv[0])
            self.foto_convidado_resize = self.foto_convidado.resize(((182, 182)),Image.Palette.ADAPTIVE)
            self.foto_convidado = ImageTk.PhotoImage(self.foto_convidado_resize)
            self.frame_foto_convidado = Label(self.frame_moldura_convidado)
            self.frame_foto_convidado.place(relx=0,rely=0,relheight=1,relwidth=1)
            self.lb_foto_convidado = Label(self.frame_foto_convidado,image=self.foto_convidado)
            self.lb_foto_convidado.place(rely=0,relx=0,relheight=1,relwidth=1)

    def convert_image_into_binary_conv(self,filename):
        with open(filename, 'rb') as file:
            foto_convidado = file.read()
        return foto_convidado
        
    def converter_de_binário_para_foto_conv(self, fotobn, diretório_retornado):
        with open(diretório_retornado, 'wb') as dir_retornado_conv:
            dir_retornado_conv.write(fotobn)       
        
    def limpa_tela_convidado(self):
        self.ed_matricula_convidado.delete(0, END)
        self.ed_nome_convidado.delete(0, END)
        self.ed_email_convidado.delete(0, END)
        self.ed_nascimento_convidado.delete(0, END)
        self.cb_sexo_convidado.set('')
        self.ed_cpf_convidado.delete(0, END)
        self.ed_telefone_convidado.delete(0, END)
        self.ed_cep_convidado.delete(0, END)
        self.ed_logradouro_convidado.delete(0, END)
        self.ed_complemento_convidado.delete(0, END)
        self.ed_bairro_convidado.delete(0, END)
        self.ed_cidade_convidado.delete(0, END)
        self.cb_modalidade_convidado.set('')
        self.lb_valor_convidado.config(text='')
        self.lb_cpf_convidado_erro.config(text='')
        self.frame_moldura_convidado.destroy()
        

        self.fln_convidado = ("C:/Users/Hugo Rodrigues/OneDrive - Anima Holding/ADS/PROGRAMAÇÃO DE SOLUÇÕES COMPUTACIONAIS/EXERCÍCIOS/A3/fotos_perfil/Locboy.png")
        self.img_convidado = Image.open(self.fln_convidado)
        self.resized_convidado = self.img_convidado.resize((183,183), Image.LANCZOS)
        self.nova_img_convidado= ImageTk.PhotoImage(self.resized_convidado)
        self.frame_moldura_convidado = Label(self.aba3, image=self.nova_img_convidado)
        self.frame_moldura_convidado.place(relx=0.625,rely=0.14,height=182,width=182)
 
    def conecta_bd_conv(self):
        self.conn_conv = sqlite3.connect("locboy.db")
        self.cursor_conv = self.conn_conv.cursor(); print('Conectando ao Banco de Dados...')

    def desconecta_bd_conv(self):
        self.conn_conv.close(); print("Desconectando do Banco de Dados.")

    def montaTabelas_conv(self): # cria tabelas dentro do banco de dados
        self.conecta_bd_conv()
        # Criar Tabela
        self.cursor_conv.execute("""
            CREATE TABLE IF NOT EXISTS convidados(
                matricula_conv INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_conv VARCHAR(40),
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
                modalidade VARCHAR(25),
                valor VARCHAR(25),
                foto_conv Blob     
              
            );        
        """)
        self.conn_conv.commit(); print("Banco de Dados criado!")
        self.desconecta_bd_conv()

    def variaveis_convidado(self):
        self.matricula_convidado = self.ed_matricula_convidado.get()
        self.nome_convidado = self.ed_nome_convidado.get()
        self.email_convidado = self.ed_email_convidado.get()
        self.nascimento_convidado = self.ed_nascimento_convidado.get()
        self.sexo_convidado = self.cb_sexo_convidado.get()
        self.cpf_convidado = self.ed_cpf_convidado.get()
        self.telefone_convidado = self.ed_telefone_convidado.get()
        self.cep_convidado = self.ed_cep_convidado.get()
        self.logradouro_convidado = self.ed_logradouro_convidado.get()
        self.complemento_convidado = self.ed_complemento_convidado.get()
        self.bairro_convidado = self.ed_bairro_convidado.get()
        self.cidade_convidado = self.ed_cidade_convidado.get()
        self.modalidade_convidado =self.cb_modalidade_convidado.get()
        self.valor_convidado = self.lb_valor_convidado["text"]
        self.imagem_convidado = self.frame_moldura_convidado["image"]
        
        
    def cadastrar_convidado(self): # adiciona os valores ao banco de dados digitados na tela
        self.variaveis_convidado()
        self.conecta_bd_conv() # conecta ao banco de dados

        for image in get_image_conv:
            self.insert_photo_convidado = self.convert_image_into_binary_conv(image)

        self.cursor_conv.execute(""" INSERT INTO convidados(nome_conv, email, nascimento, sexo, cpf, telefone, cep, logradouro, complemento, bairro, cidade, modalidade, valor, foto_conv)
         VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,? , ?)""",
         (self.nome_convidado, self.email_convidado, self.nascimento_convidado, self.sexo_convidado, self.cpf_convidado, self.telefone_convidado, self.cep_convidado, self.logradouro_convidado, self.complemento_convidado, self.bairro_convidado, self.cidade_convidado, self.modalidade_convidado, self.valor_convidado, self.insert_photo_convidado))
        self.conn_conv.commit() # validar os dados
        self.desconecta_bd_conv()
        self.select_lista_convidado()
        self.limpa_tela_convidado()

    def select_lista_convidado(self):
        self.listaConv.delete(*self.listaConv.get_children())
        self.conecta_bd_conv()
        lista_conv = self.cursor_conv.execute(""" SELECT matricula_conv, nome_conv, email, nascimento, sexo, cpf, telefone, cep, logradouro, complemento, bairro, cidade, modalidade, valor, foto_conv FROM convidados 
        ORDER BY matricula_conv; """)
        for i in lista_conv:
            self.listaConv.insert("", END, values=i)
        self.desconecta_bd_conv()

    def clique_duplo_conv(self, event):    
        self.limpa_tela_convidado()
        self.listaConv.selection()
        
        for i in self.listaConv.selection():
            col1_conv, col2_conv, col3_conv, col4_conv, col5_conv, col6_conv, col7_conv, col8_conv, col9_conv, col10_conv, col11_conv, col12_conv, col13_conv, col14_conv, col15_conv = self.listaConv.item(i, 'values')
            self.ed_matricula_convidado.insert(END, col1_conv)
            self.ed_nome_convidado.insert(END, col2_conv)
            self.ed_email_convidado.insert(END, col3_conv)
            self.ed_nascimento_convidado.insert(END, col4_conv)
            self.cb_sexo_convidado.insert(END, col5_conv)
            self.ed_cpf_convidado.insert(END, col6_conv)
            self.ed_telefone_convidado.insert(END, col7_conv)
            self.ed_cep_convidado.insert(END, col8_conv)
            self.ed_logradouro_convidado.insert(END, col9_conv)
            self.ed_complemento_convidado.insert(END, col10_conv)
            self.ed_bairro_convidado.insert(END, col11_conv)
            self.ed_cidade_convidado.insert(END, col12_conv)
            self.cb_modalidade_convidado.insert(END, col13_conv)
            self.lb_valor_convidado.config(text= col14_conv)
            self.conecta_bd_conv()
            self.cursor_conv.execute(
                f"SELECT foto_conv FROM convidados WHERE matricula_conv = (?)",(col1_conv,))
            self.insert_photo_convidado = self.cursor_conv.fetchone()
            self.cursor_conv.close()
            self.desconecta_bd_conv()   
            #converter para binario
            self.converter_de_binário_para_foto_conv(
            
            self.insert_photo_convidado[0], "C:/Users/Hugo Rodrigues/OneDrive - Anima Holding/ADS/PROGRAMAÇÃO DE SOLUÇÕES COMPUTACIONAIS/EXERCÍCIOS/A3/fotos_perfil/logo2.png")
            self.foto_convidado_recuperada = Image.open("C:/Users/Hugo Rodrigues/OneDrive - Anima Holding/ADS/PROGRAMAÇÃO DE SOLUÇÕES COMPUTACIONAIS/EXERCÍCIOS/A3/fotos_perfil/logo2.png")
            self.foto_convidado_resize = self.foto_convidado_recuperada.resize(((182, 182)),Image.Palette.ADAPTIVE)
            self.foto_convidado_recuperada = ImageTk.PhotoImage(self.foto_convidado_resize)
            
            self.lb_foto_convidado = Label(self.frame_moldura_convidado,image=self.foto_convidado_recuperada)
            self.lb_foto_convidado.place(x=0,y=0,relwidth=1,relheight=1)

            
    def deletar_convidado(self):
        self.variaveis_convidado() 
        self.conecta_bd_conv()
        self.cursor_conv.execute("""DELETE FROM convidados WHERE matricula_conv = ? """, (self.matricula_convidado,) )
        self.conn_conv.commit()
        self.desconecta_bd_conv()
        self.limpa_tela_convidado()
        self.select_lista_convidado()

    def update_convidado(self):
        self.variaveis_convidado()
        self.desconecta_bd_conv()
        self.conecta_bd_conv()

        for image in get_image_conv:
            self.insert_photo_convidado = self.convert_image_into_binary_conv(image)

        self.cursor_conv.execute(""" UPDATE convidados SET nome_conv = ?, email = ?, nascimento = ?, sexo = ?, cpf = ?, telefone = ?, cep = ?, logradouro = ?, complemento = ?, bairro = ?, cidade = ?, modalidade = ?, valor = ?, foto_conv = ? 
                                WHERE matricula_conv = ? """, (self.nome_convidado, self.email_convidado, self.nascimento_convidado, self.sexo_convidado, self.cpf_convidado, self.telefone_convidado, self.cep_convidado, self.logradouro_convidado, self.complemento_convidado, self.bairro_convidado, self.cidade_convidado, self.modalidade_convidado, self.valor_convidado, self.insert_photo_convidado, self.matricula_convidado))
        self.conn_conv.commit()                        
        self.desconecta_bd_conv()
        self.select_lista_convidado()
        self.limpa_tela_convidado()

    def buscar_convidado(self):
        self.conecta_bd_conv()
        self.listaConv.delete(*self.listaConv.get_children())
        self.ed_nome_convidado.insert(END, '%')
        nome_convidado= self.ed_nome_convidado.get()
        self.cursor_conv.execute(
            """ SELECT matricula_conv, nome_conv, email, nascimento, sexo, cpf, telefone, cep, logradouro, complemento, bairro, cidade, modalidade, valor FROM convidados 
            WHERE nome_conv LIKE "%s" ORDER BY nome_conv ASC """ % nome_convidado)
        buscanomeConv = self.cursor_conv.fetchall()
        for j in buscanomeConv:
            self.listaConv.insert("",END, values=j)
        self.limpa_tela_convidado()    
        self.desconecta_bd_conv()

    def refresh_lista_convidados(self): #Atualiza lista após buscar alguem cadastrado:
        self.variaveis_convidado()
        self.conecta_bd_conv()                       
        self.desconecta_bd_conv()
        self.select_lista_convidado()
        self.limpa_tela_convidado()

    def calendar_Frame_convidado(self):
        self.janela_5 = Toplevel()
        self.janela_5.title("Calendario")
        self.janela_5.configure(background= '#155569')
        self.janela_5.geometry('390x300')  
        self.janela_5.resizable(False, False) 
        self.calendario_3 = Calendar(self.janela_5, fg="gray75", bg="blue", font=("verdana", '9', 'bold'), locale='pt_br')
        self.calendario_3.place(relx=0.1, rely=0.1)
        self.inserirData_conv = Button(self.janela_5, text= "Inserir Data", font=('verdana', '9'), command= self.printCalendar_convidado)
        self.inserirData_conv.place(relx=0.35, rely=0.85, relheight=0.1, relwidth=0.3)

    def printCalendar_convidado (self):
        dataEntry_conv = self.calendario_3.get_date()
        self.janela_5.destroy()
        self.ed_nascimento_convidado.delete(0, END)
        self.ed_nascimento_convidado.insert(END, dataEntry_conv)
        self.inserirData_conv.destroy()  

class App(Funcs_cadastro_cliente, Funcs_cadastro_funcionario, Funcs_cadastro_convidado):
    def __init__(self):
        self.root = Tk()
        self.style = ttk.Style()
        self.tela()
        self.frames_de_tela()
        self.Widgets_aba1()
        self.Widgets_aba2()
        self.Widgets_aba3()
        self.montaTabelas()
        self.montaTabelas_func()
        self.montaTabelas_conv()
        self.select_lista()
        self.select_lista_funcionario()
        self.select_lista_convidado()
        self.Menus()
        self.root.mainloop()
    
    def tela(self):
        self.root.title("Cadastro Academia LocBoy")
        self.root.configure(background= '#155569')
        self.root.geometry('700x800')  
        self.root.resizable(True, True)  
        self.root.maxsize(width= 840, height=960)
        self.root.minsize(width= 700, height=785)
      
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

        self.abas.place(relx= 0,rely=0,  relwidth=1, relheight=1)
        self.aba1.configure(background= 'lightgrey')
        self.aba2.configure(background= 'lightgrey')
        self.aba3.configure(background= 'lightgrey')

        self.abas.add(self.aba1, text="Cadastro Cliente")
        self.abas.add(self.aba2, text="Cadastro Funcionário")
        self.abas.add(self.aba3, text="Cadastro Convidado")
         
    def Widgets_aba1 (self):
        
        #Botões:
        self.bt_limpar = Button(self.aba1, text= "Limpar", font=('verdana', '9'), command= self.limpa_tela )
        self.bt_limpar.place(relx= 0.025,rely=0.005,  relwidth=0.1, relheight= 0.035)   

        self.bt_buscar = Button(self.aba1, text= "Buscar", font=('verdana', '9'), command=self.buscar_cliente)
        self.bt_buscar.place(relx= 0.125, rely=0.005, relwidth=0.1, relheight= 0.035) 

        self.bt_refresh = Button(self.aba1, text= "Atualizar", font=('verdana', '9'), command=self.refresh_lista)
        self.bt_refresh.place(relx= 0.225, rely=0.005, relwidth=0.1, relheight= 0.035)

        self.bt_novo_cadastro = Button(self.aba1, text= "Novo", font=('verdana', '9'), command=self.validar_cadastro)
        self.bt_novo_cadastro.place(relx= 0.625, rely=0.005, relwidth=0.15, relheight= 0.035) 

        self.bt_alterar = Button(self.aba1, text= "Alterar", font=('verdana', '9'), command=self.validar_update_cadastro)
        self.bt_alterar.place(relx= 0.775, rely=0.005, relwidth=0.1, relheight= 0.035)

        self.bt_apagar = Button(self.aba1, text= "Excluir", font=('verdana', '9'), command=self.validar_exclusao)
        self.bt_apagar.place(relx= 0.875, rely=0.005, relwidth=0.1, relheight= 0.035)
        
        self.select_image = Button(self.aba1,text='Selecione a Imagem',command=self.adicionar_imagem)
        self.select_image.place(relx= 0.625, rely=0.4, width=182, relheight= 0.035)

        self.bt_data = Button(self.aba1, text= "Editar", font=('verdana', '9'), command=self.calendar_Frame)
        self.bt_data.place(relx= 0.345, rely=0.185, relwidth=0.08, height=24)

        
        #Entradas da aba1:
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
        self.ed_nascimento.place(relx=0.22, rely=0.185, relwidth= 0.115)

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

        #16-Foto do cliente/logo:
        self.fln1 = ("C:/Users/Hugo Rodrigues/OneDrive - Anima Holding/ADS/PROGRAMAÇÃO DE SOLUÇÕES COMPUTACIONAIS/EXERCÍCIOS/A3/fotos_perfil/Locboy.png")
        self.img1 = Image.open(self.fln1)
        self.resized1 = self.img1.resize((182,183), Image.LANCZOS)
        self.nova_img1= ImageTk.PhotoImage(self.resized1)
        self.frame_moldura = Label(self.aba1, image=self.nova_img1)
        self.frame_moldura.place(relx=0.625,rely=0.14,height=182,width=182)

        #17-Lista de matriculados :
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
   

        self.listaCli.column('#0', width=1, minwidth= 20)
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
       
        self.listaCli.place(relx=0.005, rely=0.7, relwidth= 1, relheight=0.3)
        
        #18-Scrollbar Vertical:
        self.scrollistaV = ttk.Scrollbar(self.aba1, orient= 'vertical', command= self.listaCli.yview)
        self.listaCli['yscrollcommand'] = self.scrollistaV.set
        self.scrollistaV.place(relx=0.975, rely=0.7, relwidth= 0.025, relheight=0.275)

        #19- Scrollbar Horizontal:
        self.scrollistaH = ttk.Scrollbar(self.aba1, orient= 'horizontal', command= self.listaCli.xview)
        self.listaCli['xscrollcommand'] = self.scrollistaH.set
        self.scrollistaH.place(relx=0.005, rely=0.975, relwidth= 1, relheight=0.025)
        
        #selecionar tipo de tema (aqlt, clam, default):
        self.style.theme_use('alt')
        
        #Estilizando tema fo Treeview selecionada:
        self.style.configure('Treeview', background='white', foreground='black',rowheight='25', fieldbackground= 'white', bd=1)
        self.style.map('Treeview', background=[('selected', 'green')])
        self.listaCli.bind("<Double-1>", self.clique_duplo)

    def Widgets_aba2 (self):
        
        #Botões:
        self.bt_limpar_funcionario = Button(self.aba2, text= "Limpar", font=('verdana', '9'), command= self.limpa_tela_funcionario )
        self.bt_limpar_funcionario.place(relx= 0.025,rely=0.005,  relwidth=0.1, relheight= 0.035)   

        self.bt_buscar_funcionario = Button(self.aba2, text= "Buscar", font=('verdana', '9'), command=self.buscar_funcionario)
        self.bt_buscar_funcionario.place(relx= 0.125, rely=0.005, relwidth=0.1, relheight= 0.035) 

        self.bt_refresh_funcionario = Button(self.aba2, text= "Atualizar", font=('verdana', '9'), command=self.refresh_lista_funcionarios)
        self.bt_refresh_funcionario.place(relx= 0.225, rely=0.005, relwidth=0.1, relheight= 0.035)

        self.bt_novo_cadastro_funcionario = Button(self.aba2, text= "Novo", font=('verdana', '9'), command=self.validar_cadastro_funcionario)
        self.bt_novo_cadastro_funcionario.place(relx= 0.625, rely=0.005, relwidth=0.15, relheight= 0.035) 

        self.bt_alterar_funcionario = Button(self.aba2, text= "Alterar", font=('verdana', '9'), command=self.validar_update_cadastro_funcionario)
        self.bt_alterar_funcionario.place(relx= 0.775, rely=0.005, relwidth=0.1, relheight= 0.035)

        self.bt_apagar_funcionario = Button(self.aba2, text= "Excluir", font=('verdana', '9'), command=self.validar_exclusao_funcionario)
        self.bt_apagar_funcionario.place(relx= 0.875, rely=0.005, relwidth=0.1, relheight= 0.035)
        
        self.select_image_funcionario = Button(self.aba2,text='Selecione a Imagem',command=self.adicionar_imagem_funcionario)
        self.select_image_funcionario.place(relx= 0.625, rely=0.4, width=182, relheight= 0.035)

        self.bt_data_funcionario = Button(self.aba2, text= "Editar", font=('verdana', '9'), command=self.calendar_Frame_funcionario)
        self.bt_data_funcionario.place(relx= 0.345, rely=0.185, relwidth=0.08, height=24)

        
        
        #Entradas da aba2:
        #1-Matrícula;
        self.lb_matricula_funcionario = Label(self.aba2, text= 'Matrícula:', bg='lightgrey')
        self.lb_matricula_funcionario.place(relx=0.025, rely=0.05)

        self.ed_matricula_funcionario = Entry(self.aba2, bd=2)
        self.ed_matricula_funcionario.place(relx=0.125, rely=0.05, relwidth= 0.1)
        #2-Nome;
        self.lb_nome_funcionario = Label(self.aba2, text= 'Nome:', bg='lightgrey')
        self.lb_nome_funcionario.place(relx=0.025, rely=0.095)

        self.ed_nome_funcionario = Entry(self.aba2, bd=2)
        self.ed_nome_funcionario.place(relx=0.125, rely=0.095, relwidth= 0.3)

        #3-Email;
        self.lb_email_funcionario = Label(self.aba2, text= 'E-mail:', bg='lightgrey')
        self.lb_email_funcionario.place(relx=0.025, rely=0.14)

        self.ed_email_funcionario = Entry(self.aba2, bd=2)
        self.ed_email_funcionario.place(relx=0.125, rely=0.14, relwidth= 0.3)

        #4-Data de nascimento;
        self.lb_nascimento_funcionario = Label(self.aba2, text= 'Data de Nascimento:', bg='lightgrey')
        self.lb_nascimento_funcionario.place(relx=0.025, rely=0.185)

        self.ed_nascimento_funcionario = Entry(self.aba2, bd=2)
        self.ed_nascimento_funcionario.place(relx=0.22, rely=0.185, relwidth= 0.115)

        #5-Sexo;
        self.lb_sexo_funcionario = Label(self.aba2, text= 'Sexo:', bg='lightgrey')
        self.lb_sexo_funcionario.place(relx=0.025, rely=0.23)

        self.lista_sexo_funcionario=['Masculino', 'Feminino']
        self.cb_sexo_funcionario= ttk.Combobox(self.aba2, values= self.lista_sexo_funcionario)
        self.cb_sexo_funcionario.place(relx=0.125, rely=0.23, relwidth=0.3, relheight=0.03)

        #6-CPF;
        self.lb_cpf_funcionario = Label(self.aba2, text= 'CPF:', bg='lightgrey')
        self.lb_cpf_funcionario.place(relx=0.025, rely=0.275)
        self.lb_cpf_funcionario_erro = Label(self.aba2, text= '', bg='lightgrey')
        self.lb_cpf_funcionario_erro.place(relx=0.43, rely=0.275)

        self.ed_cpf_funcionario = Entry(self.aba2, bd=2)
        self.ed_cpf_funcionario.place(relx=0.125, rely=0.275, relwidth= 0.3)

        #7-Telefone;
        self.lb_telefone_funcionario = Label(self.aba2, text= 'Telefone:', bg='lightgrey')
        self.lb_telefone_funcionario.place(relx=0.025, rely=0.32)
        
        self.ed_telefone_funcionario= Entry(self.aba2, bd=2)
        self.ed_telefone_funcionario.place(relx=0.125, rely=0.32, relwidth= 0.3)

        #8-CEP;
        self.lb_cep_funcionario = Label(self.aba2, text= 'CEP:', bg='lightgrey')
        self.lb_cep_funcionario.place(relx=0.025, rely=0.365)

        self.ed_cep_funcionario = Entry(self.aba2, bd=2)
        self.ed_cep_funcionario.place(relx=0.125, rely=0.365, relwidth= 0.3)

        #10-Logradouro;
        self.lb_logradouro_funcionario = Label(self.aba2, text= 'Logradouro:', bg='lightgrey')
        self.lb_logradouro_funcionario.place(relx=0.025, rely=0.41)

        self.ed_logradouro_funcionario = Entry(self.aba2, bd=2)
        self.ed_logradouro_funcionario.place(relx=0.16, rely=0.41, relwidth= 0.265)

        #11-Complemento;
        self.lb_complemento_funcionario = Label(self.aba2, text= 'Complemento:', bg='lightgrey')
        self.lb_complemento_funcionario.place(relx=0.025, rely=0.455)

        self.ed_complemento_funcionario = Entry(self.aba2, bd=2)
        self.ed_complemento_funcionario.place(relx=0.18, rely=0.455, relwidth= 0.245)

        #12-Bairro;
        self.lb_bairro_funcionario = Label(self.aba2, text= 'Bairro:', bg='lightgrey')
        self.lb_bairro_funcionario.place(relx=0.025, rely=0.50)

        self.ed_bairro_funcionario = Entry(self.aba2, bd=2)
        self.ed_bairro_funcionario.place(relx=0.125, rely=0.50, relwidth= 0.3)

        #13-Cidade;
        self.lb_cidade_funcionario = Label(self.aba2, text= 'Cidade:', bg='lightgrey')
        self.lb_cidade_funcionario.place(relx=0.025, rely=0.545)

        self.ed_cidade_funcionario = Entry(self.aba2, bd=2)
        self.ed_cidade_funcionario.place(relx=0.125, rely=0.545, relwidth= 0.3)
        
        #14-Cargo;
        self.lb_cargo_funcionario = Label(self.aba2, text= 'Cargo:', bg='lightgrey')
        self.lb_cargo_funcionario.place(relx=0.025, rely=0.59)
        
        #15-Lista de cargos;
        self.lista_cargo_funcionario=['Recepcionista', 'Instrutor','ASG']
        self.cb_cargo_funcionario= ttk.Combobox(self.aba2, values= self.lista_cargo_funcionario)
        self.cb_cargo_funcionario.place(relx=0.175, rely=0.59, relwidth=0.25, relheight=0.03)
        self.cb_cargo_funcionario.bind('<<ComboboxSelected>>', self.valores_funcionario)#Ação quando selecionado um item no combobox
       
        #16-Salário;
        self.lb_salario_funcionario = Label(self.aba2, text= 'Salário:', bg='lightgrey')
        self.lb_salario_funcionario.place(relx=0.025, rely=0.635)
        self.lb_valor_salario_funcionario = Label(self.aba2, text= '', bg='lightgrey', fg= 'blue' , font=(50))
        self.lb_valor_salario_funcionario.place(relx=0.165, rely=0.635)

        #17-Foto do funcionário/logo:
        self.fln1_funcionario = ("C:/Users/Hugo Rodrigues/OneDrive - Anima Holding/ADS/PROGRAMAÇÃO DE SOLUÇÕES COMPUTACIONAIS/EXERCÍCIOS/A3/fotos_perfil/Locboy.png")
        self.img1_funcionario = Image.open(self.fln1_funcionario)
        self.resized1_funcionario = self.img1_funcionario.resize((182,183), Image.LANCZOS)
        self.nova_img1_funcionario= ImageTk.PhotoImage(self.resized1_funcionario)
        self.frame_moldura_funcionario = Label(self.aba2, image=self.nova_img1_funcionario)
        self.frame_moldura_funcionario.place(relx=0.625,rely=0.14,height=182,width=182)

        #18-Lista de matriculados :
        self.listaFunc = ttk.Treeview(self.aba2, height= 3, column=('col1_func', 'col2_func','col3_func','col4_func','col5_func','col6_func','col7_func','col8_func','col9_func','col10_func','col11_func','col12_func','col13_func','col14_func','col15_func'))
        self.listaFunc.heading('#0', text='')
        self.listaFunc.heading('#1', text='Matrícula')
        self.listaFunc.heading('#2', text='Nome')
        self.listaFunc.heading('#3', text='E-mail')
        self.listaFunc.heading('#4', text='Nascimento')
        self.listaFunc.heading('#5', text='Sexo')
        self.listaFunc.heading('#6', text='CPF')
        self.listaFunc.heading('#7', text='Telefone')
        self.listaFunc.heading('#8', text='CEP')
        self.listaFunc.heading('#9', text='Logradouro')
        self.listaFunc.heading('#10', text='Complemento')
        self.listaFunc.heading('#11', text='Bairro')
        self.listaFunc.heading('#12', text='Cidade')
        self.listaFunc.heading('#13', text='Cargo')
        self.listaFunc.heading('#14', text='Salário')
   

        self.listaFunc.column('#0', width=1, minwidth= 20)
        self.listaFunc.column('#1', width=60, minwidth= 80)
        self.listaFunc.column('#2', width=100, minwidth= 220)
        self.listaFunc.column('#3', width=60, minwidth= 150)
        self.listaFunc.column('#4', width=60, minwidth= 100)
        self.listaFunc.column('#5', width=60, minwidth= 100)
        self.listaFunc.column('#6', width=60, minwidth= 100)
        self.listaFunc.column('#7', width=60, minwidth= 100)
        self.listaFunc.column('#8', width=60, minwidth= 100)
        self.listaFunc.column('#9', width=60, minwidth= 200)
        self.listaFunc.column('#10', width=60, minwidth= 120)
        self.listaFunc.column('#11', width=60, minwidth= 100)
        self.listaFunc.column('#12', width=60, minwidth= 100)
        self.listaFunc.column('#13', width=60, minwidth= 100)
        self.listaFunc.column('#14', width=60, minwidth= 100)
       
        self.listaFunc.place(relx=0.005, rely=0.7, relwidth= 1, relheight=0.3)
        
        #19-Scrollbar Vertical:
        self.scrollistaV_funcionario = ttk.Scrollbar(self.aba2, orient= 'vertical', command= self.listaFunc.yview)
        self.listaFunc['yscrollcommand'] = self.scrollistaV_funcionario.set
        self.scrollistaV_funcionario.place(relx=0.975, rely=0.7, relwidth= 0.025, relheight=0.275)

        #20- Scrollbar Horizontal:
        self.scrollistaH_funcionario = ttk.Scrollbar(self.aba2, orient= 'horizontal', command= self.listaFunc.xview)
        self.listaFunc['xscrollcommand'] = self.scrollistaH_funcionario.set
        self.scrollistaH_funcionario.place(relx=0.005, rely=0.975, relwidth= 1, relheight=0.025)
        
        #selecionar tipo de tema (aqlt, clam, default):
        self.style.theme_use('alt')
        
        #Estilizando tema fo Treeview selecionada:
        self.style.configure('Treeview', background='white', foreground='black',rowheight='25', fieldbackground= 'white', bd=1)
        self.style.map('Treeview', background=[('selected', 'green')])
        self.listaFunc.bind("<Double-1>", self.clique_duplo_func)

    def Widgets_aba3 (self):
        
        #Botões:
        self.bt_limpar_convidado = Button(self.aba3, text= "Limpar", font=('verdana', '9'), command= self.limpa_tela_convidado )
        self.bt_limpar_convidado.place(relx= 0.025,rely=0.005,  relwidth=0.1, relheight= 0.035)   

        self.bt_buscar_convidado = Button(self.aba3, text= "Buscar", font=('verdana', '9'), command=self.buscar_convidado)
        self.bt_buscar_convidado.place(relx= 0.125, rely=0.005, relwidth=0.1, relheight= 0.035) 

        self.bt_refresh_convidado = Button(self.aba3, text= "Atualizar", font=('verdana', '9'), command=self.refresh_lista_convidados)
        self.bt_refresh_convidado.place(relx= 0.225, rely=0.005, relwidth=0.1, relheight= 0.035)

        self.bt_novo_cadastro_convidado = Button(self.aba3, text= "Novo", font=('verdana', '9'), command=self.validar_cadastro_convidado)
        self.bt_novo_cadastro_convidado.place(relx= 0.625, rely=0.005, relwidth=0.15, relheight= 0.035) 

        self.bt_alterar_convidado = Button(self.aba3, text= "Alterar", font=('verdana', '9'), command=self.validar_update_cadastro_convidado)
        self.bt_alterar_convidado.place(relx= 0.775, rely=0.005, relwidth=0.1, relheight= 0.035)

        self.bt_apagar_convidado = Button(self.aba3, text= "Excluir", font=('verdana', '9'), command=self.validar_exclusao_convidado)
        self.bt_apagar_convidado.place(relx= 0.875, rely=0.005, relwidth=0.1, relheight= 0.035)
        
        self.select_image_convidado = Button(self.aba3,text='Selecione a Imagem',command=self.adicionar_imagem_convidado)
        self.select_image_convidado.place(relx= 0.625, rely=0.4, width=182, relheight= 0.035)

        self.bt_data_convidado = Button(self.aba3, text= "Editar", font=('verdana', '9'), command=self.calendar_Frame_convidado)
        self.bt_data_convidado.place(relx= 0.345, rely=0.185, relwidth=0.08, height=24)

        
        
        #Entradas da aba3:
        #1-Matrícula;
        self.lb_matricula_convidado = Label(self.aba3, text= 'Matrícula:', bg='lightgrey')
        self.lb_matricula_convidado.place(relx=0.025, rely=0.05)

        self.ed_matricula_convidado = Entry(self.aba3, bd=2)
        self.ed_matricula_convidado.place(relx=0.125, rely=0.05, relwidth= 0.1)
        #2-Nome;
        self.lb_nome_convidado = Label(self.aba3, text= 'Nome:', bg='lightgrey')
        self.lb_nome_convidado.place(relx=0.025, rely=0.095)

        self.ed_nome_convidado = Entry(self.aba3, bd=2)
        self.ed_nome_convidado.place(relx=0.125, rely=0.095, relwidth= 0.3)

        #3-Email;
        self.lb_email_convidado = Label(self.aba3, text= 'E-mail:', bg='lightgrey')
        self.lb_email_convidado.place(relx=0.025, rely=0.14)

        self.ed_email_convidado = Entry(self.aba3, bd=2)
        self.ed_email_convidado.place(relx=0.125, rely=0.14, relwidth= 0.3)

        #4-Data de nascimento;
        self.lb_nascimento_convidado = Label(self.aba3, text= 'Data de Nascimento:', bg='lightgrey')
        self.lb_nascimento_convidado.place(relx=0.025, rely=0.185)

        self.ed_nascimento_convidado = Entry(self.aba3, bd=2)
        self.ed_nascimento_convidado.place(relx=0.22, rely=0.185, relwidth= 0.115)

        #5-Sexo;
        self.lb_sexo_convidado = Label(self.aba3, text= 'Sexo:', bg='lightgrey')
        self.lb_sexo_convidado.place(relx=0.025, rely=0.23)

        self.lista_sexo_convidado=['Masculino', 'Feminino']
        self.cb_sexo_convidado= ttk.Combobox(self.aba3, values= self.lista_sexo_convidado)
        self.cb_sexo_convidado.place(relx=0.125, rely=0.23, relwidth=0.3, relheight=0.03)

        #6-CPF;
        self.lb_cpf_convidado = Label(self.aba3, text= 'CPF:', bg='lightgrey')
        self.lb_cpf_convidado.place(relx=0.025, rely=0.275)
        self.lb_cpf_convidado_erro = Label(self.aba3, text= '', bg='lightgrey')
        self.lb_cpf_convidado_erro.place(relx=0.43, rely=0.275)

        self.ed_cpf_convidado = Entry(self.aba3, bd=2)
        self.ed_cpf_convidado.place(relx=0.125, rely=0.275, relwidth= 0.3)

        #7-Telefone;
        self.lb_telefone_convidado = Label(self.aba3, text= 'Telefone:', bg='lightgrey')
        self.lb_telefone_convidado.place(relx=0.025, rely=0.32)
        
        self.ed_telefone_convidado= Entry(self.aba3, bd=2)
        self.ed_telefone_convidado.place(relx=0.125, rely=0.32, relwidth= 0.3)

        #8-CEP;
        self.lb_cep_convidado = Label(self.aba3, text= 'CEP:', bg='lightgrey')
        self.lb_cep_convidado.place(relx=0.025, rely=0.365)

        self.ed_cep_convidado = Entry(self.aba3, bd=2)
        self.ed_cep_convidado.place(relx=0.125, rely=0.365, relwidth= 0.3)

        #10-Logradouro;
        self.lb_logradouro_convidado = Label(self.aba3, text= 'Logradouro:', bg='lightgrey')
        self.lb_logradouro_convidado.place(relx=0.025, rely=0.41)

        self.ed_logradouro_convidado = Entry(self.aba3, bd=2)
        self.ed_logradouro_convidado.place(relx=0.16, rely=0.41, relwidth= 0.265)

        #11-Complemento;
        self.lb_complemento_convidado = Label(self.aba3, text= 'Complemento:', bg='lightgrey')
        self.lb_complemento_convidado.place(relx=0.025, rely=0.455)

        self.ed_complemento_convidado = Entry(self.aba3, bd=2)
        self.ed_complemento_convidado.place(relx=0.18, rely=0.455, relwidth= 0.245)

        #12-Bairro;
        self.lb_bairro_convidado = Label(self.aba3, text= 'Bairro:', bg='lightgrey')
        self.lb_bairro_convidado.place(relx=0.025, rely=0.50)

        self.ed_bairro_convidado = Entry(self.aba3, bd=2)
        self.ed_bairro_convidado.place(relx=0.125, rely=0.50, relwidth= 0.3)

        #13-Cidade;
        self.lb_cidade_convidado = Label(self.aba3, text= 'Cidade:', bg='lightgrey')
        self.lb_cidade_convidado.place(relx=0.025, rely=0.545)

        self.ed_cidade_convidado = Entry(self.aba3, bd=2)
        self.ed_cidade_convidado.place(relx=0.125, rely=0.545, relwidth= 0.3)
        
        #14-Cargo;
        self.lb_modalidade_convidado = Label(self.aba3, text= 'Modalidade:', bg='lightgrey')
        self.lb_modalidade_convidado.place(relx=0.025, rely=0.59)
        
        #15-Lista de modalidades;
        self.lista_modalidade_convidado=['Musculação', 'Pilates','Spinning']
        self.cb_modalidade_convidado= ttk.Combobox(self.aba3, values= self.lista_modalidade_convidado)
        self.cb_modalidade_convidado.place(relx=0.175, rely=0.59, relwidth=0.25, relheight=0.03)
        self.cb_modalidade_convidado.bind('<<ComboboxSelected>>', self.valores_convidado)#Ação quando selecionado um item no combobox
       
        #16-Preço;
        self.lb_preco_convidado = Label(self.aba3, text= 'Preço:', bg='lightgrey')
        self.lb_preco_convidado.place(relx=0.025, rely=0.635)
        self.lb_valor_convidado = Label(self.aba3, text= '', bg='lightgrey', fg= 'green' , font=(50))
        self.lb_valor_convidado.place(relx=0.165, rely=0.635)

        #17-Foto do convidado/logo:
        self.fln1_convidado = ("C:/Users/Hugo Rodrigues/OneDrive - Anima Holding/ADS/PROGRAMAÇÃO DE SOLUÇÕES COMPUTACIONAIS/EXERCÍCIOS/A3/fotos_perfil/Locboy.png")
        self.img1_convidado = Image.open(self.fln1_convidado)
        self.resized1_convidado = self.img1_convidado.resize((182,183), Image.LANCZOS)
        self.nova_img1_convidado= ImageTk.PhotoImage(self.resized1_convidado)
        self.frame_moldura_convidado = Label(self.aba3, image=self.nova_img1_convidado)
        self.frame_moldura_convidado.place(relx=0.625,rely=0.14,height=182,width=182)

        #18-Lista de matriculados :
        self.listaConv = ttk.Treeview(self.aba3, height= 3, column=('col1_conv', 'col2_conv','col3_conv','col4_conv','col5_conv','col6_conv','col7_conv','col8_conv','col9_conv','col10_conv','col11_conv','col12_conv','col13_conv','col14_conv','col15_conv'))
        self.listaConv.heading('#0', text='')
        self.listaConv.heading('#1', text='Matrícula')
        self.listaConv.heading('#2', text='Nome')
        self.listaConv.heading('#3', text='E-mail')
        self.listaConv.heading('#4', text='Nascimento')
        self.listaConv.heading('#5', text='Sexo')
        self.listaConv.heading('#6', text='CPF')
        self.listaConv.heading('#7', text='Telefone')
        self.listaConv.heading('#8', text='CEP')
        self.listaConv.heading('#9', text='Logradouro')
        self.listaConv.heading('#10', text='Complemento')
        self.listaConv.heading('#11', text='Bairro')
        self.listaConv.heading('#12', text='Cidade')
        self.listaConv.heading('#13', text='Modalidade')
        self.listaConv.heading('#14', text='Valor')
   

        self.listaConv.column('#0', width=1, minwidth= 20)
        self.listaConv.column('#1', width=60, minwidth= 80)
        self.listaConv.column('#2', width=100, minwidth= 220)
        self.listaConv.column('#3', width=60, minwidth= 150)
        self.listaConv.column('#4', width=60, minwidth= 100)
        self.listaConv.column('#5', width=60, minwidth= 100)
        self.listaConv.column('#6', width=60, minwidth= 100)
        self.listaConv.column('#7', width=60, minwidth= 100)
        self.listaConv.column('#8', width=60, minwidth= 100)
        self.listaConv.column('#9', width=60, minwidth= 200)
        self.listaConv.column('#10', width=60, minwidth= 120)
        self.listaConv.column('#11', width=60, minwidth= 100)
        self.listaConv.column('#12', width=60, minwidth= 100)
        self.listaConv.column('#13', width=60, minwidth= 100)
        self.listaConv.column('#14', width=60, minwidth= 100)
       
        self.listaConv.place(relx=0.005, rely=0.7, relwidth= 1, relheight=0.3)
        
        #19-Scrollbar Vertical:
        self.scrollistaV_convidado = ttk.Scrollbar(self.aba3, orient= 'vertical', command= self.listaConv.yview)
        self.listaConv['yscrollcommand'] = self.scrollistaV_convidado.set
        self.scrollistaV_convidado.place(relx=0.975, rely=0.7, relwidth= 0.025, relheight=0.275)

        #20- Scrollbar Horizontal:
        self.scrollistaH_convidado = ttk.Scrollbar(self.aba3, orient= 'horizontal', command= self.listaConv.xview)
        self.listaConv['xscrollcommand'] = self.scrollistaH_convidado.set
        self.scrollistaH_convidado.place(relx=0.005, rely=0.975, relwidth= 1, relheight=0.025)
        
        #selecionar tipo de tema (aqlt, clam, default):
        self.style.theme_use('alt')
        
        #Estilizando tema fo Treeview selecionada:
        self.style.configure('Treeview', background='white', foreground='black',rowheight='25', fieldbackground= 'white', bd=1)
        self.style.map('Treeview', background=[('selected', 'green')])
        self.listaConv.bind("<Double-1>", self.clique_duplo_conv)

    def valores(self, event):
        #Função para adicionar valor da mensalidade ao escolher um plano na label self.lb_preço:
        self.valor = self.cb_plano.get()
        if self.valor == self.lista_plano[0]:
            self.lb_preço['text'] = ('R$ 70,00')
        elif self.valor == self.lista_plano[1]:
            self.lb_preço['text'] = ('R$ 90,00')
        elif self.valor == self.lista_plano[2]:
            self.lb_preço['text'] = ('R$ 120,00')

    def valores_funcionario(self, event):
        #Função para adicionar valor da mensalidade ao escolher um plano na label self.lb_preço:
        self.funcao_funcionario = self.cb_cargo_funcionario.get()
        if self.funcao_funcionario == self.lista_cargo_funcionario[0]:
            self.lb_valor_salario_funcionario['text'] = ('R$ 1500,00')
        elif self.funcao_funcionario == self.lista_cargo_funcionario[1]:
            self.lb_valor_salario_funcionario['text'] = ('R$ 2000,00')
        elif self.funcao_funcionario == self.lista_cargo_funcionario[2]:
            self.lb_valor_salario_funcionario['text'] = ('R$ 1500,00')

    def valores_convidado(self, event):
        #Função para adicionar valor da mensalidade ao escolher um plano na label self.lb_preço:
        self.funcao_convidado = self.cb_modalidade_convidado.get()
        if self.funcao_convidado == self.lista_modalidade_convidado[0]:
            self.lb_valor_convidado['text'] = ('Cortesia')
        elif self.funcao_convidado == self.lista_modalidade_convidado[1]:
            self.lb_valor_convidado['text'] = ('Cortesia')
        elif self.funcao_convidado == self.lista_modalidade_convidado[2]:
            self.lb_valor_convidado['text'] = ('Cortesia')       

    def validar_cadastro(self):

        cpf=self.ed_cpf.get()
        validacpf = bool
        digitos = []

        data = self.ed_nascimento.get()
        validaData = bool
        dataDoPc = datetime.today().strftime('%Y-%m-%d')
        separacaoPc = str(dataDoPc).split('-')
        separacaoUsr = str(data).split('/')
        diaUrs = int(separacaoUsr[0])
        mesUrs = int(separacaoUsr[1])
        anoUsr = int(separacaoUsr[2])
        diaPc = int(separacaoPc[2])
        mesPc = int(separacaoPc[1])
        anoPc = int(separacaoPc[0])

        #validando Data
        if anoUsr <= anoPc - 100:
            if mesUrs > mesPc:
                validaData = False
            elif mesUrs == mesPc:
                if diaUrs >= diaPc:
                    validaData = False
                else:
                    validaData = True
            else:
                validaData = True
        else:
            validaData = True
                 
        #extrair os dígitos do CPF
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

        self.confirmar_cadastro =  messagebox.askyesno('Cadastrar cliente','Deseja confirmar cadastro?')

        if validacpf == True and validaData == True and self.confirmar_cadastro == True: 
            self.cadastrar_cliente()
            self.yes_alterar_1 =messagebox.showwarning("Cadastrar cliente", "Cadastro efetuado com sucesso!")

        elif validacpf == True and validaData == True and self.confirmar_cadastro == False:
            self.no_alterar_1 =messagebox.showwarning("Cadastrar cliente", "Cadastro cancelado!")

        elif validacpf == False and validaData == False:
            self.erro_cadastro_1 = messagebox.showerror('Erro de cadastro', 'Erro: CPF e Data de Nascimento inválidos!')

        elif validaData == False:
            self.erro_cadastro_1 = messagebox.showerror('Erro de cadastro', 'Erro: Data de Nascimento inválida!')

        elif validacpf == False: 
            self.erro_cadastro_1 = messagebox.showerror('Erro de cadastro', 'Erro: CPF inválido!')

    def validar_cadastro_funcionario(self):

        cpf_func=self.ed_cpf_funcionario.get()
        validacpf_func = bool
        digitos_func = []

        data_func = self.ed_nascimento_funcionario.get()
        validaData_func = bool
        dataDoPc_func = datetime.today().strftime('%Y-%m-%d')
        separacaoPc_func = str(dataDoPc_func).split('-')
        separacaoUsr_func = str(data_func).split('/')
        diaUrs_func = int(separacaoUsr_func[0])
        mesUrs_func = int(separacaoUsr_func[1])
        anoUsr_func = int(separacaoUsr_func[2])
        diaPc_func = int(separacaoPc_func[2])
        mesPc_func = int(separacaoPc_func[1])
        anoPc_func = int(separacaoPc_func[0])

        #validando Data
        if anoUsr_func <= anoPc_func - 100:
            if mesUrs_func > mesPc_func:
                validaData_func = False
            elif mesUrs_func == mesPc_func:
                if diaUrs_func >= diaPc_func:
                    validaData_func = False
                else:
                    validaData_func = True
            else:
                validaData_func = True
        else:
            validaData_func = True
                 
        #extrair os dígitos do CPF
        for digito in str(cpf_func):
            digitos_func.append(int(digito))

        if len(digitos_func)!= 11:
            validacpf_func = False

        elif digitos_func[0] == digitos_func[1] == digitos_func[2] == digitos_func[3] == digitos_func[4] == digitos_func[5] == digitos_func[6] == digitos_func[7] == digitos_func[8] ==digitos_func[9] == digitos_func[10]:
            validacpf_func = False
        else:
            soma1_func = digitos_func[0]*10 + digitos_func[1]*9 + digitos_func[2]*8 + digitos_func[3]*7 + digitos_func[4]*6 + digitos_func[5]*5 + digitos_func[6]*4 + digitos_func[7]*3 + digitos_func[8]*2
            resto1_func = (soma1_func * 10) % 11

            if resto1_func == 10:
                resto1_func = 0

            soma2_func = digitos_func[0]*11 + digitos_func[1]*10 + digitos_func[2]*9 + digitos_func[3]*8 + digitos_func[4]*7 + digitos_func[5]*6 + digitos_func[6]*5 + digitos_func[7]*4 + digitos_func[8]*3 + digitos_func[9]*2
            resto2_func = (soma2_func * 10) % 11

            if resto2_func == 10:
                resto2_func = 0

            if resto1_func == digitos_func[9] and resto2_func == digitos_func[10]:
                validacpf_func = True
            else:
                validacpf_func = False

        self.confirmar_cadastro_func =  messagebox.askyesno('Cadastrar funcionário','Deseja confirmar cadastro?')

        if validacpf_func == True and validaData_func == True and self.confirmar_cadastro_func == True: 
            self.cadastrar_funcionario()
            self.yes_alterar_1_func =messagebox.showwarning("Cadastrar funcionário", "Cadastro efetuado com sucesso!")

        elif validacpf_func == True and validaData_func == True and self.confirmar_cadastro_func == False:
            self.no_alterar_1_func =messagebox.showwarning("Cadastrar funcionário", "Cadastro cancelado!")

        elif validacpf_func == False and validaData_func == False:
            self.erro_cadastro_1_func = messagebox.showerror('Erro de cadastro', 'Erro: CPF e Data de Nascimento inválidos!')

        elif validaData_func == False:
            self.erro_cadastro_1_func = messagebox.showerror('Erro de cadastro', 'Erro: Data de Nascimento inválida!')

        elif validacpf_func == False: 
            self.erro_cadastro_1_func = messagebox.showerror('Erro de cadastro', 'Erro: CPF inválido!')

    def validar_cadastro_convidado(self):

        cpf_conv=self.ed_cpf_convidado.get()
        validacpf_conv = bool
        digitos_conv = []

        data_conv = self.ed_nascimento_convidado.get()
        validaData_conv = bool
        dataDoPc_conv = datetime.today().strftime('%Y-%m-%d')
        separacaoPc_conv = str(dataDoPc_conv).split('-')
        separacaoUsr_conv = str(data_conv).split('/')
        diaUrs_conv = int(separacaoUsr_conv[0])
        mesUrs_conv = int(separacaoUsr_conv[1])
        anoUsr_conv = int(separacaoUsr_conv[2])
        diaPc_conv = int(separacaoPc_conv[2])
        mesPc_conv = int(separacaoPc_conv[1])
        anoPc_conv = int(separacaoPc_conv[0])

        #validando Data
        if anoUsr_conv <= anoPc_conv - 100:
            if mesUrs_conv > mesPc_conv:
                validaData_conv = False
            elif mesUrs_conv == mesPc_conv:
                if diaUrs_conv >= diaPc_conv:
                    validaData_conv = False
                else:
                    validaData_conv = True
            else:
                validaData_conv = True
        else:
            validaData_conv = True
                 
        #extrair os dígitos do CPF
        for digito in str(cpf_conv):
            digitos_conv.append(int(digito))

        if len(digitos_conv)!= 11:
            validacpf_conv = False

        elif digitos_conv[0] == digitos_conv[1] == digitos_conv[2] == digitos_conv[3] == digitos_conv[4] == digitos_conv[5] == digitos_conv[6] == digitos_conv[7] == digitos_conv[8] ==digitos_conv[9] == digitos_conv[10]:
            validacpf_conv = False
        else:
            soma1_conv = digitos_conv[0]*10 + digitos_conv[1]*9 + digitos_conv[2]*8 + digitos_conv[3]*7 + digitos_conv[4]*6 + digitos_conv[5]*5 + digitos_conv[6]*4 + digitos_conv[7]*3 + digitos_conv[8]*2
            resto1_conv = (soma1_conv * 10) % 11

            if resto1_conv == 10:
                resto1_conv = 0

            soma2_conv = digitos_conv[0]*11 + digitos_conv[1]*10 + digitos_conv[2]*9 + digitos_conv[3]*8 + digitos_conv[4]*7 + digitos_conv[5]*6 + digitos_conv[6]*5 + digitos_conv[7]*4 + digitos_conv[8]*3 + digitos_conv[9]*2
            resto2_conv = (soma2_conv * 10) % 11

            if resto2_conv == 10:
                resto2_conv = 0

            if resto1_conv == digitos_conv[9] and resto2_conv == digitos_conv[10]:
                validacpf_conv = True
            else:
                validacpf_conv = False

        self.confirmar_cadastro_conv =  messagebox.askyesno('Cadastrar convidado','Deseja confirmar cadastro?')

        if validacpf_conv == True and validaData_conv == True and self.confirmar_cadastro_conv == True: 
            self.cadastrar_convidado()
            self.yes_alterar_1_conv =messagebox.showwarning("Cadastrar convidado", "Cadastro efetuado com sucesso!")

        elif validacpf_conv == True and validaData_conv == True and self.confirmar_cadastro_conv == False:
            self.no_alterar_1_conv =messagebox.showwarning("Cadastrar convidado", "Cadastro cancelado!")

        elif validacpf_conv == False and validaData_conv == False:
            self.erro_cadastro_1_conv = messagebox.showerror('Erro de cadastro', 'Erro: CPF e Data de Nascimento inválidos!')

        elif validaData_conv == False:
            self.erro_cadastro_1_conv = messagebox.showerror('Erro de cadastro', 'Erro: Data de Nascimento inválida!')

        elif validacpf_conv == False: 
            self.erro_cadastro_1_conv = messagebox.showerror('Erro de cadastro', 'Erro: CPF inválido!')

    def validar_update_cadastro(self):
        cpf=self.ed_cpf.get()
        validacpf = bool
        digitos = []

        data = self.ed_nascimento.get()
        validaData = bool
        dataDoPc = datetime.today().strftime('%Y-%m-%d')
        separacaoPc = str(dataDoPc).split('-')
        separacaoUsr = str(data).split('/')
        diaUrs = int(separacaoUsr[0])
        mesUrs = int(separacaoUsr[1])
        anoUsr = int(separacaoUsr[2])
        diaPc = int(separacaoPc[2])
        mesPc = int(separacaoPc[1])
        anoPc = int(separacaoPc[0])

        #validando Data
        if anoUsr <= anoPc - 100:
            if mesUrs > mesPc:
                validaData = False
            elif mesUrs == mesPc:
                if diaUrs >= diaPc:
                    validaData = False
                else:
                    validaData = True
            else:
                validaData = True
        else:
            validaData = True

        #extrair os dígitos do CPF
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

        self.confirmar_alterar =  messagebox.askyesno('Alterar dados cliente','Deseja confirmar alteração de cadastro?')

        if validacpf == True and validaData == True and self.confirmar_alterar == True: 
            self.update_cliente()
            self.yes_alterar =messagebox.showwarning("Alterar dados cliente", "Alteração de cadastro confirmada!")

        elif validacpf == True and validaData == True and self.confirmar_alterar == False:
            self.no_alterar =messagebox.showwarning("Alterar dados cliente", "Alteração de cadastro cancelada!")

        elif validacpf == False and validaData == False:
            self.erro_cadastro_1 = messagebox.showerror('Erro de cadastro', 'Erro: CPF e Data de Nascimento inválidos!')

        elif validaData == False:
            self.erro_cadastro_1 = messagebox.showerror('Erro de cadastro', 'Erro: Data de Nascimento inválida!')

        elif validacpf == False: 
            self.erro_cadastro_1 = messagebox.showerror('Erro de cadastro', 'Erro: CPF inválido!')

    def validar_update_cadastro_funcionario(self):
        cpf_func=self.ed_cpf_funcionario.get()
        validacpf_func = bool
        digitos_func = []

        data_func = self.ed_nascimento_funcionario.get()
        validaData_func = bool
        dataDoPc_func = datetime.today().strftime('%Y-%m-%d')
        separacaoPc_func = str(dataDoPc_func).split('-')
        separacaoUsr_func = str(data_func).split('/')
        diaUrs_func = int(separacaoUsr_func[0])
        mesUrs_func = int(separacaoUsr_func[1])
        anoUsr_func = int(separacaoUsr_func[2])
        diaPc_func = int(separacaoPc_func[2])
        mesPc_func = int(separacaoPc_func[1])
        anoPc_func = int(separacaoPc_func[0])

        #validando Data
        if anoUsr_func <= anoPc_func - 100:
            if mesUrs_func > mesPc_func:
                validaData_func = False
            elif mesUrs_func == mesPc_func:
                if diaUrs_func >= diaPc_func:
                    validaData_func = False
                else:
                    validaData_func = True
            else:
                validaData_func = True
        else:
            validaData_func = True

        #extrair os dígitos do CPF
        for digito in str(cpf_func):
            digitos_func.append(int(digito))

        if len(digitos_func)!= 11:
            validacpf_func = False

        elif digitos_func[0] == digitos_func[1] == digitos_func[2] == digitos_func[3] == digitos_func[4] == digitos_func[5] == digitos_func[6] == digitos_func[7] == digitos_func[8] ==digitos_func[9] == digitos_func[10]:
            validacpf_func = False
        else:
            soma1_func = digitos_func[0]*10 + digitos_func[1]*9 + digitos_func[2]*8 + digitos_func[3]*7 + digitos_func[4]*6 + digitos_func[5]*5 + digitos_func[6]*4 + digitos_func[7]*3 + digitos_func[8]*2
            resto1_func = (soma1_func * 10) % 11

            if resto1_func == 10:
                resto1_func = 0

            soma2_func = digitos_func[0]*11 + digitos_func[1]*10 + digitos_func[2]*9 + digitos_func[3]*8 + digitos_func[4]*7 + digitos_func[5]*6 + digitos_func[6]*5 + digitos_func[7]*4 + digitos_func[8]*3 + digitos_func[9]*2
            resto2_func = (soma2_func * 10) % 11

            if resto2_func == 10:
                resto2_func = 0

            if resto1_func == digitos_func[9] and resto2_func == digitos_func[10]:
                validacpf_func = True
            else:
                validacpf_func = False

        self.confirmar_alterar_func =  messagebox.askyesno('Alterar dados funcionário','Deseja confirmar alteração de cadastro?')

        if validacpf_func == True and validaData_func == True and self.confirmar_alterar_func == True: 
            self.update_funcionario()
            self.yes_alterar_func =messagebox.showwarning("Alterar dados funcionário", "Alteração de cadastro confirmada!")

        elif validacpf_func == True and validaData_func == True and self.confirmar_alterar_func == False:
            self.no_alterar_func =messagebox.showwarning("Alterar dados funcionário", "Alteração de cadastro cancelada!")

        elif validacpf_func == False and validaData_func == False:
            self.erro_cadastro_1_func = messagebox.showerror('Erro de cadastro', 'Erro: CPF e Data de Nascimento inválidos!')

        elif validaData_func == False:
            self.erro_cadastro_1_func = messagebox.showerror('Erro de cadastro', 'Erro: Data de Nascimento inválida!')

        elif validacpf_func == False: 
            self.erro_cadastro_1_func = messagebox.showerror('Erro de cadastro', 'Erro: CPF inválido!')

    def validar_update_cadastro_convidado(self):
        cpf_conv=self.ed_cpf_convidado.get()
        validacpf_conv = bool
        digitos_conv = []

        data_conv = self.ed_nascimento_convidado.get()
        validaData_conv = bool
        dataDoPc_conv = datetime.today().strftime('%Y-%m-%d')
        separacaoPc_conv = str(dataDoPc_conv).split('-')
        separacaoUsr_conv = str(data_conv).split('/')
        diaUrs_conv = int(separacaoUsr_conv[0])
        mesUrs_conv = int(separacaoUsr_conv[1])
        anoUsr_conv = int(separacaoUsr_conv[2])
        diaPc_conv = int(separacaoPc_conv[2])
        mesPc_conv = int(separacaoPc_conv[1])
        anoPc_conv = int(separacaoPc_conv[0])

        #validando Data
        if anoUsr_conv <= anoPc_conv - 100:
            if mesUrs_conv > mesPc_conv:
                validaData_conv = False
            elif mesUrs_conv == mesPc_conv:
                if diaUrs_conv >= diaPc_conv:
                    validaData_conv = False
                else:
                    validaData_conv = True
            else:
                validaData_conv = True
        else:
            validaData_conv = True

        #extrair os dígitos do CPF
        for digito in str(cpf_conv):
            digitos_conv.append(int(digito))

        if len(digitos_conv)!= 11:
            validacpf_conv = False

        elif digitos_conv[0] == digitos_conv[1] == digitos_conv[2] == digitos_conv[3] == digitos_conv[4] == digitos_conv[5] == digitos_conv[6] == digitos_conv[7] == digitos_conv[8] ==digitos_conv[9] == digitos_conv[10]:
            validacpf_conv = False
        else:
            soma1_conv = digitos_conv[0]*10 + digitos_conv[1]*9 + digitos_conv[2]*8 + digitos_conv[3]*7 + digitos_conv[4]*6 + digitos_conv[5]*5 + digitos_conv[6]*4 + digitos_conv[7]*3 + digitos_conv[8]*2
            resto1_conv = (soma1_conv * 10) % 11

            if resto1_conv == 10:
                resto1_conv = 0

            soma2_conv = digitos_conv[0]*11 + digitos_conv[1]*10 + digitos_conv[2]*9 + digitos_conv[3]*8 + digitos_conv[4]*7 + digitos_conv[5]*6 + digitos_conv[6]*5 + digitos_conv[7]*4 + digitos_conv[8]*3 + digitos_conv[9]*2
            resto2_conv = (soma2_conv * 10) % 11

            if resto2_conv == 10:
                resto2_conv = 0

            if resto1_conv == digitos_conv[9] and resto2_conv == digitos_conv[10]:
                validacpf_conv = True
            else:
                validacpf_conv = False

        self.confirmar_alterar_conv =  messagebox.askyesno('Alterar dados convidado','Deseja confirmar alteração de cadastro?')

        if validacpf_conv == True and validaData_conv == True and self.confirmar_alterar_conv == True: 
            self.update_convidado()
            self.yes_alterar_conv =messagebox.showwarning("Alterar dados convidado", "Alteração de cadastro confirmada!")

        elif validacpf_conv == True and validaData_conv == True and self.confirmar_alterar_conv == False:
            self.no_alterar_conv =messagebox.showwarning("Alterar dados convidado", "Alteração de cadastro cancelada!")

        elif validacpf_conv == False and validaData_conv == False:
            self.erro_cadastro_1_conv = messagebox.showerror('Erro de cadastro', 'Erro: CPF e Data de Nascimento inválidos!')

        elif validaData_conv == False:
            self.erro_cadastro_1_conv = messagebox.showerror('Erro de cadastro', 'Erro: Data de Nascimento inválida!')

        elif validacpf_conv == False: 
            self.erro_cadastro_1_conv = messagebox.showerror('Erro de cadastro', 'Erro: CPF inválido!')

    def validar_exclusao(self):

        self.confirmar_exclusao =  messagebox.askyesno('Excluir cliente','Deseja confirmar exclusão do cliente?')

        if self.confirmar_exclusao == True: 
            self.deletar_cliente()
            self.yes_excluir =messagebox.showwarning("Excluir cliente", "Cliente excluído com sucesso!")

    def validar_exclusao_funcionario(self):

        self.confirmar_exclusao_func =  messagebox.askyesno('Excluir funcionário','Deseja confirmar exclusão do funcionário?')

        if self.confirmar_exclusao_func == True: 
            self.deletar_funcionario()
            self.yes_excluir_func = messagebox.showwarning("Excluir funcionário", "Funcionário excluído com sucesso!")

    def validar_exclusao_convidado(self):

        self.confirmar_exclusao_conv =  messagebox.askyesno('Excluir convidado','Deseja confirmar exclusão do convidado?')

        if self.confirmar_exclusao_conv == True: 
            self.deletar_convidado()
            self.yes_excluir_conv = messagebox.showwarning("Excluir convidado", "Convidado excluído com sucesso!")

    def Menus(self):
        menubar = Menu(self.frame_1)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit() : self.root.destroy()

        menubar.add_cascade(label = "Opções", menu= filemenu)
        menubar.add_cascade(label = "Ajuda", menu= filemenu2)
        
        filemenu.add_command(label="Sair", command= Quit)
        filemenu2.add_command(label= "Instruções de uso", command=self.janela_instrucoes)
    
    def janela_instrucoes(self):  
  
        self.Janela_2 = Toplevel()
        self.Janela_2.title('Nova Janela')
        self.Janela_2.configure(background= '#155569')
        self.Janela_2.geometry('900x300')
        self.Janela_2.resizable(True, True )
        self.Janela_2.transient(self.root)
        self.Janela_2.focus_force()
        self.Janela_2.grab_set()
       
        #Label com instruções:
        self.lb_instrucoes = Label(self.Janela_2, text= 
        '''Instruções de uso:

        1 - Para realizar o cadastro de um novo aluno, basta preencher os dados, selecionar o plano desejado e clicar no botão "Novo";
        2 - O espaço de dados onde há a matrícula, não será necessário preenchimento;
        3 - Para apagar todos os campos de preenchimento clique em 'Limpar';
        4 - Para alterar os dados de um aluno, basta seleciona-lo com duplo clique, e após a alteração, clicar no botão "Alterar";
        5 - Para apagar o cadastro de um aluno, selecione-o com duplo clique em seu nome na lista de cadastro e depois aperte o botão 'Apagar';
        6 - Para encontrar os dados de um aluno, preencha o nome no campo necessário, e em seguida, clique no botão "Buscar";
        7 - Para recarregar a lista de cadastrados na ordem correta, selecione "Atualizar";
        8 - Antes de confirmar na caixa após o cadastro, verifique se todos os dados estão corretos;
        9 - Após o cadastro, o número de matrícula é inalterável. 

        ''', bg='lightgrey', justify= LEFT, anchor='n')
        self.lb_instrucoes.place(relx=0.02, rely=0.02,relwidth=0.96, relheight=0.96)
        
        
App()
