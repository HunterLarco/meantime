(function(){
  
  function Page(frame){
    var self = this;
    self.super(frame);
    
    
    self.getContacts = GetSelectedContacts;
    self.reset =  Reset;
    
    
    function Reset(){
      self.elements.input.value = '';
      self.elements.buttons.self.checked = false;
    }
    
    function GotoCapture(){
      app.pages['capture'].focus();
    }
    function GotoDatePicker(){
      if(!self.elements.buttons.continue.classList.contains('ready')) return;
      app.pages['datepicker'].focus();
    }
    
    function BindEnterKey(event){
      if(event.which != 13) return;
      
      var value = self.elements.input.value,
          type;

      var isValidEmail = (/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/).test(value),
          type = isValidEmail ? 'email' : 'mobile';

      if(type == 'mobile' && value.replace(/[^0-9]/g,'').length <= 5) return;

      var contact = document.createElement('div');
      contact.classList.add('contact');
          var checkbox = document.createElement('input');
          checkbox.setAttribute('type', 'checkbox');
          checkbox.contact = {};
          checkbox.contact[type] = value;
          checkbox.addEventListener('click', CheckContinueButton);
          contact.appendChild(checkbox);
          var text = document.createElement('div');
          text.classList.add('text');
          text.innerHTML = value;
          contact.appendChild(text);
      
      var frame = self.elements.frames.contacts.new;
      
      if(frame.children.length < 3)
        frame.appendChild(contact);
      else
        frame.insertBefore(contact, frame.children[2]);
        
      setTimeout(checkbox.click.bind(checkbox), 10);
      self.elements.input.value = '';
    }
    
    function GetSelectedContacts(){
      var contacts = frame.getElementsByTagName('input'),
          list = [];
      for(var i=0,input; input=contacts[i++];){
        if(input.getAttribute('type') != 'checkbox') continue;
        var contact = input.contact;
        if(!contact) continue;
        if(input.checked) list.push(contact);
      }
      return list;
    }
    function CheckContinueButton(){
      var contacts = GetSelectedContacts();
      if(contacts.length > 0)
        self.elements.buttons.continue.classList.add('ready');
      else
        self.elements.buttons.continue.classList.remove('ready');
    }
    
    function LoadSelfContact(){
      self.elements.buttons.self.contact = {};
      self.elements.buttons.self.contact['email'] = app.getUser().getEmail();
      self.elements.buttons.self.contact['name'] = 'self';
      if(!!app.getUser().getMobileNumber())
        self.elements.buttons.self.contact['mobile'] = app.getUser().getMobileNumber();
    }
    
    
    (function Constructor(){
      if(!!app.getUser()) LoadSelfContact();
      else app.addEventListener('userload', LoadSelfContact);
      self.elements.buttons.self.addEventListener('click', CheckContinueButton);
      self.elements.buttons.back.addEventListener('click', GotoCapture);
      self.elements.buttons.continue.addEventListener('click', GotoDatePicker);
      self.elements.input.addEventListener('keyup', BindEnterKey);
    })();
  }
  
  
  if(!window.pages) window.pages = {};
  window.pages['contacts'] = Page;
  
})();