(function(){
  
  function Page(frame){
    var self = this;
    self.super(frame);
    
    
    self.getCapture = GetCapture;
    self.reset = Reset;
    
    
    var video, recording = false;
    
    
    function GetCapture(){
      if(!video) return '';
      return video.getDataURI();
    }
    
    function BeginWebcam(){
      if(!!video){
        video.restart();
        return;
      }
      video = new Camera(self.elements.video.canvas);
      video.addEventListener('record', function(){
        app.hide(self.elements.video.notice);
        recording = true;
        self.elements.buttons.snap.classList.add('usable');
      });
      video.record();
    }
    
    function TakePicture(){
      if(!recording) return;
      self.elements.buttons.snap.removeEventListener('click', TakePicture);
      self.elements.buttons.cancel.addEventListener('click', Cancel);
      self.elements.buttons.continue.addEventListener('click', Continue);
      video.capture();
      ToggleButtons();
    }
    
    function Cancel(){
      ToggleButtons();
      self.elements.buttons.cancel.removeEventListener('click', Cancel);
      self.elements.buttons.continue.removeEventListener('click', Continue);
      self.elements.buttons.snap.addEventListener('click', TakePicture);
    }
    function Continue(){
      app.pages['contacts'].focus();
    }
    
    function ToggleButtons(){
      self.elements.buttons.snap.classList.toggle('usable');
      self.elements.buttons.cancel.classList.toggle('usable');
      self.elements.buttons.continue.classList.toggle('usable');
    }
    
    function Reset(){
      self.elements.buttons.snap.classList.add('usable');
      self.elements.buttons.cancel.classList.remove('usable');
      self.elements.buttons.continue.classList.remove('usable');
      self.elements.buttons.snap.addEventListener('click', TakePicture);
      video.stop();
    }
    
    
    (function Constructor(){
      self.addEventListener('focus', BeginWebcam);
      self.elements.buttons.snap.addEventListener('click', TakePicture);
    })();
  }
  
  
  if(!window.pages) window.pages = {};
  window.pages['capture'] = Page;
  
})();