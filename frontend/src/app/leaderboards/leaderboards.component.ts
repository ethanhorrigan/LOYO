import { Component, OnInit } from '@angular/core';
import { Summoner } from '../summoner/Summoner';
import { APIServiceService } from '../apiservice.service';
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
  public Summoners: Summoner[];

  constructor(
    private apiService: APIServiceService,
    private http: HttpClient
  ) { }

  ngOnInit() {
    this.http.get<PlayersResponse>(this.url).subscribe(result  => {
      this.summoners = result.players;
      console.log(result);
      console.log(this.summoners);
    }, error => console.error(error));
    
  }
}
