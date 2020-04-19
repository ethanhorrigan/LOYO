import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DynamicrouteComponent } from './dynamicroute.component';

describe('DynamicrouteComponent', () => {
  let component: DynamicrouteComponent;
  let fixture: ComponentFixture<DynamicrouteComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DynamicrouteComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DynamicrouteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
