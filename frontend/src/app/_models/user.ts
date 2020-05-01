
export class User {
    username: string;
    summonerName: string;
    password: string;
    role: string;
}

export class UserLogin {
    username: string;
    password: string;
}

// What data do i want to display on the user page?
//
export class UserProfile {
    username: string;
    summonerName: string;
    rank: string;
    wins: number;
    losses: number;
    playerIcon: number;
    poitns: number;

    // i also want to get the matches they are in.
    // should this be on a seperate query?
    // i can attempt to join both tables into one JSON object.
    matchName: string;
    
}

export class TempUser {
    summonerName: string;

    constructor(summonerName: string) {
        this.summonerName = summonerName;
    }
}
