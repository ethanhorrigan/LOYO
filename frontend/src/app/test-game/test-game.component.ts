import { Component, OnInit } from '@angular/core';
import { UserService } from '../_services/user.service';
import { Games, GameResponse } from '../_models/team';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-test-game',
  templateUrl: './test-game.component.html',
  styleUrls: ['./test-game.component.scss']
})
export class TestGameComponent implements OnInit {
  
  public game: Games[];

  constructor(
    private userService: UserService,
    private http: HttpClient
    ) { 
  }

  ngOnInit() {
    this.getGames();
  }

  date: Date = new Date();
  today = this.date.getDate() + '/' + (this.date.getMonth() + 1) + '/' + this.date.getFullYear();

  /**
   * Retrieve all current games.
   */
  getGames() {
    this.http.get<GameResponse>("https://limitless-fjord-64117.herokuapp.com/create").subscribe(data => {
      this.game = data.games;
      console.log(this.game[0].match_name);
      console.log(this.game);
    });
  }

}
