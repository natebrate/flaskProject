from flask import Flask, jsonify, url_for
from flask_httpauth import HTTPBasicAuth, HTTPDigestAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort, make_response, request
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_the_secret_key'
auth = HTTPDigestAuth()

users = {
    "john": "hello",
    "susan": "bye"
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


tasks = [
    {
        "id": 1,
        'title': u"Buy groceries",
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        "id": 2,
        'title': u"Learn Python",
        'description': u'Find a good python tutorial',
        'done': False
    }
]


@app.route('/')
@app.route('/index')
@auth.login_required
def index():
    tasks = [
        {
            "id": 1,
            'title': u"Buy groceries",
            'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
            'done': False
        },
        {
            "id": 2,
            'title': u"Learn Python",
            'description': u'Find a good python tutorial',
            'done': False
        }
    ]
    return render_template('index.html' % auth.username(), tasks=tasks)


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_task():
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
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
    return jsonify({'task': tasks}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']):
        abort(400)
    if 'description' in request.json and type(request.json['description']):
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


if __name__ == '__main__':
    app.run(debug=True)
