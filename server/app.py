from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)
api = Api(app)

taskMax = 3
taskPool = 6


person = {
    '1': {
        'name':"Itch",
        'perso': "mechanic",
        'tasks': [],
        'count': 0,
        'coin':0,
        'taskDone':0
    },
    '2': {
        'name':"Bob",
        'perso': 'duty fullfiller',
        'tasks': [],
        'count': 0,
        'coin':0,
        'taskDone':0
    }
}

tasks = {
}

selectedTask = {}

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
        for item in selectedTask:
            task = selectedTask[item]
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
        p = {'name':json_data['name'], 'perso': json_data['perso'], 'tasks': [],'count':0,'coin':0,'taskDone':0}
        person_id = int(max(person.keys(),key=int))+1
        person[str(person_id)] = p
        RecordMessage("Added person " + p['name'])
        return person_id

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
        comp = {str(task_id): tasks[idFinish]}
        ptask.append(comp)
        RecordMessage("Task " +  tasks[idFinish]['name'] + " has been finished by " + p['name'])
        return person[person_id]

class OneTask(Resource):
    def get(self, person_id):
        print(person_id)
        if(person[person_id]['taskDone'] < taskMax):
            task = GetNextTask(person[str(person_id)]['perso'])
            if(task != None):
                RecordMessage("Task " + task['name'] + " has been give to " + person[person_id]['name'])
            if(task != None):     
                person[person_id]['taskDone'] = person[person_id]['taskDone'] +1   
                retTask = {'name': task['name'], 'weight': 6-task['weight'][person[person_id]['perso']]}
                return retTask
            else:
                return {'name':"Do nothing", 'weight':0}
        else:
            tasks.clear()
            asignTask.clear()
            selectedTask.clear()
            person[person_id]['taskDone'] = 0
            ReadTask()
            return {'name':"Go to sleep", 'weight':0}

class Governement(Resource):
    def get(self):
        msg= messages
       # ClearMessages()
        return msg

def ReadTask():
    personality=["duty_fullfiller","mechanic","nurturer","thinker","scientist"]    
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
            task={'name':taskName,'weight':weight}
            tasks[idx1]=task
    RandomSixTask()
    

def RandomSixTask():
    nbMax = int(max(tasks.keys(),key=int))
    for i in range(6):
        ran = random.randint(1,nbMax)
        print(str(ran))
        if(ran not in selectedTask.keys()):
            task = tasks[ran]
            selectedTask[str(i)] = task

api.add_resource(Persons, '/persons')
api.add_resource(Tasks, '/tasks')
api.add_resource(OnePerson, '/persons/<person_id>')
api.add_resource(OneTask, '/persons/<person_id>/next')
api.add_resource(Governement,'/gov')

ReadTask()


if __name__ == '__main__':    
    app.run(host='0.0.0.0',port=5002, debug=True)
    

