from riotwatcher import RiotWatcher, ApiError
from player import Player
from team import Team
from numpy import allclose
import numpy as np
import utils as u
import json

watcher = RiotWatcher('RGAPI-821dbdd5-5f6e-4657-a8c0-d1148340a94c')

QUEUE_TYPE = 'RANKED_SOLO_5x5'
players = ['Yupouvit', 'Tommy Shlug', 'Afferent', 'FUBW Gilgamesh', 'Globhopper', 'MacCionaodha', 'BigDaddyHoulihan', 'ChaonesJ', 'VVickedZ', 'FUBW Archer']
mmr = {'PLATINUM3': 1990, 'DIAMOND1': 2840, 'PLATINUM1': 2130, 'GOLD2': 1710, 'BRONZE3': 940, 'SILVER3': 1290, 'GOLD4': 1570, 'DIAMOND4': 2270, 'SILVER2': 1360, 'GOLD3': 1640, 'PLATINUM4': 1920, 'GOLD1': 1780, 'SILVER1': 1430, 'DIAMOND3': 2340}
my_region = 'euw1'

registered = []
teamObject = []

rankStr = ''

team1 = []
team2 = []
tmpPlayers = []
mmrArray = []

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

class Summoner():
    def getPlayerDetails(self):
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

def sortSummoners():
    for x in range(len(players)):
        print("--------------")
        count = 0
        playerDetails = watcher.summoner.by_name(my_region, players[x])
        summonerData  = watcher.league.by_summoner(my_region, playerDetails['id'])

        if(summonerData[count]['queueType'] == QUEUE_TYPE):
            rank = summonerData[count]['rank']
            rankToInt = u.romanToInt(rank)
            rankStr = summonerData[count]['tier'] + str(rankToInt)
        else:
            while (summonerData[count]['queueType'] != QUEUE_TYPE):
                count+=1
                if(summonerData[count]['queueType'] == QUEUE_TYPE):
                    rank = summonerData[count]['rank']
                    rankToInt = roman_to_int(rank)
                    rankStr = summonerData[count]['tier'] + str(rankToInt)
                    count = 0
                    break
        count = 0      
        print("Count: {count}".format(count=count))

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

# This function returns the difference in MMR beween two players
def getDifference(player1, player2):
    diff = 0
    if(player1 >= player2):
        diff = abs(player1 - player2)
    if(player2 >= player1):
        diff = abs(player2 - player1)
    return diff

# https://stackoverflow.com/questions/13602170/how-do-i-find-the-difference-between-two-values-without-knowing-which-is-larger
def buildArrays(p):
    tmpDiff = []

    for x in range(0, len(p), 1):
        tmpPlayers.append(p[x])
        mmrArray.append(tmpPlayers[x].getMMR())
        if(x != 0):
            tmpDiff.append(abs(mmrArray[x-1] - mmrArray[x]))

    print(tmpDiff)
    

    with open('ranked.json', 'w') as json_file:
        json.dump(mmrArray, json_file, sort_keys=True, indent=2)

def matchMaking():
    matching = True
    unmatched = registered[:]
    mmrCopy = mmrArray[:]
    unmatchedPlayers = len(unmatched)
    mmrCopyLength = len(mmrCopy)
    toMatch = 1
    while matching:
        
        currentPlayer = unmatched[unmatchedPlayers-1]

        player1 = currentPlayer.getSummonerName()
        player2 = unmatched[toMatch-1].getSummonerName() 


        currDiff = getDifference(currentPlayer.getMMR(), unmatched[toMatch-1].getMMR())
        print("Difference between Player {player1} and {player2} is {diff}".format(player1=player1, player2=player2, diff=currDiff))

        if(player1 != player2):
                # Delete from array so player cannot match with itselfs
                currIndex = unmatched.index(currentPlayer)
                tmpPlayer = currentPlayer
                mmrCopy.pop(currIndex)
                #Find the best match
                bestMatch = mmrCopy[np.abs(np.array(mmrCopy) - currentPlayer.getMMR()).argmin()]
                print("Best Match : {match}".format(match=bestMatch))
                #find the index of the best match in the mmrArray
                newIndex = mmrCopy.index(bestMatch)
                print("Index of Best Match in MMR ARRAY: {index}".format(index=newIndex))
                #find the index of the best match in the players array
                getPlayer = unmatched[newIndex].getSummonerName()
                print("Index of Best Match in Player ARRAY: {index}".format(index=getPlayer))
                #find the index of the best match in the unmatched array
                indexUnmatched = 0
                for j in range(0, len(unmatched), 1):
                    if(getPlayer == unmatched[j].getSummonerName()):
                        indexUnmatched = j
                        break
                print("Index of Best Match in Unmatched Array: {index}".format(index=indexUnmatched))
                #remove best match from unmatched array
                #append both players to teams
                team1.append(currentPlayer.getSummonerName())
                print("Team 2 Pending : {pending}".format(pending=unmatched[indexUnmatched].getSummonerName()))
                team2.append(unmatched[indexUnmatched].getSummonerName())
                unmatched.pop(currIndex)
                unmatched.pop(indexUnmatched)
                mmrCopy.pop(newIndex)
                unmatchedPlayers-=2
                mmrCopyLength-=1
                
        for a in range(len(team1)):
            print("Team 1: [{team}]".format(team=team1[a]))

        for b in range(len(team2)):
            print("Team 2: [{team}]".format(team=team2[b]))

        if(player1 == player2):
            if(len(team1) > len(team2)):
                team2.append(currentPlayer)
                toMatch+=1
            else:
                team1.append(currentPlayer)
                toMatch+=1
        #End Matching
        if(unmatchedPlayers == 0):
            matching = False

        print("Unmatched Players {unmatched}.".format(unmatched=unmatchedPlayers))
  


# https://en.m.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm

# buildArrays(registered)
# matchMaking()

for a in range(len(team1)):
    # t = Team(1, team1[a].getSummonerName(), team1[a].getRank(), team1[a].getMMR())
    # teamObject.append(t)
    print("Team 1: [{team}]".format(team=team1[a]))

for b in range(len(team2)):
    # t2 = Team(2, team2[b].getSummonerName(), team2[b].getRank(), team2[b].getMMR())
    # teamObject.append(t2)
    print("Team 2: [{team}]".format(team=team2[b]))

with open('teams.json', 'w') as json_file:
    json.dump(team1, json_file, sort_keys=True, indent=2)

with open('teams.json', 'w') as json_file:
    json.dump(team2, json_file, sort_keys=True, indent=2)

# try:
#     response = watcher.summoner.by_name(my_region, 'this_is_probably_not_anyones_summoner_name')
# except ApiError as err:
#     if err.response.status_code == 429:
#         print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
#         print('this retry-after is handled by default by the RiotWatcher library')
#         print('future requests wait until the retry-after time passes')
#     elif err.response.status_code == 404:
#         print('Summoner with that ridiculous name not found.')
#     else:
#         raise