import { Component, OnInit } from '@angular/core';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Option } from './times';
import { Time } from '@angular/common';

@Component({
  selector: 'app-createtournament',
  templateUrl: './createtournament.component.html',
  styleUrls: ['./createtournament.component.scss']
})
export class CreatetournamentComponent implements OnInit {


  //Form Variables
  submitted = false;
  

  // Time picking module
  public format: string = "hh:mm tt";


  createForm: FormGroup;
  //formBuilder: any;

  //Blocking Variables

  hours: Option[] = [
    {name: '12', value:12},
    {name: '11', value:12},
    {name: '10', value:12},
    {name: '9', value:12},
    {name: '8', value:12},
    {name: '7', value:12},
    {name: '6', value:12},
    {name: '5', value:12},
    {name: '4', value:12},
    {name: '3', value:12},
    {name: '2', value:12},
    {name: '1', value:12},
  ];
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
      this.maxDate = new Date(currentYear, currentMonth + 1, currentDay);
      //end of constructor
    }

  /**
   * Build the form on page init.
   */
  ngOnInit() {
    this.createForm = this.formBuilder.group({
      // Admin is Current user logged in
      gameName: [,  Validators.required],
      date: [{value: 'Select Date', disabled: true}, Validators.required],
      gameMode: ['', Validators.required]
  });
  }

  /**
   * Getter for retrieveing form details
   */
  get form() { return this.createForm.controls; }

  /**
   * On Form Submission
   */
  onSubmit() {
    this.submitted = true;

    // Stop if the form is invalid
    if (this.createForm.invalid) {
      return;
    }

    this.date = this.form.date.value;
    this.finalDate = this.date.getFullYear() + "-" + this.date.getDate() + "-" + this.date.getMonth()
    console.log(this.date.getUTCDay());
    
  }

  



}
