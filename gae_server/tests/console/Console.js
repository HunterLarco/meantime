function Console(){
  var con = this;
  
  this.log = Log;
  this.warn = Warn;
  this.error = Err;
  this.openclose = OpenClose;
  
  var frame;
  
  function OpenClose(){
    frame.style.display = frame.style.display == 'block' ? 'none' : 'block';
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
    frame.appendChild(line);
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
    frame = document.createElement('div');
    frame.setAttribute('class', 'console prettyprint');
    document.body.appendChild(frame);
  }
  
  MakeConsole();
  
}