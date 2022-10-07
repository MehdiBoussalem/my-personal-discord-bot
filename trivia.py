import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

reqSession = requests.Session()
url ="https://opentdb.com/api.php?amount=1"

def isbool(json):

    if json['results'][0]['type'] == 'boolean':
        return True
    return False

def getQuestion(url):
    reponse = reqSession.get(url)
    catogory = reponse.json()['results'][0]['category']
    question = reponse.json()['results'][0]['question']
    question = question.replace('&quot;', '"')
    question = question.replace('&#039;', "'")
    question = question.replace('&amp;', '&')
    question = translate(question)
    correct_answer = reponse.json()['results'][0]['correct_answer']
    correct_answer = correct_answer.replace('&quot;', '"')
    correct_answer = correct_answer.replace('&#039;', "'")
    correct_answer = correct_answer.replace('&amp;', '&')
    correct_answer = translate(correct_answer)
    incorrect_answers = reponse.json()['results'][0]['incorrect_answers']
    incorrect_answers = [x.replace('&quot;', '"') for x in incorrect_answers]
    incorrect_answers = [x.replace('&#039;', "'") for x in incorrect_answers]
    incorrect_answers = [x.replace('&amp;', '&') for x in incorrect_answers]
    incorrect_answers = [translate(x) for x in incorrect_answers]
    is_boolean = isbool(reponse.json())
    return catogory, question, correct_answer, incorrect_answers, is_boolean

def translate(text, lang='FR'):
    key = config['DEEPL']['key']

    url = "https://api-free.deepl.com/v2/translate?text=" + text + "&target_lang="+lang+"&auth_key=" + key
    response = reqSession.get(url)
    return response.json()['translations'][0]['text']

