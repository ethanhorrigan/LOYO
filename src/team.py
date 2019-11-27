
class Team:
        # Method to create object (Constructor)
    def __init__(self, teamNumber, summonerName, rank, mmr):
        self.teamNumber = teamNumber
        self.summonerName= summonerName
        self.rank = rank
        self.mmr = mmr

    def getSummonerName(self):        
        return self.summonerName
    
    def getTeamNumber(self):
        return self.teamNumber
    
    def getRank(self):        
        return self.rank

    def getMMR(self):
        return self.mmr

    def __str__(self):
        return 'Team(teamNumber='+str(self.teamNumber)+', name='+self.summonerName+', rank='+self.rank+', mmr='+str(self.mmr)+' )'  