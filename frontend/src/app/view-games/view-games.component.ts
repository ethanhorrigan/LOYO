import { Component, OnInit } from '@angular/core';
import { UserService } from '../_services/user.service';
import { Games, GameResponse } from '../_models/team';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-view-games',
  templateUrl: './view-games.component.html',
  styleUrls: ['./view-games.component.scss']
})
export class ViewGamesComponent implements OnInit {
  
  public game: Games[];
  searchText: string;
  private dates: Observable<string[]>;

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
  gameTimes() {
    for (let index = 0; index < this.game.length; index++) {
      console.log(this.game[index].date);
      //this.dates.push(this.game[index].date);
      
    }
  }

  getGames() {
    this.http.get<GameResponse>("https://limitless-fjord-64117.herokuapp.com/create").subscribe(data => {
      this.game = data.games;
      console.log(this.game);
    });
    
  }

}
