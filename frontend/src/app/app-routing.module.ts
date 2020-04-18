import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SummonerComponent } from './summoner/summoner.component';
import { TeamsComponent } from './teams/teams.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { GamesComponent } from './games/games.component';
import { LeaderboardsComponent } from './leaderboards/leaderboards.component';
import { TestGameComponent } from './test-game/test-game.component';
import { CreatetournamentComponent } from './createtournament/createtournament.component';


const routes: Routes = [
  { path: 'summoner', component: SummonerComponent },
  { path: 'teams', component: TeamsComponent},
  { path: 'login', component: LoginComponent},
  { path: 'games', component: GamesComponent},
  { path: 'leaderboards', component: LeaderboardsComponent},
  { path: 'test', component: TestGameComponent},
  { path: 'register', component: RegisterComponent},
  { path: 'creategame', component: CreatetournamentComponent},
  { path: '**', component: GamesComponent } // Wildward Route
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
