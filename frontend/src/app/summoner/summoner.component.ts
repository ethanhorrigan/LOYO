import { APIServiceService } from '../apiservice.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-summoner',
  templateUrl: './summoner.component.html',
  styleUrls: ['./summoner.component.scss']
})
export class SummonerComponent implements OnInit {
  albums;

  constructor(
    private apiService: APIServiceService
  ) { }

  ngOnInit() {
    this.albums = this.apiService.getAlbums();
  }

}
