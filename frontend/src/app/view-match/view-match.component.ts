import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ViewGamesComponent } from '../view-games/view-games.component';
import { UserService } from '../_services/user.service';
import { Games, Participants, NewParticipant, FinalMatchResponse, FinalMatch } from '../_models/team';
import { AuthenticationService } from '../_services/authentication.service';
import { tap, map } from 'rxjs/operators';
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
  private admin: boolean = false;
 

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
  
      console.log("vat");
      
      this.sub = this.getAdmin().subscribe(data => {
        this.adminUser = data.toString();
        console.log(this.adminUser);
      });
    }

   ngOnInit() {
     //this.checkAdmin();
     
     this.getMatch();

    // i need to check if it is the admin
    // if not then i dunno
    this.getParticipants();
    
    //
    //this.getPlayerCount();


    //this.beginMM();

  }

  getAdmin() {
    return this.http.get<string>(`https://limitless-fjord-64117.herokuapp.com/admin/${this.matchId}`);
  }

  checkAdmin() {
    console.log(this.adminUser);
    console.log(this.user);
    console.log(this.matchId);
    
    
    if(this.adminUser == this.user) {
      this.admin = true;
    }
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  getMatch() {
    this.userService.getMatch(this.matchId).subscribe(data =>  {
      this.matchDetails = data.games;
      this.matchName = this.matchDetails[0].match_name;
    });
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
    });
  }


  getPlayerCount() {
    this.userService.getParticipantCount(this.matchId).subscribe(data => {
      this.playerCount = Number(data);
    });
  }
  
  beginMM() {
    /**
     * matchmaking needs an array of participants
     * and the match id?
     * returns a sorted match of particpants sorted by team ? 
     */
    
    if(this.playerCount == 9 && this.doMM == false) {
    this.userService.getMM(this.matchId).subscribe(data => {
      this.finalMatch = data.final_match;
      console.log(this.finalMatch[0].team1[0]);

      this.doMM = true;
    });
  }
  }

  getOutcome() {
    /**
     * Outcome needs to update values for all participants
     * so outcome needs:
     * the MatchID
     * Participants []
     * and the actual outcome of the game
     * 
     * 
     * only update values for
     *  winning team participants.
     */
  }

}
