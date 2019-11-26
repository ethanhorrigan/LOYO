# Player.
class Player:
    
    # Method to create object (Constructor)
    def __init__(self, summonerName, rank, mmr, position):
         
        self.summonerName= summonerName
        self.rank = rank
        self.mmr = mmr
        self.position = position

    def getSummonerName(self):        
        return self.summonerName

    def setSummonerName(self, name):
        self.summonerName = name
     
    def getRank(self):        
        return self.rank
    
    def setRank(self, rank):
        self.rank = rank

    def getMMR(self):
        return self.mmr

    def setMMR(self, mmr):
        self.mmr = mmr

    def getPosition(self):
        return self.position
    
    def setPosition(self, position):
        self.position = position

    def __str__(self):
        return 'Player(name='+self.summonerName+', rank='+self.rank+', mmr='+str(self.mmr)+' )'    