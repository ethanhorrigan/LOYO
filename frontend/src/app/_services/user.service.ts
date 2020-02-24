import { Injectable, DebugElement } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User, TempUser } from '../_models';

@Injectable({ providedIn: 'root' })
export class UserService {
    constructor(private http: HttpClient) { }

    getAll() {
        return this.http.get<User[]>(`http://127.0.0.1:5002/users`);
        //return this.http.get('http://127.0.0.1:5002/players');
    }

    addToLobby(user: string) {
        console.log("UserService: AddToLobby")
        return this.http.post(`http://127.0.0.1:5002/lobby`, user);
    }

    register(user: User) {
        console.log(user);
        return this.http.post(`http://127.0.0.1:5002/users`, user);
    }

    delete(id: number) {
        return this.http.delete(`http://127.0.0.1:5002/users/${id}`);
    }

    login(username: string) {
        console.log("login called")
        return this.http.get(`http://127.0.0.1:5002/users/${username}`);
    }


}