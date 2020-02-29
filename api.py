from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS
import json
import bcrypt
from src.watchTest import Summoner

db_connect = create_engine('sqlite:///fantasyleague.db')
app = Flask(__name__)
api = Api(app)

CORS(app)


class Players(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to the db
        query = conn.execute(
            "select summonerName, rank, tier, wins, losses, primaryRole, secondaryRole from players")
        result = {'players': [dict(zip(tuple(query.keys()), i))
                              for i in query.cursor]}
        return result


class PlayerStandings(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to the db
        query = conn.execute("SELECT * FROM Players ORDER BY wins DESC;")
        result = {'players': [dict(zip(tuple(query.keys()), i))
                              for i in query.cursor]}
        return result


class Lobby(Resource):
    def post(self):
        conn = db_connect.connect()  # connect to the db
        SummonerName = request.json['summonerName']
        conn.execute(
            "insert into Lobby values(null,'{0}')".format(SummonerName))
        print("entered")
        return request.json
    def get(self):
        conn = db_connect.connect()
        query = conn.execute(
            "select COUNT(summonerName) from Lobby")
        qResult = query.cursor.fetchall()
        playerCount = qResult[0][0]
        # return request.json
        return playerCount


class Users(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        # This line performs query and returns json result
        query = conn.execute("select username from users")
        # Fetches first column that is Employee ID
        return {'users': [i[0] for i in query.cursor.fetchall()]}

    def post(self):
        conn = db_connect.connect()  # connect to the db
        Username = request.json['username']
        SummonerName = request.json['summonerName']
        print("SummonerName: {0}".format(SummonerName))
        Password = request.json['password']
        role = request.json['role']
        getSummoner(SummonerName)
        # first check if username exists
        query = conn.execute(
            "select COUNT(username) from Users where username= ?", (Username))
        qResult = query.cursor.fetchall()
        status = ""
        # print(qResult)
        if qResult[0][0] > 0:
            print("Username Taken")
            status = "UT"
        # check if summoner name exists
        query2 = conn.execute(
            "select COUNT(summonerName) from Users where summonerName= ?", (SummonerName))
        qResult2 = query2.cursor.fetchall()
        print(qResult2[0][0])
        if qResult2[0][0] > 0:
            # print("Summonername Taken")
            status = "ST"

        # if both pass, register user
        else:
            # print("Registration Valid")
            hashed = create_password(Password)
            conn.execute("INSERT INTO users VALUES(null, '{0}', '{1}', '{2}', '{3}')".format(
                Username, SummonerName, hashed, role))
            status = "OK"
            print(request.json)

        return status


class UsersName(Resource):
    def get(self, username):
        conn = db_connect.connect()
        query = conn.execute(
            "select COUNT(username) from Users where username= ?", (username))
        getResult = query.cursor.fetchall()
        print("Usernames in Table: {0}".format(getResult[0][0]))
        status = ""
        if getResult[0][0] == 0:
            status = "USERNAME_OK"
        else:
            status = "USERNAME_TAKEN"
        print(status)
        return status


class Employees(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        # This line performs query and returns json result
        query = conn.execute("select * from employees")
        # Fetches first column that is Employee ID
        return {'employees': [i[0] for i in query.cursor.fetchall()]}


class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute(
            "select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple(query.keys()), i))
                           for i in query.cursor]}
        return jsonify(result)


class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute(
            "select * from employees where EmployeeId =%d " % int(employee_id))
        result = {'data': [dict(zip(tuple(query.keys()), i))
                           for i in query.cursor]}
        response = jsonify(result)
        return response


api.add_resource(Players, '/players')  # Route_1
api.add_resource(PlayerStandings, '/playerstandings')  # Route_2
api.add_resource(Lobby, '/lobby')  # Route_3
api.add_resource(Employees, '/employees')  # Route_1
api.add_resource(Tracks, '/tracks')  # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>')  # Route_3
api.add_resource(Users, '/users')  # Route_4
api.add_resource(UsersName, '/users/<username>')  # Route_3

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

def create_password(pw):
    hash = bcrypt.hashpw(password=pw.encode('utf-8'), salt=bcrypt.gensalt())
    return hash.decode('utf-8')

def validate_password(pw, hpw):
    return bcrypt.checkpw(pw.encode('utf-8'), hpw.encode('utf-8'))

if __name__ == '__main__':
    app.run(port='5002')
