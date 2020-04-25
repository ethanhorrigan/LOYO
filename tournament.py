class Tournament():
    
    def __init__(self, t_id, t_name, t_type, teams):
        self.t_id = t_id
        self.t_name = t_name
        self.t_type = t_type
        self.teams = teams

    def build_bracket(self, teams):
        pass

    def print_bracket(self, bracket):
        pass


class Team():
    def __init__(self, team_name, team_mmr):
        self.team_name = team_name
        self.team_mmr = team_mmr

    def __repr__(self):
        return repr((self.team_name, self.team_mmr))

class Ranks():
    """
    bronze pref
    silver pref
    gold pref
    plat pref
    diamond pref
    """
    BRONZE = [100,200,300,400]
    SILVER = [500,600,700,800]
    GOLD = [900,1000,1100,1200]
    PLAT = [1300,1400,1500,1600]
    DIAMOND = [1700,1800,1900,2000]
    RANKS = [BRONZE, SILVER, GOLD, PLAT, DIAMOND]

class MatchMaking():
    """
    I need to sort array of teams by mmr values
    https://docs.python.org/3/howto/sorting.html
    """

    def __init__(self, players):
        self.players = players

    def build_preferences(self):
        player1_pref = [self.players.index(2), self.players.index(3)] # 0
        player2_pref = [self.players.index(3), self.players.index(1)] # 1
        player3_pref = [self.players.index(4), self.players.index(2)] # 2
        player4_pref = [self.players.index(3), self.players.index(5)] # 3
        player5_pref = [self.players.index(6), self.players.index(4)] # 4
        player6_pref = [self.players.index(7), self.players.index(5)] # 0
        player7_pref = [self.players.index(8), self.players.index(6)] # 1
        player8_pref = [self.players.index(9), self.players.index(7)] # 2
        player9_pref = [self.players.index(10), self.players.index(8)] # 3
        player10_pref = [self.players.index(9), self.players.index(8)] # 4
        pref = [
            player1_pref, 
            player2_pref, 
            player3_pref, 
            player4_pref, 
            player5_pref,
            player6_pref,
            player7_pref,
            player8_pref,
            player9_pref,
            player10_pref
        ]
        return pref


    def stableMatching(self):
        n = 10
        preferences = self.build_preferences()
        # womenPreferences = self.build_women_pref()
    # Initially, all n men are unmarried
        unmatched = list(range(n))
        # None of the men has a spouse yet, we denote this by the value None
        manSpouse = [None] * n                      
        # None of the women has a spouse yet, we denote this by the value None
        womanSpouse = [None] * n                      
        # Each man made 0 proposals, which means that 
        # his next proposal will be to the woman number 0 in his list
        nextManChoice = [0] * n                       
        
        # While there exists at least one unmarried man:
        while unmatched:
            # Pick an arbitrary unmarried man
            he = unmatched[0]                      
            # Store his ranking in this variable for convenience
            hisPreferences = preferences[he]    
            print("His preference ",hisPreferences)   
            # Find a woman to propose to
            she = hisPreferences[nextManChoice[he]] 
            # Store her ranking in this variable for convenience
            # herPreferences = womenPreferences[she]
            # Find the present husband of the selected woman (it might be None)
            currentHusband = womanSpouse[she]
            print("Current Husband: ",currentHusband)
            
            # Now "he" proposes to "she". 
            # Decide whether "she" accepts, and update the following fields
            # 1. manSpouse
            # 2. womanSpouse
            # 3. unmarriedMen
            # 4. nextManChoice
            if currentHusband == None:
                #No Husband case
                #"She" accepts any proposal
                womanSpouse[she] = he
                manSpouse[he] = she
                #"His" nextchoice is the next woman
                #in the hisPreferences list
                nextManChoice[he] = nextManChoice[he] + 1
                #Delete "him" from the 
                #Unmarried list
                unmatched.pop(0)
                print('Unmatched: ', unmatched)
            else:
                #Husband exists
                #Check the preferences of the 
                #current husband and that of the proposed man's
                currentIndex = preferences.index(currentHusband)
                hisIndex = preferences.index(he)
                #Accept the proposal if 
                #"he" has higher preference in the herPreference list
                if currentIndex > hisIndex:
                    #New stable match is found for "her"
                    womanSpouse[she] = he
                    manSpouse[he] = she
                    nextManChoice[he] = nextManChoice[he] + 1
                    #Pop the newly wed husband
                    unmatched.pop(0)
                    #Now the previous husband is unmarried add
                    #him to the unmarried list
                    unmatched.insert(0,currentHusband)
                else:
                    nextManChoice[he] = nextManChoice[he] + 1
        return manSpouse

test_teams = [
    Team('team1', 1200),
    Team('team2', 1800),
    Team('team3', 1500),
    Team('team4', 1100)
]

test_players = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
]

# test_teams = sorted(test_teams, key=lambda team: team.team_mmr)
# print(test_teams)
test_players.sort()
# print(test_players)
m = MatchMaking(test_players)

print(m.stableMatching())

# for team in test_teams:
#     print(team.team_mmr)
    