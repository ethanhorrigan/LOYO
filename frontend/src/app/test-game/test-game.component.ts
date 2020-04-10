import { Component, OnInit } from '@angular/core';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-test-game',
  templateUrl: './test-game.component.html',
  styleUrls: ['./test-game.component.scss']
})
export class TestGameComponent implements OnInit {
  


  constructor(private userService: UserService) { 
  }

  ngOnInit() {
  }

  date: Date = new Date();
  today = this.date.getDate() + '/' + (this.date.getMonth() + 1) + '/' + this.date.getFullYear();

  /**
   * Retrieve all current games.
   */

  addToLobby() {
    //let tempUser: TempUser;
    this.userService.getGames()
      .subscribe(data => {
        console.log(data);
        location.reload();
      });

  }
}
