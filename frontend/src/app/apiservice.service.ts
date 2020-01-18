import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class APIServiceService {

  constructor(
    private http: HttpClient
  ) 
  { }

  data2: Object;

  public getPlayers() {
    return this.http.get('http://127.0.0.1:5002/players');    
  }
}
