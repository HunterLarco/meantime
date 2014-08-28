(function(){
  
  function InboxPage(frame){
    var self = this;
    self.super(frame);
    
    
    self.reset = Reset;
    
    
    function Reset(){}
    
    function ShowHeaderButtons(){
      app.show(document.getElementById('header_buttons'));
    }
    
    
    (function Constructor(){
      self.addEventListener('focus', ShowHeaderButtons);
    })();
  }
  
  
  if(!window.pages) window.pages = {};
  window.pages['inbox'] = InboxPage;
  
})();