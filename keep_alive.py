from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
	return "Bot is up and running :D"
