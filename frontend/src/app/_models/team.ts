export class Team {
    id: number;
    top: string;
    jungle: string;
    mid: string;
    adc: string;
    support: string;

    constructor(id, top, jungle, mid, adc, support) {
        this.id = id;
        this.top = top;
        this.jungle = jungle;
        this.mid = mid;
        this.adc = adc;
        this.support = support;
    }
}

export interface TeamResponse
{
    teams: Team[];
}

export class Match {
    teamID: number;
    matchID: number;
    summonerName: string;

    constructor(teamID, matchID, summonerName) {
        this.teamID = teamID;
        this.matchID = matchID;
        this.summonerName = summonerName;
    }
}

export interface MatchResponse
{
    match: Match[];
}