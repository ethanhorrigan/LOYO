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

export class Games {
    /**
     *   _uuid = UUIDGenerator.generate_uuid(self) # Create UUID
        _match_name = request.json['match_name']
        _match_type = request.json['match_type']
        _date = request.json['date']
        _time = request.json['time']
        print(Outcome.PENDING.value)
        _outcome = str(Outcome.PENDING.value)
        _match_admin = request.json['player_name']
     */
    match_uuid: string;
    match_name: string;
    match_type: string;
    date: string; //possible change to Date object?
    time: string; //possible change to Date object?
    outcome: string;
    admin: string;
}

export interface GameResponse {
    games: Games[];
}

export class Participants {
    match_uuid: string;
    username: string;
    summoner_name: string;
    player_icon: string;
}

export interface NewParticipant {
    username: string;
    match_uuid: string;
}

export interface ParticipantsResponse {
    participants: Participants[];
}

export interface MatchResponse {
    match: Match[];
}
