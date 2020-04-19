import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-dynamicroute',
  templateUrl: './dynamicroute.component.html',
  styleUrls: ['./dynamicroute.component.scss']
})
export class DynamicrouteComponent implements OnInit {
  username: string;
  private sub:any;

  constructor(private activatedRoute: ActivatedRoute) { }

  ngOnInit() {
    this.sub = this.activatedRoute.params.subscribe(params => {
      this.username = params['username']
    });
  }

}
