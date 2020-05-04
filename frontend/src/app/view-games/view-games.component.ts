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
  game_times: string[] = [];
  searchText: string;
  private dates: Observable<string[]>;

  badge: string = 'badge badge-primary';
  badges: string[] = [];

  constructor(
    private userService: UserService,
    private http: HttpClient
    ) { 
  }

  ngOnInit() {
    this.getGames();
   // this.gameTimes();
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
      let date = this.game[9].date.replace('-', '');
      console.log(date);
      this.calculateDays(this.game);
      console.log(this.game);
    });
  }

  calculateDays(match: Games[]) {
    let until = null;
    match.forEach(element => {
      element.date;
      let year = element.date.substr(0, 4);
      let month = element.date.substr(5, 2);
      if(month.startsWith('0')) {
        month = month.replace('0', '');
      }
      let day = element.date.substr(8,2);

      
    // console.log(year);
    // console.log(month);
    // console.log(day);

    
    const currentMonth = (new Date().getUTCMonth()+ 1).toString();
    const currentDay = new Date().getDate();
    console.log('currentMonth:', currentMonth);
    let daysUntil = null;

    if(currentMonth == month) {
      daysUntil = Number(day) - currentDay;
      console.log(daysUntil);
      
    }
    let result = null;
    let badge = null;
    if(daysUntil == 1) {
      result = "IN "+daysUntil+" DAY";
      badge = 'badge badge-primary';
    }
    
    else {
      result = "IN "+daysUntil+" DAYS";
      badge = 'badge badge-primary';
    }

    if(daysUntil == null) {
      result = "GAME FINISHED";
      badge = 'badge badge-danger';
    }

    console.log(result);
    if(result != null || result != undefined) {
      this.game_times.push(result);
      this.badges.push(badge);
    }
    });


    console.log(this.game_times[0]);


    
    // console.log(matchDate);
   // return result;
  }

}
