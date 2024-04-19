from conexao import Conexao
from mensagem import Mensagem
from usuario import Usuario
from contato import Contato

class Chat:
    def __init__(self, usuario: Usuario, telefone: str):
        self.usuario = usuario
        self.telefone = telefone

    def enviar_mensagem(self, conteudo, destinatario):
        try:
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            sql = "INSERT INTO tb_mensagem (tel_remetente, tel_destinatario, mensagem) VALUES (%s, %s, %s)"
            val = (self.telefone, destinatario.telefone, conteudo)
            mycursor.execute(sql, val)

            mydb.commit()
            mydb.close()

            return True
        except Exception as e:
            print(e)
            return False

    def verificar_mensagem(self, quantidade: int, destinatario: Contato):
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        sql = f"SELECT tel_remetente, mensagem FROM tb_mensagem WHERE (tel_remetente = '{self.telefone}' AND tel_destinatario = '{destinatario.telefone}') OR (tel_remetente = '{destinatario.telefone}' AND tel_destinatario = '{self.telefone}')"

        mycursor.execute(sql)

        resultado = mycursor.fetchall()

        mensagens = []

        for linha in resultado:
            # Buscar o nome do remetente com base no telefone
            tel_remetente = linha[0]
            remetente = self.buscar_nome_por_telefone(tel_remetente)

            mensagem = {"remetente": remetente, "mensagem": linha[1]}
            mensagens.append(mensagem)

        return mensagens

    def retorna_usuarios(self):
        try:
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            sql = "SELECT nome, tel FROM tb_usuario ORDER BY nome"
            mycursor.execute(sql)
            resultado = mycursor.fetchall()
            lista_usuarios = []

            for linha in resultado:
                lista_usuarios.append({'nome': linha[0], 'telefone': linha[1]})

            return lista_usuarios
        except Exception as e:
            print(e)
            return []



    def buscar_nome_por_telefone(self, telefone: str):
        try:
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            sql = "SELECT nome FROM tb_usuario WHERE tel = %s"
            val = (telefone,)
            mycursor.execute(sql, val)
            resultado = mycursor.fetchone()

            if resultado:
                return resultado[0]
            else:
                return "Desconhecido"  # Ou outra mensagem padrão se não encontrar o nome
        except Exception as e:
            print(e)
            return "Desconhecido"