/*

blue | viewable
purple | locked
grey | viewed
  sand on bottom | viewable
  sand gone | not viewable
light circle | dissapearing

*/
(function(){
  
  function InboxPage(frame){
    var self = this;
    self.super(frame);
    
    
    self.reset = Reset;
    
    
    var messages = [];
    
    
    function Reset(){}
    
    function ShowHeaderButtons(){
      app.show(document.getElementById('header_buttons'));
    }
     
    function FormatDate(date){
      var date = new Date(date);
      var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      var hour = date.getHours()%12 == 0 ? 12 : date.getHours()%12,
          minute = ((date.getMinutes()+'').length == 1 ? '0' : '') + date.getMinutes(),
          ampm = date.getHours() >= 12 ? 'pm' : 'am';
      return months[date.getMonth()]+' '+date.getDate()+', '+date.getFullYear()+', at '+hour+':'+minute+''+ampm;
    }
    function FormatDateTime(time, date){
      var stamp = '',
          type = 'time';
      
      var constants = {
        second: 1000,
        minute: 1000*60,
        hour  : 1000*60*60,
        day   : 1000*60*60*24,
        week  : 1000*60*60*24*7,
        month : 1000*60*60*24*30,
        year  : 1000*60*60*24*365
      }
      
      if      (time < constants.minute)    stamp = Math.round(time/constants.second)     + ' seconds';
      else if (time < constants.minute*20) stamp = Math.round(time/constants.minute)     + ' minutes';
      else if (time < constants.hour)      stamp = Math.round(time/constants.minute/5)*5 + ' minutes';
      else if (time < constants.day){      stamp = Math.round(time/constants.hour)       + ' hours';}
      else {
        stamp = FormatDate(date);
        type = 'date'
      }
      
      return {
        stamp: stamp,
        type: type
      };
    }
    
    function OpenViewer(message, onload){
      document.getElementById('viewer_sender').innerHTML = message.getSender().fullname || message.getSender().email || message.getSender().phone;
      document.getElementById('viewer_image').addEventListener('load', Show);
      document.getElementById('viewer_image').setAttribute('src', message.getURL());
      if (message.getSender().email != app.getUser().getEmail()) message.read();
      document.getElementById('viewer_close').addEventListener('click', Hide);
      function Hide(){
        document.getElementById('viewer_image').removeEventListener(Show);
        document.getElementById('viewer_close').removeEventListener(Hide);
        app.hide(document.getElementById('viewer'), function(){
          document.getElementById('viewer_image').removeAttribute('src');
        });
      }
      function Show(){
        app.show(document.getElementById('viewer'), onload);
      }
    }
    
    function AddNewMessage(event){
      if(messages.length == 0) self.elements.frames.messages.innerHTML = '';
      
      var user = event.user,
          message = event.message;
          
      // beginning of sorter ~ orders chronologically in bins (now, future, past)
     
      var sorted = {viewable: [], read: [], waiting: []};
      function getBin(m){
        return m.isRead() ? sorted.read : (m.isViewable() ? sorted.viewable : sorted.waiting);
      }
      
      var messagebin = getBin(message),
          messageadded = false;
      for(var i=0,m; m=messages[i++];){
        var currentbin = getBin(m);
        if(!messageadded &&
            messagebin == currentbin &&
            Math.abs(message.getPendingTime()) < Math.abs(m.getPendingTime())
          ){
          messagebin.push(message);
          messageadded = true;
        }
        currentbin.push(m);
      }
      if(!messageadded) messagebin.push(message);
      messages = sorted.viewable.concat(sorted.waiting.concat(sorted.read));
    
      // end of sorter
      
      var index = messages.indexOf(message),
          sender = message.getSender(),
          isent = sender.email == app.getUser().getEmail();
      
      var div = document.createElement('div');
      div.classList.add('gift');
        var image = document.createElement('div');
        image.classList.add('image');
          var skin = document.createElement('img');
          skin.setAttribute('src', '/images/inbox/empty_locked.png');
          image.appendChild(skin);
          var canvas = document.createElement('canvas');
          image.appendChild(canvas);
        div.appendChild(image);
        var text = document.createElement('div');
        text.classList.add('text');
          var title = document.createElement('div');
          title.classList.add('title');
          if (isent) title.innerHTML = message.getRecipient().fullname || message.getRecipient().email || message.getRecipient().phone || message.getRecipient();
          else title.innerHTML = sender.fullname || sender.email || sender.phone;
          text.appendChild(title);
          var data = document.createElement('div');
          data.classList.add('data');
          
          function DrawHourglass(){
            var ctx = canvas.getContext('2d'),
                width = canvas.width,
                height = canvas.height,
                percent = (message.getPendingTime()) / Math.abs(message.getViewableDate() - message.getSentDate());
            percent = Math.max(Math.min(percent, 1), 0);
            ctx.clearRect(0,0,width,height);
            ctx.fillStyle = 'rgb(255,246,209)';
            ctx.fillRect(width*20/80,height*40/80,width*36/80,-percent*23/80*height);
            ctx.fillRect(width*20/80,height*(1-17/80),width*36/80,(1-percent)*-23/80*height);
            
            if(message.isDisappearing() && message.isRead() && !isent) ctx.clearRect(0,0,width,height);
            
            if(message.isViewable()) skin.setAttribute('src', '/images/inbox/empty.png');
            if(message.isRead()) skin.setAttribute('src', '/images/inbox/empty_gone.png');
          }
          
          function SetLabel(){
            DrawHourglass();
            var stamp = FormatDateTime(Date.now()-message.getSentDate(), message.getSentDate());
            if(isent)
              stamp = stamp.type == 'time' ?
                      'sent '+stamp.stamp+' ago' :
                      'sent on '+stamp.stamp;
            else
              stamp = stamp.type == 'time' ?
                      'recieved '+stamp.stamp+' ago' :
                      'recieved on '+stamp.stamp;
            data.innerHTML = stamp + ' - ';
          
            if(message.isRead())
              data.innerHTML += 'read on ' + FormatDate(message.getReadDate());
            else if(message.isViewable()){
              data.innerHTML += 'viewable now';
            }else{
              setTimeout(SetLabel, message.getPendingTime());
              var stamp = FormatDateTime(message.getPendingTime(), message.getViewableDate());
              stamp = 'viewable ' + (stamp.type == 'time' ? 'in' : 'on') + ' ' + stamp.stamp;
              data.innerHTML += stamp;
            }
          }
          
          function ReadMessage(){
            if(!message.isViewable() || (message.isRead() && message.isDisappearing() && !isent)) return;
            OpenViewer(message, function(){
              self.elements.frames.messages.removeChild(div);
              SetLabel();
              self.elements.frames.messages.appendChild(div);
            });
          }
          div.addEventListener('click', ReadMessage);
          
          window.setInterval(SetLabel, 1000*60);
          SetLabel();
          
          text.appendChild(data);
        div.appendChild(text);
        
        if(!self.elements.frames.messages.children[index]) self.elements.frames.messages.appendChild(div);
        else self.elements.frames.messages.insertBefore(div, self.elements.frames.messages.children[index]);
      
    }
    function ListenToMessages(){
      var user = app.getUser();
      for(var i=0,message; message=user.getMessages()[i++];)
        AddNewMessage({user:user,message:message});
      app.getUser().addEventListener('message', AddNewMessage);
    }
    
    
    (function Constructor(){
      self.addEventListener('focus', ShowHeaderButtons);
      if(!!app.getUser()) ListenToMessages()
      else app.addEventListener('userload', ListenToMessages);
    })();
  }
  
  
  if(!window.pages) window.pages = {};
  window.pages['inbox'] = InboxPage;
  
})();