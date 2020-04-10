import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-test-game',
  templateUrl: './test-game.component.html',
  styleUrls: ['./test-game.component.scss']
})
export class TestGameComponent implements OnInit {

  
  constructor() { }

  ngOnInit() {
  }

  date: Date =new Date(); 
  today = this.date.getDate()+'/'+(this.date.getMonth()+1)+'/'+this.date.getFullYear();

}
