"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var api_service_1 = require('./api.service');
var router_1 = require('@angular/router');
var ChatComponent = (function () {
    function ChatComponent(_APIService, router) {
        this._APIService = _APIService;
        this.router = router;
    }
    ChatComponent.prototype.ngOnInit = function () {
        var _this = this;
        this._APIService.fetchUser()
            .subscribe(function (res) {
            _this.fetchChats();
        }, function (error) {
            _this.router.navigate(['/signup']);
        });
    };
    ChatComponent.prototype.fetchChats = function () {
        var _this = this;
        this._APIService.fetchChats()
            .subscribe(function (res) {
            _this.chats = [];
            for (var _i = 0, res_1 = res; _i < res_1.length; _i++) {
                var chat = res_1[_i];
                _this.chats.push(new Chat(_this._APIService, chat));
            }
            if (_this.chats.length > 0) {
                _this.selectChat(_this.chats[0]);
            }
        }, function (error) {
            console.log(error);
        });
    };
    ChatComponent.prototype.selectChat = function (chat) {
        this.selectedChat = chat;
        this.selectedChat.fetchMessages();
    };
    ChatComponent.prototype.sendMessage = function (form) {
        var _this = this;
        var text = form.value.message;
        this._APIService.sendMessageToChat(this.selectedChat.id, text)
            .subscribe(function (res) {
            var messages = _this.selectedChat.messages;
            if (messages.length > 0) {
                _this.selectedChat.fetchMessagesSince(messages[messages.length - 1]);
            }
            else {
                _this.selectedChat.fetchMessages();
            }
            ;
            form.reset();
        }, function (error) {
            console.log(error);
        });
    };
    ChatComponent.prototype.searchUsers = function (form) {
        var _this = this;
        var text = form.value.name;
        if (text.length > 0) {
            this._APIService.searchUsers(text)
                .subscribe(function (res) {
                _this.userSearch = true;
                _this.usersFound = [];
                for (var _i = 0, res_2 = res; _i < res_2.length; _i++) {
                    var member = res_2[_i];
                    _this.usersFound.push(new ChatMember(member));
                }
            }, function (error) {
                _this.userSearch = false;
                _this.usersFound = [];
                console.log(error);
            });
        }
        else {
            this.userSearch = false;
            this.usersFound = [];
        }
    };
    ChatComponent.prototype.selectUser = function (user) {
        var _this = this;
        this._APIService.createChat([user.name]).subscribe(function (res) {
            if (_this.userSearch == true) {
                _this.userSearch = false;
                _this.usersFound = [];
            }
            console.log(res);
            var new_chat = new Chat(_this._APIService, res);
            _this.chats.push(new_chat);
            _this.selectChat(new_chat);
        }, function (error) {
            console.log(error);
        });
    };
    ChatComponent = __decorate([
        core_1.Component({
            selector: 'chat',
            templateUrl: './app/templates/chat.component.html',
        }), 
        __metadata('design:paramtypes', [api_service_1.APIService, router_1.Router])
    ], ChatComponent);
    return ChatComponent;
}());
exports.ChatComponent = ChatComponent;
var Message = (function () {
    function Message(o) {
        this.id = o['id'];
        this.message = o['message'];
        this.date_created = o['date_created'];
        this.sender = new ChatMember(o['sender']);
    }
    return Message;
}());
exports.Message = Message;
var Chat = (function () {
    function Chat(_APIService, o) {
        this._APIService = _APIService;
        this.id = o['id'];
        this.name = o['name'];
        this.date_recent_activity = o['date_recent_activity'];
        this.date_created = o['date_recent_activity'];
        this.members = [];
        for (var _i = 0, _a = o['members']; _i < _a.length; _i++) {
            var member = _a[_i];
            this.members.push(new ChatMember(member));
        }
        this.messages = [];
        if (o['last_message']) {
            this.last_message = new Message(o['last_message']);
        }
    }
    Chat.prototype.fetchMessages = function () {
        var _this = this;
        this._APIService.fetchMessages(this.id).subscribe(function (res) {
            _this.messages = [];
            for (var _i = 0, res_3 = res; _i < res_3.length; _i++) {
                var message = res_3[_i];
                _this.messages.unshift(new Message(message));
            }
        }, function (error) {
            console.log(error);
        });
    };
    Chat.prototype.fetchMessagesSince = function (message) {
        var _this = this;
        this._APIService.fetchMessagesSinceId(this.id, message.id).subscribe(function (res) {
            for (var _i = 0, res_4 = res; _i < res_4.length; _i++) {
                var message_1 = res_4[_i];
                _this.messages.push(new Message(message_1));
            }
        }, function (error) {
            console.log(error);
        });
    };
    return Chat;
}());
exports.Chat = Chat;
var ChatMember = (function () {
    function ChatMember(o) {
        this.name = o['name'];
        this.avatar = o['avatar'];
        this.date_recent_activity = o['date_recent_activity'];
        this.date_created = o['date_created'];
    }
    return ChatMember;
}());
exports.ChatMember = ChatMember;
//# sourceMappingURL=chat.component.js.map