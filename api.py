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
import urllib.parse as urlparse
from src.LoyoEnums import Outcome

# db_connect = create_engine('sqlite:///fantasyleague.db')

# Session = sessionmaker()
# Session.configure(bind=db_connect)
# session = Session()

database = "d34bp9cpp983nn"
user = "cfrqbgcghvvkyw"
db_password = "553a3ddb1f43deb191cf1001d58ba5ce319d55f24e83ebad7c91f03fab8d90dd"
host = "ec2-35-168-54-239.compute-1.amazonaws.com"
port = "5432"

app = Flask(__name__)
api = Api(app)

watcher = RiotWatcher('RGAPI-646600b8-b063-4402-a7f6-7defa618ffdd')

QUEUE_TYPE = 'RANKED_SOLO_5x5'
my_region = 'euw1'

CORS(app) # To solve the CORS issue when making HTTP Requests

try:
    # dsn=None, connection_factory=None, cursor_factory=None, **kwargs
    connection = psycopg2.connect(user=user, password=db_password, host=host, port=port, database=database)
    
    # connection = psycopg2.connect(user = "postgres", password = "horrigan902", host = "127.0.0.1", port ="5432", database = "loyo_db")
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
    def get_account_id(self):
        """
        Retrieves the account id to the corresponding summoner name

        Args:
            self: The summoner name.

        Returns:
            The account id for that summoner.

        """
        player_details = watcher.summoner.by_name(my_region, self)
        return player_details['accountId']
    def get_player_icon(self):
        player_icon = watcher.summoner.by_name(my_region, self)
        return player_icon['profileIconId']

    def get_lastest_game_id(self):
        account_id = Summoner.get_account_id(self)
        match_id = watcher.match.matchlist_by_account(my_region, account_id)
        return match_id['matches'][0]['gameId']

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

# print(Summoner.get_match_id('Yupouvit'))

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
        # conn = db_connect.connect()  # connect to the db
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

        cursor.execute("SELECT summoner_name, user_name, rank, mmr, wins, losses, primary_role, player_icon FROM users ORDER BY wins DESC")
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
        cursor = connection.cursor() # connect to the db

        cursor.execute("DELETE FROM lobby")

        _summoner_name = request.json['summonerName'] # Get SummonerName from requests
        role_query = ("SELECT primary_role FROM users WHERE summoner_name = %s")
        param = [_summoner_name]
        cursor.execute(role_query, param)
        # _primary_role = cursor.fetchall()
        _primary_role = cursor.fetchall()[0][0]
        print(_primary_role)

        connection.commit()

        _rank = Summoner.get_rank_string(self, _summoner_name) # Get rank

        # mmr_query = conn.execute("SELECT mmr from Ranks where rank= ?", (_rank)) # Get the Users from the Lobby
        cursor.execute("SELECT mmr from Ranks where rank='{0}'".format(_rank))
        res = cursor.fetchall()
        _mmr = res[0][0]
        cursor.execute("insert into Lobby values('{0}', '{1}', '{2}')".format(_summoner_name, _mmr, _primary_role))

        connection.commit()
        return request.json
    def get(self):
        """
        Get the amount of players currently in the lobby, to verify
        if enough players are avaialable for a match to begin.

        Returns:
        The amount of players currently waiting in the lobby.

        """       
        cursor = connection.cursor() # connect to the db
        query = ("select COUNT(summoner_name) from Lobby")
        cursor.execute(query)
        qResult = cursor.fetchall()
        playerCount = qResult[0][0]
        if playerCount <= 10:
            playerCount = qResult[0][0]
        else:
            playerCount = "FULL"
        return playerCount

class SummonerName(Resource):
    def get(self, user_name):
        cursor = connection.cursor()
        query = ("SELECT summoner_name from users WHERE user_name =%s")
        query_param = [user_name]
        cursor.execute(query, query_param)
        result = cursor.fetchall()
        
        return result
# Register
class Users(Resource):

    def get(self):
        """
        Validates a password with the corresponding hashed password.

        Args:
        player: The password .
        Returns:
        hashed version of the users password.

        """       
        cursor = connection.cursor() # connect to the db
        # This line performs query and returns json result
        query = ("select username from users")
        cursor.execute(query)
        # Fetches first column that is Employee ID
        return {'users': [i[0] for i in cursor.fetchall()]}

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
        Username = request.json['username']
        SummonerName = request.json['summonerName']
        
        Password = request.json['password']
        role = request.json['role']
        _account_id = Summoner.get_account_id(SummonerName) # get the account id
        _rank_string = Summoner.get_rank_string(self, SummonerName)
        _player_icon = Summoner.get_player_icon(SummonerName)
        print(_player_icon)
        cursor = connection.cursor()
        query = ("select COUNT(user_name) from Users where user_name= %s")
        param = [Username]
        cursor.execute(query, param)
        qResult = cursor.fetchall()
        status = ""
        if qResult[0][0] > 0:
            print("Username Taken")
            status = "UT"

        query2 = ("select COUNT(summoner_name) from Users where summoner_name= %s")
        param2 = [SummonerName]
        cursor.execute(query2, param2)

        qResult2 = cursor.fetchall()
        print(qResult2[0][0])
        if qResult2[0][0] > 0:
            status = "ST"

        # if both pass, register user
        else:
            # print("Registration Valid")
            hashed = PasswordSetup.create_password(self, Password)

            mmr_query = ("SELECT mmr from Ranks where rank= %s")
            mmr_param = [_rank_string]
            cursor.execute(mmr_query, mmr_param)
            _mmr = cursor.fetchall()[0]

            # add icon http://ddragon.leagueoflegends.com/cdn/10.7.1/img/profileicon/588.png
            r_query = ("INSERT INTO users (summoner_name, user_name, password, rank, mmr, primary_role, account_id, player_icon) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)")
            r_values = (SummonerName, Username, hashed, _rank_string, _mmr, role, _account_id, _player_icon)

            cursor.execute(r_query, r_values)

            initial_query = ("Update users set wins = 0, losses = 0 where user_name = %s")
            initial_param = [Username]
            cursor.execute(initial_query, initial_param)
            connection.commit()

            status = "OK"
            print(request.json)

        return status
            
