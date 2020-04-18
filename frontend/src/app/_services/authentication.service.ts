import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { User, UserLogin } from '../_models';


@Injectable({ providedIn: 'root' })
export class AuthenticationService {

    public currentUser: String;

    constructor(private http: HttpClient) {
    }

    public get currentUserValue(): String {
        return this.currentUser;
    }

    public getUserInStorage() {
        return localStorage.getItem('currentUser');
    }

    // login(username, password) {
    //     return this.http.post<any>(`http://127.0.0.1:5002/users/authenticate`, { username, password })
    //         .pipe(map(user => {
    //             // store user details and jwt token in local storage to keep user logged in between page refreshes
    //             localStorage.setItem('currentUser', JSON.stringify(user));
    //             this.currentUserSubject.next(user);
    //             return user;
    //         }));
    // }

    // login(username: string) {
    //     return this.http.post(`http://127.0.0.1:5002/login/${username}`);
    // }

    
    login(username, password) {
        return this.http.post<Boolean>(`https://limitless-fjord-64117.herokuapp.com/login`, { username, password }).pipe(map(user => {
            if(user == true) {
                localStorage.setItem('currentUser', username);
            }
            else {
                
            }
            return user;
        }));
    }

    logout() {
        // remove user from local storage and set current user to null
        localStorage.removeItem('currentUser');
        this.currentUser = null;
        location.reload();
    }
}