from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@localhost:5432/todoapp'
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    # Debugging Messages
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


db.create_all()

## Adding ToDo items
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    # Get data from a Form
    # description = request.form.get('description', '')
    # Get data from a Fetch AJAX request
    try:
        description = request.get_json()['description']
        todo = Todo(description = description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/')
## The Controller
def index():
    return render_template('index.html', data=Todo.query.all())
