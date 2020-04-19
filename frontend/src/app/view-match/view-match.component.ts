import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TestGameComponent } from '../test-game/test-game.component';
import { UserService } from '../_services/user.service';
import { Games, Participants, NewParticipant } from '../_models/team';
import { AuthenticationService } from '../_services/authentication.service';

@Component({
  selector: 'app-view-match',
  templateUrl: './view-match.component.html',
  styleUrls: ['./view-match.component.scss']
})
export class ViewMatchComponent implements OnInit, OnDestroy {

  private sub: any;
  matchId: string;
  user: string;

  public matchDetails: Games[];
  public participants: Participants[];

  constructor(
    private activatedRoute: ActivatedRoute,
    private userService: UserService,
    private auth: AuthenticationService) { 
      this.user = this.auth.getUserInStorage();
    }

  ngOnInit() {
    this.sub = this.activatedRoute.params.subscribe(params => {
      this.matchId = params['matchId'];
    });

    this.getMatch();
    this.getParticipants();
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  getMatch() {
    this.userService.getMatch(this.matchId).subscribe(data =>  {
      this.matchDetails = data.games;
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
      this.participants = data.participants;
      console.log(this.participants);
    });
  }

}
