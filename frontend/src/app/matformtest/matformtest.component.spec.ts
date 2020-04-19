import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MatformtestComponent } from './matformtest.component';

describe('MatformtestComponent', () => {
  let component: MatformtestComponent;
  let fixture: ComponentFixture<MatformtestComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MatformtestComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MatformtestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
