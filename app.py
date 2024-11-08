# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Bienvenido a Artigow!'

if __name__ == '__main__':
    app.run(debug=True)
