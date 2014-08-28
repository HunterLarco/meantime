function Camera(canvas){
  var self = this;
  
  
  var ctx,
      video,
      stream,
      image,
      listeners = {};
  
  
  self.record = Record;
  self.capture = Capture;
  self.stop = Stop;
  self.pause = Pause;
  self.restart = Restart;
  self.getDataURI = GetDataURI;
  self.addEventListener = AddEventListener;
  self.removeEventListener = RemoveEventListener;
  
  
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
    if(!listeners[event]) return;
    for(var i=0,funct; funct=listeners[event][i++];)
      funct(data);
  }
  
  
  function GetUserMedia(options, callback, onerror){
    (navigator.getUserMedia       ||
     navigator.webkitGetUserMedia ||
     navigator.mozGetUserMedia    ||
     navigator.msGetUserMedia).call(navigator, options, callback, onerror);
  }
  
  
  function RequestAnimationFrame(callback){
    (window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame     ||
    window.oRequestAnimationFrame       ||
    window.msRequestAnimationFrame      ||
    function(callback){
    	window.setTimeout( callback, 1000 / 60 );
    }).call(window, callback);
  }
  
  
  function CreateObjectURL(object){
    return (window.URL || window.webkitURL).createObjectURL(object);
  }
  
  
  function SetupCanvas(){
    ctx = canvas.getContext('2d');
    ctx.translate(canvas.width, 0);
    ctx.scale(-1, 1);
  }
  
  
  function ClearCanvas(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
  
  
  function UpdateCanvas(){
    if(video.paused || video.ended) return;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    RequestAnimationFrame(UpdateCanvas);
  }
  
  
  function ConnectStream(localstream){
    video.src = CreateObjectURL(localstream);
    stream = localstream;
  }
  
  
  function SetupVideoReciever(){
    video = document.createElement('video');
    video.setAttribute('autoplay','');
    video.addEventListener('play', UpdateCanvas, false);
  }
  
  
  function OnMediaError(event){
    FireEvent('error', event);
  }
  
  
  function Record(){
    if(!!video) return Restart();
    GetUserMedia({video:true, audio:false}, function(mediaStream){
      FireEvent('record');
      SetupCanvas();
      SetupVideoReciever();
      ConnectStream(mediaStream);
    }, OnMediaError);
  }
  
  
  function Stop(){
    Pause();
    video.src = null;
    video = null;
    stream.stop();
    ClearCanvas();
  }
  
  
  function Pause(){
    video.pause();
  }
  
  
  function Restart(){
    if(!video) return self.record();
    if(!video.paused) return;
    video.play();
  }
  
  
  function Capture(){
    image = canvas.toDataURL();
    Pause();
    return image
  }
  
  
  function GetDataURI(){
    return image;
  }
  
  
}