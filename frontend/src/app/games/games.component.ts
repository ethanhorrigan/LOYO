import { Component, OnInit } from '@angular/core';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-games',
  templateUrl: './games.component.html',
  styleUrls: ['./games.component.scss']
})
export class GamesComponent implements OnInit {

  constructor(private userService: UserService) { }

  ngOnInit() {
  }


  today = new Date();
  time = this.today.getHours() + ":" + this.today.getMinutes() + ":" + this.today.getSeconds();

  timeTillGame = 19.00 - this.today.getHours()

  addToLobby() {
    console.log("Added to lobby")
    this.userService.addToLobby("Yupouvit");
  }
}
