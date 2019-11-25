from riotwatcher import RiotWatcher, ApiError
from player import Player
from numpy import allclose
import json

watcher = RiotWatcher('RGAPI-a10d0baa-5e83-44e1-a146-f38ea137a3b4')

QUEUE_TYPE = 'RANKED_SOLO_5x5'
players = ['Horro', 'Obi Sean Kenobi', 'Zethose', 'PadraigL99', 'Tommy Shlug', 'Farrago Jerry', 'Communism', 'MacCionaodha', 'BigDaddyHoulihan', 'BigHaus']
mmr = {'PLATINUM3': 1920, 'GOLD2': 1710, 'BRONZE3': 940, 'SILVER3': 1290, 'GOLD4': 1570, 'DIAMOND4': 2270, 'SILVER2': 1360, 'GOLD3': 1640}
my_region = 'euw1'

registered = []

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

# for x in range(len(registered)):
#     print(registered[x])


# https://stackoverflow.com/questions/13602170/how-do-i-find-the-difference-between-two-values-without-knowing-which-is-larger
def buildTeam(p):
    diff = 10000
    team1 = []
    team2 = []
    tmpPlayers = []
    mmrArray = []
    count = 0
    totalMMR = 0
    teamCount = 0
    running = 1

    for x in range(len(p)):
        tmpPlayers.append(p[x])
        mmrArray.append(tmpPlayers[x].getMMR())
        totalMMR += tmpPlayers[x].getMMR()

    mmrArray.sort()

    goalMMR = totalMMR / 2
    goalPlayer = goalMMR / 5
    print("TOTAL MMR: {total}, GOAL MMR: {goal}, GOAL PLAYER MMR: {p} ".format(total=totalMMR, goal=goalMMR, p=goalPlayer))

    m = mmrArray[:len(mmrArray)//2]
    w = mmrArray[len(mmrArray)//2:]
    print("m: {m}".format(m=m))
    print("w: {w}".format(w=w))
    print("mmr array : {a}".format(a=mmrArray))

    tc = 0
    for i in range(len(mmrArray)):
        if(tc == 0):
            team1.append(mmrArray[i])
        if(tc == 1):
            team2.append(mmrArray[i])
            tc = 0
        tc+=1

    print("team1: {t1}".format(t1=team1))

        # print(w[s].getMMR)

        # if(tmpPlayers[s].getMMR() == mmrArray[count]):
        #     team1.append(tmpPlayers[s])
        #     mmrArray.remove(mmrArray[count])
        #     teamCount+=1
        # else:
        #     count+=1
        #     team2.append(tmpPlayers[s])
        # teamCount+=1

        # if(teamCount == 10):
        #     break

    # for i in range(len(team1)):
    #     print("[TEAM 1] {name}".format(name=team1[i].getSummonerName()))

    # for j in range(len(team2)):
    #     print("[TEAM 2] {name}".format(name=team2[j].getSummonerName()))

# https://en.m.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm
is_stable = False
# while is_stable == False:
#         is_stable = True
#         for b in W:
#             is_paired = False # whether b has a pair which b ranks <= to n
#             for n in range(1, len(B) + 1):
#                 a = rankings[(b, n)]
#                 a_partner, a_n = partners[a]
#                 if a_partner == b:
#                     if is_paired:
#                         is_stable = False
#                         partners[a] = (rankings[(a, a_n + 1)], a_n + 1)
#                     else:
#                         is_paired = True

buildTeam(registered)

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