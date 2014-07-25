(function(){
  
  var gateway = '';
  
  
  
  
  
  
  var Request = function RequestHandler(url){
    var self = this;
    
    function Instance(data, callback, onerror){
      var timeMemory,
          argumentMemory,
          callback = callback || new Function(),
          onerror = onerror || new Function(),
          data = data || {};
      
      this.post = function(){
        function OnResponse(event){
          if (xmlhttp.readyState==4){
            if(xmlhttp.status==200){
              var data = JSON.parse(event.target.response);
              if(data.stat == 'fail'){
                onerror(new ErrorEvent(data.code, data.message));
              }else{
                CheckNewSession(data);
                callback(data);
              }
            }else if(xmlhttp.status==500){
              onerror(new ErrorEvent(-1, 'Unknown Server Error'));
            };
          };
        }
        
        if(arguments.callee.caller!=RequestJSRetry)
          timeMemory = 0;
        var xmlhttp = !!window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
        argumentMemory = arguments;
        xmlhttp.onreadystatechange = OnResponse;
        xmlhttp.onerror = OnError;
        xmlhttp.open('POST', gateway + url, true);
        AddSessionToPost(data);
        xmlhttp.send(JSON.stringify(data));
      }
      
      function OnError(){
        onerror(new ErrorEvent(-1, 'Request Error!'));
      }
      
      function RequestJSRetry(){
        this.post.apply(this,argumentMemory);
      };
    }
    
    self.post = function RequestJSSend(data,callback,onerror){
      new Instance(data,callback,onerror).post();
    };
    
    var ErrorEvent = function(errorcode,message){
      var event = this;
      this.stat = 'fail';
      this.code = errorcode;
      this.message = message;
      this.retry = function(){
        timeMemory++;
        timeout = Math.pow(2,timeMemory);
        if(timeout>60){timeout=60};
        console.warn('Retrying Request In "'+timeout+'" Seconds');
        setTimeout(RequestJSRetry,timeout*1000);
      };
      this.warn = function(message){
        console.warn(message+'\n    Error Code: '+event.code+'\n    Error Message: "'+event.message+'"');
      };
      this.error = function(message){
        console.error(message+'\n    Error Code: '+event.code+'\n    Error Message: "'+event.message+'"');
      };
    };
  };
  
  
  Request.loadGateway = function(_gateway){
    gateway = _gateway;
  }
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  var storage = window.localStorage;
  
  var uid, ulid, sid;
  LoadSession();
  
  function LoadSession(){
    uid = storage.getItem('uid');
    ulid = storage.getItem('ulid');
    sid = storage.getItem('sid');
  }
  
  function CheckNewSession(data){
    if(!data['setsession']) return;
    if(!!data.session.sid){
      uid = data['session']['uid'];
      storage.setItem('uid', uid);
    }
    if(!!data.session.ulid){
       ulid = data['session']['ulid'];
       storage.setItem('ulid', ulid);
     }
    if(!!data.session.uid){
      sid = data['session']['sid'];
      storage.setItem('sid', sid);
    }
  }
  
  function AddSessionToPost(data){
    if(!!uid) data['uid'] = uid;
    if(!!ulid) data['ulid'] = ulid;
    if(!!sid) data['sid'] = sid;
  }
  
  Request.hasSession = function(){
    return !!uid && !!sid && !!ulid;
  }
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  window.Request = Request;
  
  
})();