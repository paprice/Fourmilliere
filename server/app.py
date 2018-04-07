from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jsonpify import jsonify 
import random

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('perso')

def GetNextTask():
    return "nom de tache,100,50,25,30"

person = {
    '1':{
         'perso':"Enginering",
         'tasks':[]
    },
    '2':{
        'perso':'Doctor',
        'tasks':[]
    }
}

tasks = {
    '1':{
        'name':'tache 1',
        'price':450
    },
    '2':{
        'name':'tache 2',
        'price':300
    }
}

def GetRandomTask():
    nbMax = int(max(tasks.keys()))
    ran = random.randint(1,nbMax)
    return str(ran)

class Personalities(Resource):
    def get(self):
        return person
    def post(self):
        args = parser.parse_args()
        p = {'perso':args['perso'],'tasks':[]}
        person_id = int(max(person.keys()))+1
        person[person_id] = p

class Tasks(Resource):
    def get(self):
        return tasks

class OnePerson(Resource):
    def get(self,person_id):
        return person[person_id]

class OneTask(Resource):
    def get(self):
        ran = GetRandomTask()
        return tasks[ran]
    

api.add_resource(Personalities,'/perso')
api.add_resource(Tasks, '/tasks')
api.add_resource(OnePerson,'/perso/<person_id>')
api.add_resource(OneTask,'/tasks/next')

if __name__ == '__main__':
     app.run(debug=True)



