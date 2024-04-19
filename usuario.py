# conectando ao banco de dados
from conexao import Conexao
from hashlib import sha256



#criando o  cursor


class Usuario:
    def __init__(self):
        self.telefone = None
        self.nome = None
        self.senha = None
        self.logado = False
        
# primeira forma
    def cadastrar(self, telefone, nome, senha):

        # criptografando a senha
        senha = sha256(senha.encode()).hexdigest()

        try:
            #sql = "INSERT INTO tb_usuario (tel, nome, senha) VALUES (%s, %s, %s)"
            #val = (self.tel, self.nome, self.senha)
            #mycursor.execute(sql, val)
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()
        
            # segunda forma 
            sql = f"INSERT INTO tb_usuario (tel, nome, senha) VALUES ('{telefone}', '{nome}', '{senha}')"
            mycursor.execute(sql)

    

            self.telefone = telefone
            self.nome = nome
            self.senha = senha
            self.logado = True 

            mydb.commit()
            

            return True
        except:
            return False

    def logar(self, telefone, senha):
        senha = sha256(senha.encode()).hexdigest()
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        #primeira forma
        sql = "SELECT tel, nome, senha FROM tb_usuario WHERE tel=%s AND senha=%s;"
        valores = (telefone, senha)
        mycursor.execute(sql,valores)

        # #segunda forma
        # sql = f"SELECT tel, nome, senha FROM tb_usuario WHERE tel='{telefone}' AND senha='{senha}'"
        # mycursor.execute(sql)

        resultado = mycursor.fetchone()

        if not resultado == None:
            self.logado = True
            self.nome = resultado[1]
            self.telefone = resultado[0]
            self.senha = resultado [2]
        else:
            self.logado =  False




        mydb.commit()
        mydb.close()