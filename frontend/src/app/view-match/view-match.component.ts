import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TestGameComponent } from '../test-game/test-game.component';

@Component({
  selector: 'app-view-match',
  templateUrl: './view-match.component.html',
  styleUrls: ['./view-match.component.scss']
})
export class ViewMatchComponent implements OnInit, OnDestroy {

  private sub: any;
  matchId: string;

  constructor(
    private activatedRoute: ActivatedRoute,
    private gameComponent: TestGameComponent) { }

  ngOnInit() {

    this.gameComponent.game
    this.sub = this.activatedRoute.params.subscribe(params => {
      this.matchId = params['matchId'];
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
