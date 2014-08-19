(function(){
  
  
  
  var formlocked = false;


  function BindChangePassword(){
    document.getElementById('passlocked_changepass').addEventListener('click', ChangePassword);
  }


  function BindUnlock(){
    document.getElementById('passlocked_unlock').addEventListener('click', UnlockAccount);
  }


  function LockForm(){
    formlocked = true;
    var unlock = document.getElementById('passlocked_unlock'),
        changepass = document.getElementById('passlocked_changepass');
    unlock.classList.add('disabled');
    changepass.classList.add('disabled');
  }


  function UnlockForm(){
    formlocked = false;
    var unlock = document.getElementById('passlocked_unlock'),
        changepass = document.getElementById('passlocked_changepass');
    unlock.classList.remove('disabled');
    changepass.classList.remove('disabled');
  }


  function UnlockAccount(){
    if(formlocked) return;
    LockForm();
    var unlock = document.getElementById('unlock');
    unlock.innerHTML = 'working';
    var request = new Request('user/unlock');
    function Callback(event){
      app.hideshow(document.getElementById('passlocked_frame'), document.getElementById('inbox_frame'));
    }
    function OnError(event){
      UnlockForm();
      unlock.innerHTML = 'Skip &amp; Unlock';
      UnexpectedError();
    }
    request.post({}, Callback, OnError);
  }


  function UnexpectedError(){
    document.getElementById('passlocked_error').innerHTML = 'Uh Oh... Unkown Error!';
  }
  function OnEmptyFields(){
    document.getElementById('passlocked_error').innerHTML = 'Please fill out all fields';
  }
  function OnNoPassMatch(){
    document.getElementById('passlocked_error').innerHTML = 'You\'re passwords do not match';
  }
  function OnOldPassFailure(){
    document.getElementById('passlocked_error').innerHTML = 'Incorrect Password';
  }


  function ChangePassword(){
    if(formlocked) return;
    LockForm();
  
    var button = document.getElementById('passlocked_changepass'),
        oldpassword = document.getElementById('passlocked_oldpass'),
        newpassword = document.getElementById('passlocked_newpass'),
        newpassword2 = document.getElementById('passlocked_newpass2');
  
    if(!newpassword.value || !newpassword2.value || !oldpassword.value) return OnError({code:-100});
    if(newpassword.value != newpassword2.value) return OnError({code:-101});
  
    button.innerHTML = 'working';
    var request = new Request('user/changepassword');
    function Callback(event){
      app.hideshow(document.getElementById('passlocked_frame'), document.getElementById('inbox_frame'));
      setTimeout(function(){app.show(document.getElementById('header_buttons'));}, 550);
    }
    function OnError(event){
      UnlockForm();
      button.innerHTML = 'Change Password';
      if(event.code == -100) return OnEmptyFields();
      if(event.code == -101) return OnNoPassMatch();
      if(event.code == 201) return OnOldPassFailure();
      return UnexpectedError();
    }
    request.post({
      'password': newpassword.value,
      'old_password': oldpassword.value
    }, Callback, OnError);
  }





  window.addEventListener('load', function(){
    BindChangePassword();
    BindUnlock();
  });
  
  
  
})();