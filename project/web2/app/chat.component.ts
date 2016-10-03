import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { APIService } from './api.service';
import { Router } from '@angular/router';
import { NgForm } from '@angular/forms';

@Component({
    selector: 'chat',
    templateUrl: './app/templates/chat.component.html',
})
export class ChatComponent implements OnInit {
	chats: Chat[];
	selectedChat: Chat;

	userSearch: boolean;
	usersFound: ChatMember[];

	constructor(
		private _APIService: APIService,
		private router: Router,
	) {}
	
	ngOnInit() {
		this._APIService.fetchUser()
    	.subscribe(
        	(res: any) => {
                this.fetchChats()
            },
            (error: any) => {
                this.router.navigate(['/signup']) 
            }
        );
    }

    fetchChats() {
    	this._APIService.fetchChats()
    	.subscribe(
    		(res: any) => {
    			this.chats = [];
                for(let chat of res){
                	this.chats.push(
                		new Chat(
                			this._APIService, 
                			chat
                		)
                	);
                }
                if(this.chats.length>0){
                	this.selectChat(this.chats[0])
            	}
            },
            (error: any) => {
                console.log(error)
            }
    	)
    }

    selectChat(chat:Chat){
    	this.selectedChat = chat;
    	this.selectedChat.fetchMessages();
    }

    sendMessage(form: NgForm){
        let text = form.value.message;

        this._APIService.sendMessageToChat(this.selectedChat.id, text)
        .subscribe(
            (res: any) => {
            	let messages: Message[] = this.selectedChat.messages;

            	if(messages.length > 0){
	                this.selectedChat.fetchMessagesSince(
	                	messages[messages.length-1]
	                );
	            }else{
	            	this.selectedChat.fetchMessages();
	            };
	            form.reset();
            },
            (error: any) => {
            	console.log(error);
            }
        );
    }

    searchUsers(form: NgForm){
    	let text = form.value.name;

    	if(text.length > 0){
	    	this._APIService.searchUsers(text)
	        .subscribe(
	            (res: any[]) => {
	            	this.userSearch = true;
	            	this.usersFound = [];
					for(let member of res){
						this.usersFound.push(
							new ChatMember(member)
						);
					}
	            },
	            (error: any) => {
	            	this.userSearch = false;
	            	this.usersFound = [];
	            	console.log(error);
	            }
	        );
	    }else{
	    	this.userSearch = false;
	        this.usersFound = [];
	    }
    }

    selectUser(user:ChatMember){
    	this._APIService.createChat([user.name]).subscribe(
            (res: any[]) => {
            	if(this.userSearch == true){
					this.userSearch = false;
            		this.usersFound = [];
            	}
            	console.log(res)
            	let new_chat = new Chat(
            		this._APIService, 
            		res
            	);
            	this.chats.push(new_chat);
            	this.selectChat(new_chat);
            },
            (error: any) => {
            	console.log(error);
            }
        );
    }
}

export class Message {
	id: string;
	sender: ChatMember;
	message:   string;
	date_created: Date;

	constructor(o: Object){
		this.id = o['id'];
		this.message = o['message'];
		this.date_created = o['date_created'];
		this.sender = new ChatMember(o['sender']);
	}
}

export class Chat {
	id: string;
	name:    string;
	date_recent_activity: Date;
	date_created: Date;
	members: ChatMember[];
	messages: Message[];
	last_message: Message;

	constructor(
		private _APIService: APIService,
		o: Object,
	){
		this.id = o['id'];
		this.name = o['name'];
		this.date_recent_activity = o['date_recent_activity'];
		this.date_created = o['date_recent_activity'];

		this.members = [];
		for(let member of o['members']){
			this.members.push(
				new ChatMember(member)
			);
		}
		
		this.messages = [];
		if(o['last_message']){
			this.last_message = new Message(o['last_message']);
		}
	}

	fetchMessages(){
		this._APIService.fetchMessages(this.id).subscribe(
            (res: any) => {
                this.messages = [];
                for(let message of res){
					this.messages.unshift(
						new Message(message)
					);
				}
            },
            (error: any) => {
            	console.log(error);
            }
        );
	}

	fetchMessagesSince(message:Message){
		this._APIService.fetchMessagesSinceId(this.id, message.id).subscribe(
			(res: any) => {
                for(let message of res){
					this.messages.push(
						new Message(message)
					);
				}
            },
            (error: any) => {
            	console.log(error);
            }
        );
	}
}

export class ChatMember {
	name: string;
	avatar: string;
	date_recent_activity: Date;
	date_created: Date;

	constructor(o: Object){
		this.name = o['name'];
		this.avatar = o['avatar'];
		this.date_recent_activity = o['date_recent_activity'];
		this.date_created = o['date_created'];
	}
}