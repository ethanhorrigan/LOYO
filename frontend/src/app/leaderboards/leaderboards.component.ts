import { Component, OnInit } from '@angular/core';
import { Summoner } from '../summoner/Summoner';
import { HttpClient } from '@angular/common/http';
import { PlayersResponse } from '../summoner/PlayerResponse';

@Component({
  selector: 'app-leaderboards',
  templateUrl: './leaderboards.component.html',
  styleUrls: ['./leaderboards.component.scss']
})
export class LeaderboardsComponent implements OnInit {
  summ;
  url = 'https://limitless-fjord-64117.herokuapp.com/playerstandings';
  res = [];
  public summoners: Summoner[];

  constructor(
    private http: HttpClient
  ) { }

  ngOnInit() {
    this.http.get<PlayersResponse>(this.url).subscribe(result  => {
      this.summoners = result.players;
    }, error => console.error(error));
  }
}
