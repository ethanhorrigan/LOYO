import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
/* HTTP Services */
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';


/* App Components*/
import { SummonerComponent } from './summoner/summoner.component';
import { TeamsComponent } from './teams/teams.component';
import { NewuserComponent } from './newuser/newuser.component';

const appRoutes: Routes = [
  { path: 'summoner', component: SummonerComponent }
];


@NgModule({
  declarations: [
    AppComponent,
    SummonerComponent,
    TeamsComponent,
    NewuserComponent
  ],
  imports: [
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
    ),
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
