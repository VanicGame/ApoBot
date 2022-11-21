from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return "Bot is up and running :D"
