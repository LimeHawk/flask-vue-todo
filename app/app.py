from flask import Flask, render_template, jsonify, request, redirect, url_for
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from datetime import datetime
from config import Config
from forms import TaskForm

load_dotenv('./.flaskenv')

# Cria a instância do aplicativo Flask e carrega as configurações do objeto Config
app = Flask(__name__)
app.config.from_object(Config)

# Cria uma instância do SQLAlchemy para manipular o banco de dados
db = SQLAlchemy(app)

# Define a classe de modelo para a tabela "tasks" usando DataClass e SQLAlchemy
@dataclass
class Task(db.Model):
    id: int
    title: str
    date: datetime
    completed: bool

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(140))
    date = db.Column(db.DateTime(), default=datetime.now())
    completed = db.Column(db.Boolean(), default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Task id: {self.id} - {self.title}>'

# Define a rota da página inicial
@app.route('/')
def index():
    tasks = Task.query.all()
     # Retorna uma resposta JSON se a solicitação vier de uma solicitação Ajax
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(tasks)
    # Retorna a página HTML padrão com as tarefas existentes
    return render_template('index.html')

# Define a rota para criar uma nova tarefa
@app.route('/create', methods=['POST'])
def create_task():
    # Obtém o input do usuário enviado como dados JSON
    user_input = request.get_json()

    # Valida o formulário com base no esquema definido em "TaskForm"
    form = TaskForm(data=user_input)
    # Se o formulário for válido, cria uma nova tarefa e adiciona ao banco de dados
    if form.validate():
        task = Task(title=form.title.data)
        print(task)
        db.session.add(task)
        db.session.commit()
        # Retorna a nova tarefa criada como uma resposta JSON
        return jsonify(task)

    # Se houver um erro no formulário, redireciona para a página inicial
    print('error',user_input)
    return redirect(url_for('index'))

# Define a rota para excluir uma tarefa
@app.route('/delete', methods=['POST'])
def delete_task():
    # Obtém o ID da tarefa enviada como dados JSON
    task_id = request.get_json().get('id')
    
    # Obtém a tarefa com o ID especificado do banco de dados e a exclui
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()

    # Retorna uma resposta JSON de sucesso
    return jsonify({'result':'okay'}),200

# Define a rota para marcar uma tarefa como concluída
@app.route('/complete',methods=['POST'])
def complete_task():
    # Obtém o ID da tarefa enviada como dados JSON
    task_id = request.get_json().get('id')
    task = Task.query.filter_by(id=task_id).first()

    # Obtém a tarefa com o ID especificado do banco de dados e marca como concluída
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return jsonify({'result':'okay'}),200


@app.route('/getTasks')
def get_tasks():
    tasks = Task.query.all()
    return jsonify(tasks)
    
    
if __name__ == '__main__':
    app.run()
