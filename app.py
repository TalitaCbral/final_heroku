from flask import Flask, render_template, redirect, request, flash, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query
#comentario comitt

app = Flask(__name__)
app.secret_key = 'project2'

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///projetofinal.sqlite3'
db = SQLAlchemy(app)

class Portifolio(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True )
    nome = db.Column(db.String(150), nullable=False)
    imagem = db.Column(db.String(500), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    video = db.Column(db.String(500), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    def __init__(self, nome, imagem, descricao, video, autor):
        self.nome = nome
        self.imagem = imagem
        self.descricao = descricao
        self.video = video
        self.autor = autor
### Criando rotas abaixo###
@app.route('/') # renderiza a pagina principal(rota)
def index():
    session['usuario_logado'] = None # sempre que for para rota principal, 'desloga' o usuario
    return render_template('index.html')
#######


@app.route('/login')
def login():
    session['usuario_logado'] = None
    return render_template('login.html')
@app.route('/auth', methods=['GET', 'POST']) # Rota de autenticação
def auth():
    if request.form['senha'] == 'admin': # Se a senha for 'admin' faça:
        session['usuario_logado'] = 'admin' # Adiciona um usuario na sessão
        flash('Login feito com sucesso!') # Envia mensagem de sucesso
        return redirect('/adm') # Redireciona para a rota adm
    else: # Se a senha estiver errada, faça:
        flash('Erro no login, tente novamente!')  # Envia mensagem de erro
        return redirect('/login') # Redireciona para a rota login   
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    return redirect('/login')
#PAINEL ADMINISTRATIVO#



@app.route('/adm')
def adm():
    if 'usuario_logado' not in session or session ['usuario_logado']==None:
        flash('Fação o login antes')
        return redirect('/login')
    portifolio = Portifolio.query.all()
    return render_template('adm.html', portifolio=portifolio)
    # if 'usuario_logado' not in session or session ['usuario_logado']==None:
    #    flash('Faça o login antes de acessar o painel administrativo')
    #    return redirect('/login')
    # portifolio = Portifolio.query.all() #vai ler tudo, select * from projetos
    # return render_template('adm.html', portifolio= portifolio, portifolio='')

### CRIAR/ADD ITEM
@app.route('/new', methods=['GET', 'POST'])
def new(): # new definido no formulario de inclusao na pagina adm
    if request.method == 'POST': # Verifica se o metodo recebido na requisição é POST
        # cria o objeto projeto, adiconando os campos do form nele.
        portifolio = Portifolio(
            request.form['nome'],
            request.form['imagem'],
            request.form['descricao'],
            request.form['video'],
            request.form['autor']
        )
        db.session.add(portifolio) # Adiciona o objeto projeto no banco de dados.
        db.session.commit() # Confirma a operação
        flash('Item Adicionado com suceso!')
        return redirect('/adm') 

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    portifolio = Portifolio.query.get(id)
    if request.method == 'POST':
        portifolio.nome = request.form['nome']
        portifolio.descricao = request.form['descricao']
        portifolio.imagem = request.form['imagem']
        portifolio.video = request.form['video']
        portifolio.autor = request.form['autor']
        db.session.commit()
        return redirect('/adm')
    return render_template('edit.html', portifolio=portifolio) 

@app.route("/<id>")
def get_by_id(id):
    portifolio = Portifolio.query.get(id)
    return render_template('delete.html', portifolio=portifolio)

#### DELETAR ####
@app.route('/delete/<id>')
def delete(id):
    portifolio = Portifolio.query.get(id)
    db.session.delete(portifolio)
    db.session.commit()
    flash('Item Deletado com sucesso!')
    return redirect('/adm')
#######
@app.route('/antonio') # renderiza a pagina (rota)
def antonio():
    # portifolio = Portifolio.query.all()
    portifolio = Portifolio.query.filter(Portifolio.autor.ilike('%antonio%')) #faz o filtro 
    return render_template('antonio.html', portifolio=portifolio )
@app.route('/elisama') # renderiza a pagina (rota)
def elisama():
    # projetos = Projeto.query.all()
    portifolio = Portifolio.query.filter(Portifolio.autor.ilike('%Elisama%')) #faz o filtro
    return render_template('elisama.html', portifolio=portifolio)
@app.route('/fellipe') # renderiza a pagina(rota)
def fellipe():
    # projetos = Projeto.query.all()
    portifolio = Portifolio.query.filter(Portifolio.autor.ilike('%fellipe%')) #faz o filtro
    return render_template('fellipe.html', portifolio=portifolio)
@app.route('/rudhy') # renderiza a pagina principal(rota)
def rudhy():
    # projetos = Projeto.query.all()
    portifolio = Portifolio.query.filter(Portifolio.autor.ilike('%rudhy%')) #faz o filtro
    return render_template('rudhy.html', portifolio=portifolio)
@app.route('/sobre') # renderiza a pagina (rota)
def sobre():
    # portifolio = Portifolio.query.all()
    portifolio = Portifolio.query.filter(Portifolio.autor.ilike('%sobre%')) #faz o filtro 
    return render_template('sobre.html', portifolio=portifolio )

if __name__ == '__main__':
    db.create_all() #cria o banco de dados 
    app.run(debug=True)