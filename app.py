from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from usuario import Usuario
from chat import Chat
from contato import Contato
from conexao import Conexao

app = Flask(__name__)

app.secret_key = "batatinhafrita123"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/cadastro', methods=['POST'])
def cadastro():
    telefone = request.form.get('telefone')
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    usuario = Usuario()

    if usuario.cadastrar(telefone, nome, senha):
        session['usuario_logado'] = {'nome': usuario.nome, 'telefone': usuario.telefone}
        return render_template("chat.html")
    else:
        session.clear()
        return jsonify({'mensagem': 'Erro ao cadastrar'}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        telefone = request.form.get('telefone')
        senha = request.form.get('senha')

        usuario = Usuario()
        usuario.logar(telefone, senha)

        if usuario.logado:
            session["usuario_logado"] = {"nome": usuario.nome, "telefone": usuario.telefone}
            return redirect("/chat")
        else:
            return redirect("/login")

    return render_template("index.html")


@app.route('/chat')
def chat():
    if "usuario_logado" not in session:
        return redirect("/login")

    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)

    # Suponha que 'telefone_destinatario' seja o telefone do contato com quem o usuário está interagindo
    telefone_destinatario = 'telefone_do_destinatario'

    # Busca o contato pelo telefone
    contato_destinatario = buscar_contato_por_telefone(telefone_destinatario)
    
    if contato_destinatario:
        # Se o contato for encontrado, verifica as mensagens
        mensagens = chat.verificar_mensagem(10, contato_destinatario)
        contatos = chat.retorna_usuarios()  
        return render_template("chat.html", contatos=contatos, mensagens=mensagens)
    else:
        # Se o contato não for encontrado, retorna uma mensagem de erro
        return render_template("chat.html", mensagem="Contato não encontrado")


@app.route("/get/usuarios")
def api_get_usuarios():
    if "usuario_logado" not in session:
        return jsonify({'mensagem': 'Usuário não autenticado'}), 401

    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)

    contatos = chat.retorna_usuarios()

    return jsonify(contatos), 200

def buscar_contato_por_telefone(telefone):
    try:
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        sql = "SELECT nome, tel FROM tb_usuario WHERE tel = %s"
        val = (telefone,)
        mycursor.execute(sql, val)
        resultado = mycursor.fetchone()

        if resultado:
            nome_contato, telefone_contato = resultado
            contato = Contato(nome_contato, telefone_contato)
            return contato
        else:
            return None
    except Exception as e:
        print(e)
        return None
    

@app.route("/get/mensagens/<tel_destinatario>")
def api_get_mensagens(tel_destinatario):
    if "usuario_logado" not in session:
        return jsonify({'mensagem': 'Usuário não autenticado'}), 401

    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]

    chat = Chat(nome_usuario, telefone_usuario)
    contato_destinatario = Contato("", tel_destinatario)

    lista_de_mensagens = chat.verificar_mensagem(0, contato_destinatario)

    return jsonify(lista_de_mensagens), 200


@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    if "usuario_logado" not in session:
        return jsonify({'mensagem': 'Usuário não autenticado'}), 401

    # Recolher o telefone do destinatário e a mensagem do JSON enviado pelo front end
    dados = request.json
    telefone_destinatario = dados.get('telefone_destinatario')
    mensagem = dados.get('mensagem')

    # Buscar informações do usuário logado na sessão
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]

    # Instanciar objeto Chat com o usuário logado
    chat = Chat(nome_usuario, telefone_usuario)

    # Instanciar um objeto destinatário
    destinatario = Contato("", telefone_destinatario)

    # Chamar o método enviar_mensagem
    if chat.enviar_mensagem(mensagem, destinatario):
        return jsonify({'mensagem': 'Mensagem enviada com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Erro ao enviar a mensagem'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")
