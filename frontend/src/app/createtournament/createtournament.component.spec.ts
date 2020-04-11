import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatetournamentComponent } from './createtournament.component';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ReactiveFormsModule, FormsModule, FormBuilder } from '@angular/forms';
import { RouterTestingModule } from '@angular/router/testing';
import { MatRadioModule } from '@angular/material/radio';

describe('CreatetournamentComponent', () => {
  let component: CreatetournamentComponent;
  let fixture: ComponentFixture<CreatetournamentComponent>;

  const formBuilder: FormBuilder = new FormBuilder();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CreatetournamentComponent],
      imports: [HttpClientTestingModule, ReactiveFormsModule, RouterTestingModule, FormsModule, MatRadioModule],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
      providers: [
        { provide: FormBuilder, useValue: formBuilder }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreatetournamentComponent);
    component = fixture.componentInstance;
    component.registerForm = formBuilder.group({
      username: 'test',
      summonerName: 'test',
      password: 'test',
      role: 'test'
    });
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should validate username', () => {
    const nameInput = component.registerForm.controls.username;

    expect(nameInput.valid).toBeFalsy();

    nameInput.setValue('TestName');
    expect(nameInput.valid).toBeTruthy();
  });
  
  it('should validate summonername', () => {
    const summonerIn = component.registerForm.controls.summonerName;
    summonerIn.setValue('TestSN');
    expect(summonerIn.valid).toBeTruthy();
  });
  
  it('should validate empty summonername', () => {
    const summonerIn = component.registerForm.controls.summonerName;
    expect(summonerIn.valid).toBeFalsy();
  });



});
