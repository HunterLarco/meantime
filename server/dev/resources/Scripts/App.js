(function(){
  
  // EVENTS: onuserload
  function App(pages){
    var self = app = this;
    self.super();
    
    
    self.Page = EventListenerClass.extend(PageObject);
    
    self.pages = {};
    self.pages.current = GetCurrentPage;
    
    self.hide = HideElement;
    self.show = ShowElement;
    
    self.setUser = SetUser;
    self.getUser = GetUser;
    
    
    var currentpage = null,
        user = null
    
    
    function InitializePages(){
      for(var pagename in pages){
        page = pages[pagename];
        self.pages[pagename] = new (self.Page.extend(page))(document.getElementById(pagename));
      }
    }
    
    function HideElement(frame, callback){
      var callback = typeof callback == 'function' ? callback : new Function();
      frame.classList.add('hideshow');
      setTimeout(function(){
        frame.classList.add('opaque');
        setTimeout(function(){
          frame.classList.add('gone');
          callback();
        }, 520);
      }, 10);
    }
    function ShowElement(frame, callback){
      var callback = typeof callback == 'function' ? callback : new Function();
      frame.classList.add('hideshow');
      frame.classList.remove('gone');
      setTimeout(function(){
        frame.classList.remove('opaque');
        setTimeout(callback, 520);
      }, 10);
    }
    
    function GetCurrentPage(){
      return currentpage;
    }
    
    function SetUser(__user__){
      user = __user__;
      self.__events__.fire('userload');
    }
    function GetUser(){
      return user;
    }
    
    /* PaneObject */
    function PageObject(frame){
      var self = this;
      self.super();
      
      
      self.app = GetApp;
      self.getFrame = GetFrame;
      self.focus = Focus;
      self.blur = Blur;
      self.reset = Function.prototype.extend.ABSTRACT;
      self.elements = {};
      
      
      LoadElements();
      
      
      function LoadElements(){
        function Recurse(frame){
          var elems = frame.children;
          for(var i=0,elem; elem=elems[i++];){
            Recurse(elem);
            var loc = elem.getAttribute('data-name');
            if(!loc) continue;
            var loc = loc.split('.'),
                root = self.elements;
            for(var j=0,piece; piece=loc.slice(0,-1)[j++];){
              if(!root[piece]) root[piece] = {};
              root = root[piece];
            }
            root[loc[loc.length-1]] = elem;
          }
        }
        Recurse(frame);
      }
      
      
      function GetApp(){
        return app;
      }
      
      
      function GetFrame(){
        return frame;
      }
      
      
      function Blur(callback){
        var event = {callback:null};
        if(!self.__events__.fire('blur', event)) return;
        function __callback__(){
          if(typeof callback == 'function') callback();
          if(typeof event.callback == 'function')
            event.callback();
          self.derived.derived.reset();
        }
        app.hide(frame, __callback__);
      }
      
      
      function Focus(callback){
        var event = {callback:null};
        if(!self.__events__.fire('focus', event)) return;
        function __callback__(){
          if(typeof callback == 'function') callback();
          if(typeof event.callback == 'function')
            event.callback();
        }
        function __focus__(){
          currentpage = self;
          app.show(frame, __callback__);
        }
        if(app.pages.current() == null)
          __focus__();
        else
          app.pages.current().blur(__focus__);
      };
      
      
    }
    /* End of PaneObject */
    
    
    (function Constructor(){
      InitializePages();
    })();
  }
  App = EventListenerClass.extend(App);
  
  
  App.AUTHOR = 'Hunter John Larco';
  App.VERSION = 'v0.0.0';
  
  
  window.App = App;
  
})();