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
    match_uuid: string;
    match_name: string;
    match_type: string;
    date: string; //possible change to Date object?
    time: string; //possible change to Date object?
    outcome: string;
    admin: string;

    constructor(match_name, match_type, date, time, admin) {
        this.match_name = match_name;
        this.match_type = match_type;
        this.date = date;
        this.time = time;
        this.admin = admin;
    }
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

export class FinalMatch {
    match_uuid: string;
    team1: string[];
    team2: string[];
}

export interface ParticipantsResponse {
    participants: Participants[];
}

export interface MatchResponse {
    match: Match[];
}

export interface FinalMatchResponse {
    final_match: FinalMatch[];
}
