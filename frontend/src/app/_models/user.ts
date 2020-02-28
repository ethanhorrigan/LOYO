
export class User {
    username: string;
    summonerName: string;
    password: string;
    role: string;
}

export class TempUser {
    summonerName: string;

    constructor(summonerName: string) {
        this.summonerName = summonerName;
    }
}
