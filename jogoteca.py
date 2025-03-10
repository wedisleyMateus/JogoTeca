from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for
)

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('wedisley mateus', 'beru', 123)
usuario2 = Usuario('pereira francelino', 'igris', 456)
usuario3 = Usuario('Sendyy', 'bebe', 789)

usuarios = { usuario1.nickname: usuario1, usuario2.nickname: usuario2, usuario3.nickname: usuario3}

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Rack in Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
lista = [jogo1, jogo2, jogo3]

app = Flask(__name__)
app.secret_key = 'alura'

@app.route('/novo')
def novo_jogo():
    if 'usuario_logado' not in session:
        return redirect(url_for('login', proxima=url_for('novo_jogo')))
    else:
        return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar_jogo():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('login'))

@app.route('/')
def jogos():
    if 'usuario_logado' not in session:
        return redirect(url_for('login', proxima=url_for('jogos')))
    else:
        return render_template('lista.html', titulo='Jogoteca', jogos=lista)

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == str(usuario.senha):
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Senha Invalida!')
            return redirect(url_for('login'))

@app.route('/logout', methods=['POST',])
def logout():
    session.pop('usuario_logado', None)
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))

app.run(debug=True)
