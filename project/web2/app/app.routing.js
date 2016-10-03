"use strict";
var router_1 = require('@angular/router');
var home_component_1 = require('./home.component');
var signup_component_1 = require('./signup.component');
var chat_component_1 = require('./chat.component');
var appRoutes = [
    { path: '', component: home_component_1.HomeComponent },
    { path: 'signup', component: signup_component_1.SignupComponent },
    { path: 'chat', component: chat_component_1.ChatComponent },
];
exports.appRoutingProviders = [];
exports.routing = router_1.RouterModule.forRoot(appRoutes);
//# sourceMappingURL=app.routing.js.map