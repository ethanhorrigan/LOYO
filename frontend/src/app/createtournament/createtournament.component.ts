import { Component, OnInit } from '@angular/core';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-createtournament',
  templateUrl: './createtournament.component.html',
  styleUrls: ['./createtournament.component.scss']
})
export class CreatetournamentComponent implements OnInit {
  createForm: FormGroup;
  //formBuilder: any;

  //Blocking Variables

  minDate: Date;
  maxDate: Date;

  day: number;
  month: string;
  year: number;

  date: Date;

  finalDate: any;

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    ) { 

      //In constructor
      const currentYear = new Date().getFullYear();
      const currentDay = new Date().getDate();
      const currentMonth = new Date().getMonth();
      this.minDate = new Date(currentYear, currentMonth, currentDay)
      this.maxDate = new Date(currentYear, 11, 31);
      //end of constructor
    }


  ngOnInit() {
    this.createForm = this.formBuilder.group({
      // Admin is Current user logged in
      gameName: [,  Validators.required],
      date: [{value: 'Select Date', disabled: true}, Validators.required],
      gameMode: ['', Validators.required]
  });
  }


  get form() { return this.createForm.controls; }

  

  onSubmit() {
    this.date = this.form.date.value;
    this.finalDate = this.date.getFullYear() + "-" + this.date.getDate() + "-" + this.date.getMonth()
    console.log(this.date.getUTCDay());
    
  }

  



}
