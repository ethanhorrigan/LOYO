import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RegisterComponent } from './register.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { RouterTestingModule } from '@angular/router/testing';
import { MatRadioModule } from '@angular/material/radio';

fdescribe('RegisterComponent', () => {
  let component: RegisterComponent;
  let fixture: ComponentFixture<RegisterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RegisterComponent ],
      imports: [ HttpClientTestingModule, ReactiveFormsModule, RouterTestingModule, FormsModule, MatRadioModule ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterComponent);
    component = fixture.componentInstance;
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

  it('should validate summonername status', () => {
    const status = component.summonerTaken;
    expect(status).toBeFalsy();
  });

  it('should validate role ', () => {
    const nameInput = component.registerForm.controls.role;

    expect(nameInput.valid).toBeFalsy();

    nameInput.setValue('Top');
    expect(nameInput.valid).toBeTruthy();
  });


  
  it('should validate empty summonername', () => {
    const summonerIn = component.registerForm.controls.summonerName;
    expect(summonerIn.valid).toBeFalsy();
  });
  
});
