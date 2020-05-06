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
import src.utils.constants as constants
from src.matchmaking.elo import Elo
from src.matchmaking.matchmake import Summoners, Matchmake
import src.rating.rating as r

app = Flask(__name__)
api = Api(app)

watcher = RiotWatcher(constants.RIOT_API_KEY)

QUEUE_TYPE = 'RANKED_SOLO_5x5'
my_region = 'euw1'


CORS(app) # To solve the CORS issue when making HTTP Requests

try:

    connection = psycopg2.connect(user=constants.USER, password=constants.DB_PASSWORD, host=constants.HOST, port=constants.PORT, database=constants.DATABASE)


    # connection = psycopg2.connect(user = "postgres", password = "horrigan902", host = "127.0.0.1", port ="5432", database = "loyo_db")
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    # print(connection.get_dsn_parameteres())
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")
    
    
except (Exception, psycopg2.Error) as error:
    print ("Error while connecting to PostgreSQL", error)


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
        return player_details['id']
    def get_player_icon(self):
        """Gets the player icon id from Riots API

        Returns:
            int -- player icon id
        """        
        player_icon = watcher.summoner.by_name(my_region, self)
        return player_icon['profileIconId']

    def get_lastest_game_id(self):
        account_id = Summoner.get_account_id(self)
        match_id = watcher.match.matchlist_by_account(my_region, account_id)
        return match_id['matches'][0]['gameId']
    
    def get_total_games(self):
        account_id = Summoner.get_account_id(self)
        wins = watcher.league.by_summoner(my_region, account_id)
        total_games = wins[0]['wins'] + wins[0]['losses']
        return total_games

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
        # query = conn.execute("select summonerName, rank, tier, wins, losses, primaryRole, secondaryRole from players")
        # result = {'players': [dict(zip(tuple(query.keys()), i))
        #                       for i in query.cursor]}
        # return result
        pass


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

        cursor.execute("SELECT summoner_name, user_name, rank, mmr, wins, losses, primary_role, player_icon, points FROM users ORDER BY points DESC")
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

