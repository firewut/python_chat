import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { APIService } from './api.service';
import { Router } from '@angular/router';

@Component({
    selector: 'home',
    templateUrl: './app/templates/home.component.html',
})
export class HomeComponent implements OnInit {
	constructor(
        private _APIService: APIService,
        private router: Router,
    ) {}
	
	ngOnInit() {
		this._APIService.fetchUser()
    	.subscribe(
        	(res: any) => {
                this.router.navigate(['/chat'])
            },
            (error: any) => {
                this.router.navigate(['/signup']) 
            }
        );
    }
}
