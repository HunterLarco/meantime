(function(){
  
  
  
  function BindLogin(){
    var email = document.getElementById('sessionlocked_email'),
        password = document.getElementById('sessionlocked_password'),
        button = document.getElementById('sessionlocked_button'),
        error = document.getElementById('sessionlocked_error');
    button.addEventListener('click', SendLogin);
    var sending = false;
    function RunError(callback){
      sending = false;
      button.innerHTML = 'log in';
      button.classList.remove('disabled');
      callback();
    }
    function UnknownError(){
      error.innerHTML = 'Uh Oh... Unknown Error!';
    }
    function IncorrectPassword(){
      error.innerHTML = 'Email Password Combination Not Recognized';
    }
    function OnError(event){
      switch(event.code){
        case 201: return RunError(IncorrectPassword);
        default: return RunError(UnknownError);
      }
    }
    function Callback(){
      app.hideshow(document.getElementById('sessionlocked_frame'), document.getElementById('inbox_frame'));
      setTimeout(function(){app.show(document.getElementById('header_buttons'));}, 550);
    }
    function SendLogin(){
      if(sending) return;
      sending = true;
      error.innerHTML = '';
      button.innerHTML = 'working...';
      button.classList.add('disabled');
      var request = new Request('user/unlock');
      request.post({
        email: email.value,
        password: password.value
      }, Callback, OnError);
    }
  }


  window.addEventListener('load', function(){
    BindLogin();
  });
  
  
  
})();