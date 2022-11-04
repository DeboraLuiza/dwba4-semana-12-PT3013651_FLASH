import logging
import traceback

import flask
from replit import db

app = flask.Flask(__name__)

@app.errorhandler(500)
def internal_server_error(e: str):
    return flask.jsonify(error=str(e)), 500


@app.route('/', methods=['GET', 'POST'])
def cadastroContatos():
  try:
    contatos = db.get('contatos', {}); 
    print(contatos);
    
    if flask.request.method == "POST": 
      
      #resgatando o email e o nome
      contatos[flask.request.form['email']] = {'nome': flask.request.form['nome'],'telefone': flask.request.form['telefone'], 'assunto': flask.request.form['contato-assunto'], 'mensagem': flask.request.form['mensagem'], 'opcResposta': flask.request.form['opcResposta']}
    db['contatos'] = contatos
      
    
    #momento em que o servidor retorna os dados para o cliente
    return flask.render_template('contatos.html', contatos=contatos) 
  except Exception as e:
    logging.exception('failed to database')
    flask.abort(500, description=str(e) + ': ' + traceback.format_exc())


#quando for trocar para limpar apenas 1 registro
@app.route('/limparBanco', methods=['POST'])
def limparBanco():
  try:
    del db["contatos"];
    return flask.render_template('contatos.html')
  except Exception as e:
    logging.exception(e)
    return flask.render_template('contatos.html')
    
app.run('0.0.0.0')




#from flask import Flask

#app = Flask(__name__)


#@app.route('/')
#def index():
#    return 'Hello from Flask!'


#app.run(host='0.0.0.0', port=81)


