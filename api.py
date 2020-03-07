from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker
import json
import bcrypt
from src.playerdetails import PlayerDetails
from src.watchTest import Summoner

db_connect = create_engine('sqlite:///fantasyleague.db')


Session = sessionmaker()
Session.configure(bind=db_connect)
session = Session()

app = Flask(__name__)
api = Api(app)


CORS(app) # To solve the CORS issue when making HTTP Requests

class PasswordSetup:
    def create_password(self, pw):
        """
        Creates a hash for a given password.

        Args:
            player: The password to be converted to hash. 
            This is to ensure privacy for the users password.
        Returns:
            Hashed version of the users password.

        """
        hash = bcrypt.hashpw(password=pw.encode('utf-8'), salt=bcrypt.gensalt())
        return hash.decode('utf-8')

    def validate_password(self, pw, hpw):
        """
        Validates a password with the corresponding hashed password.

        Args:
            player: The password .
        Returns:
            hashed version of the users password.

        """
        print(bcrypt.checkpw(pw.encode('utf-8'), hpw.encode('utf-8')))
        return bcrypt.checkpw(pw.encode('utf-8'), hpw.encode('utf-8'))

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
        SummonerName = request.json['summonerName'] # Get SummonerName
        _rank = Summoner.get_rank_string(self, SummonerName) # Get rank
        mmr_query = conn.execute("SELECT mmr from Ranks where rank= ?", (_rank)) # Get the Users from the Lobby
        res = mmr_query.cursor.fetchall()
        _mmr = res[0][0]
        conn.execute("insert into Lobby values(null,'{0}', '{1}', '{2}')".format(SummonerName, _rank, _mmr))
        return request.json
    def get(self):
        conn = db_connect.connect()
        query = conn.execute(
            "select COUNT(summonerName) from Lobby")
        qResult = query.cursor.fetchall()
        playerCount = qResult[0][0]
        if playerCount <= 10:
            playerCount = qResult[0][0]
        else:
            playerCount = "FULL"
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
            hashed = PasswordSetup.create_password(self, Password)
            conn.execute("INSERT INTO users VALUES(null, '{0}', '{1}', '{2}', '{3}')".format(
                Username, SummonerName, hashed, role))
            status = "OK"
            print(request.json)

        return status
# CORS(app)
class Login(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        conn = db_connect.connect()

        query = conn.execute("select COUNT(username) from Users where username= ?", (username))
        username_from_db = query.cursor.fetchall()

        if username_from_db[0][0] > 0:
            query2 = conn.execute("select password from Users where username= ?", (username))
            hpw_from_db = query2.cursor.fetchall()
            print(hpw_from_db[0][0])
            response = PasswordSetup.validate_password(self, password, hpw_from_db[0][0])
        else:
            response = False
        return response

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

class MatchMaking(Resource):
    def get(self):
        matching_state = True # Set matching state to true
        conn = db_connect.connect() # Connect to the Database
        
        query = conn.execute("select summonerName FROM Lobby order by mmr desc") # Get the Users from the Lobby

        # Add Players in Lobby to the matchmaking queue
        results = query.cursor.fetchall()
        count = 0
        while matching_state:
            # for i in results:
            _summoner_name_1 = results[count][0]
            count+=1
            _summoner_name_2 = results[count][0]
            print("Summoner Name: {0}".format(_summoner_name_1))
            print("Summoner Name: {0}".format(_summoner_name_2))
            conn.execute("insert into Match values('{0}', '{1}')".format(1, _summoner_name_1))
            conn.execute("insert into Match values('{0}', '{1}')".format(2, _summoner_name_2))
            # _rank_str = Summoner.get_rank_string(self, _summonerName)
            # mmr_query = conn.execute("SELECT mmr from Ranks where rank= ?", (_rank_str)) # Get the Users from the Lobby
            # res = mmr_query.cursor.fetchall()
            # _mmr = res[0][0]
            # p = PlayerDetails(_summonerName, _rank_str, _mmr)
            # print(p)
            count +=1
            if(count == 10):
                matching_state = False

            # Sort the Match Table
            match_query = conn.execute("select team, player FROM Match order by team desc")

        return {'match': [i[0] for i in match_query.cursor.fetchall()]}

class Employees(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        # This line performs query and returns json result
        query = conn.execute("select * from employees")
        # Fetches first column that is Employee ID
        return {'employees': [i[0] for i in query.cursor.fetchall()]}

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
api.add_resource(Employees_Name, '/employees/<employee_id>')  # Route_3
api.add_resource(Users, '/users')  # Route_4
api.add_resource(UsersName, '/users/<username>')  # Route_3
api.add_resource(Login, '/login')  # Login Route
api.add_resource(MatchMaking, '/mm')  # Matchmaking Route

# Methods


def getSummoner(player):
        # Connect to the database
        # conn = db_connect.connect()
        # Search for the Summoner
    summonerDetails = Summoner.get_player_details(player)
    # print(summonerDetails)
    # Check if the Summoner Exists
    # Return Summoner Data
    # Retrieve SummonerID
    # Insert SummonerID Into USERS Table for the given summoner



if __name__ == '__main__':
    app.run(port='5002')
