''' 
The Chatbot

author: Sawyer
'''

from flask import Flask
from flask import render_template, redirect, request
import ast
import random

conversation = {}

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def pick_nickname_and_password():
	return render_template('pick_nickname.html')

@app.route('/redirect', methods = ['POST', 'GET'])
def get_nickname_and_redirect():
	nickname = str(request.form['nickname'])
	password = str(request.form['password'])
	if check_password(nickname, password):
		url = '/converse/'+nickname
		return redirect(url)
	return redirect('/')

@app.route('/converse/<nickname>', methods = ['POST', 'GET'])
def index(nickname):
	responses = []
	if nickname in conversation:
		responses = conversation[nickname]
	return render_template('main.html', nickname=nickname, responses=responses)

@app.route('/respond/<nickname>', methods = ['POST', 'GET'])
def respond(nickname):
	try:
		search = str(request.form['searchkey'])
		text = take_input(search, nickname)
	except:
		pass
	url = '/converse/'+nickname
	return redirect(url)

@app.route('/add_response/<nickname>/<post>', methods = ['POST', 'GET'])
def add_response_from_user(nickname, post):
	value = str(request.form['suggestion'])
	add_entry(str(post), value)
	remove_from_unresponded(post)
	url = '/converse/'+nickname
	return redirect(url)

@app.route('/logout/<nickname>', methods = ['POST', 'GET'])
def logout(nickname):
	clear_conversation(nickname)
	return redirect('/')

@app.route('/make_responses', methods = ['POST', 'GET'])
def suggest_responses():
	unanswered = make_unresponded_list()
	return render_template('help.html', unanswered=unanswered)

@app.route('/alternate_help/<post>', methods = ['POST', 'GET'])
def add_alternate_help(post):
	add_to_unresponded_alternate(post)
	url = '/make_responses'
	return redirect(url)

@app.route('/add_response_help/<post>', methods = ['POST', 'GET'])
def add_response_help(post):
	value = str(request.form['suggestion'])
	add_entry(str(post), value)
	remove_from_unresponded(post)
	url = '/make_responses'
	return redirect(url)

def check_password(user, password):
	f = open('users.txt', 'r+')
	x = f.read()
	y = ast.literal_eval(x)
	if user not in y:
		add_user(user, password)
		return True
	if y[user] == password:
		return True
	return False

def add_user(user, password):
	f = open('users.txt', 'r+')
	x = f.read()
	y = ast.literal_eval(x)
	y[user] = password
	z = str(y)
	new_file = open('users.txt', 'w')
	new_file.write(z)
	new_file.close()

def add_entry(key, value):
	f = open('responses.txt', 'r+')
	x = f.read()
	y = ast.literal_eval(x)
	if key not in y:
		y[key] = []
	if value not in y[key]:
		y[key].append(value)
	z = str(y)
	new_file = open('responses.txt', 'w')
	new_file.write(z)
	new_file.close()

def make_dictionary():
	f = open('responses.txt', 'r+')
	x = f.read()
	return ast.literal_eval(x)

def make_unresponded_list():
	f = open('unresponded.txt', 'r+')
	x = f.read()
	return ast.literal_eval(x)

def make_alternate_dictionary():
	f = open('alternate.txt', 'r+')
	x = f.read()
	return ast.literal_eval(x)

def make_alternate_list():
	f = open('unresponded_alternate.txt', 'r+')
	x = f.read()
	return ast.literal_eval(x)

def find_response(key):
	dictionary = make_dictionary()
	if key in dictionary:
		return pick_from_responses(dictionary[key])
	add_to_unresponded(key)
	return None

def pick_from_responses(l):
	if type(l) == list:
		length = len(l)
		index = random.randint(0,length-1)
		return l[index]

def add_to_unresponded(key):
	f = open('unresponded.txt', 'r+')
	x = f.read()
	l = ast.literal_eval(x)
	if key not in l:
		l.append(key)
	l = str(l)
	new_file = open('unresponded.txt', 'w')
	new_file.write(l)
	new_file.close()

def remove_from_unresponded(key):
	f = open('unresponded.txt', 'r+')
	x = f.read()
	l = ast.literal_eval(x)
	if key in l:
		l.remove(key)
	l = str(l)
	new_file = open('unresponded.txt', 'w')
	new_file.write(l)
	new_file.close()

def take_input(key, user):
	response = Response(key, 'user')
	if user in conversation:
		conversation[user].append(response)
	else:
		conversation[user] = []
		conversation[user].append(response)
	if key in make_alternate_dictionary():
		res = make_alternate_response(key)
	else:
		res = find_response(key)
	if res == None:
		res = "Sorry, we don't have a response for that yet"
	response = Response(res, 'chatbot')
	conversation[user].append(response)	
	return res

def clear_conversation(user):
	conversation[user] = []

def add_to_unresponded_alternate(message):
	f = open('unresponded_alternate.txt', 'r+')
	x = f.read()
	l = ast.literal_eval(x)
	if message not in l:
		l.append(str(message))
	l = str(l)
	new_file = open('unresponded_alternate.txt', 'w')
	new_file.write(l)
	new_file.close()

def remove_from_unresponded_alternate(message):
	f = open('unresponded_alternate.txt', 'r+')
	x = f.read()
	l = ast.literal_eval(x)
	if message in l:
		l.remove(message)
	l = str(l)
	new_file = open('unresponded_alternate.txt', 'w')
	new_file.write(l)
	new_file.close()

def make_alternate_response(key):
	d = make_alternate_dictionary()
	if key not in d:
		return None
	function = d[key]
	if function == 'something':
		return something()

def add_alternate_function(key, function):
	f = open('alternate.txt', 'r+')
	x = f.read()
	d = ast.literal_eval(x)
	if key not in d:
		d[key] = function
	d = str(d)
	new_file = open('alternate.txt', 'w')
	new_file.write(d)
	new_file.close()
	remove_from_unresponded_alternate(key)

class Response:
	def __init__(self, text, speaker):
		self.text = text
		self.speaker = speaker

def something():
	return 'hello again'

if __name__ == '__main__':
	add_alternate_function('something', 'something')
	app.run()