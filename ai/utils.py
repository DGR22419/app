import json
import os

# def load_questions():
#     # Adjust the path based on where your JSON file is stored
#     json_path = os.path.join(os.path.dirname(__file__), 'data', 'questions.json')
#     with open(json_path, 'r') as file:
#         questions = json.load(file)
#     return questions

####################################################################################
#                                   python                                         #
####################################################################################

def python_easy():
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'python' , 'py_easy.json')
    with open(json_path, 'r') as file:
        questions = json.load(file)
    return questions

def python_inter():
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'python' , 'py_inter.json')
    with open(json_path, 'r') as file:
        questions = json.load(file)
    return questions

def python_adv():
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'python' , 'py_adv.json')
    with open(json_path, 'r') as file:
        questions = json.load(file)
    return questions

####################################################################################
#                                       java                                       #
####################################################################################

def java_easy():
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'java' , 'jv_easy.json')
    with open(json_path, 'r') as file:
        questions = json.load(file)
    return questions

def java_inter():
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'java' , 'jv_inter.json')
    with open(json_path, 'r') as file:
        questions = json.load(file)
    return questions

def java_adv():
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'java' , 'jv_adv.json')
    with open(json_path, 'r') as file:
        questions = json.load(file)
    return questions

####################################################################################