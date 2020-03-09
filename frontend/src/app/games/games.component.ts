import { Component, OnInit } from '@angular/core';
import { first, delay } from 'rxjs/operators';
import { UserService } from '../_services/user.service';
import { TempUser } from '../_models';
import { Team, TeamResponse, Match, MatchResponse } from '../_models/team';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-games',
  templateUrl: './games.component.html',
  styleUrls: ['./games.component.scss']
})
export class GamesComponent implements OnInit {

    // test variables
    players: string[] = ['Yupouvit', 'Communism', 'Tommy Shlug', 'Thrasius123', 'Afferent', 'ChaonesJ', 'BigDaddyHoulihan', 'VVickedz', 'FUBW Gilgamesh', 'FUBW Archer'];
    url = ' http://127.0.0.1:5002/mm';
    // end of test variables
  
    // player variables
    _summonerName: string;
    _summonerRole: string;
    blueTeam: Team;
    redTeam: Team;
  
    today = new Date();
    show = false;
    time = this.today.getHours() + ":" + this.today.getMinutes() + ":" + this.today.getSeconds();
  
    timeTillGame = 19.00 - this.today.getHours()
    registeredPlayers: any;

    public match: Match[];

    
  constructor(
    private userService: UserService, 
    private http: HttpClient
    ){}

  async ngOnInit() {
    // Check the Lobby on page init
    // if lobby is full, begin matchmaking and return the teams.
    // if(this.getPlayers() == "FULL") {
    //   console.log("im in init");
    // }

     this.getMatch();
     console.log(this.getNumberOfGames(36));
     
  }
  

  getPlayers() {
    this.userService.getLobby().pipe(first()).subscribe(data => {
      this.registeredPlayers = data;
      JSON.stringify(this.registeredPlayers);
      console.log(JSON.stringify(this.registeredPlayers));
      
    });
    return this.registeredPlayers;
  }

  getBlueTeam() {

  }

  getRedTeam() {

  }
  getMatch() {
    this.http.get<MatchResponse>(this.url).subscribe(data => {
      this.match = data.match;
      console.log(this.match);
    });
    // this.userService.getMM().subscribe(data => {
    //   console.log(data);
    // });
  }

  /**
   * Returns the number of games depending on the amount of players in the lobby.
   * @param n The number of players in the lobby.
   */
  getNumberOfGames(n: number) {
    return Math.floor(n / 10) * 10 / 10;
  }

  /**
   * Adds the user to the Lobby "Queue".
   * Reload the page to update the lobby amount.
   */
  getName() {
    console.log(this.match[5].summonerName);
  }

  async addToLobby() {
    let tempUser: TempUser;
    for (var i = 0; i < this.players.length; i++) {
      tempUser = new TempUser(this.players[i]);
      this.userService.addToLobby(tempUser)
        .pipe(delay(10000))
        .subscribe(async (data) => {
          console.log(data);
          location.reload();
        });
    }
  }
}
