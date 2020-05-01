import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { User, UserLogin } from '../_models';


@Injectable({ providedIn: 'root' })
export class AuthenticationService {

    public currentUser: String;

    constructor(private http: HttpClient) {
        this.currentUser = this.getUserInStorage();
    }

    public get currentUserValue(): String {
        return this.currentUser;
    }

    public getUserInStorage() {
        return localStorage.getItem('currentUser');
    }

    
    login(username, password) {
        return this.http.post<Boolean>(`https://limitless-fjord-64117.herokuapp.com/login`, { username, password }).pipe(map(user => {
            if(user == true) {
                localStorage.setItem('currentUser', username);
                this.updateDetails(username).subscribe (res => {
                    console.log("request succesfull.");
                    
                }, error => {
                    console.error("error during request");
                });
            }
            else {
                
            }
            return user;
        }));
    }

    updateDetails(username) {
        return this.http.patch(`https://limitless-fjord-64117.herokuapp.com/users/${username}`, username);
    }

    logout() {
        // remove user from local storage and set current user to null
        localStorage.removeItem('currentUser');
        this.currentUser = null;
        location.reload();
    }
}