import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
/* HTTP Services */
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


/* App Components*/
import { SummonerComponent } from './summoner/summoner.component';
import { TeamsComponent } from './teams/teams.component';
import { NewuserComponent } from './newuser/newuser.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';

const appRoutes: Routes = [
  { path: 'summoner', component: SummonerComponent }
];


@NgModule({
  declarations: [
    AppComponent,
    SummonerComponent,
    TeamsComponent,
    NewuserComponent,
    LoginComponent,
    RegisterComponent
  ],
  imports: [
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
    ),
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
