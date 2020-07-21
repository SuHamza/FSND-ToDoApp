from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@localhost:5432/todoapp'
# Disable 'SQLALCHEMY_TRACK_MODIFICATIONS' to avoid Deprecation warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Create a Migrate instance & link to our Flask App & SQLAlchemy DB
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    # Debugging Messages
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

# Removed to use Migrate instead
#db.create_all()

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
