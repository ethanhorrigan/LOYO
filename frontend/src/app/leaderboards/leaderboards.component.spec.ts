import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LeaderboardsComponent } from './leaderboards.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('LeaderboardsComponent', () => {
  let component: LeaderboardsComponent;
  let fixture: ComponentFixture<LeaderboardsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LeaderboardsComponent ],
      imports: [ HttpClientTestingModule ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LeaderboardsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