class CreateMatch(Resource):
    """
    Handles CRUD operations for creating matches.
    """     
    def post(self):
        """
        MATCH_TABLE
        _match_uuid
        _match_name
        _match_type
        _date
        _time
        _outcome
        _region ??
        _current_player
        _match_admin
        MATCH_PARTICIPANTS
        _match_uuid
        _match_name
        _player_name
        """
        _uuid = UUIDGenerator.generate_uuid(self) # Create UUID
        _match_name = request.json['match_name']
        _match_type = request.json['match_type']
        _date = request.json['date']
        _time = request.json['time']
        print(Outcome.PENDING.value)
        _outcome = str(Outcome.PENDING.value)
        _match_admin = request.json['player_name']

        cursor = connection.cursor() # Connect to DB
        query = ("INSERT into matches (match_uuid, match_name, match_type, date, time, admin, outcome) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        param = _uuid, _match_name, _match_type, _date, _time, _match_admin, _outcome
        cursor.execute(query, param)
        connection.commit()

        return request.json
    def get(self):
        cursor = connection.cursor()
        query = ("Select match_uuid, match_name, match_type, date, time, admin, outcome from matches")
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        result = {'games': [dict(zip(columns, row)) for row in cursor.fetchall()]}
        return result

class GetMatch(Resource):
    def get (self, _match_uuid):
        cursor = connection.cursor()
        query = ("Select match_uuid, match_name, match_type, date, time, admin, outcome from matches WHERE match_uuid =%s")
        query_param = [_match_uuid]
        cursor.execute(query, query_param)
        columns = [desc[0] for desc in cursor.description]
        result = {'games': [dict(zip(columns, row)) for row in cursor.fetchall()]}
        return result
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
        cursor = connection.cursor() # connect to the db
        query = ("select COUNT(user_name) from Users where user_name= %s")
        param = [username]
        cursor.execute(query,param)
        username_from_db = cursor.fetchall()

        if username_from_db[0][0] > 0:
            query2 = ("select password from Users where user_name= %s")
            cursor.execute(query2,param)
            hpw_from_db = cursor.fetchall()
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
        
        cursor = connection.cursor() # connect to the db
        query = ("select COUNT(user_name) from Users where user_name= %s")
        param = [username]
        cursor.execute(query,param)
        getResult = cursor.fetchall()
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
        # conn = db_connect.connect() # Connect to the Database
        cursor = connection.cursor()
        
        query = ("select summoner_name FROM Lobby order by mmr desc") # Get the Users from the Lobby
        cursor.execute(query)

        uuid = UUIDGenerator.generate_uuid(self) # Generate a Unique ID for the match.

        results = cursor.fetchall() # Get the players currently in the lobby.
        count = 0
        while matching_state:
            _summoner_name_1 = results[count][0]
            count+=1
            _summoner_name_2 = results[count][0]
            # conn.execute("insert into Match values")
            m_one_query = ("insert into Match values(%s, %s, %s)")
            m_one_values = (1, _summoner_name_1, uuid)
            cursor.execute(m_one_query, m_one_values)

            m_two_query = ("insert into Match values(%s, %s, %s)")
            m_two_values = (1, _summoner_name_2, uuid)
            cursor.execute(m_two_query, m_two_values)
            # conn.execute("insert into Match values('{0}', '{1}', '{2}')".format(2, _summoner_name_2, uuid))
            connection.commit()
            count +=1
            if(count == 10):
                matching_state = False
            # Sort the Match Table
            match_query = ("select team, summoner_name, uuid FROM Match order by team asc")
            cursor.execute(match_query)

        return {'match': [dict(zip(tuple(cursor.keys()), i)) for i in cursor]}

api.add_resource(Players, '/players')  # Route_1
api.add_resource(PlayerStandings, '/playerstandings')  # Route_2
api.add_resource(Lobby, '/lobby')  # Route_3
api.add_resource(UsersName, '/users/<username>')  # Route_4
api.add_resource(Users, '/users')  # Route_5
api.add_resource(SummonerName, '/s/<username>')  # Route_5
api.add_resource(Login, '/login')  # Route_6
api.add_resource(MatchMaking, '/mm')  # Route_7
api.add_resource(CreateMatch, '/create')  # Route_8
api.add_resource(GetMatch, '/getmatch/<_match_uuid>')  # Route_5

if __name__ == '__main__':
    app.run(port='5002')
