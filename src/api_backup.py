from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker
from riotwatcher import RiotWatcher, ApiError
import json
import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor
from uuidcreator import UUIDGenerator

db_connect = create_engine('sqlite:///fantasyleague.db')

Session = sessionmaker()
Session.configure(bind=db_connect)
session = Session()

app = Flask(__name__)
api = Api(app)

watcher = RiotWatcher('RGAPI-12c35bf1-b43f-4007-882e-6c63132628c6')

QUEUE_TYPE = 'RANKED_SOLO_5x5'
my_region = 'euw1'

CORS(app) # To solve the CORS issue when making HTTP Requests

try:
    # dsn=None, connection_factory=None, cursor_factory=None, **kwargs
    connection = psycopg2.connect(user = "postgres", password = "horrigan902", host = "127.0.0.1", port ="5432", database = "loyo_db")
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    # print(connection.get_dsn_parameteres())
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")
    
    
except (Exception, psycopg2.Error) as error:
    print ("Error while connecting to PostgreSQL", error)

class Match():
    # Game Outcome
    # Get gameId from the players account id
    def get_player_id(self, summoner_name):
        pass
    def get_match_id(self, player_id):
        pass
# TODO: get summoner details
class Summoner():
    def get_player_details(self):
        """
        Verifies if the Player exists in Riot's database.

        Args:
            self: The player name which is used to verify if the player exists.

        Returns:
            The value if the Summoner Name is found else the Summoner Name is Not Found.

        """
        try:
            response = watcher.summoner.by_name(my_region, self)
        except ApiError as err:
            if err.response.status_code == 429:
                print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
                print('this retry-after is handled by default by the RiotWatcher library')
                print('future requests wait until the retry-after time passes')
            elif err.response.status_code == 404:
                print("SUMMONER_NOT_FOUND")
                response = "SUMMONER_NOT_FOUND"
            else:
                raise
        return response
        
    def get_rank(self):
        """
        Retrieves the rank of the Summoner as an Integer.

        Args:
            self: The Summoners name

        Returns:
            The rank of the Summoner as an Integer

        """
        count = 0
        player_details = watcher.summoner.by_name(my_region, self)
        summoner_data  = watcher.league.by_summoner(my_region, player_details['id'])
        if(summoner_data[count]['queueType'] == QUEUE_TYPE):
            rank = summoner_data[count]['rank'] # Retrieve the Rank
            rank_as_int = Summoner.roman_to_int(self, rank) # Converts rank to an Integer
            response = rank_as_int
        else:
            while(summoner_data[count]['queueType'] != QUEUE_TYPE):
                count+=1
                if(summoner_data[count]['queueType'] == QUEUE_TYPE):
                    rank = summoner_data[count]['rank'] # Retrieve the Rank
                    rank_as_int = Summoner.roman_to_int(self, rank) # Converts rank to an Integer
                    # count = 0
                    response = rank_as_int
        return response
    
    def get_tier(self):
        """
        Retrieves the Tier of the Summoners current rank between (1..4)

        Args:
            self: The summoners name to check.

        Returns:
            The Tier of the Summoners Rank

        """
        count = 0
        player_details = watcher.summoner.by_name(my_region, self)
        summoner_data = watcher.league.by_summoner(my_region, player_details['id'])

        if(summoner_data[count]['queueType'] == QUEUE_TYPE):
            response = summoner_data[count]['tier']
        else:
            while(summoner_data[count]['queueType'] != QUEUE_TYPE):
                count += 1
                if(summoner_data[count]['queueType'] == QUEUE_TYPE):
                    response = summoner_data[count]['tier']
        return response
    
    def get_rank_string(self, player):
        """
        Combines the Rank and Tier for a Player into one String.

        Args:
            player: The players details for rank and tier lookup.
        Returns:
            Rank and Tier as a String.

        """
        _rank = Summoner.get_rank(player)
        _tier = Summoner.get_tier(player)
        _response = _tier + str(_rank)
        return _response

    # Convert Roman Numerals to INT
    def roman_to_int(self, s):
        rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        int_val = 0
        for i in range(len(s)):
            if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
                int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
            else:
                int_val += rom_val[s[i]]
        return int_val

    def get_difference(self, player1, player2):
        """
        Retrieves the difference in MMR between two players

        Args:
            player1: the first players MMR.
            player2: the second players MMR.

        Returns:
            The MMR Difference between the two players.

        """
        diff = 0
        if(player1 >= player2):
            diff = abs(player1 - player2)
        if(player2 >= player1):
            diff = abs(player2 - player1)
        return diff
    def get_outcome(self, match_id):
        pass
    def get_match_id(self, player):
        pass

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
        """
        Retrieves the players in-game statistics.

        Returns:
        Players Stats in JSON format.

        """
        conn = db_connect.connect()  # connect to the db
        query = conn.execute(
            "select summonerName, rank, tier, wins, losses, primaryRole, secondaryRole from players")
        result = {'players': [dict(zip(tuple(query.keys()), i))
                              for i in query.cursor]}
        return result


