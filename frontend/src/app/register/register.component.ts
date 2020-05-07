import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first, tap, map } from 'rxjs/operators';
import { concatMap } from 'rxjs/operators';
import { UserService } from '../_services/user.service';
import { AuthenticationService } from '../_services/authentication.service';
import { debug } from 'util';

@Component({
    styleUrls: ['./register.component.scss'],
    templateUrl: 'register.component.html'
})

export class RegisterComponent implements OnInit {
    registerForm: FormGroup;
    loading = false;
    submitted = false;
    changed = false;
    usernameTaken;
    summonerTaken = false;
    role: string;
    nameOnChange: string;
    selection: string;
    usernameStatus: string = null;

    constructor(
        private formBuilder: FormBuilder,
        private router: Router,
        private authenticationService: AuthenticationService,
        private userService: UserService
    ) {
        // redirect to home if already logged in
        if (this.authenticationService.currentUserValue) {
            this.router.navigate(['/']);
        }
    }

    ngOnInit() {
        this.registerForm = this.formBuilder.group({
            username: ['', Validators.required],
            summonerName: ['', Validators.required],
            password: ['', [Validators.required, Validators.minLength(6)]],
            role: ['', Validators.required]
        });
    }

    onUsernameChange() {
        //Check the Username on the API
        this.userService.login(this.f.username.value).pipe(first()).subscribe(data => {
            this.usernameStatus = data.toString();
            this.checkUsernameStatus(this.usernameStatus);
        });
        this.changed = true;
        return this.nameOnChange = this.f.username.value;
    }

    checkUsernameStatus(_status: string) {
        if (_status == "USERNAME_OK") {
            this.usernameTaken = false;
        }
        if (_status == "USERNAME_TAKEN") {
            this.usernameTaken = true;
        }
    }

    // convenience getter for easy access to form fields
    get f() { return this.registerForm.controls; }

    onSubmit() {
        this.submitted = true;

        // stop here if form is invalid
        if (this.registerForm.invalid) {
            return;
        }
        this.loading = true;

        this.userService.register(this.registerForm.value)
            .pipe(first())
            .subscribe(
                data => {
                    if (data == "UT") {
                        this.usernameTaken = true;
                    }

                    if (data == "ST") {
                        this.summonerTaken = true;
                    }
                    if (data == "OK") {
                        this.router.navigate(['/login']);
                    }
                },
                error => {
                    this.loading = false;
                });
    }

    getUsers() {
        this.userService.getAll();
    }

    getRole(event: any) {
        this.role = this.selection
    }
}
