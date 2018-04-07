from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
import random

app = Flask(__name__)
api = Api(app)

person = {
    '1': {
        'name':"Itch",
        'perso': "mechanic",
        'tasks': [],
        'count': 0
    },
    '2': {
        'name':"Bob",
        'perso': 'duty fulfiller',
        'tasks': [],
        'count': 0
    }
}

tasks = {
    '1': {
        'name': 'tache 1',
        'weight': {
            'duty fulfiller':3,
            'mechanic':1
        }
    },
    '2': {
        'name': 'tache 2',
                'weight': {
            'duty fulfiller':1,
            'mechanic':4
        }
    }
}

asignTask = []

messages = {
    '1':{
        'message':"Server start"}
}

def FindId(name):
    for item in tasks:
        if(tasks[item]['name'] == name):
            return item

def RecordMessage(msg):
    nbr = int(max(messages.keys(),key=int))+1
    messages[str(nbr)] = {'message':msg}

def GetNextTask(perso):
    nbMax = int(max(tasks.keys(),key=int))
    if(len(asignTask) < nbMax):
        finalTask = {'name':"",'weight':{}}
        finalTask['weight'][perso] = 0
        for item in tasks:
            task = tasks[item]
            if(item not in asignTask):
                if(task['weight'][perso] > finalTask['weight'][perso]):
                    finalTask = task
                    idTask = item
        asignTask.append(idTask)
        return finalTask
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
        idFinish = FindId(json_data['name'])
        asignTask.remove(int(idFinish))
        comp = {str(task_id): tasks[str(idFinish)]}
        ptask.append(comp)
        RecordMessage("Task " +  tasks[str(idFinish)]['name'] + " has been finished by " + p['name'])
        return person[person_id]

class OneTask(Resource):
    def get(self, person_id):
        task = GetNextTask(person[person_id]['perso'])
        if(task != None):
            RecordMessage("Task " + task['name'] + " has been give to " + person[person_id]['name'])
        return task

class Governement(Resource):
    def get(self):
        msg= messages
       # ClearMessages()
        return msg

def ReadTask():
    with open("task.csv","r") as filestream:
        for idx1,line in enumerate(filestream):        
            currentline=line.split(",")
            weight={}
            for index, word in enumerate(currentline):
                word=word.rstrip()
                if(index==0):
                    taskName=word
                else:
                    weight[personality[index-1]]=int(word) 
            task={'task_name':taskName,'weights':weight}
            tasks[idx1]=task

api.add_resource(Persons, '/persons')
api.add_resource(Tasks, '/tasks')
api.add_resource(OnePerson, '/persons/<person_id>')
api.add_resource(OneTask, '/persons/<person_id>/next')
api.add_resource(Governement,'/gov')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002, debug=True)


