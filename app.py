from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import datetime
import os
import sqlite3

# Importa os blueprints
from Confeitaria3.chatbot import chatbot_bp
from Confeitaria3.faq import faq_bp
from Confeitaria3.recomendacoes import recomendacoes_bp

# ====================== CONFIGURAÇÃO ======================
load_dotenv()

app = Flask(__name__)  # cria o app primeiro
app.secret_key = 'sua_chave_secreta'

# depois registra os blueprints
app.register_blueprint(chatbot_bp)
app.register_blueprint(faq_bp)
app.register_blueprint(recomendacoes_bp)


# Configuração para permitir url_for com _external=True fora de uma requisição
app.config['SERVER_NAME'] = 'localhost:5000'  # ou seu domínio se for produção
app.config['PREFERRED_URL_SCHEME'] = 'http'   # use 'https' se estiver em produção


DB_NAME = 'bancoTeste.db'
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# ====================== EMAIL ======================
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = int(os.getenv('MAIL_PORT') or 587)
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL') == 'True'
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

if not all([MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER]):
    raise ValueError("Alguma variável de e-mail não foi definida no .env")

app.config.update(
    MAIL_SERVER=MAIL_SERVER,
    MAIL_PORT=MAIL_PORT,
    MAIL_USE_TLS=MAIL_USE_TLS,
    MAIL_USE_SSL=MAIL_USE_SSL,
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER=MAIL_DEFAULT_SENDER
)
mail = Mail(app)

#=======================DB================================
DB_NAME= 'bancoTeste.db'

