import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
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
    usernameTaken = false;
    summonerTaken = false;
    role: string;
    nameOnChange: string;
    selection: string;

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
        
        console.log(this.f.username.value)
        this.userService.login(this.f.username.value).subscribe( data => {
            console.log(data);
            if(data = "taken") {
                this.usernameTaken = true;
            }
            if(data = "TEST") {
                
                this.usernameTaken = false;
            }
        });
        console.log("check user api called")
        return this.nameOnChange = this.f.username.value;
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
        //this.userService.login(this.f.username.value);
            this.userService.register(this.registerForm.value)
                .pipe(first())
                .subscribe(
                    data => {
                        if(data = "UT") {
                            this.usernameTaken = true;
                            console.log(this.usernameTaken)
                        }

                        if(data = "ST") {
                            this.summonerTaken = true;
                            console.log(this.usernameTaken)
                        }
                        if(data = "OK" && this.usernameTaken == false && this.summonerTaken == false) {
                            this.router.navigate(['/login']);
                        }
                        console.log(data);
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