class PlayerStandings(Resource):
    def get(self):
        """
        Get the leaderboards from the database.

        Returns:
        Leaderboards from the database.

        """

        # conn = db_connect.connect()  # connect to the db
        # query = conn.execute("SELECT * FROM Players ORDER BY wins DESC;")
        # result = {'players': [dict(zip(tuple(query.keys()), i))for i in query.cursor]}
        # return result

        cursor = connection.cursor()

        cursor.execute("SELECT summoner_name, user_name, rank, tier, mmr, wins, losses, primary_role FROM users ORDER BY wins DESC")
        # cursor.execute("select array_to_json(array_agg(row_to_json(t))) from (select summoner_name, wins, losses, rank, primary_role from users) t")
        # https://stackoverflow.com/questions/10252247/how-do-i-get-a-list-of-column-names-from-a-psycopg2-cursor/46000207#46000207
        columns = [desc[0] for desc in cursor.description]
        result = {'players': [dict(zip(columns, row)) for row in cursor.fetchall()]}

        return result


class Lobby(Resource):
    def post(self):
        """
        Inserts a user to the lobby, the lobby is used to hold players,
        before matchmaking takes place.

        Returns:
        Inserts a user to the lobby and returns the data in JSON.

        """
        
        conn = db_connect.connect()  # connect to the db
        SummonerName = request.json['summonerName'] # Get SummonerName
        _rank = Summoner.get_rank_string(self, SummonerName) # Get rank
        # mmr_query = conn.execute("SELECT mmr from Ranks where rank= ?", (_rank)) # Get the Users from the Lobby
        cursor = connection.cursor()
        cursor.execute("SELECT mmr from Ranks where rank= ?", (_rank))
        res = cursor.fetchall()
        _mmr = res[0][0]
        conn.execute("insert into Lobby values(null,'{0}', '{1}', '{2}')".format(SummonerName, _rank, _mmr))
        return request.json
    def get(self):
        """
        Get the amount of players currently in the lobby, to verify
        if enough players are avaialable for a match to begin.

        Returns:
        The amount of players currently waiting in the lobby.

        """       
        conn = db_connect.connect()
        query = conn.execute("select COUNT(summonerName) from Lobby")
        qResult = query.cursor.fetchall()
        playerCount = qResult[0][0]
        if playerCount <= 10:
            playerCount = qResult[0][0]
        else:
            playerCount = "FULL"
        return playerCount


class Users(Resource):
    def get(self):
        """
        Validates a password with the corresponding hashed password.

        Args:
        player: The password .
        Returns:
        hashed version of the users password.

        """       
        conn = db_connect.connect()  # connect to database
        # This line performs query and returns json result
        query = conn.execute("select username from users")
        # Fetches first column that is Employee ID
        return {'users': [i[0] for i in query.cursor.fetchall()]}

    def post(self):
        """
        Handles user registration.
        First check if the user exists, if not continue.
        Check if the the summoner name exists in RIOT's Database.
        If both username and summoner name don't exist, proceed to register the user.
        Encrypt the password for an extra layer of security.

        Returns:
        A register user inserted into the database.
        """       
        conn = db_connect.connect()  # connect to the db
        Username = request.json['username']
        SummonerName = request.json['summonerName']
        Password = request.json['password']
        role = request.json['role']
        # first check if username exists
        query = conn.execute(
            "select COUNT(username) from Users where username= ?", (Username))
        qResult = query.cursor.fetchall()
        status = ""
        if qResult[0][0] > 0:
            print("Username Taken")
            status = "UT"
        query2 = conn.execute(
            "select COUNT(summonerName) from Users where summonerName= ?", (SummonerName))
        qResult2 = query2.cursor.fetchall()
        print(qResult2[0][0])
        if qResult2[0][0] > 0:
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

class Login(Resource):
    def post(self):
        """
        Handles user authentication.
        First check if the user exists, if not continue, else return false.
        Compare the password given with the hashed password in the database for a given user.

        Returns:
        True if authentication is correct.
        False if the user or password is incorrect.
        """     
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
        """
        Handles user verification.
        Checks if the user exists in the database.

        Returns:
        USERNAME_OK if the username does not exist.
        USERNAME_TAKEN if the username already exists.
        """    
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
        return status

class MatchMaking(Resource):
    def get(self):
        """
        Handles the matchmaking process.
        Set the matching_state to true while there is still users in the lobby.
        Generate a Universally unique identifier for each match created to
        distinguish between matches.
        Insert players into their respective teams.

        Returns:
        Match ready teams.
        """    
        matching_state = True # Set matching state to true
        conn = db_connect.connect() # Connect to the Database
        
        query = conn.execute("select summonerName FROM Lobby order by mmr desc") # Get the Users from the Lobby

        uuid = UUIDGenerator.generate_uuid(self) # Generate a Unique ID for the match.

        results = query.cursor.fetchall() # Get the players currently in the lobby.
        count = 0
        while matching_state:
            _summoner_name_1 = results[count][0]
            count+=1
            _summoner_name_2 = results[count][0]
            conn.execute("insert into Match values('{0}', '{1}', '{2}')".format(1, _summoner_name_1, uuid))
            conn.execute("insert into Match values('{0}', '{1}', '{2}')".format(2, _summoner_name_2, uuid))
            count +=1
            if(count == 10):
                matching_state = False
            # Sort the Match Table
            match_query = conn.execute("select team, summoner_name, uuid FROM Match order by team asc")

        return {'match': [dict(zip(tuple(match_query.keys()), i)) for i in match_query.cursor]}

api.add_resource(Players, '/players')  # Route_1
api.add_resource(PlayerStandings, '/playerstandings')  # Route_2
api.add_resource(Lobby, '/lobby')  # Route_3
api.add_resource(UsersName, '/users/<username>')  # Route_4
api.add_resource(Users, '/users')  # Route_5
api.add_resource(Login, '/login')  # Route_6
api.add_resource(MatchMaking, '/mm')  # Route_7

if __name__ == '__main__':
    app.run(port='5002')
