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
var SignupComponent = (function () {
    function SignupComponent(_APIService, router) {
        this._APIService = _APIService;
        this.router = router;
    }
    SignupComponent.prototype.registerUser = function (form) {
        var _this = this;
        this.error = false;
        var name = form.value.name;
        this._APIService.registerUser(name)
            .subscribe(function (res) {
            _this._APIService.SessionId = res.SessionId;
            localStorage.setItem('SessionId', _this._APIService.SessionId);
            _this.router.navigate(['/chat']);
        }, function (error) { _this.error = true; _this.errorMessage = error; });
    };
    SignupComponent = __decorate([
        core_1.Component({
            selector: 'signup',
            templateUrl: './app/templates/signup.component.html',
        }), 
        __metadata('design:paramtypes', [api_service_1.APIService, router_1.Router])
    ], SignupComponent);
    return SignupComponent;
}());
exports.SignupComponent = SignupComponent;
//# sourceMappingURL=signup.component.js.map