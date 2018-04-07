from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
import random

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

person = {
    '1': {
        'perso': "Enginering",
        'tasks': [],
        'count': 0
    },
    '2': {
        'perso': 'Doctor',
        'tasks': [],
        'count': 0
    }
}

tasks = {
    '1': {
        'name': 'tache 1',
        'price': 450
    },
    '2': {
        'name': 'tache 2',
        'price': 300
    }
}

asignTask = []


def CreateTask(tasksJson):
    task = {}
    
    task['name'] = tasksJson['name']
    return task

def GetRandomTask():
    nbMax = int(max(tasks.keys()))
    if(len(asignTask) < nbMax):
        ran = random.randint(1, nbMax)
        task = tasks[str(ran)]
        while(task in asignTask):
            ran = random.randint(1, nbMax)
            task = tasks[str(ran)]
        asignTask.append(task)
        return task
    else:
        return None


class Personalities(Resource):
    def get(self):
        return person

    def post(self):
        #args = parser.parse_args()
        json_data = request.get_json(force=True)
        p = {'perso': json_data['perso'], 'tasks': json_data['tasks'],'count':0}
        person_id = int(max(person.keys()))+1
        person[person_id] = p
        return person


class Tasks(Resource):
    def get(self):
        return tasks

class OnePerson(Resource):
    def get(self, person_id):
        return person[person_id]

    def post(self, person_id):
        json_data = request.get_json(force=True)
        p = person[person_id]
        p['count'] = p['count']+1
        ptask = p['tasks']
        task_id = p['count']
        task = CreateTask(json_data)
        asignTask.remove(task)
        comp = {str(task_id): task}
        ptask.append(comp)
        return person[person_id]


class OneTask(Resource):
    def get(self):
        task = GetRandomTask()
        return task


api.add_resource(Personalities, '/perso')
api.add_resource(Tasks, '/tasks')
api.add_resource(OnePerson, '/perso/<person_id>')
api.add_resource(OneTask, '/tasks/next')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002, debug=True)