class UpdateUser(Resource):
    def patch(self, _username):
        cursor = connection.cursor()
        response = 'not added'
        summoner_q = constants.GET_SUMMONER_NAME
        summoner_p = [_username]
        cursor.execute(summoner_q, summoner_p)
        _summoner_name = cursor.fetchall()[0][0]


        _account_id = Summoner.get_account_id(_summoner_name)
        _rank = Summoner.get_rank_string(self, _summoner_name)
        _total_games = Summoner.get_total_games(_summoner_name)
        print(_rank)
        mq = constants.MMR_QUERY
        mp = [_rank]
        cursor.execute(mq, mp)
        _mmr = cursor.fetchall()[0][0]
        _mmr = _mmr + abs(r.calculate_growth_rate(_mmr, _total_games))
        _player_icon = Summoner.get_player_icon(_summoner_name)
        _total_games = Summoner.get_total_games(_summoner_name)

        query1 = ("UPDATE users SET rank=%s, mmr=%s, player_icon=%s, total_games=%s, account_id=%s WHERE user_name=%s")
        param2 = [_rank, _mmr, _player_icon, _total_games, _account_id, _username]
        cursor.execute(query1, param2)
        print('RowCount:', cursor.rowcount)
        print('Param:', cursor.rowcount)
        response = 'added'

        connection.commit()
        cursor.close()
        return response
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
        _total_games = Summoner.get_total_games(SummonerName)

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
            r_query = ("INSERT INTO users (summoner_name, user_name, password, rank, mmr, primary_role, account_id, player_icon, total_games) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            r_values = (SummonerName, Username, hashed, _rank_string, _mmr, role, _account_id, _player_icon, _total_games)

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
        _outcome = 'PENDING'
        _match_admin = request.json['admin']

        cursor = connection.cursor() # Connect to DB
        query = ("INSERT into matches (match_uuid, match_name, match_type, date, time, admin, outcome) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        param = _uuid, _match_name, _match_type, _date, _time, _match_admin, _outcome
        cursor.execute(query, param)
        connection.commit()

        return request.json
    def get(self):
        cursor = connection.cursor()
        query = ("Select match_uuid, match_name, match_type, date, time, admin, outcome from matches order by date asc")
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

class GetParticipants(Resource):
    def get(self, _match_id):
        cursor = connection.cursor()
        p_query = ("Select match_uuid, username, summoner_name, player_icon from participants where match_uuid=%s")
        p_param = [_match_id]
        cursor.execute(p_query, p_param)
        columns = [desc[0] for desc in cursor.description]
        result = {'participants': [dict(zip(columns, row)) for row in cursor.fetchall()]}
        return result

class GetParticipantCount(Resource):
    def get(self, _match_uuid):
        cursor = connection.cursor()
        query = ("Select COUNT(summoner_name) from participants where match_uuid=%s ")
        param = [_match_uuid]
        cursor.execute(query, param)

        qResult = cursor.fetchall()
        connection.commit()
        print(qResult[0][0])
        return qResult[0][0]

class AddToMatch(Resource):
    def post(self):
        _username = request.json['username']
        _match_uuid = request.json['match_uuid']

        cursor = connection.cursor()
        user_query = ("SELECT summoner_name, player_icon, mmr from users where user_name=%s")
        user_param = [_username]

        cursor.execute(user_query, user_param)
        result = cursor.fetchall()
        _summoner_name = result[0][0]
        _player_icon = result[0][1]
        _mmr = result[0][2]

        # # check the participant db first before inserting
        check_query=("SELECT COUNT(summoner_name) FROM participants where summoner_name=%s AND match_uuid=%s")
        check_param=[_summoner_name, _match_uuid]
        cursor.execute(check_query, check_param)
        check_result = cursor.fetchall()
        print(check_result[0][0])

        if check_result[0][0] == 0:
            p_query = ("insert into participants values(%s, %s, %s, %s, %s)")
            p_param = (_match_uuid, _username, _summoner_name, _player_icon, _mmr)
            cursor.execute(p_query, p_param)
            connection.commit()
        # Get user details
        return 'Added'
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

class PlayerAdmin(Resource):
    def get(self, match_id):
        admin = False
        cursor = connection.cursor()
        try:
            query = (constants.ADMIN_QUERY)
            param = [match_id]
            cursor.execute(query, param)
            response = cursor.fetchall()[0][0]
        except psycopg2.Error as error:
            print('Error getting data: PlayerAdmin')
        finally:
            cursor.close()
        return response

class MyUpcomingGames(Resource):
    def get(self, username):
        result = None
        game_list = []
        columns = []
        cursor = connection.cursor()
        try:
            query = (constants.GET_MATCH_IDS)
            param = [username]
            cursor.execute(query, param)
            result = cursor.fetchall()
            count = 0
            for id in result:
                mid = result[count][0]
                query = (constants.GET_MATCH)
                param = [mid]
                cursor.execute(query, param)
                game_list.append(cursor.fetchall()[0])
                # columns.append([desc[0] for desc in cursor.description])
                count += 1
        except psycopg2.Error as error:
            print('Error getting data: Upcoming Games')
        finally:
            connection.commit()
            cursor.close()
        return game_list 
class MatchStatus(Resource):
    def get(self, match_id):
        result = None
        cursor = connection.cursor()
        try:
            query = (constants.GET_MATCH_STATUS)
            param = [match_id]
            cursor.execute(query, param);
            result = cursor.fetchall()[0][0]
        except psycopg2.Error as error:
            result = 'error getting match status..'
        finally:
            connection.commit()
            cursor.close()

        return result
class Finalmatch(Resource):
    def post(self):
        response = None
        _match_uuid = request.json['match_uuid']
        _winning_team = request.json['winning_team']
        _losing_team = request.json['losing_team']
        print(_match_uuid)
        print(_winning_team)
        print(_losing_team)

        team1_index = 1
        team2_index = 2

        _outcome = 'FINISHED'

        cursor = connection.cursor()
        try:
            # set the match to finished
            query = (constants.CLOSE_MATCH)
            param = [_outcome, _match_uuid]
            cursor.execute(query, param)

            query = (constants.UPDATE_TEAM)
            param = [_winning_team, _losing_team, _match_uuid]
            cursor.execute(query, param)

            query2 = (constants.WINNING_TEAM)
            param2 = [_match_uuid]
            cursor.execute(query2, param2)
            result = cursor.fetchall()[0][int(_winning_team.replace('team',''))]
            print(len(result))

            print(result)
            for name in result:
                query = (constants.UPDATE_OUTCOME)
                param = [1, name, _match_uuid]
                cursor.execute(query, param)
                print(name)
            
            queryL = (constants.WINNING_TEAM)
            paramL = [_match_uuid]
            cursor.execute(queryL, paramL)
            result = cursor.fetchall()[0][int(_losing_team.replace('team', ''))]
            print(len(result))

            for name in result:
                query = (constants.UPDATE_OUTCOME)
                param = [0, name, _match_uuid]
                cursor.execute(query, param)
                print(name)
                
            UpdateRating.post(self, _match_uuid)
            #print(result[0][0][1])
            response = constants.SUCCESS
        except psycopg2.Error as identifier:
            response = '400: Bad Request'
        finally:
            connection.commit()
            cursor.close()
        return response

class UpdateRating(Resource):
    def post(self, _match_uuid):
        cursor = connection.cursor()
        # get the participants that won and their mmr.
        # get the participants that lost and their mmr.


        # Querying with multiple where conditions and multiple columns

        win_query = ("select username, mmr, outcome from participants where outcome=1 and match_uuid=%s")
        win_param = [_match_uuid]
        cursor.execute(win_query, win_param)
        result = (cursor.fetchall())

        lose_query = ("select username, mmr, outcome from participants where outcome=0 and match_uuid=%s")
        lose_param = [_match_uuid]
        cursor.execute(lose_query, lose_param)
        result_loss = (cursor.fetchall())

        count = len(result)
        l_count = len(result_loss)

        mmr_list = []
        loss_mmr_list = []
        # fill up average mmr list
        for i in range(count):
            _name = result[i][0]
            _mmr = result[i][1]
            mmr_list.append(_mmr)
        
        for j in range(l_count):
            _name = result_loss[j][0]
            _mmr = result_loss[j][1]
            loss_mmr_list.append(_mmr)


        print('Winner Avg MMR:', r.get_average_mmr(mmr_list))
        print('Loser Avg MMR:', r.get_average_mmr(loss_mmr_list))

        winner_rating = r.get_average_mmr(mmr_list)
        loser_rating = r.get_average_mmr(loss_mmr_list)

        e = Elo(winner_rating, loser_rating, 5, 0)
        _points = e.update_points()
        
        
        # lose_query = ("select wins from users where user_name=%s")
        # lose_param = [_match_uuid]
        # cursor.execute(lose_query, lose_param)
        # result_loss = (cursor.fetchall())
        for i in range(count):
            # Select the wins for the player so we can update their wins.
            wa_query = ("select wins, points from users where user_name=%s")
            wa_param = [result[i][0]]
            cursor.execute(wa_query, wa_param)
            wa = (cursor.fetchall())
            wins = wa[0][0] + 1
            total_points = wa[0][1] + _points
            update_query = ("update users set points=%s, wins=%s where user_name=%s")
            update_param = [total_points, wins, result[i][0]]
            cursor.execute(update_query, update_param)
        
        # update user loss
        for i in range(l_count):
            loss_query = ("select losses from users where user_name=%s")
            loss_param = [result_loss[i][0]]
            cursor.execute(loss_query, loss_param)
            loss_count = (cursor.fetchall())
            losses = loss_count[0][0] + 1
            lq = ("update users set losses=%s where user_name=%s")
            lp = [losses, result_loss[i][0]]
            cursor.execute(lq, lp)
        connection.commit()

        return result
class MM2(Resource):
    def get(self, match_id):
        players = []
        cursor = connection.cursor()
        p_query = ("SELECT summoner_name, mmr from participants where match_uuid=%s order by mmr desc")
        p_param = [match_id]
        cursor.execute(p_query, p_param)
        response = cursor.fetchall()
        for player in response:
            ply = Summoners(player[0], player[1])
            players.append(ply)
        # print(players[0].player_name)
        teams = Matchmake.matchmake(self, players)
        print(teams[0].player1.player_name)
        print(teams[0].player2.player_name)
        print(teams[0].player3.player_name)
        print(teams[0].player4.player_name)
        print(teams[0].player5.player_name)
        print(teams[0].mmr)
        print('vs')
        print(teams[1].player1.player_name)
        print(teams[1].player2.player_name)
        print(teams[1].player3.player_name)
        print(teams[1].player4.player_name)
        print(teams[1].player5.player_name)
        print(teams[1].mmr)
        return response
class MatchMaking(Resource):
    def get(self, _match_uuid):
        """
        Handles the matchmaking process.
        Set the matching_state to true while there is still users in the lobby.
        Generate a Universally unique identifier for each match created to
        distinguish between matches.
        Insert players into their respective teams.

        Returns:
        Match ready teams.
        """    


        # Param Variables
        # _match_uuid = request.json['match_uuid']
        matching_state = True # Set matching state to true
        # conn = db_connect.connect() # Connect to the Database
        team_1 = []
        team_2 = []
        cursor = connection.cursor()
        
        query = (constants.GET_MATCH_STATUS)
        param = [_match_uuid]
        cursor.execute(query, param)
        mcount = cursor.fetchall()
        print(mcount[0][0])

        p_query = ("SELECT summoner_name from participants where match_uuid=%s order by mmr desc")
        p_param = [_match_uuid]
        cursor.execute(p_query, p_param)

        results = cursor.fetchall() # Get the players currently in the lobby.
        count = 0
        if(mcount[0][0] == 'PENDING'):
            while matching_state:
                _summoner_name_1 = results[count][0]
                count+=1
                _summoner_name_2 = results[count][0]
                # conn.execute("insert into Match values")
                team_1.append(_summoner_name_1)
                team_2.append(_summoner_name_2)
                # m_one_query = ("insert into final_match values(%s, %s, %s)")
                # m_one_values = (_match_uuid, _summoner_name_1, uuid)
                # cursor.execute(m_one_query, m_one_values)

                # m_two_query = ("insert into Match values(%s, %s, %s)")
                # m_two_values = (1, _summoner_name_2, uuid)
                # cursor.execute(m_two_query, m_two_values)
                # conn.execute("insert into Match values('{0}', '{1}', '{2}')".format(2, _summoner_name_2, uuid))
                # connection.commit()
                count +=1
                if(count == 10):
                    fm_query = ("INSERT into final_match values(%s, %s, %s)")
                    fm_param = [_match_uuid, team_1, team_2]
                    cursor.execute(fm_query, fm_param)
                    query = (constants.CLOSE_MATCH)
                    param = ['ONGOING', _match_uuid]
                    cursor.execute(query, param)
                    matching_state = False
            
            # Sort the Match Table
        match_query = ("select match_uuid, team1, team2 FROM final_match where match_uuid=%s")
        match_param = [_match_uuid]
        cursor.execute(match_query, match_param)
        connection.commit()
        columns = [desc[0] for desc in cursor.description]
        result = {'final_match': [dict(zip(columns, row)) for row in cursor.fetchall()]}
        return result

api.add_resource(Players, '/players')  # Route_1
api.add_resource(PlayerStandings, '/playerstandings')  # Route_2
api.add_resource(Lobby, '/lobby')  # Route_3
api.add_resource(UsersName, '/users/<username>')  # Route_4
api.add_resource(Users, '/users')  # Route_5
api.add_resource(UpdateUser, '/users/<_username>')  # Route_5
api.add_resource(SummonerName, '/s/<username>')  # Route_5
api.add_resource(Login, '/login')  # Route_6
api.add_resource(MatchMaking, '/mm/<_match_uuid>')  # Route_7
api.add_resource(CreateMatch, '/create')  # Route_8
api.add_resource(GetMatch, '/getmatch/<_match_uuid>')  # Route_5
api.add_resource(AddToMatch, '/addtomatch')  # Route_8
api.add_resource(GetParticipants, '/getparticipants/<_match_id>')
api.add_resource(GetParticipantCount, '/getparticipantcount/<_match_uuid>')
api.add_resource(UpdateRating, '/updatescore/<_match_uuid>')
api.add_resource(PlayerAdmin, '/admin/<match_id>')
api.add_resource(MatchStatus, '/matchstatus/<match_id>')
api.add_resource(Finalmatch, '/finalmatch')
api.add_resource(MyUpcomingGames, '/mygames/<username>')
api.add_resource(MM2, '/mm2/<match_id>')


if __name__ == '__main__':
    app.run(port='5002')
