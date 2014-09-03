(function(){
  
  function Page(frame){
    var self = this;
    self.super(frame);
    
    
    self.reset = new Function();
    
    
    var formlocked = false;
    
    
    function Reset(){
      self.elements.frames.contacts.innerHTML = '';
      checkboxes = [];
      self.elements.buttons.continue.classList.remove('disabled');
      formlocked = false;
      self.elements.buttons.disappearing.checked = false;
    }
    
    function CheckContinueButton(){
      var contacts = GetSelectedContacts();
      if(contacts.length == 0) self.elements.buttons.continue.classList.add('disabled');
      else self.elements.buttons.continue.classList.remove('disabled');
    }
    function Send(){
      if(self.elements.buttons.continue.classList.contains('disabled') || formlocked) return;
      formlocked = true;
      
      self.elements.buttons.continue.innerHTML = 'working';
      
      var timestamp = app.pages['datepicker'].getDate().getTime(),
          contacts = GetSelectedContacts(),
          image = app.pages['capture'].getCapture(),
          disappearing = self.elements.buttons.disappearing.checked;
      
      app.getUser().sendMessage(image, contacts, timestamp, disappearing, function OnSuccess(){
        self.elements.buttons.continue.innerHTML = 'send message';
        app.pages['inbox'].focus();
      });
    }
    
    function LoadDate(){
      self.elements.labels.date.innerHTML = FormatDate(app.pages['datepicker'].getDate());
    }
    
    function FormatDate(date){
      var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      var hour = date.getHours()%12 == 0 ? 12 : date.getHours()%12,
          minute = ((date.getMinutes()+'').length == 1 ? '0' : '') + date.getMinutes(),
          ampm = date.getHours() >= 12 ? 'pm' : 'am';
      return months[date.getMonth()]+' '+date.getDate()+', '+date.getFullYear()+', at '+hour+':'+minute+''+ampm;
    }
    
    
    // ------------------- BEGINNING OF CONTACT CODE ------------------- //
    
    var checkboxes = [];
    
    function GetSelectedContacts(){
      var list = [];
      for(var i=0,checkbox; checkbox=checkboxes[i++];){
        if(!checkbox.checked) continue;
        if(!!checkbox.contact.email) list.push(checkbox.contact.email);
        else if(!!checkbox.contact.mobile) list.push(checkbox.contact.mobile);
      }
      return list;
    }
    
    function LoadContacts(){
      var contacts = app.pages['datepicker'].getContacts();
      
      for(var i=0,contact; contact=contacts[i++];){
        var title = contact.name || contact.email || contact.mobile;
        
        var div = document.createElement('div');
        div.classList.add('contact');
          var checkbox = document.createElement('input');
          checkbox.setAttribute('type', 'checkbox');
          checkbox.contact = contact;
          checkbox.addEventListener('click', CheckContinueButton);
          checkbox.checked = true;
          checkboxes.push(checkbox);
          div.appendChild(checkbox);
          var text = document.createElement('div');
          text.classList.add('text');
          text.innerHTML = title;
          div.appendChild(text);
        
        self.elements.frames.contacts.appendChild(div);
      }
    }
    
    // ------------------- END OF CONTACT CODE ------------------- //
    
    
    (function Constructor(){
      self.addEventListener('focus', function(){
        Reset();
        LoadContacts();
        LoadDate();
      });
      self.elements.buttons.back.addEventListener('click', function(){app.pages['datepicker'].focus()});
      self.elements.buttons.continue.addEventListener('click', Send);
    })();
  }
  
  
  if(!window.pages) window.pages = {};
  window.pages['sendmessage'] = Page;
  
})();