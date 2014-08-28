(function(){
  
  function FirstVisitPage(frame){
    var self = this;
    self.super(frame);
    
    
    self.reset = new Function();
    
    
    function BindContinueButton(){
      self.elements.buttons.continue.addEventListener('click', self.app().pages['signup'].focus);
    }
    function SetDoneFlag(){
      User.Cookies.set('firstvisit', 'done');
    }
    
    
    (function Constructor(){
      BindContinueButton();
      self.addEventListener('blur', SetDoneFlag);
    })();
  }
  
  
  if(!window.pages) window.pages = {};
  window.pages['firstvisit'] = FirstVisitPage;
  
})();