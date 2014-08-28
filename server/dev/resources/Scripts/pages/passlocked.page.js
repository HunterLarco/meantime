(function(){
  
  function Page(frame){
    var self = this;
    self.super(frame);
    
    
    self.reset = new Function();

    
    (function Constructor(){})();
  }
  
  
  if(!window.pages) window.pages = {};
  window.pages['passlocked'] = Page;
  
})();