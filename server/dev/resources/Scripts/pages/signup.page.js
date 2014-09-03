(function(){
  
  function SignupPage(frame){
    var self = this;
    self.super(frame);
    
    
    self.reset = Reset;
    
    
    var formlocked = false;
    
    
    self.addEventListener('blur', ShowHeaderButtons);
    self.addEventListener('focus', HideHeaderButtons);
    
    
    function HideHeaderButtons(){
      self.app().hide(document.getElementById('header_buttons'));
    }
    function ShowHeaderButtons(){
      self.app().show(document.getElementById('header_buttons'));
    }
    
    function UserLoad(user){
      app.setUser(user);
      GotoInbox();
    }
    function GotoInbox(){
      self.app().pages['inbox'].focus();
    }
    
    function EnableForm(){
      self.elements.goto.login.classList.remove('disabled');
      self.elements.goto.signup.classList.remove('disabled');
      self.elements.login.button.classList.remove('disabled');
      self.elements.signup.button.classList.remove('disabled');
      self.elements.login.button.innerHTML = 'log in';
      self.elements.signup.button.innerHTML = 'sign up';
    }
    function DisableForm(){
      self.elements.goto.login.classList.add('disabled');
      self.elements.goto.signup.classList.add('disabled');
      self.elements.login.button.classList.add('disabled');
      self.elements.signup.button.classList.add('disabled');
      self.elements.login.button.innerHTML = 'working';
      self.elements.signup.button.innerHTML = 'working';
    }
    
    function ThrowError(message){
      if(!message) return;
      self.elements.error.innerHTML = message;
      formlocked = false;
    }
    function SendLogin(){
      if(formlocked) return;
      formlocked = true;
      var email = self.elements.login.email.value,
          password = self.elements.login.password.value;
      if(!email || !password) return ThrowError('Please Complete All Fields');
      var errormap = {};
      errormap[User.ERRORS.INCORRECTCREDENTIALS] = function(){ThrowError('Email &amp; Password Combination Not Recognized');};
      errormap[User.ERRORS.USERDOESNTEXIST]      = function(){ThrowError('Email &amp; Password Combination Not Recognized');};
      errormap[User.ERRORS.BRUTEFORCE] = function(){app.pages['passlocked'].focus();};
      errormap['default'] = function(){ThrowError('Uh Oh! Unknown Error');}
      errormap['always'] = EnableForm
      DisableForm();
      User.login(email, password, UserLoad, errormap);
    }
    function SendSignup(){
      if(formlocked) return;
      formlocked = true;
      var email = self.elements.signup.email.value,
          password = self.elements.signup.password.default.value;
          password_verify = self.elements.signup.password.verify.value;
      if(!email || !password || !password_verify) return ThrowError('Please Complete All Fields');
      if(password != password_verify) return ThrowError('Passwords Must Match');
      var isValidEmail = (/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/).test(email);
      if(!isValidEmail) return ThrowError('Please Use A Valid Email');
      var errormap = {};
      errormap[User.ERRORS.EMAILUSED] = function(){ThrowError('Email Already In Use');};
      errormap['default'] = function(){ThrowError('Uh Oh! Unknown Error');}
      errormap['always'] = EnableForm
      DisableForm();
      User.signup(email, password, UserLoad, errormap);
    }
    
    function BindSubmitButtons(){
      self.elements.login.button.addEventListener('click', SendLogin);
      self.elements.signup.button.addEventListener('click', SendSignup);
    }
    function BindToggleButtons(){
      self.elements.goto.login.addEventListener('click', Toggle);
      self.elements.goto.signup.addEventListener('click', Toggle);
      function Toggle(event){
        if(event.target.classList.contains('disabled')) return;
        frame.classList.toggle('login');
      }
    }
    function BindEnterKey(){
      var signup_fields = [
            self.elements.signup.email,
            self.elements.signup.password.default,
            self.elements.signup.password.verify
          ],
          login_fields = [
            self.elements.login.email,
            self.elements.login.password
          ];
      
      for(var i=0,field; field=signup_fields[i++];)
        field.addEventListener('keyup', MoveToNextSignup);
      
      for(var i=0,field; field=login_fields[i++];)
        field.addEventListener('keyup', MoveToNextLogin);
      
      function MoveToNextSignup(event){
        MoveToNext(event, signup_fields, SendSignup);
      }
      
      function MoveToNextLogin(event){
        MoveToNext(event, login_fields, SendLogin);
      }
      
      function MoveToNext(event, fields, OnSuccess){
        if(event.which != 13) return;
        for(var i=0,field; field=fields[i++];)
          if(field.value.length == 0)
            return field.focus();
        if(typeof OnSuccess == 'function') OnSuccess();
      }
    }
    
    function Reset(){
      self.elements.signup.email.value = '';
      self.elements.signup.password.default.value = '';
      self.elements.signup.password.verify.value = '';
      self.elements.signup.button.innerHTML = 'sign up';
      
      self.elements.login.email.value = '';
      self.elements.login.password.value = '';
      self.elements.login.button.innerHTML = 'log in';
      
      formlocked = false;
      EnableForm();
    }
    
    
    (function Constructor(){
      BindEnterKey();
      BindToggleButtons();
      BindSubmitButtons();
    })();
  }
  
  
  if(!window.pages) window.pages = {};
  window.pages['signup'] = SignupPage;
  
})();