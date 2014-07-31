(function(){
  
  var old_add = HTMLElement.prototype.addEventListener;
  HTMLElement.prototype.addEventListener = function(name, funct){
    if(!this.__listeners__) this.__listeners__ = {};
    if(!this.__listeners__[name]) this.__listeners__[name] = [];
    this.__listeners__[name].push(funct);
    old_add.apply(this, arguments);
  };
  
  var old_remove = HTMLElement.prototype.removeEventListener;
  HTMLElement.prototype.removeEventListener = function(name, funct){
    if(!this.__listeners__) this.__listeners__ = {};
    if(!this.__listeners__[name]) this.__listeners__[name] = [];
    var index = this.__listeners__[name].indexOf(funct);
    if(index > -1) this.__listeners__[name].splice(index, 1);
    old_remove.apply(this, arguments);
  };
  
  HTMLElement.prototype.getEventListeners = function(name){
    var array = this.__listeners__[name] || [];
    array.dispatch = function EventDispatch(event){
      for(var i=0,funct; funct=array[i++];)
        if(funct.hasOwnProperty('handleEvent'))
          funct.handleEvent(event);
        else
          funct(event);
    }
    return array;
  }
  
})();