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

def prettify(file):
    """
    Turn an ugly json into a prettier one.
    '.json' is left off of file for m̶y̶  your convenience.
    """
    with open(f'{file}.json', "r") as ugly, open(f'{file}_prettified.json', "w") as pretty:
        pretty.write(prettyjson(json.load(ugly)))

def prettyjson(obj, width=95, buffer=0):
    """
    Return obj in a pretty json format.
    """
    if not isinstance(obj, (dict, list, tuple)):
        return stringify(obj)

    if isinstance(obj, dict):
        open_, close, line = *'{}', []
        for key, value in obj.items():
            key = stringify(key)
            line.append(f'{key}: {prettyjson(value, width, buffer + len(key) + 3)}')
    else:
        open_, close, line = *'[]', [prettyjson(item, width, buffer + 1) for item in obj]

    joiners = ', ', f',\n{" " * (buffer + 1)}'
    for joiner in joiners:
        joined = f'{open_}{joiner.join(line)}{close}'
        if len(joined) <= width:
            break
    return joined

def stringify(obj):
    if isinstance(obj, str):
        return f'"{obj}"'
    if isinstance(obj, bool):
        return str(obj).lower()
    return str(obj)

class Players(Resource):
    def get(self):
        conn = db_connect.connect() # connect to the db
        query = conn.execute("select Summoner_Name, Rank, Tier, MMR, Points from players")
        result = {'players':[dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
      

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


if __name__ == '__main__':
     app.run(port='5002')
     