# ====================== INICIALIZAÇÃO DO BANCO ======================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)
    
    # Tabela de produtos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        preco REAL NOT NULL,
        imagem TEXT
    )
    """)
    
    conn.commit()
    conn.close()

# Rodar sempre que o app iniciar
init_db()

# ====================== FUNÇÕES ======================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def enviar_email_boas_vindas(nome, email):
    if not email:
        return
    msg = Message(subject="Bem-vindo à Confeitaria Gatito!", recipients=[email])
    msg.html = render_template("emails/boas_vindas.html", nome=nome)
    mail.send(msg)

def enviar_email_pedido(nome, email, id_pedido, valor):
    if not email:
        return
    print("Enviando e-mail...")
    msg = Message(subject="Pedido Confirmado - Confeitaria Gatito", recipients=[email])
    msg.html = render_template("emails/pedido_confirmado.html", nome=nome, id_pedido=id_pedido, valor=valor)
    mail.send(msg)

def enviar_email_rota_entrega(nome,email, id_pedido, valor):
    if not email:
        return
    print("enviando----")
    msg = Message(subject="Pedido em rota de entrega - Confeitaria Gatito", recipients=[email])
    msg.html = render_template("emails/rota_entrega.html", nome=nome, id_pedido=id_pedido, valor=valor)
    mail.send(msg)

# ====================== ROTAS PÚBLICAS ======================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/produtos")
def produtos():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # <- ESSA LINHA
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return render_template("produtos.html", produtos=produtos)

@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        destinatario = MAIL_DEFAULT_SENDER
        if not destinatario:
            flash("Erro: destinatário de e-mail não definido.", "danger")
            return redirect(url_for('contato'))

        msg = Message(subject=f"Mensagem de Contato - {nome}", recipients=[destinatario])
        msg.body = f"Nome: {nome}\nEmail: {email}\nMensagem:\n{mensagem}"
        mail.send(msg)
        flash("Mensagem enviada com sucesso!", "success")
        return redirect(url_for('contato'))

    return render_template("contato.html")

@app.route("/cestas-buy")
def cestas_buy():
    return render_template("cestas-buy.html")

@app.route("/dados_anuais")
def dados_anuais():
    return render_template("dados_anuais.html")

@app.route("/eclairs-buy")
def eclairs_buy():
    return render_template("eclairs-buy.html")

@app.route("/gateus-buy")
def gateus_buy():
    return render_template("gateus-buy.html")

@app.route("/milfolhas-buy")
def milfolhas_buy():
    return render_template("milfolhas-buy.html")

@app.route("/pagina_compra/<int:produto_id>")
def pagina_compra(produto_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id=?", (produto_id,))
    produto = cursor.fetchone()
    conn.close()

    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("produtos"))

    return render_template("pagina-compra.html", produto=produto)

@app.route("/adicionar_carrinho/<int:produto_id>")
def adicionar_carrinho(produto_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id=?", (produto_id,))
    produto = cursor.fetchone()
    conn.close()

    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("produtos"))

    if "carrinho" not in session:
        session["carrinho"] = []

    session["carrinho"].append({
        "id": produto["id"],
        "nome": produto["nome"],
        "preco": produto["preco"]
    })
    session.modified = True

    flash(f"{produto['nome']} adicionado à sacola!", "success")
    return redirect(url_for("sacola"))

@app.route("/sacola")
def sacola():
    carrinho = session.get("carrinho", [])
    total = sum([float(item["preco"]) for item in carrinho])
    return render_template("sacola.html", carrinho=carrinho, total=total)

@app.route("/finalizar_pedido", methods=["POST"])
def finalizar_pedido():
    if 'usuario' not in session:
        flash("Faça login para finalizar o pedido.", "danger")
        return redirect(url_for("login"))

    carrinho = session.get("carrinho", [])
    if not carrinho:
        flash("Sua sacola está vazia!", "warning")
        return redirect(url_for("sacola"))

    nome = session['usuario']

    # Busca o email do usuário no banco
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM login WHERE nome=?", (nome,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        flash("Usuário não encontrado no banco de dados.", "danger")
        return redirect(url_for("home"))

    email = user[0]
    total = sum([float(item["preco"]) for item in carrinho])
    id_pedido = int(datetime.now().timestamp())  # ID simples baseado no tempo

    try:
        enviar_email_pedido(nome, email, id_pedido, f"R$ {total:.2f}")
        flash("Pedido finalizado! Você receberá um e-mail de confirmação.", "success")
        # Envia e-mail de rota de entrega
        enviar_email_rota_entrega(nome, email, id_pedido, f"R$ {total:.2f}")
        flash("Pedido finalizado! Você receberá e-mails de confirmação e rota de entrega.", "success")
        session.pop("carrinho", None)  # limpa a sacola
    except Exception as e:
        flash(f"Erro ao enviar e-mail: {e}", "danger")
    

    return redirect(url_for("home"))


# ====================== CRUD DE PRODUTOS ======================================================================
@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        file = request.files.get('imagem')
        filename = None
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, descricao, preco, imagem) VALUES (?, ?, ?, ?)",
                       (nome, descricao, preco, filename))
        conn.commit()
        conn.close()
        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for("produtos"))

    return render_template("novo.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id=?", (id,))
    produto = cursor.fetchone()
    if request.method == "POST":
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        imagem = produto[4] if produto else None
        file = request.files.get('imagem')
        if file and allowed_file(file.filename):
            imagem = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, imagem))
        cursor.execute("UPDATE produtos SET nome=?, descricao=?, preco=?, imagem=? WHERE id=?",
                       (nome, descricao, preco, imagem, id))
        conn.commit()
        conn.close()
        flash("Produto atualizado com sucesso!", "success")
        return redirect(url_for('produtos'))
    conn.close()
    return render_template("editar.html", produto=produto)

@app.route("/excluir/<int:id>")
def excluir(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Produto excluído com sucesso!", "success")
    return redirect(url_for('produtos'))

# ====================== AUTENTICAÇÃO ======================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Checa se já existe
        cursor.execute("SELECT * FROM login WHERE email=?", (email,))
        if cursor.fetchone():
            flash("Email já cadastrado!", "danger")
            return redirect(url_for('register'))
        cursor.execute("INSERT INTO login (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conn.commit()
        conn.close()
        try:
            enviar_email_boas_vindas(nome, email)
        except Exception as e:
            flash(f"Cadastro realizado, mas falha ao enviar e-mail: {e}", "warning")
        flash("Cadastro realizado com sucesso! Verifique seu e-mail.", "success")
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        senha = request.form['senha']
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login WHERE email=? AND senha=?", (email, senha))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['usuario'] = user[1]  # nome
            flash(f"Bem-vindo(a), {user[1]}!", "success")
            return redirect(url_for('home'))
        flash("Email ou senha incorretos!", "danger")
        return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('usuario', None)
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for('home'))

@app.route("/editar_conta", methods=["GET", "POST"])
def editar_conta():
    if 'usuario' not in session:
        flash("Faça login para acessar esta página.", "danger")
        return redirect(url_for('login'))
    usuario_nome = session['usuario']
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login WHERE nome=?", (usuario_nome,))
    usuario = cursor.fetchone()
    if request.method == "POST":
        novo_nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cursor.execute("UPDATE login SET nome=?, email=?, senha=? WHERE id=?", 
                       (novo_nome, email, senha, usuario[0]))
        conn.commit()
        conn.close()
        session['usuario'] = novo_nome
        flash("Conta atualizada com sucesso!", "success")
        return redirect(url_for('home'))
    conn.close()
    return render_template("editar_conta.html", user=usuario)

@app.route("/excluir_conta", methods=["POST"])
def excluir_conta():
    if 'usuario' not in session:
        flash("Faça login para excluir a conta.", "danger")
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM login WHERE nome=?", (session['usuario'],))
    conn.commit()
    conn.close()
    session.pop('usuario', None)
    flash("Conta excluída com sucesso!", "success")
    return redirect(url_for('home'))


# ====================== EXECUÇÃO ======================
if __name__ == "__main__":
    app.run(debug=True)
