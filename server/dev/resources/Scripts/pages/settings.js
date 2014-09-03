(function(){
  
  function LoadSettings(){
  	var sidebar = new Sidebar(
      document.getElementById('sidebar'),
      document.getElementById('header_settingsbutton')
    );
    var tree = sidebar.tree();
    
    /* ----------------------- ON CAPTURE CLOSE SETTINGS ----------------------- */
    
    document.getElementById('header_capturebutton').addEventListener('click', sidebar.hide);
  
    /* ----------------------- LOGOUT ----------------------- */

    tree.menu.children.logout.self.addEventListener('click', Logout);
    function Logout(){
      app.getUser().logout();
      sidebar.toggle();
      location.reload()
    }
  
    /* ----------------------- ACCOUNT NOTIFICATIONS ----------------------- */
  
    app.addEventListener('userload', RenderAccountDetails);
    if(!!app.getUser()) RenderAccountDetails();
    function RenderAccountDetails(){
      var user = app.getUser();
      
      (function BindFullName(){
        var title  = document.getElementById('sidebar_name'),
            input  = document.getElementById('sidebar_name_input'),
            button = document.getElementById('sidebar_name_button');
        
        if(!user.getFullName())
          tree.menu.children.account.menu.children.name.setNotifications(1);
        
        title.innerHTML   = user.getFullName() || '';
        input.placeholder = user.getFullName() || 'Prince Leah';
        button.addEventListener('click', SendUpdate);
        
        function SendUpdate(event){
          event.stopPropagation();
          if(input.value.length == 0) return;
          if(input.value.split(' ').length < 2) return;
          user.setFullName(input.value);
          title.innerHTML = input.value;
          input.placeholder = input.value;
          input.value = '';
          tree.menu.children.account.menu.children.name.menu.back.click();
          tree.menu.children.account.menu.children.name.setNotifications(0);
        }
      })();
      
      (function BindMobileNumber(){
        var title  = document.getElementById('sidebar_mobile'),
            input  = document.getElementById('sidebar_mobile_input'),
            button = document.getElementById('sidebar_mobile_button');
        
        if(!user.getMobileNumber())
          tree.menu.children.account.menu.children.mobile.setNotifications(1);
        
        title.innerHTML   = user.getMobileNumber() || '';
        input.placeholder = user.getMobileNumber() || '555 555-5555';
        button.addEventListener('click', SendUpdate);
        
        function SendUpdate(event){
          event.stopPropagation();
          if(input.value.length == 0) return;
          if(input.value.replace(/[^0-9]/g,'').length < 7) return;
          user.setMobileNumber(input.value);
          title.innerHTML = input.value;
          input.placeholder = input.value;
          input.value = '';
          tree.menu.children.account.menu.children.mobile.menu.back.click();
          tree.menu.children.account.menu.children.mobile.setNotifications(0);
        }
      })();
      
      (function BindEmail(){
        var title  = document.getElementById('sidebar_email'),
            input  = document.getElementById('sidebar_email_input'),
            button = document.getElementById('sidebar_email_button');
        
        title.innerHTML   = user.getEmail();
        input.placeholder = user.getEmail();
        button.addEventListener('click', SendUpdate);
        
        function SendUpdate(event){
          event.stopPropagation();
          if(input.value.length == 0) return;
          var isValidEmail = (/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/).test(input.value);
          if(!isValidEmail) return;
          user.setEmail(input.value);
          title.innerHTML = input.value;
          input.placeholder = input.value;
          input.value = '';
          tree.menu.children.account.menu.children.email.menu.back.click();
        }
      })();
      
      (function BindChangePassword(){
        var input    = document.getElementById('sidebar_changepassword'),
            input2   = document.getElementById('sidebar_changepassword_verify'),
            oldinput = document.getElementById('sidebar_changepassword_old'),
            button   = document.getElementById('sidebar_changepassword_button');
        
        button.addEventListener('click', SendUpdate);
        
        function SendUpdate(event){
          event.stopPropagation();
          if(input.value.length == 0 || input2.value.length == 0) return;
          if(input.value != input2.value) return;
          
          var errormap = {};
          errormap[User.ERRORS.INCORRECTCREDENTIALS] = function(){
            return;
          }
          
          user.changePassword(oldinput.value, input.value, 
            function OnSuccess(){
              input.value  = '';
              input2.value = '';
              oldinput.value = ''
              tree.menu.children.account.menu.children.password.menu.back.click();
            }, errormap
          );
        }
      })();
      
      (function BindDelete(){
        var button  = document.getElementById('sidebar_delete_button');
        
        button.addEventListener('click', SendUpdate);
        
        function SendUpdate(event){
          app.getUser().delete(function(){
            location.reload();
          });
        }
      })();
    }
  
  };
  
  
  window.Settings = {};
  window.Settings.load = LoadSettings;
  
})();