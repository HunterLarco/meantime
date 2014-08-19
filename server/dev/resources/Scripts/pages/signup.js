(function(){


  
  
  function BindSignup(){
    var email = document.getElementById('signup_s_email'),
        password = document.getElementById('signup_s_password'),
        password2 = document.getElementById('signup_s_password2'),
        button = document.getElementById('signup_s_button'),
        error = document.getElementById('signup_error');
    button.addEventListener('click', SendSignup);
    var sending = false;
    function RunError(callback){
      sending = false;
      button.innerHTML = 'sign up';
      button.classList.remove('disabled')
      callback();
    }
    function InvalidEmail(){
      error.innerHTML = 'Invalid Email';
    }
    function PasswordsMismatch(){
      error.innerHTML = 'Passwords Don\'t Match';
    }
    function NoPassword(){
      error.innerHTML = 'Please Provide a Password';
    }
    function EmailUsed(){
      error.innerHTML = 'Email Already In Use';
    }
    function UnknownError(){
      error.innerHTML = 'Uh Oh... Unknown Error!';
    }
    function OnError(event){
      switch(event.code){
        case 200: return RunError(EmailUsed);
        default: return RunError(UnknownError);
      }
    }
    function Callback(){
      app.hideshow(document.getElementById('signup_frame'), document.getElementById('inbox_frame'));
      setTimeout(function(){app.show(document.getElementById('header_buttons'));}, 550);
    }
    function SendSignup(){
      if(sending) return;
      sending = true;
      error.innerHTML = '';
      // check email
      var isValidEmail = (/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/).test(email.value);
      if(!isValidEmail) return RunError(InvalidEmail);
      // check passwords
      if(password.value.length == 0) return RunError(NoPassword);
      if(password.value != password2.value) return RunError(PasswordsMismatch);
      // send
      button.innerHTML = 'working...';
      button.classList.add('disabled')
      var request = new Request('user/signup');
      request.post({
        email: email.value,
        password: password.value
      }, Callback, OnError);
    }
  }




  function BindLogin(){
    var email = document.getElementById('signup_l_email'),
        password = document.getElementById('signup_l_password'),
        button = document.getElementById('signup_l_button'),
        error = document.getElementById('signup_error');
    button.addEventListener('click', SendLogin);
    var sending = false;
    function RunError(callback){
      sending = false;
      button.innerHTML = 'log in';
      button.classList.remove('disabled')
      callback();
    }
    function UnknownError(){
      error.innerHTML = 'Uh Oh... Unknown Error!';
    }
    function UserDoesntExist(){
      error.innerHTML = 'Email Password Combination Not Recognized';
    }
    function IncorrectPassword(){
      error.innerHTML = 'Email Password Combination Not Recognized';
    }
    function BruteSuspected(){
      app.hideshow(document.getElementById('signup_frame'), document.getElementById('passlocked_frame'));
    }
    function OnError(event){
      switch(event.code){
        case 203: return RunError(UserDoesntExist);
        case 201: return RunError(IncorrectPassword);
        case 202: return BruteSuspected();
        default: return RunError(UnknownError);
      }
    }
    function Callback(){
      app.hideshow(document.getElementById('signup_frame'), document.getElementById('inbox_frame'));
      setTimeout(function(){app.show(document.getElementById('header_buttons'));}, 550);
    }
    function SendLogin(){
      if(sending) return;
      sending = true;
      error.innerHTML = '';
      button.innerHTML = 'working...';
      button.classList.add('disabled')
      var request = new Request('user/login');
      request.post({
        email: email.value,
        password: password.value
      }, Callback, OnError);
    }
  }




  function BindToggleButtons(){
    document.getElementById('signup_gotologin').addEventListener('click', Toggle);
    document.getElementById('signup_gotosignup').addEventListener('click', Toggle);
    function Toggle(){
      document.getElementById('signup_frame').classList.toggle('login');
    }
  }


  
  window.addEventListener('load', function(){
    BindToggleButtons();
    BindSignup();
    BindLogin();
  });




})();