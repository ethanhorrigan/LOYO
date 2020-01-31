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
  url = ' http://127.0.0.1:5002/playerstandings';
  res = [];
  public summoners: Summoner[];

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
