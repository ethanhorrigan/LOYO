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
  public upcomingGames: any[] = [];
  public finishedGames: any[] = [];
  noGames: boolean = false;


  constructor(
    private http: HttpClient,
    private service: UserService,
    private auth: AuthenticationService
  ) { }

  ngOnInit() {
    this.getUpcomingGames();
  }

  getUpcomingGames() {
    this.service.getUpcomingGames(this.user).subscribe(g => {
      
      g.forEach(element => {
        if(element[6] == "PENDING") {
          this.upcomingGames.push(element);
        }

        if(element[6] == "FINISHED") {
          this.finishedGames.push(element);
        }
      });

      if(this.upcomingGames.length == 0) {
        this.noGames = true;
      }
    });
  }
}
