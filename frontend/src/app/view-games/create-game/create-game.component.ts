import { Component, OnInit, NgModule } from '@angular/core';
import { AmazingTimePickerService } from 'amazing-time-picker';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { UserService } from 'src/app/_services/user.service';
import { Games } from 'src/app/_models/team';
import { AuthenticationService } from 'src/app/_services/authentication.service';
import { first } from 'rxjs/operators';
import { MAT_DATE_LOCALE, DateAdapter } from '@angular/material/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-game',
  templateUrl: './create-game.component.html',
  styleUrls: ['./create-game.component.scss']
})
@NgModule({
  providers: [
    {provide: MAT_DATE_LOCALE, useValue: 'en-GB'},
  ],
})
export class CreateGameComponent implements OnInit {

  createForm: FormGroup;
  private selectedTime: string;
  submitted = false;
  private game: Games;
  loading = false;
  user: string;
  date: string;


  /**
   * https://material.angular.io/components/datepicker/overview
   */
  minDate: Date;
  maxDate: Date;

  constructor(
    private formBuilder: FormBuilder, 
    private userService: UserService,
    private router: Router,
    private authService: AuthenticationService,
    private dateAdapter: DateAdapter<Date>) { 
      this.dateAdapter.setLocale('en-GB'); 
      this.user = this.authService.getUserInStorage();
      const currentYear = new Date().getFullYear();
      const date = new Date();
      this.minDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
      this.maxDate = new Date(currentYear + 1, 11, 31);
    }

  /*
 match_uuid: string;
 match_name: string;
 match_type: string;
 date: string; //possible change to Date object?
 time: string; //possible change to Date object?
 outcome: string;
 admin: string;
*/
  ngOnInit() {
    this.createForm = this.formBuilder.group({
      matchName: ['', Validators.required],
      matchType: ['', Validators.required],
      date: ['', Validators.required],
      time: ['', Validators.required],

    });

  }

  get f() { return this.createForm.controls;}

  get d() {
    let day = this.f.date.value.getDate();
    if(day < 10) {
      day = '0' + day;
    }   
    
    let month = this.f.date.value.getMonth() + 1;
    if(month < 10) {
      month = '0' + month;
    }
    
    const year = this.f.date.value.getFullYear();
    return day + '-' + month + '-' + year;
  }

  onSubmit() {
    this.submitted = true;


    if(this.createForm.invalid) {
      return;
    }
    
    this.loading = true;

    this.game = new Games(this.f.matchName.value, this.f.matchType.value, this.d, this.f.time.value, this.user);
    
    this.userService.createMatch(this.game).pipe(first()).subscribe(data => {
      this.router.navigate(['/']);
    },
    error => {
      this.loading = false;
    });
  }

  onDateChange(event: any) {
    this.date = event.value;
  }


}
