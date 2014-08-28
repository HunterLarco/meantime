(function(){
  
  function Page(frame){
    var self = this;
    self.super(frame);
    
    
    self.reset = Reset;
    
    
    var formlocked = false;
    
    
    function LockForm(){
      formlocked = true;
      self.elements.buttons.skip.classList.add('disabled');
      self.elements.buttons.change.classList.add('disabled');
    }
    function UnlockForm(){
      formlocked = false;
      self.elements.buttons.skip.classList.remove('disabled');
      self.elements.buttons.change.classList.remove('disabled');
    }
    
    function UnlockAccount(){
      if(formlocked) return;
      LockForm();
      self.elements.buttons.skip.innerHTML = 'working';
      app.getUser().unlock(app.pages['inbox'].focus);
    }
    
    function ThrowError(message){
      UnlockForm();
      self.elements.buttons.change.innerHTML = 'Change Password';
      self.elements.error.innerHTML = message;
    }
    function ChangePassword(){
      if(formlocked) return;
      LockForm();
      
      var button             = self.elements.buttons.change,
          oldpassword        = self.elements.password.old,
          newpassword        = self.elements.password.default,
          newpassword_verify = self.elements.password.verify;
      
      if(!newpassword.value || !newpassword_verify.value || !oldpassword.value) return ThrowError('Please Complete All Fields');
      if(newpassword.value != newpassword_verify.value) return ThrowError('New Passwords Must Match');
      
      button.innerHTML = 'working';
      
      var errormap = {};
      errormap[User.ERRORS.INCORRECTCREDENTIALS] = function(){ThrowError('Incorrect Password');}
      
      app.getUser().changePassword(oldpassword.value, newpassword.value, app.pages['inbox'].focus, errormap);
    }
    
    function Reset(){
      self.elements.error.innerHTML = '';
      self.elements.password.default.value = '';
      self.elements.password.verify.value = '';
      self.elements.password.old.value = '';
      self.elements.buttons.change.innerHTML = 'Change Password';
      self.elements.buttons.skip.innerHTML = 'Skip &amp; Unlock';
      UnlockForm();
    }
    
    
    (function Constructor(){
      self.elements.buttons.change.addEventListener('click', ChangePassword);
      self.elements.buttons.skip.addEventListener('click', UnlockAccount);
    })();
  }
  
  
  if(!window.pages) window.pages = {};
  window.pages['passlocked_auth'] = Page;
  
})();