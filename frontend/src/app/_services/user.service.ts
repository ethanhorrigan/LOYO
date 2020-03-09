import { Injectable, DebugElement } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User, TempUser } from '../_models';
import { Match } from '../_models/team';

@Injectable({ providedIn: 'root' })
export class UserService {
    constructor(private http: HttpClient) { }

    getAll() {
        return this.http.get<User[]>(`http://127.0.0.1:5002/users`);
    }

    addToLobby(tempUser: TempUser) {
        return this.http.post(`http://127.0.0.1:5002/lobby`, tempUser)
    }

    getLobby() {
        return this.http.get(`http://127.0.0.1:5002/lobby`);
    }

    getMM() {
        return this.http.get<Match[]>(`http://127.0.0.1:5002/mm`);
    }

    register(user: User) {
        console.log(user);
        return this.http.post(`http://127.0.0.1:5002/users`, user);
    }

    delete(id: number) {
        return this.http.delete(`http://127.0.0.1:5002/users/${id}`);
    }

    login(username: string) {
        return this.http.get(`http://127.0.0.1:5002/users/${username}`);
    }
}