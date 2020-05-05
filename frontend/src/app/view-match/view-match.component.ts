import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ViewGamesComponent } from '../view-games/view-games.component';
import { UserService } from '../_services/user.service';
import { Games, Participants, NewParticipant, FinalMatchResponse, FinalMatch, UpdateFinalMatch } from '../_models/team';
import { AuthenticationService } from '../_services/authentication.service';
import { tap, map, first } from 'rxjs/operators';
import { resolve } from 'url';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-view-match',
  templateUrl: './view-match.component.html',
  styleUrls: ['./view-match.component.scss']
})
export class ViewMatchComponent implements OnInit, OnDestroy {

  private sub: any;
  matchId: string;
  user: string;
  matchName: string;
  max: boolean = false;
  doMM: boolean = false;
  playerCount: number;
  adminUser: string;


 
  /* Admin Variables*/
  admin: boolean = false;
  submitted: boolean = false;
  winningTeam: string;
  losingTeam: string;
  selection:string;

  /* UI Display vars */
  daysUntil: string;
  badge: string = 'badge badge-primary';

  list: [string, string];

  /* team vars */
  team_one: string[] = [];
  team_two: string[] = [];

  p1t1: string;
  p2t1: string;
  p3t1: string;
  p4t1: string;
  p5t1: string;

  public matchDate: string;
  public matchDetails: Games[];
  public participants: Participants[];
  public finalMatch: FinalMatch[];

  constructor(
    private activatedRoute: ActivatedRoute,
    private userService: UserService,
    private http: HttpClient,
    private auth: AuthenticationService) { 
      this.user = this.auth.getUserInStorage();
      
      this.sub = this.activatedRoute.params.subscribe(params => {
        this.matchId = params['matchId'];
      });

      this.getAdmin();
      
    }

   ngOnInit() {
     
    console.log(this.admin);

    
    this.getMatch();

    this.getParticipants();

    

  }

  checkAdmin() {
    if(this.adminUser == this.user) {
      return true;
    }
    return false;
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  getAdmin() {
    this.userService.getAdmin(this.matchId).pipe(first()).subscribe(data => {
      this.adminUser = data;
      this.admin = this.checkAdmin();
    });
  }

  getMatch() {
    this.userService.getMatch(this.matchId).subscribe(data =>  {
      this.matchDetails = data.games;
      this.matchName = this.matchDetails[0].match_name;
      this.matchDate = this.matchDetails[0].date;
      this.daysUntil = this.calculateDays(this.matchDate);
    });
  }

  calculateDays(matchDate: string) {
    let year = matchDate.substr(0, 4);
    let month = matchDate.substr(5, 2);
    if(month.startsWith('0')) {
      month = month.replace('0', '');
    }
    let day = matchDate.substr(8,2);

    console.log(year);
    console.log(month);
    console.log(day);

    const currentMonth = (new Date().getUTCMonth()+ 1).toString();
    const currentDay = new Date().getDate();
    console.log('currentMonth:', currentMonth);
    let daysUntil = null;

    if(currentMonth == month) {
      daysUntil = Number(day) - currentDay;
      console.log(daysUntil);
      
    }
    let result = null;
    if(daysUntil == 1) {
      result = "IN "+daysUntil+" DAY";
      this.badge = 'badge badge-primary';
    }
    
    else {
      result = "IN "+daysUntil+" DAYS";
      this.badge = 'badge badge-primary';
    }

    if(daysUntil == null) {
      result = "GAME FINISHED";
      this.badge = 'badge badge-danger';
    }

    
    console.log(matchDate);
    return result;
  }

  joinMatch() {
    /**
     * I know the username data that is stored in localStorage
     * how do i relate username to participants
     * how do i know which match to add too?
     * this.matchId? 
     */
    let participant: NewParticipant = {
      username: this.user,
      match_uuid: this.matchId
    };


    this.userService.addPlayerToMatch(participant).subscribe(data => {
      location.reload();
    }); 
  }

  getParticipants() {
    this.userService.getParticipants(this.matchId).subscribe(data => {
      console.log(data.participants)
      this.participants = data.participants;
      this.getPlayerCount();
    });
  }


  getPlayerCount() {
    this.userService.getParticipantCount(this.matchId).subscribe(data => {
      this.playerCount = Number(data);

      if(this.playerCount == 10) {
        this.beginMM();
      }
    });
  }
  
  beginMM() {
    /**
     * matchmaking needs an array of participants
     * and the match id?
     * returns a sorted match of particpants sorted by team ? 
     */
    
    if(this.playerCount == 10 && this.doMM == false) {
    
    this.userService.getMM(this.matchId).subscribe(data => {
      this.finalMatch = data.final_match;

      console.log(this.finalMatch[0].team1);
      console.log(this.finalMatch[0].team2);
      console.log(this.finalMatch[0].team1[1]);
      console.log(this.finalMatch[0].team1[2]);

      for (let index = 0; index < 5; index++) {
        this.team_one[index] = this.finalMatch[0].team1[index];
      }

      for (let index = 0; index < 5; index++) {
        this.team_two[index] = this.finalMatch[0].team2[index];
      }

      this.p1t1 = this.finalMatch[0].team1[0];
      this.p2t1 = this.finalMatch[0].team1[1];
      this.p3t1 = this.finalMatch[0].team1[2];
      console.log(this.p1t1);
      
      this.p4t1 = this.finalMatch[0].team1[3];
      this.p5t1 = this.finalMatch[0].team1[4];


      this.doMM = true;
    });
  }
  }

  onAdminSubmit() {
    console.log("im in");
    
    this.submitted = true;
    if(this.selection == null || this.selection == undefined) {
      return;
    }

    let fmatch: UpdateFinalMatch = {
      match_uuid: this.matchId,
      winning_team: this.winningTeam,
      losing_team: this.losingTeam
    }

    this.userService.updateFinalMatch(fmatch).subscribe(data => {});
  }

  onTeamChange(event: any) {

    console.log(event.value);
    
    this.selection = event.value;

    this.sortTeam(this.selection)
  }

  sortTeam(selection: string) {
    const team_1 = 'team1';
    const team_2 = 'team2';

    if(this.selection == team_1) {
      this.winningTeam = team_1;
      this.losingTeam = team_2;
    }

    
    else if(this.selection == team_2) {
      this.winningTeam = team_2;
      this.losingTeam = team_1;
    }

    console.log('Winning Team: ', this.winningTeam);
    console.log('Losing Team: ', this.losingTeam);
    
  }
  

}
