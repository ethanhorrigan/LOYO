from itertools import combinations
import random
from riotwatcher import RiotWatcher, ApiError


def calc_mmr(summoners):
    total = 0
    for s in summoners:
        total = total + s.mmr
    return total / len(summoners)

def check_overlap(team1, team2):
    for player1 in team1.player_list:
        for player2 in team2.player_list:
            if player1 == player2:
                return True
    return False

class Summoners:
    def __init__(self, player_name, mmr):
        self.player_name = player_name
        self.mmr = mmr

class Team:

    def __init__(self, player1, player2, player3, player4, player5):
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.player5 = player5
        self.mmr = self.calculate_mmr()
        self.player_list = [self.player1, self.player2, self.player3, self.player4, self.player5]

    def calculate_mmr(self):
        total = self.player1.mmr + self.player2.mmr + self.player3.mmr + self.player4.mmr + self.player5.mmr
        return total / 5

class Matchmake:
    def __init__(self, players):
        self.players = players
    
    def matchmake(self, players):
        summoners = players
        random.shuffle(summoners)
        avg_mmr = calc_mmr(summoners)
        teams = []

        possible = list(combinations(summoners, 5))

        for p in possible:
            # print(p[0].mmr)
            teams.append(Team(p[0], p[1], p[2], p[3], p[4]))
        
        best = 10000
        team1 = None

        for team in teams:
            
            if abs(team.mmr - avg_mmr) < best:
                print(team.mmr)
                team1 = team
                best = abs(team.mmr - avg_mmr)
        teams.remove(team1)

        best = 10000
        team2 = None
        for current_team in teams:
            if abs(team.mmr - avg_mmr) < best:
                if check_overlap(current_team, team1):
                    continue
                else:
                    team2 = current_team
                    best = abs(current_team.mmr - avg_mmr)

        # print(team2.player1.player_name)
        # print(team2)
        teams = team1, team2
        return teams
