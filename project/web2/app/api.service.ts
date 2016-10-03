import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

@Injectable()
export class APIService {
	baseUrl: string;
	SessionId: string;

	constructor(private http: Http) {
		this.baseUrl = 'http://127.0.0.1:8080';
	}

	createAuthorizationHeader(headers:Headers) {
		this.SessionId = localStorage.getItem('SessionId');
		headers.append('Authorization', `SessionId ${this.SessionId}`); 
	}

	registerUser(name:string): Observable<any> {
		let body = new FormData();
		body.append('name', name)
		
		return this.http.post(`${this.baseUrl}/users`, body)
			.map(response => response.json());
	}

	fetchUser(): Observable<any> {
		let headers = new Headers();
    	this.createAuthorizationHeader(headers);

		return this.http.get(`${this.baseUrl}/users`, {headers: headers})
			.map(response => response.json());
	}

	fetchChats(): Observable<any> {
		let headers = new Headers();
    	this.createAuthorizationHeader(headers);

		return this.http.get(`${this.baseUrl}/chats`, {headers: headers})
			.map(response => response.json());
	}

	fetchMessages(chat_id:string): Observable<any> {
		let headers = new Headers();
    	this.createAuthorizationHeader(headers);

		return this.http.get(`${this.baseUrl}/chats/${chat_id}/messages`, {headers: headers})
			.map(response => response.json());
	}

	fetchMessagesSinceId(chat_id:string, message_id:string): Observable<any> {
		let headers = new Headers();
    	this.createAuthorizationHeader(headers);

		return this.http.get(`${this.baseUrl}/chats/${chat_id}/messages?since_id=${message_id}`, {headers: headers})
			.map(response => response.json());
	}

	sendMessageToChat(chat_id:string, text:string): Observable<any> {
		let headers = new Headers();
    	this.createAuthorizationHeader(headers);

		let body = new FormData();
		body.append('message', text)
		
		return this.http.post(`${this.baseUrl}/chats/${chat_id}`, body, {headers: headers});
	}

	searchUsers(name:string): Observable<any> {
		let headers = new Headers();
    	this.createAuthorizationHeader(headers);

    	return this.http.get(`${this.baseUrl}/users?name=${name}`, {headers: headers})
			.map(response => response.json());
	}

	createChat(users:string[]): Observable<any> {
		let headers = new Headers();
    	this.createAuthorizationHeader(headers);

    	let body = new FormData();
    	for(let user of users){
			body.append('members', user)
    	}

    	return this.http.post(`${this.baseUrl}/chats`, body, {headers: headers})
    		.map(response => response.json());
	}

	addUserToChat(chat_id:string, users:string[]): Observable<any> {
		let headers = new Headers();
    	this.createAuthorizationHeader(headers);

    	let body = new FormData();
    	for(let user of users){
			body.append('members', user)
    	}

    	return this.http.post(`${this.baseUrl}/chats/${chat_id}/`, body, {headers: headers});
	}

	sendMessageToUsers(users:string[], text:string): Observable<any> {
		let headers = new Headers();
    	this.createAuthorizationHeader(headers);

		let body = new FormData();
		for(let user of users){
			body.append('recipients', user)
		}
		body.append('message', text);
		
		return this.http.post(`${this.baseUrl}/message`, body, {headers: headers});
	}
}