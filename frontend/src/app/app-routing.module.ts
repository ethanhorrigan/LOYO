import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SummonerComponent } from './summoner/summoner.component';
import { TeamsComponent } from './teams/teams.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { GamesComponent } from './games/games.component';
import { LeaderboardsComponent } from './leaderboards/leaderboards.component';
import { ViewGamesComponent } from './view-games/view-games.component';
import { DynamicrouteComponent } from './dynamicroute/dynamicroute.component';
import { ViewMatchComponent } from './view-match/view-match.component';


const routes: Routes = [
  { path: 'summoner', component: SummonerComponent },
  { path: 'teams', component: TeamsComponent},
  { path: 'login', component: LoginComponent},
  { path: 'games', component: GamesComponent},
  { path: 'leaderboards', component: LeaderboardsComponent},
  { path: 'viewgames', component: ViewGamesComponent},
  { path: 'register', component: RegisterComponent},
  { path: 'user/:username', component: DynamicrouteComponent},
  { path: 'match/:matchId', component: ViewMatchComponent},
  { path: '**', component: ViewGamesComponent }, // Wildward Route
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
