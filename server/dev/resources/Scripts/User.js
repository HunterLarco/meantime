(function(){
  
  GATEWAY = '/api/';
  POLL_RATE = 1000*60;// a minute
  
  
  function XMLHTTPInstance(data, callback, onerror){
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
            onerror(new ErrorEvent(data.code, data.message, data));
          }else{CheckNewSession(data);
            callback(data);
          }
        }else{
          onerror(new ErrorEvent(-1, 'Unknown Server Error'));
        };
      };
    }
  
    this.post = function(url){
      var xmlhttp = SetupRequest(arguments, 'POST', url);
      if(!xmlhttp) return;
      xmlhttp.send(JSON.stringify(data));
    }
  
    this.get = function(url){
      var xmlhttp = SetupRequest(arguments, 'POST', url);
      xmlhttp.send();
    }
  
    function OnError(event){
      onerror(new ErrorEvent(-2, 'Request Error!'));
    }
  
    function RequestJSRetry(){
      usedfunct.apply(this,argumentMemory);
    };
  
    var ErrorEvent = function(errorcode,message,response){
      var event = this;
      this.__response__ = response;
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

  function CheckNewSession(data){
    if(!data['setsession']) return;
    if(!!data.session.uid)
      cookies.set('uid',data.session.uid,30);
    if(!!data.session.ulid)
     cookies.set('ulid',data.session.ulid,30);
    if(!!data.session.sid)
      cookies.set('sid',data.session.sid,30);
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
  
  var Request = function Request(url, body, OnSuccess, errormap){
    function __success__(event){
      CheckNewSession(event);
      if(typeof Request.overhead == 'function')
        if(false == Request.overhead(event)) return;
      if(typeof OnSuccess == 'function') OnSuccess(event);
    }
    function __error__(event){
      CheckNewSession(event);
      if(typeof Request.overhead == 'function')
        if(false == Request.overhead(event.__response__)) return;
      if(!errormap) errormap = {};
      if(!!errormap.always) errormap.always(event);
      if(!!errormap[event.code]) return errormap[event.code](event);
      if(!!errormap.default) return errormap.default(event);
      console.warn('Unhandled Error');
    }
    AddSessionToPost(body);
    var instance = new XMLHTTPInstance(body, __success__, __error__);
    instance.post(GATEWAY+url);
  }
  
  var cookies = new (function(){
    var self = this;
    
    
    self.set = function(cookiename, value, days){
  		var days = days || 365,
  		    expirationDate = new Date(Date.now()+1000*60*60*24*days),
  		    cookie = escape(value) + '; expires=' + expirationDate.toUTCString() + '; path=/;';
  		document.cookie = cookiename + "=" + cookie;
    }
    
    
    self.get = function(cookiename){
      var ARRcookies = document.cookie.split(';');
      for (var i=0; i<ARRcookies.length; i++){
        var x = ARRcookies[i].substr(0, ARRcookies[i].indexOf('=')),
            y = ARRcookies[i].substr(ARRcookies[i].indexOf('=') + 1);
        x = x.replace(/^\s+|\s+$/g,"");
        if (x == cookiename) return unescape(y);
      }
    }
    
    
    self.delete = function(cookiename){
      self.set(cookiename, 'delete', -1);
    }
  })();
  
  
  var Message = function Message(user, data){
    var self = this;
    self.super();
    
    
    self.getURL = GetURL;
    
    self.getSender = GetSender;
    self.getSentDate = GetSentDate;
    
    self.getRecipient = GetRecipient;
    
    self.isRead = IsRead;
    self.getReadDate = GetReadDate;
    
    self.isViewable = IsViewable;
    self.getViewableDate = GetViewableDate
    self.getPendingTime = GetPendingTime;
    
    self.isDisappearing = IsDisappearing;
    
    self.read = Read;
    
    
    var key = data.key,
        disappearing = data.disappearing    || false,
        viewable_date = user.time.toLocalTime(data.viewable_date) || Date.now(),
        sender = data.sender,
        isread = !!data.readdate,
        readdate = isread ? user.time.toLocalTime(data.readdate) : null,
        sentdate = user.time.toLocalTime(data.sent_date),
        recipient = data.recipient;
        
        
    function IsViewable(){
      return GetPendingTime() <= 0; 
    }
    function GetViewableDate(){
      return viewable_date;
    }
    function GetURL(){
      readdate = Date.now();
      return '/api/get/message?key='+key;
    }
    function GetPendingTime(){
      var time = viewable_date - Date.now();
      return time;
    }
    function GetSender(){
      return sender;
    }
    function IsRead(){
      return isread;
    }
    function GetReadDate(){
      return readdate;
    }
    function GetSentDate(){
      return sentdate;
    }
    function GetRecipient(){
      return recipient;
    }
    function IsDisappearing(){
      return disappearing;
    }
    function Read(){
      isread = true;
      readdate = Date.now()
    }
    
        
    (function Constructor(){
      // pass
    })();
  }
  Message = EventListenerClass.extend(Message);
  
  
  // REMOINDER: locks listeners
  // EVENTS: onlogout, onpasslock, onsesslock, onmessage
  var User = function User(data){
    var self = this;
    self.super();
    
    
    self.getEmail        = GetEmail;
    self.getFullName     = GetFullName;
    self.getMobileNumber = GetMobileNumber;
    self.getContacts     = GetContacts;
    self.getMessages     = GetMessages;
    self.getSession      = GetSession;
    
    self.setEmail        = SetEmail;
    self.setFullName     = SetFullName;
    self.setMobileNumber = SetMobileNumber;
    
    self.changePassword = ChangePassword;
    
    self.unlock = Unlock;
    
    self.isPassLocked = IsPassLocked;
    self.isSessLocked = IsSessLocked;
    
    self.logout = Logout;
    self.delete = Delete;
    
    self.sendMessage = SendMessage;
    
    self.time = {}
    self.time.toLocalTime = ServerToLocalTime;
    self.time.toServerTime = LocalToServerTime;
    
    self.sendFeedback = SendFeedback;
    
    
    var email    = data.email    || null,
        mobile   = data.phone    || null,
        fullname = data.fullname || null,
        contacts = data.contacts || [],
        messages = [],
        messages_loaded = [];// a list of the keys of messages already in the messages array
    
    var messagesInterval,
        synctime = data.synctime*1000,
        markedtime = Date.now();
    
    var passlocked = data.passlocked || false,
        sesslocked = data.sesslocked || false,
        unlockfunction = [];
    
    
    function SendFeedback(content, tags, callback){
      Request('feedback/send', {
        content: content,
        tags: tags
      },
      callback, {default:function(event){event.retry();}});
    }
    
    function RequestOverhead(response){
      if(!response) return true;
      return CheckPassLocked(response) && CheckSessionLocked(response);
    }
    function CheckPassLocked(event){
      if(event.passlocked && !passlocked){
        passlocked = true;
        unlockfunction.push(UnlockPassUser);
        self.__events__.fire('passlock');
        return false;
      }
      return true;
    }
    function CheckSessionLocked(event){
      if(event.sesslocked && !sesslocked){
        sesslocked = true;
        unlockfunction.push(UnlockSessUser);
        self.__events__.fire('sesslock');
        return false;
      }
      return true;
    }
    
    function GetEmail(){
      return email;
    }
    function GetFullName(){
      return fullname;
    }
    function GetMobileNumber(){
      return mobile;
    }
    function GetContacts(){
      return contacts;
    }
    function GetMessages(){
      return messages;
    }
    function GetSession(){
      return {
        uid: cookies.get('uid'),
        ulid: cookies.get('ulid'),
        sid: cookies.get('sid')
      }
    }
    
    // throws EMAILUSED
    function SetEmail(newemail, callback, errormap){
      Request('user/setemail', {
        email: newemail
      }, function OnSuccess(event){
        email = newemail;
        if(typeof callback == 'function') callback(event);
      }, errormap);
    }
    function SetFullName(newname, callback){
      Request('user/setname', {
        'name': newname
      }, function OnSuccess(callback){
        fullname = newname;
        if(typeof callback == 'function') callback(event);
      }, {
        default: function(event){event.retry()}
      });
    }
    function SetMobileNumber(newnumber, callback){
      Request('user/setmobile', {
        'mobile': newnumber
      }, function OnSuccess(event){
        mobile = newnumber;
        if(typeof callback == 'function') callback(event);
      }, {
        default: function(event){event.retry()}
      });
    }
    
    // throws INCORRECTCREDENTIALS
    function ChangePassword(oldp, newp, callback, errormap){
      Request('user/changepassword', {
        password: newp,
        old_password: oldp
      },
      callback, errormap);
    }
    
    // throws INCORRECTCREDENTIALS
    function UnlockSessUser(email, password, callback, errormap){
      Request('user/unlock', {
        email: email,
        password: password
      },
      function OnSuccess(event){
        unlockfunction.pop();
        sesslocked = false;
        if(typeof callback == 'function') callback(event);
      }, errormap);
    }
    function UnlockPassUser(callback){
      Request('user/unlock', {},
      function OnSuccess(event){
        unlockfunction.pop();
        passlocked = false;
        if(typeof callback == 'function') callback(event);
      }, {
        default: function(event){event.retry();}
      });
    }
    function Unlock(){
      if(unlockfunction.length == 0) return;
      unlockfunction[unlockfunction.length-1].apply(this, arguments);
    }
    
    function IsPassLocked(){
      return passlocked;
    }
    function IsSessLocked(){
      return sesslocked;
    }
    
    function Logout(){
      StopPollingMessages();
      cookies.delete('uid');
      cookies.delete('ulid');
      cookies.delete('sid');
      self.__events__.fire('logout')
    }
    function Delete(callback){
      Request('user/delete', {},
      function OnSuccess(event){
        self.logout();
        if(typeof callback == 'function') callback();
      }, {
        default: function(event){event.retry();}
      });
    }
    
    function SendMessage(uri, recipients, date, disappearing, OnSuccess){
      Request('messages/send', {
        'uri': uri,
        'recipients': recipients,
        'disappearing': typeof disappearing == 'boolean' ? disappearing : false,
        'date': LocalToServerTime(date)
      }, function(event){
        contacts = event.contacts;
        if(typeof OnSuccess == 'function') OnSuccess();
      }, {default: function(event){event.retry();}});
    }
    
    function StartPollingMessages(){
      messagesInterval = setInterval(UpdateMessages, POLL_RATE);
    }
    function StopPollingMessages(){
      clearInterval(messagesInterval);
    }
    function UpdateMessages(){
      Request('messages/get', {},
      AddNewMessages);
    }
    function AddNewMessages(event){
      for(var i=0,message; message=event.messages[i++];){
        if(messages_loaded.indexOf(message.key) > -1) continue;
        messages_loaded.push(message.key);
        var newmessage = new Message(self, message);
        messages.push(newmessage);
        self.__events__.fire('message', {
          user: self,
          message: newmessage
        });
      }
    }
    
    
    // gets milliseconds returns seconds
    function LocalToServerTime(time){
      var time = (time-markedtime)+synctime;
      return Math.round(time/1000);
    }
    // gets seconds returns milliseconds
    function ServerToLocalTime(time){
      time *= 1000;
      return (time-synctime)+markedtime;
    }
    
    
    (function contructor(){
      // Request.overhead reads data before being send to OnSuccess of OnError
      Request.overhead = RequestOverhead;
      AddNewMessages({
        messages: data.messages || []
      });
      StartPollingMessages();
      if(passlocked) unlockfunction.push(UnlockPassUser);
      if(sesslocked) unlockfunction.push(UnlockSessUser);
    })();
  }
  User = EventListenerClass.extend(User);
  
  
  // throws INCORRECTCREDENTIALS, BRUTEFORCE, USERDOESNTEXIST
  User.login = function(email, password, OnSuccess, errormap){
    function __OnSuccess__(event){
      if(typeof OnSuccess == 'function') OnSuccess(new User(event.user));
    }
    Request('user/login', {
      email: email,
      password: password,
      timezone: new Date().getTimezoneOffset()
    }, __OnSuccess__, errormap);
  }
  
  
  // throws EMAILUSED
  User.signup = function(email, password, OnSuccess, errormap){
    function __OnSuccess__(event){
      if(typeof OnSuccess == 'function') OnSuccess(new User(event.user));
    }
    Request('user/signup', {
      email: email,
      password: password
    }, __OnSuccess__, errormap);
  }
  
  
  User.Cookies = cookies;
  
  
  User.ERRORS = {
    EMAILUSED: 200,
    INCORRECTCREDENTIALS: 201,
    BRUTEFORCE: 202,
    USERDOESNTEXIST: 203
  }
  
  
  window.User = User;
  
})();