from riotwatcher import RiotWatcher, ApiError
from player.player import Player
import json

watcher = RiotWatcher('RGAPI-6758d4f4-e43a-44d2-9067-08759e83971d')

QUEUE_TYPE = 'RANKED_SOLO_5x5'
players = ['Horro', 'Obi Sean Kenobi', 'Zethose', 'PadraigL99', 'Tommy Shlug', 'Farrago Jerry', 'Communism', 'MacCionaodha', 'BigDaddyHoulihan', 'BigHaus']
mmr = {'PLATINUM3': 1920, 'GOLD2': 1710, 'BRONZE3': 940, 'SILVER3': 1290, 'GOLD4': 1570, 'DIAMOND4': 2270, 'SILVER2': 1360, 'GOLD3': 1640}
my_region = 'euw1'

registered = []

mmrJson = json.dumps(mmr)

with open('mmr.json', 'w') as json_file:
    json.dump(mmr, json_file, sort_keys=True, indent=2)

rankStr = ''


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

# horro = watcher.summoner.by_name(my_region, "Horro")
# roles = watcher.league.positions_by_summoner(my_region, horro['id'])


for x in range(len(players)):
    print("--------------")
    count = 0
    playerDetails = watcher.summoner.by_name(my_region, players[x])
    summonerData  = watcher.league.by_summoner(my_region, playerDetails['id'])

    if(summonerData[count]['queueType'] == QUEUE_TYPE):
        rank = summonerData[count]['rank']
        rankToInt = roman_to_int(rank)
        rankStr = summonerData[count]['tier'] + str(rankToInt)
        # print("{name} is {tier} {rank}".format(name=playerDetails['name'], tier=summonerData[count]['tier'], rank=rankToInt))
        # print(summonerData[count]['queueType'])
    else:
        while (summonerData[count]['queueType'] != QUEUE_TYPE):
            # print(count)
            count+=1
            if(summonerData[count]['queueType'] == QUEUE_TYPE):
                rank = summonerData[count]['rank']
                rankToInt = roman_to_int(rank)
                rankStr = summonerData[count]['tier'] + str(rankToInt)
                # print("{name} is {tier} {rank}".format(name=playerDetails['name'], tier=summonerData[count]['tier'], rank=rankToInt))
                # print(summonerData[count]['queueType'])
                count = 0
                break
        count = 0      

    # print(rankStr)
    # print("{name} is {tier} {rank}".format(name=playerDetails['name'], tier=summonerData[1]['tier'], rank=rankToInt))
    print("{name}'s ID = {id}".format(name=playerDetails['name'], id=playerDetails['id']))
    for key in mmr:
        if(key == rankStr):
            tmpMMR = mmr[key]
            # print("{name}'s MMR = {mmr}".format(name=playerDetails['name'], mmr=mmr[key]))

    p = Player(playerDetails['name'], rankStr, tmpMMR)
    registered.append(p)
    print(p.getSummonerName())
    print(p.getRank())
    print(p.getMMR())

for x in range(len(registered)):
    print(registered[x])

summonerData = json.dumps(summonerData)



with open('ranked.json', 'w') as json_file:
    json.dump(summonerData, json_file, sort_keys=True, indent=2)


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