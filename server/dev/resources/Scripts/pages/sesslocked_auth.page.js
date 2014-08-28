(function(){
  
  function Page(frame){
    var self = this;
    self.super(frame);
    
    
    self.reset = Reset;
    
    
    var formlocked = false;
    
    
    function Reset(){
      self.elements.button.innerHTML = 'log in';
      self.elements.error.innerHTML = '';
      self.elements.email.value = '';
      self.elements.error.value = '';
    }
    
    function LockForm(){
      formlocked = true;
      self.elements.button.classList.add('disabled');
      self.elements.button.innerHTML = 'working';
    }
    function UnlockForm(){
      formlocked = false;
      self.elements.button.classList.remove('disabled');
      self.elements.button.innerHTML = 'log in';
    }
    function ThrowError(message){
      self.elements.error.innerHTML = message;
      UnlockForm();
    }
    function Unlock(){
      if(formlocked) return;
      LockForm();
      
      var email = self.elements.email.value,
          password = self.elements.password.value;
      
      if(!email || !password) return ThrowError('Please Complete All Fields');
      
      var errormap = {};
      errormap[User.ERRORS.INCORRECTCREDENTIALS] = function(){ThrowError('Unknown User / Password Combination')}
      errormap[User.ERRORS.INCORRECTCREDENTIALS]
      
      app.getUser().unlock(email, password, app.pages['inbox'].focus, errormap);
    }
    
    
    (function Constructor(){
      self.elements.button.addEventListener('click', Unlock);
    })();
  }
  
  
  if(!window.pages) window.pages = {};
  window.pages['sesslocked_auth'] = Page;
  
})();