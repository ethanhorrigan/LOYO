import { Component, OnInit } from '@angular/core';
import { first, delay } from 'rxjs/operators';
import { UserService } from '../_services/user.service';
import { TempUser } from '../_models';

@Component({
  selector: 'app-games',
  templateUrl: './games.component.html',
  styleUrls: ['./games.component.scss']
})
export class GamesComponent implements OnInit {

  constructor(private userService: UserService) { }

  async ngOnInit() {
    this.getPlayers();
  }
  
  // test variables
  players: string[] = ['Yupouvit', 'Communism', 'Tommy Shlug', 'Thraius123', 'Afferent', 'ChaonesJ', 'BigDaddyHoulihan', 'VVickedz', 'FUBW Gilgamesh', 'FUBW Archer'];
  // end of test variables

  today = new Date();
  show = false;
  time = this.today.getHours() + ":" + this.today.getMinutes() + ":" + this.today.getSeconds();

  timeTillGame = 19.00 - this.today.getHours()
  registeredPlayers: any;

  getPlayers() {
    this.userService.getLobby().pipe(first()).subscribe(data => {
      this.registeredPlayers = data;
      JSON.stringify(this.registeredPlayers);
      console.log(JSON.stringify(this.registeredPlayers));
    });
    this.allowPlayersJoin();
  }

  allowPlayersJoin() {
    console.log((this.registeredPlayers));
    if (Number(this.registeredPlayers == 2)) {
    }
  }

  print(string: any) {
    console.log(string);
  }

  async addToLobby() {
    let tempUser: TempUser;
    for (var i = 0; i < this.players.length; i++) {
      tempUser = new TempUser(this.players[i]);
      this.userService.addToLobby(tempUser)
        .pipe(delay(5000))
        .subscribe(async (data) => {
          console.log(data);
          location.reload();
        });
    }
  }
}
