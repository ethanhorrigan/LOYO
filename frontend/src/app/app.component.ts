import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from './_services/authentication.service';
import { Router } from '@angular/router';
import { LeaderboardsComponent } from './leaderboards/leaderboards.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

constructor(
  private http: HttpClient,
  private router: Router,
  private authenticationService: AuthenticationService) {}

  
  title = 'LOYO';
  playerName: string = this.authenticationService.getUserInStorage(); // Get the current user (in local storage)
  logStatus: string;
  log: boolean = false;

  ngOnInit() {
    if(this.authenticationService.getUserInStorage() != null) {
      this.logStatus = 'Logout';
      this.log = true;
    }
    else if(this.authenticationService.getUserInStorage() == null) {
      this.logStatus = 'Login';
      this.log = false;
    }
  }

  logout() {
    if(this.authenticationService.getUserInStorage() != null) {
      this.authenticationService.logout();
    }
    else if (this.authenticationService.getUserInStorage() == null) {
      this.router.navigate(['/login']);
    }
  }
}
