import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../_services/authentication.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {

  private sub: any;
  isUser: boolean;
  subjectProfile: string;
  loggedUser: string;
  constructor(
    private auth: AuthenticationService,
    private activatedRoute: ActivatedRoute) { 

    this.sub = this.activatedRoute.params.subscribe(params => {
      this.subjectProfile = params['profileId']
    });

    this.loggedUser = this.auth.getUserInStorage();

    
  }

  ngOnInit() {    
  }


}
