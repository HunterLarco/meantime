(function(){
  
  var gateway = '';
  
  
  var Request = function RequestHandler(url){
    var self = this;
    self.URL = url;
    var _callback, xmlhttp, _onerror;
    function OnError(){
      _onerror('Request Error!');
    }
    function OnResponse(event){
      if (xmlhttp.readyState==4){
        if(xmlhttp.status==200){
          var data = JSON.parse(event.target.response);
          _callback(data);
        }else{
          _onerror('ERROR</br>xmlhttp.status = '+xmlhttp.status)
        };
      };
    }
    self.post = function RequestJSSend(data,callback,onerror){
      _callback = callback || new Function();
      _onerror = onerror || new Function();
      var data = data || {};
      xmlhttp.onreadystatechange=OnResponse;
      xmlhttp.onerror=OnError;
      xmlhttp.open("POST",gateway+url,true);
      xmlhttp.send(JSON.stringify(data));
    };
    self.get = function RequestJSSend(callback,onerror){
      _callback = callback || new Function();
      _onerror = onerror || new Function();
      xmlhttp.onreadystatechange=OnResponse;
      xmlhttp.onerror=OnError;
      xmlhttp.open("GET",gateway+url,true);
      xmlhttp.send();
    };
    if (window.XMLHttpRequest){xmlhttp=new XMLHttpRequest();}else{xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");};
  };
  
  
  Request.loadGateway = function(_gateway){
    gateway = _gateway;
  }
  
  
  window.Request = Request;
  
  
})();