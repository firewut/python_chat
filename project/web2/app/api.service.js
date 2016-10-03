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
var http_1 = require('@angular/http');
require('rxjs/add/operator/map');
var APIService = (function () {
    function APIService(http) {
        this.http = http;
        this.baseUrl = 'http://127.0.0.1:8080';
    }
    APIService.prototype.createAuthorizationHeader = function (headers) {
        this.SessionId = localStorage.getItem('SessionId');
        headers.append('Authorization', "SessionId " + this.SessionId);
    };
    APIService.prototype.registerUser = function (name) {
        var body = new FormData();
        body.append('name', name);
        return this.http.post(this.baseUrl + "/users", body)
            .map(function (response) { return response.json(); });
    };
    APIService.prototype.fetchUser = function () {
        var headers = new http_1.Headers();
        this.createAuthorizationHeader(headers);
        return this.http.get(this.baseUrl + "/users", { headers: headers })
            .map(function (response) { return response.json(); });
    };
    APIService.prototype.fetchChats = function () {
        var headers = new http_1.Headers();
        this.createAuthorizationHeader(headers);
        return this.http.get(this.baseUrl + "/chats", { headers: headers })
            .map(function (response) { return response.json(); });
    };
    APIService.prototype.fetchMessages = function (chat_id) {
        var headers = new http_1.Headers();
        this.createAuthorizationHeader(headers);
        return this.http.get(this.baseUrl + "/chats/" + chat_id + "/messages", { headers: headers })
            .map(function (response) { return response.json(); });
    };
    APIService.prototype.fetchMessagesSinceId = function (chat_id, message_id) {
        var headers = new http_1.Headers();
        this.createAuthorizationHeader(headers);
        return this.http.get(this.baseUrl + "/chats/" + chat_id + "/messages?since_id=" + message_id, { headers: headers })
            .map(function (response) { return response.json(); });
    };
    APIService.prototype.sendMessageToChat = function (chat_id, text) {
        var headers = new http_1.Headers();
        this.createAuthorizationHeader(headers);
        var body = new FormData();
        body.append('message', text);
        return this.http.post(this.baseUrl + "/chats/" + chat_id, body, { headers: headers });
    };
    APIService.prototype.searchUsers = function (name) {
        var headers = new http_1.Headers();
        this.createAuthorizationHeader(headers);
        return this.http.get(this.baseUrl + "/users?name=" + name, { headers: headers })
            .map(function (response) { return response.json(); });
    };
    APIService.prototype.createChat = function (users) {
        var headers = new http_1.Headers();
        this.createAuthorizationHeader(headers);
        var body = new FormData();
        for (var _i = 0, users_1 = users; _i < users_1.length; _i++) {
            var user = users_1[_i];
            body.append('members', user);
        }
        return this.http.post(this.baseUrl + "/chats", body, { headers: headers })
            .map(function (response) { return response.json(); });
    };
    APIService.prototype.addUserToChat = function (chat_id, users) {
        var headers = new http_1.Headers();
        this.createAuthorizationHeader(headers);
        var body = new FormData();
        for (var _i = 0, users_2 = users; _i < users_2.length; _i++) {
            var user = users_2[_i];
            body.append('members', user);
        }
        return this.http.post(this.baseUrl + "/chats/" + chat_id + "/", body, { headers: headers });
    };
    APIService.prototype.sendMessageToUsers = function (users, text) {
        var headers = new http_1.Headers();
        this.createAuthorizationHeader(headers);
        var body = new FormData();
        for (var _i = 0, users_3 = users; _i < users_3.length; _i++) {
            var user = users_3[_i];
            body.append('recipients', user);
        }
        body.append('message', text);
        return this.http.post(this.baseUrl + "/message", body, { headers: headers });
    };
    APIService = __decorate([
        core_1.Injectable(), 
        __metadata('design:paramtypes', [http_1.Http])
    ], APIService);
    return APIService;
}());
exports.APIService = APIService;
//# sourceMappingURL=api.service.js.map