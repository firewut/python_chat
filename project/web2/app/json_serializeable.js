"use strict";
var Serializable = (function () {
    function Serializable() {
    }
    Serializable.prototype.fillFromJSON = function (json) {
        var jsonObj = JSON.parse(json);
        for (var propName in jsonObj) {
            this[propName] = jsonObj[propName];
        }
    };
    return Serializable;
}());
exports.Serializable = Serializable;
//# sourceMappingURL=json_serializeable.js.map