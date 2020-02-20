import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
import { UserService } from '../_services/user.service';
import { AuthenticationService } from '../_services/authentication.service';


@Component({
    styleUrls: ['./register.component.scss'],
    templateUrl: 'register.component.html'
})
export class RegisterComponent implements OnInit {
    registerForm: FormGroup;
    loading = false;
    submitted = false;
    role: string;

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

    // convenience getter for easy access to form fields
    get f() { return this.registerForm.controls; }

    onSubmit() {
        this.submitted = true;

        // stop here if form is invalid
        if (this.registerForm.invalid) {
            console.log("error in register form");
            return;
        }
        this.loading = true;

        // this.userService.login(this.f.username.value);
        // this.userService.login(this.f.username.value
            this.userService.register(this.registerForm.value)
                .pipe(first())
                .subscribe(
                    data => {
                        this.router.navigate(['/login']);
                    },
                    error => {
                        this.loading = false;
                    });
    }

    getUsers() {
        this.userService.getAll();
    }

    getRole(event: any) {
        this.role = event.target.value
    }
}
