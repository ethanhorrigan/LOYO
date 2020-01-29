from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS
import json

db_connect = create_engine('sqlite:///fantasyleague.db')
app = Flask(__name__)
api = Api(app)

CORS(app)

class Players(Resource):
    def get(self):
        conn = db_connect.connect() # connect to the db
        query = conn.execute("select Summoner_Name, Rank, Tier, MMR, Points from players")
        result = {'players':[dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
      

class Users(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from users") # This line performs query and returns json result
        return {'users': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
    def post(self, username, summonerName, password, token):
        print("entered post")
        conn = db_connect.connect() # connect to the db
        cursor = conn.cursor()
        query = """INSERT INTO users (username, summonerName, password, token) VALUES (?, ?, ?, ?);"""
        data_tuple = (username, summonerName, password, token)
        cursor.execute(query, data_tuple)
        conn.commit()
class Employees(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from employees") # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID

class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        response = jsonify(result)
        return response
        

api.add_resource(Players, '/players') # Route_1
api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3
api.add_resource(Users, '/users/register') # Route_4


if __name__ == '__main__':
     app.run(port='5002')
     