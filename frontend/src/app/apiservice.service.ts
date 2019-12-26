import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class APIServiceService {

  constructor(
    private http: HttpClient
  ) 
  { }

  public getAlbums() {
    return this.http.get('https://jsonplaceholder.typicode.com/albums');
  }
}
