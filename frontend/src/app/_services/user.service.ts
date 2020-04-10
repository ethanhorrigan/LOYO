import { Injectable, DebugElement } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User, TempUser } from '../_models';
import { Match, Game } from '../_models/team';

@Injectable({ providedIn: 'root' })

/* 
* @description
* This services handles the HTTP Request routes to the API
* Currently, the routes are static and should be changed to relative paths in the future.
*/
export class UserService {
    constructor(private http: HttpClient) { }

    deploy_url : string = "https://limitless-fjord-64117.herokuapp.com";
    local_url : string = "http://127.0.0.1:5002"

    getAll() {
        return this.http.get<User[]>(`https://limitless-fjord-64117.herokuapp.com/users/users`);
        //return this.http.get<User[]>(this.deploy_url + '/users/users')
    }

    addToLobby(tempUser: TempUser) {
        return this.http.post(`https://limitless-fjord-64117.herokuapp.com/lobby`, tempUser)
    }

    getLobby() {
        return this.http.get(`https://limitless-fjord-64117.herokuapp.com/lobby`);
    }

    getMM() {
        return this.http.get<Match[]>(`https://limitless-fjord-64117.herokuapp.com/mm`);
    }

    // getGames() {
    //     return this.http.get<Game[]>(`https://limitless-fjord-64117.herokuapp.com/create`);
    // }

    // register(user: User) {
    //     console.log(user);
    //     return this.http.post(`http://127.0.0.1:5002/users`, user);
    // }

    register(user: User) {
        console.log(user);
        ///return this.http.post(`https://limitless-fjord-64117.herokuapp.com/users`, user);
        return this.http.post(this.deploy_url + '/users', user);
    }
    //https://limitless-fjord-64117.herokuapp.com/

    delete(id: number) {
        return this.http.delete(`https://limitless-fjord-64117.herokuapp.com/users/${id}`);
    }

    login(username: string) {
        return this.http.get(`https://limitless-fjord-64117.herokuapp.com/users/${username}`);
    }
}