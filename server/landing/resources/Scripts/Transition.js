(function(){
  
  function Transition(runner){
    var self = this;
    
    var frameRate = 20,
        forceStop = false,
        running = false;
    
    var runner = runner || new Function();
    
    self.run = Run;
    self.stop = Stop;
    
    self.getFrameRate = GetFrameRate;
    self.setFrameRate = SetFrameRate;
    
    function GetFrameRate(){
      return frameRate;
    }
    function SetFrameRate(rate){
      var old = frameRate;
      frameRate = rate;
      return old;
    }
    
    function Run(callback, time){
      if(running) return false;
      running = true;
      var callback = callback || new Function(),
          time = time || 0;
      function Recurse(i){
        if(forceStop){
          forceStop = false;
          return;
        }
        if(i>=time){
          runner(1, time, time);
          running = false;
          callback();
          return;
        }
        runner(i/time, i, time);
        setTimeout(function(){
          Recurse(i + frameRate);
        }, frameRate);
      }
      Recurse(0);
      return true;
    }
    
    function Stop(){
      forceStop = true;
    }
    
  }
  
  
  
  
  
  
  
  
  
  Transition.EaseInOut = function EaseInOut(time, runner, callback){
    var t = new Transition(function(percent, i, time){
      runner(Sigmoid(i,time));
    });
    t.run(callback, time);
    
    function Sigmoid(x,width){
      function resizeSigmoid(x,width){
        var normalization = 1/(rawSigmoid(width,width)-rawSigmoid(0,width));
        return (rawSigmoid(x,width)-rawSigmoid(0,width))*normalization;
      }
      function rawSigmoid(x,width){
        width /= 2;
        return 1/(1+Math.exp(-4/width*(x-width)));
      }
      function limitSigmoid(val){
        function max(v,l){
          return l-(l-v+Math.abs(l-v))/2;
        }
        function min(v,l){
          return (v-l+Math.abs(v-l))/2+l;
        }
        return max(min(val,0),1);
      }
      return limitSigmoid(resizeSigmoid(x,width));
    }
  }
  
  
  
  
  
  
  
  
  
  
  
  Transition.Bounce = function Bounce(time, runner, callback){
    var t = new Transition(function(percent, i, time){
        if(percent < 0.5){
          var state = Bounce(i, time*0.5);
        }else if(percent < 0.8){
          var state = Bounce(i-time*0.5, 0.3*time)*10/34;
        }else if(i <= time){
          var state = Bounce(i-0.8*time, 0.2*time)*3/34;
        }
        runner(state);
    });
    t.run(callback, time);
    
    function Bounce(i, distance){
      if(i==0) return 0;
      return -Math.pow(((2*i/distance)%2-1)/Math.ceil(i/distance),2)+1;
    }
  }
  
  
  
  
  
  
  
  
  window.Transition = Transition;
  
})();