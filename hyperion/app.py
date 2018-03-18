#!flask/bin/python
from flask import Flask, jsonify, abort, request, url_for, make_response
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy.dialects.postgresql import JSONB

connect_str = "dbname='hyperion' user='hyperion' host='localhost' " + \
              "password='hyperion'"

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = connect_str
db = SQLAlchemy(app)


@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


#   curl -i http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
# @auth.login_required
def get_tasks():
    return jsonify({'tasks': list(map(make_public_task, tasks))})


#   curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}'
#   http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
# @auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


#   curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/todo/api/v1.0/tasks/2
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
# @auth.login_required
def update_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
# @auth.login_required
def delete_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if not task:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


#   curl -i http://localhost:5000/todo/api/v1.0/tasks/3
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if not task:
        abort(404)
    return jsonify(dict(task[0]))


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120), unique=False)
    lastName = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(220), unique=False)

    def __init__(self, firstName, lastName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email


@app.route('/insert_user', methods=['POST'])
def insertUser():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    #todo: insert json into database
    db.session.add(task)
    db.session.commit()
    return jsonify({'task': task}), 201


Variable_tableName = 'person'


@app.route('/dropdb', methods=['GET'])
def drop_db():
    engine = create_engine("postgresql://hyperion:hyperion@localhost/hyperion", echo=True)
    if engine.dialect.has_table(engine, Variable_tableName):  # If table don't exist, Create.
        metadata = MetaData(engine)
        Table(Variable_tableName, metadata)
        metadata.drop_all()
        return jsonify({'result': True})
    return jsonify({'result': False})


@app.route('/createdb', methods=['GET'])
def create_table():
    engine = create_engine("postgresql://hyperion:hyperion@localhost/hyperion", echo=True)
    if not engine.dialect.has_table(engine, Variable_tableName):  # If table don't exist, Create.
        metadata = MetaData(engine)
        # Create a table with the appropriate Columns
        Table(Variable_tableName, metadata,
              Column('id', Integer, primary_key=True, nullable=False),
              Column('data', JSONB))
        # Implement the creation
        metadata.create_all()
        return jsonify({'result': True})
    return jsonify({'result': False})


if __name__ == '__main__':
    app.run(debug=True)
