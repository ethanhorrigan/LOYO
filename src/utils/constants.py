
"""
Deployment Database Credentials
"""
DATABASE = "d34bp9cpp983nn"
USER =  "cfrqbgcghvvkyw"
DB_PASSWORD = "553a3ddb1f43deb191cf1001d58ba5ce319d55f24e83ebad7c91f03fab8d90dd"
HOST = "ec2-35-168-54-239.compute-1.amazonaws.com"
PORT = "5432"

RIOT_API_KEY = 'RGAPI-5ac05e6e-8871-43d3-b4a0-dc16f6cacc5f'

ADMIN_QUERY = 'select admin from matches where match_uuid=%s'
GET_SUMMONER_NAME = 'select summoner_name from users where user_name=%s'
UPDATE_SUMMOMER = 'Update users set account_id=%s, rank=%s, mmr=%s, player_icon=%s, total_games=%s where user_name=%s'
MMR_QUERY = "select mmr from ranks where rank=%s"