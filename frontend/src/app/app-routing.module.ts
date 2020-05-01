import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SummonerComponent } from './summoner/summoner.component';
import { TeamsComponent } from './teams/teams.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { LeaderboardsComponent } from './leaderboards/leaderboards.component';
import { ViewGamesComponent } from './view-games/view-games.component';
import { ViewMatchComponent } from './view-match/view-match.component';
import { CreateGameComponent } from './view-games/create-game/create-game.component';
import { TournamentComponent } from './view-match/tournament/tournament.component';
import { ProfileComponent } from './profile/profile.component';
import { AuthGuard } from './_helpers';


const routes: Routes = [
  { path: 'summoner', component: SummonerComponent },
  { path: 'teams', component: TeamsComponent},
  { path: 'login', component: LoginComponent},
  { path: 'games', component: ViewGamesComponent},
  { path: 'leaderboards', component: LeaderboardsComponent},
  { path: 'viewgames', component: ViewGamesComponent},
  { path: 'creategame', component: CreateGameComponent},
  { path: 'register', component: RegisterComponent},
  { path: 'match/:matchId', component: ViewMatchComponent},
  { path: 'profile/:profileId', component: ProfileComponent, canActivate: [AuthGuard]},
  { path: 'tournament', component: TournamentComponent},
  { path: '**', component: ViewGamesComponent }, // Wildward Route
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
