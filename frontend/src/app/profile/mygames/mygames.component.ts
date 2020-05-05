import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserService } from 'src/app/_services/user.service';
import { AuthenticationService } from 'src/app/_services/authentication.service';
import { Games } from 'src/app/_models/team';

@Component({
  selector: 'app-mygames',
  templateUrl: './mygames.component.html',
  styleUrls: ['./mygames.component.scss']
})
export class MygamesComponent implements OnInit {

  user: string = this.auth.getUserInStorage();
  public games: Games[];
  noGames: boolean = true;


  constructor(
    private http: HttpClient,
    private service: UserService,
    private auth: AuthenticationService
  ) { }

  ngOnInit() {
  }

  getUpcomingGames() {
    this.service.getUpcomingGames(this.user).subscribe(g => {
      this.games = g.games;
    });
  }
}
