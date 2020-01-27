import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SummonerComponent } from './summoner/summoner.component';
import { TeamsComponent } from './teams/teams.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';


const routes: Routes = [
  { path: 'summoner', component: SummonerComponent },
  { path: 'teams', component: TeamsComponent},
  { path: 'login', component: LoginComponent},
  { path: 'register', component: RegisterComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
