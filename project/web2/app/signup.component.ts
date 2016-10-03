import { Component } from '@angular/core';
import { APIService } from './api.service';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';


@Component({
    selector: 'signup',
    templateUrl: './app/templates/signup.component.html',
})
export class SignupComponent {
    error: boolean;
    errorMessage: string;

	constructor(
        private _APIService: APIService,
        private router: Router,
    ) {}

    registerUser(form: NgForm){
        this.error = false;
        let name = form.value.name;

        this._APIService.registerUser(name)
            .subscribe(
                (res: any) => {
                    this._APIService.SessionId =res.SessionId; 
                    localStorage.setItem('SessionId', this._APIService.SessionId);
                    this.router.navigate(['/chat'])
                },
                (error: any) => {this.error =true; this.errorMessage =error}
            );
    }
}
