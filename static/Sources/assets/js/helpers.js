"use strict";
window.addEventListener("DOMContentLoaded", () => {
    const login = new LoginForm("form");
});
class LoginForm {
    /**
     * @param el CSS selector of the form element
     */
    constructor(el) {
        var _a, _b;
        /** Timeout for the login attempt */
        this.loginTimeout = 0;
        /** Username entered in the form */
        this._username = "";
        /** Password entered in the form */
        this._password = "";
        /** Display the password. */
        this._passwordShow = false;
        /** There are errors with the user input. */
        this._hasErrors = false;
        /** User is logging in. */
        this._loginWorking = false;
        this.el = document.querySelector(el);
        (_a = this.el) === null || _a === void 0 ? void 0 : _a.addEventListener("click", this.passwordShowToggle.bind(this));
      
    }
   
  
    
  
  
    passwordShowToggle(e) {
        const { target } = e;
        const eye = target;
        if (eye.hasAttribute("data-password-show")) {
            this.passwordShow = !this.passwordShow;
        }
    }
}
var PasswordDisplay;
(function (PasswordDisplay) {
    PasswordDisplay["Off"] = "off";
    PasswordDisplay["On"] = "on";
})(PasswordDisplay || (PasswordDisplay = {}));
var PasswordDisplayLabel;
(function (PasswordDisplayLabel) {
    PasswordDisplayLabel["Hide"] = "Hide password";
    PasswordDisplayLabel["Show"] = "Show password";
})(PasswordDisplayLabel || (PasswordDisplayLabel = {}));
