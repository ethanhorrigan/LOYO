from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS
import json
from watchTest import Summoner

db_connect = create_engine('sqlite:///fantasyleague.db')
app = Flask(__name__)
api = Api(app)

CORS(app)

class Players(Resource):
    def get(self):
        conn = db_connect.connect() # connect to the db
        query = conn.execute("select summonerName, rank, tier, wins, losses, primaryRole, secondaryRole from players")
        result = {'players':[dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
class PlayerStandings(Resource):
    def get(self):
        conn = db_connect.connect() # connect to the db
        query = conn.execute("SELECT * FROM Players ORDER BY wins DESC;")
        result = {'players':[dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
class Lobby(Resource):
    def post(self):
        conn = db_connect.connect() # connect to the db
        SummonerName = request.json['SummonerName']
        conn.execute("insert into Lobby values(null,'{0}')".format(SummonerName))
        print(request.json)
        return request.json


class Users(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select username from users") # This line performs query and returns json result
        return {'users': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
    def post(self):
        conn = db_connect.connect() # connect to the db
        Username = request.json['username']
        SummonerName = request.json['summonerName']
        print("SummonerName: {0}".format(SummonerName))
        Password = request.json['password']
        role = request.json['role']
        getSummoner(SummonerName)
        # first check if username exists
        query = conn.execute("select COUNT(username) from Users where username= ?", (Username))
        # print(query.cursor.fetchall())
        qResult = query.cursor.fetchone()
        status = ""
        # print(qResult)
        if qResult != '(0,)':
            print("Username Taken")
            status = "UT"
        # check if summoner name exists
        query2 = conn.execute("select COUNT(summonerName) from Users where summonerName= ?", (SummonerName))
        qResult2 = query2.cursor.fetchall()
        print(qResult2[0][0])
        if qResult2 != '(0,)':
            # print("Summonername Taken")
            status = "ST"

        # if both pass, register user
        else:
            # print("Registration Valid")
            conn.execute("INSERT INTO users VALUES(null, '{0}', '{1}', '{2}', '{3}')".format(Username, SummonerName, Password, role))
            status = "OK"
            print(request.json)

        return status
class UsersName(Resource):
    def get(self, username):
        conn = db_connect.connect() 
        query = conn.execute("select username from Users where username= ?", (username))
        getResult = query.cursor.fetchone()
        print(getResult)
        if getResult is None:
            print("test")
            return "TEST"

            
        return "taken"
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
api.add_resource(PlayerStandings, '/playerstandings') # Route_2
api.add_resource(Lobby, '/lobby') # Route_3
api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3
api.add_resource(Users, '/users') # Route_4
api.add_resource(UsersName, '/users/<username>') # Route_3

# Methods
def getSummoner(player):
        # Connect to the database
        # conn = db_connect.connect()
        # Search for the Summoner
        summonerDetails = Summoner.getPlayerDetails(player)
        # print(summonerDetails)
        # Check if the Summoner Exists
        # Return Summoner Data
        # Retrieve SummonerID
        # Insert SummonerID Into USERS Table for the given summoner

if __name__ == '__main__':
     app.run(port='5002')
     