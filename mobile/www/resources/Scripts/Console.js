function Console(){
  var self = this;
  
  self.log = Log;
  self.warn = Warn;
  self.error = Err;
  self.openclose = OpenClose;
  
  self.__frame__;
  
  function OpenClose(){
    self.__frame__.style.display = self.__frame__.style.display == 'block' ? 'none' : 'block';
  }
  
  function _log(){
    var shift = [].shift,
        join = [].join,
        color = shift.apply(arguments),
        messages = arguments;
    for(var i=0,message; message=messages[i++];)
      messages[i-1] = PrettyPrint(message);
    var line = document.createElement('div');
    line.setAttribute('class', 'line '+color);
    line.innerHTML = join.call(messages, '&nbsp;&nbsp;&nbsp;&nbsp;');
    self.__frame__.appendChild(line);
  }
  
  function Log(){
    var unshift = [].unshift;
    unshift.call(arguments, 'log');
    _log.apply(con, arguments);
  }
  
  function Err(){
    var unshift = [].unshift;
    unshift.call(arguments, 'error');
    _log.apply(con, arguments);
  }
  
  function Warn(){
    var unshift = [].unshift;
    unshift.call(arguments, 'warning');
    _log.apply(con, arguments);
  }
  
  function MakeConsole(){
    self.__frame__ = document.createElement('div');
    self.__frame__.setAttribute('class', 'console prettyprint');
    document.body.appendChild(self.__frame__);
  }
  
  MakeConsole();
  
}