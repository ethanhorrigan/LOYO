import { Component, OnInit } from '@angular/core';
import { UserService } from '../_services/user.service';
import { TempUser } from '../_models';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-games',
  templateUrl: './games.component.html',
  styleUrls: ['./games.component.scss']
})
export class GamesComponent implements OnInit {

  constructor(private userService: UserService) { }

  async ngOnInit() {
    //parseInt(JSON.stringify(this.getPlayers()));
    await this.getPlayers();
  }


  today = new Date();
  time = this.today.getHours() + ":" + this.today.getMinutes() + ":" + this.today.getSeconds();

  timeTillGame = 19.00 - this.today.getHours()
  registeredPlayers: any;

  getPlayers() {
    this.userService.getLobby().pipe(first()).subscribe(data => { 
      this.registeredPlayers = data;
      JSON.stringify(this.registeredPlayers);
    });
  }

  addToLobby() {
    let tempUser = new TempUser("Yupouvit");
    this.userService.addToLobby(tempUser)
      .pipe(first())
      .subscribe(
        data => {
          console.log(data);
          location.reload();
        });
    // this.userService.addToLobby("PadraigL99");
    // this.userService.addToLobby("Communism");
    // this.userService.addToLobby("Tommy Shlug");
    // this.userService.addToLobby("Thrasius123");
    // this.userService.addToLobby("Afferent");
    // this.userService.addToLobby("ChaonesJ");
    // this.userService.addToLobby("BigDaddyHoulihan");
    // this.userService.addToLobby("VVickedz");
    // this.userService.addToLobby("FUBW Gilgamesh");
  }
}
