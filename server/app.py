from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
import random

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

person = {
    '1': {
        'name':"Itch",
        'perso': "Enginering",
        'tasks': [],
        'count': 0
    },
    '2': {
        'name':"Bob",
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

messages = {
    '1':{
        'message':"Server start"}
}

#def ClearMessages():
#    nbr = int(max(messages.keys()))
#    lastMsg = messages[str(nbr)]
#    messages.clear()
#    messages['1'] = lastMsg

def RecordMessage(msg):
    nbr = int(max(messages.keys(),key=int))+1
    messages[str(nbr)] = {'message':msg}

def GetRandomTask():
    nbMax = int(max(tasks.keys(),key=int))
    if(len(asignTask) < nbMax):
        ran = random.randint(1, nbMax)
        task = tasks[str(ran)]
        while(ran in asignTask):
            ran = random.randint(1, nbMax)
            task = tasks[str(ran)]
        asignTask.append(ran)
        return task
    else:
        return None

class Persons(Resource):
    def get(self):
        return person

    def post(self):
        json_data = request.get_json(force=True)
        p = {'name':json_data['name'], 'perso': json_data['perso'], 'tasks': json_data['tasks'],'count':0}
        print(max(person.keys(),key=int))
        person_id = int(max(person.keys(),key=int))+1
        person[person_id] = p
        RecordMessage("Added person " + p['name'])
        return person[person_id]

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
        idFinish = int(json_data['id'])
        asignTask.remove(idFinish)
        comp = {str(task_id): tasks[str(idFinish)]}
        ptask.append(comp)
        RecordMessage("Task " +  tasks[str(idFinish)]['name'] + " has been finished by " + p['name'])
        return person[person_id]

class OneTask(Resource):
    def get(self):
        task = GetRandomTask()
        RecordMessage("Task " + task['name'] + " has been give")
        return task

class Governement(Resource):
    def get(self):
        msg= messages
       # ClearMessages()
        return msg

api.add_resource(Persons, '/persons')
api.add_resource(Tasks, '/tasks')
api.add_resource(OnePerson, '/persons/<person_id>')
api.add_resource(OneTask, '/tasks/next')
api.add_resource(Governement,'/gov')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002, debug=True)
