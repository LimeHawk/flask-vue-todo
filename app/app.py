from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import redirect
from flask import url_for

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from datetime import datetime

from config import Config



load_dotenv('./.flaskenv')


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

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
        return f'<Task id: {self.id} - {self.title}'


from forms import TaskForm

@app.route('/')
def index():
    tasks = Task.query.all()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(tasks)
    
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_task():
    user_input = request.get_json()

    form = TaskForm(data=user_input)


    if form.validate():
        task = Task(title=form.title.data)
        print(task)
        db.session.add(task)
        db.session.commit()

        return jsonify(task)

    print('error',user_input)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()