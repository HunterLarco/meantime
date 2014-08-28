(function(){
  
  function Page(frame){
    var self = this;
    self.super(frame);
    
    
    self.reset =  Reset;
    
    
    function Reset(){
      
    }
    
    
    (function Constructor(){
      
    })();
  }
  
  
  if(!window.pages) window.pages = {};
  window.pages[pagename] = Page;
  
})();