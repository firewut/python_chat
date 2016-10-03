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
var ChatAPIService = (function () {
    function ChatAPIService(http) {
        this.http = http;
        this.baseUrl = 'http://localhost:8080';
    }
    ChatAPIService.prototype.fetchChats = function () {
        return this.http.get(this.baseUrl + "/chats")
            .map(function (response) { return response.json(); });
    };
    ChatAPIService.prototype.fetchMessages = function (chat_id) {
        return this.http.get((this.baseUrl + "/chats/") + chat_id + "/messages")
            .map(function (response) { return response.json(); });
    };
    ChatAPIService = __decorate([
        core_1.Injectable(), 
        __metadata('design:paramtypes', [http_1.Http])
    ], ChatAPIService);
    return ChatAPIService;
}());
exports.ChatAPIService = ChatAPIService;
//# sourceMappingURL=api-service.js.map