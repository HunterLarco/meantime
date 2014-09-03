function EventListenerClass(){
  var self = this;
  
  
  self.addEventListener = AddEventListener;
  self.removeEventListener = RemoveEventListener;
  self.__events__ = [];
  self.__events__.fire = FireEvent;
  
  
  var listeners = {};
  
  
  function AddEventListener(event, funct){
    if(typeof event != 'string' || typeof funct != 'function') return;
    if(self.__events__.indexOf(event) == -1) self.__events__.push(event);
    if(!listeners[event]) listeners[event] = [];
    listeners[event].push(funct);
  }
  
  
  function RemoveEventListener(event, funct){
    if(typeof event != 'string' || typeof funct != 'function') return;
    if(self.__events__.indexOf(event) != -1) self.__events__.splice(self.__events__.indexOf(event), 1);
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