import { Component, OnInit } from '@angular/core';
import { AmazingTimePickerService } from 'amazing-time-picker';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { UserService } from 'src/app/_services/user.service';
import { Games } from 'src/app/_models/team';
import { AuthenticationService } from 'src/app/_services/authentication.service';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-create-game',
  templateUrl: './create-game.component.html',
  styleUrls: ['./create-game.component.scss']
})
export class CreateGameComponent implements OnInit {

  createForm: FormGroup;
  private selectedTime: string;
  submitted = false;
  private game: Games;
  loading = false;
  user: string;

  constructor(
    private formBuilder: FormBuilder, 
    private userService: UserService,
    private authService: AuthenticationService) { 
      this.user = this.authService.getUserInStorage();
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

  onSubmit() {
    this.submitted = true;
    this.loading = true;

    this.game = new Games(this.f.matchName.value, this.f.matchType.value, this.f.date.value, this.f.time.value, this.user);
    
    this.userService.createMatch(this.game).pipe(first()).subscribe(data => {
      this.loading = false;
    });
  }


}
