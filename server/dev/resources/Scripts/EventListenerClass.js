function EventListenerClass(){
  this.addEventListener = AddEventListener;
  this.removeEventListener = RemoveEventListener;
  this.__events__ = {};
  this.__events__.fire = FireEvent;
  
  
  var listeners = {};
  
  
  function AddEventListener(event, funct){
    if(typeof event != 'string' || typeof funct != 'function') return;
    if(!listeners[event]) listeners[event] = [];
    listeners[event].push(funct);
  }
  
  
  function RemoveEventListener(event, funct){
    if(typeof event != 'string' || typeof funct != 'function') return;
    if(!listeners[event]) return;
    var index = listeners[event].indexOf(funct);
    while(index>-1){
      listeners[event].splice(index, 1);
      index = listeners[event].indexOf(funct);
    }
  }
  
  
  function FireEvent(event, data){
    var data = data || {};
    data.type = event;
    if(!listeners[event]) return true;
    for(var i=0,funct; funct=listeners[event][i++];)
      if(funct(data) === false) return false;
    return true;
  }
}