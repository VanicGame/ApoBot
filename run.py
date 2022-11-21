import os

os.system("python main.py")
os.system("gunicorn keep_alive:app")
