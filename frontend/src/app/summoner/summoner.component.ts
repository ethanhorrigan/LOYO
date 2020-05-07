
import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { debug } from 'util';
import { Summoner } from "./Summoner";
import { PlayersResponse } from "./PlayerResponse";

@Component({
  selector: 'app-summoner',
  templateUrl: './summoner.component.html',
  styleUrls: ['./summoner.component.scss']
})
export class SummonerComponent implements OnInit {
  summ;
  url = ' http://127.0.0.1:5002/players';
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
