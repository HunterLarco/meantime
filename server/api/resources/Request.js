(function(){
  
  var gateway = '{{gateway|safe}}';
  
  
  
  
  
  
  var Request = function RequestHandler(url){
    var self = this;
    
    function Instance(data, callback, onerror){
      var timeMemory,
          argumentMemory,
          usedfunct,
          callback = callback || new Function(),
          onerror = onerror || new Function(),
          data = data || {};
      
      function CreateCorsRequest(method, url){
        var xhr = !!window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
        if ("withCredentials" in xhr) {
          xhr.open(method, url, true);
        } else if (typeof XDomainRequest != "undefined") {
          xhr = new XDomainRequest();
          xhr.open(method, url);
        } else {
          // CORS not supported.
          xhr = null;
        }
        return xhr;
      }
      
      function SetupRequest(requestargs, method, url){
        if(requestargs.callee.caller != RequestJSRetry)
          timeMemory = 0;
        usedfunct = requestargs.callee;
        argumentMemory = requestargs;
        var xmlhttp = CreateCorsRequest(method, url);
        if(!xmlhttp){
          OnError(new ErrorEvent(-1, 'Cors Not Enabled In This Browser'));
          return;
        }
        xmlhttp.onreadystatechange = OnResponse;
        xmlhttp.onerror = OnError;
        return xmlhttp;
      }
      
      function OnResponse(event){
        var xmlhttp = event.target;
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
            if(!!window.app && !!window.app.console)
              window.app.console.error('XMLHTTP STATUS 500');
            onerror(new ErrorEvent(-1, 'Unknown Server Error'));
          };
        };
      }
      
      this.post = function(){
        var xmlhttp = SetupRequest(arguments, 'POST', gateway + url);
        if(!xmlhttp) return;
        AddSessionToPost(data);
        xmlhttp.send(JSON.stringify(data));
      }
      
      this.get = function(){
        var xmlhttp = SetupRequest(arguments, 'POST', gateway + url);
        xmlhttp.send();
      }
      
      function OnError(event){
        onerror(new ErrorEvent(-2, 'Request Error!'));
      }
      
      function RequestJSRetry(){
        usedfunct.apply(this,argumentMemory);
      };
      
      var ErrorEvent = function(errorcode,message){
        var event = this;
        this.stat = 'fail';
        this.code = errorcode;
        this.message = message;
        this.retry = function(){
          timeout = Math.pow(2,timeMemory);
          timeMemory++;
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
    }
    
    self.post = function RequestJSPost(data,callback,onerror){
      new Instance(data,callback,onerror).post();
    };
    self.get = function RequestJSGet(callback,onerror){
      new Instance(null,callback,onerror).get();
    };
  };
  
  
  Request.loadGateway = function(_gateway){
    gateway = _gateway;
  }
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  var cookies = {
  	get:function(c_name){
  		var i,x,y,ARRcookies=document.cookie.split(";");
  		for (i=0;i<ARRcookies.length;i++)
  		  {
  		  x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
  		  y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
  		  x=x.replace(/^\s+|\s+$/g,"");
  		  if (x==c_name)
  		    {
  		    return unescape(y);
  		    };
  		  };
  	},
  	set:function(c_name,value,exdays){
  		var exdays = exdays || 365;
  		var exdate=new Date();
  		exdate.setDate(exdate.getDate() + exdays);
  		var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString()+"; path=/;");
  		document.cookie=c_name + "=" + c_value;
  	},
  	delete:function(c_name){
  		this.set(c_name,"",-1);
  	}
  };
  
  this.logout = function(){
    cookies.delete('uid');
    cookies.delete('ulid');
    cookies.delete('sid');
  }
  
  function CheckNewSession(data){
    if(!data['setsession']) return;
    if(!!data.session.uid)
      cookies.set('uid',uid,30);
    if(!!data.session.ulid)
     cookies.set('ulid',ulid,30);
    if(!!data.session.sid)
      cookies.set('sid',sid,30);
  }
  
  function AddSessionToPost(data){
    var uid, ulid, sid;
    uid = cookies.get('uid');
    ulid = cookies.get('ulid');
    sid = cookies.get('sid');
    if(!!uid) data['uid'] = uid;
    if(!!ulid) data['ulid'] = ulid;
    if(!!sid) data['sid'] = sid;
  }

  
  
  
  
  
  
  
  
  
  
  window.Request = Request;
  
  
})();