from riotwatcher import RiotWatcher, ApiError
import json

watcher = RiotWatcher('RGAPI-e350fdee-f812-4982-a0f8-d8a91dfde6e3')

players = ['Horro', 'Obi Sean Kenobi', 'Zethose', 'PadraigL99', 'Tommy Shlug', 'Farrago Jerry', 'Communism', 'MacCionaodha', 'BigDaddyHoulihan', 'BigHaus']
my_region = 'euw1'


# playerDetails = watcher.summoner.by_name(my_region, 'horro')
# print(playerDetails)

# all objects are returned (by default) as a dict
# lets see if I got diamond yet (I probably didn't)

# Convert Roman Numerals to INT
def roman_to_int(s):
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    int_val = 0
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]
    return int_val

for x in range(len(players)):
    playerDetails = watcher.summoner.by_name(my_region, players[x])
    summonerData  = watcher.league.by_summoner(my_region, playerDetails['id'])
    rank = summonerData[1]['rank']
    rankToInt = roman_to_int(rank)
    print("{name} is {tier} {rank}".format(name=playerDetails['name'], tier=summonerData[1]['tier'], rank=rankToInt))



# print("{name} is a level {level} summoner on the {region} server, current rank: {rank}".format(name=summoner.name,
#                                                                           level=summoner.level,
#                                                                           region=summoner.region, rank=summoner.rank_last_season))

# print(json.dumps(summonerData, indent=2))

summonerData = json.dumps(summonerData)



with open('ranked.json', 'w') as json_file:
    json.dump(summonerData, json_file, sort_keys=True, indent=2)
# Lets get some champions


# For Riot's API, the 404 status code indicates that the requested data wasn't found and
# should be expected to occur in normal operation, as in the case of a an
# invalid summoner name, match ID, etc.
#
# The 429 status code indicates that the user has sent too many requests
# in a given amount of time ("rate limiting").

try:
    response = watcher.summoner.by_name(my_region, 'this_is_probably_not_anyones_summoner_name')
except ApiError as err:
    if err.response.status_code == 429:
        print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
        print('this retry-after is handled by default by the RiotWatcher library')
        print('future requests wait until the retry-after time passes')
    elif err.response.status_code == 404:
        print('Summoner with that ridiculous name not found.')
    else:
        raise