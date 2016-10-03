import { NgModule }       from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import { FormsModule }    from '@angular/forms';
import { HttpModule }     from '@angular/http';


import { routing,
         appRoutingProviders }  from './app.routing';
import { AppComponent }         from './app.component';
import { HomeComponent }        from './home.component';
import { SignupComponent }      from './signup.component';
import { ChatComponent }        from './chat.component';
import { APIService }           from './api.service';
import { TruncatePipe }         from './truncate.pipe';


@NgModule({
  imports: [ 
    BrowserModule,
  	FormsModule,
  	HttpModule,
  	routing
  ],
  declarations: [ 
  	AppComponent,
  	SignupComponent,
  	HomeComponent,
  	ChatComponent,
  	TruncatePipe,
  ],
  providers: [
    appRoutingProviders,
    APIService,
    TruncatePipe
  ],
  bootstrap: [
  	AppComponent,
  ]
})
export class AppModule { }
