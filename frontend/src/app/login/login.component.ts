import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
import { AuthenticationService } from '../_services/authentication.service';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


// @Component({templateUrl: 'login.component.html'})

@Component({
    styleUrls: ['./login.component.scss'],
    templateUrl: 'login.component.html'
})

export class LoginComponent implements OnInit {
    loginForm: FormGroup;
    loading = false;
    submitted = false;
    invalid = false;
    loggedIn = false;
    returnUrl: string;

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
    ) {
        // redirect to home if already logged in
        if (this.authenticationService.currentUserValue) { 
            this.router.navigate(['/']);
        }
    }

    ngOnInit() {
        this.loginForm = this.formBuilder.group({
            username: ['', Validators.required],
            password: ['', Validators.required]
        });
        console.log(this.authenticationService.getUserInStorage())
        if(this.authenticationService.getUserInStorage() == null) {
            this.loggedIn = false;
        }
        // get return url from route parameters or default to '/'
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    }

    // convenience getter for easy access to form fields
    get f() { return this.loginForm.controls; }

    // onSubmit() {
    //     this.submitted = true;

    //     // stop here if form is invalid
    //     if (this.loginForm.invalid) {
    //         return;
    //     }

    //     this.loading = true;
    //     this.authenticationService.login(this.f.username.value, this.f.password.value)
    //         .pipe(first())
    //         .subscribe(
    //             data => {
    //                 this.router.navigate([this.returnUrl]);
    //             },
    //             error => {
    //                 this.loading = false;
    //             });
    // }

    onSubmit() {
        this.submitted = true;

        // stop here if form is invalid
        if (this.loginForm.invalid) {
            return;
        }

        if(this.authenticationService.getUserInStorage() != null) {
            this.loggedIn = true;
            return;
        }

        this.loading = true;
        this.authenticationService.login(this.f.username.value, this.f.password.value)
            .pipe(first())
            .subscribe(
                data => {
                    //
                    let response = JSON.stringify(data);
                    console.log(response);
                    if(response == "true") {
                        this.invalid = false;
                        this.router.navigate([this.returnUrl]);
                    }
                    if(response == "false") {
                        this.invalid = true;
                        this.loading = false;
                    }
                },
                error => {
                    this.loading = false;
                });
    }
}
