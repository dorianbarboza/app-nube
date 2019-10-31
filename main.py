from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import requests
import json

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dorian:dorian12345@/app_bd?host=/cloudsql/app-nube-bd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dorian:dorian12345@localhost/app_bd'

db = SQLAlchemy(app)

@app.route('/home/')
def home():
    url = 'http://127.0.0.1:8080/app-nube/api/v1.0/usuario/getall/'
    response = requests.get(url)

    if response.status_code == 200:
        contenido = response.content
    return render_template('home.html', contenido = contenido)

class Usuario(db.Model):

    #__tablename__ = 'Usuario'

    ID_Usuario = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(10), unique = False)
    password = db.Column(db.String(10), unique = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<ID_Usuario> {}'.format(self.ID_Usuario)

    def serialize(self):
        return {
            'ID_Usuario': self.ID_Usuario,
            'username': self.username,
            'password': self.password
            }

@app.route('/app-nube/api/v1.0/usuario/getall/', methods = ['GET'])
def get_all():
    try:
        users = Usuario.query.all()
        return  jsonify([e.serialize() for e in users])
    except Exception as e:
	    return(str(e))


if __name__ == '__main__':
    app.run(debug = True, host = '127.0.0.1', port = 8080)
    db.create_all()
