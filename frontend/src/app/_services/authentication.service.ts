import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { User, UserLogin } from '../_models';


@Injectable({ providedIn: 'root' })
export class AuthenticationService {

    private currentUserSubject: BehaviorSubject<User>;
    public currentUser: Observable<User>;

    constructor(private http: HttpClient) {
        this.currentUserSubject = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('currentUser')));
        this.currentUser = this.currentUserSubject.asObservable();
    }

    public get currentUserValue(): User {
        return this.currentUserSubject.value;
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
                this.currentUserSubject.next(username);
            }
            else {
                
            }
            return user;
        }));
    }

    logout() {
        // remove user from local storage and set current user to null
        localStorage.removeItem('currentUser');
        this.currentUserSubject.next(null);
    }
}