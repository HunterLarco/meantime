(function(){
  
  var snapscroller = function(elem, options){
    var self = this,
        options = isNot(options) ? {} : options;
    
    
    // -------------------------------------------- public constants -------------------------------------------- //
    
    
    self.FRICTION = options.friction || 0.05;
    
    self.addEventListener = AddEventListener;
    self.removeEventListener = RemoveEventListener;
    
    self.appendChild = AppendChild;
    self.removeChild = RemoveChild;
    self.clearChildren = ClearHTML;
    
    
    // -------------------------------------------- private variables -------------------------------------------- //
    
    
    // records the scroll positions of all children (populated
    // on construction and whenever appendChild is called)
    var snapMap = [];
    // records all motion and gesture data, keys created when needed
    var mouse = {};
    // animation data
    var animation = {
      isRunning: false,
      forceStop: false,
      modifier : 1
    };
    // event listeners (a hashtable of arrays of functions)
    // thusfar supports: onchange
    var listeners = {};
    
    
    // -------------------------------------------- private constants --------------------------------------------//
    
    
    // the amount of touches required to be considered a change of direction
    // this is used so that a accidental motion down when lifting the finger
    // from scrolling up doesn't cause scrolling to go in the wrong direction.
    var TOUCHES_TO_CHANGE_DIRECTION = 5;
    // the  minimum amount of pixel motion required to be considered a gesture
    // attempt.
    var MIN_MOTION_GESTURE = 5;
    
    
    // -------------------------------------------- constructor -------------------------------------------- //
    
    
    (function Constructor(){
      BuildInitialSnapMap();
      BindSnapMap();
      BindTouchEvents();
    })();
    
    
    // -------------------------------------------- private methods -------------------------------------------- //
    
    
    function isNot(item){
      var undefined;
      return item === undefined || item === null;
    }
    
    
    function AddEventListener(event, funct){
      if(isNot(event) || isNot(funct)) return;
      if(!listeners[event]) listeners[event] = [];
      listeners[event].push(funct);
    }
    
    
    function RemoveEventListener(event, funct){
      if(isNot(event) || isNot(funct)) return;
      if(!listeners[event]) return;
      do{
        var index = listeners[event].indexOf(funct);
        listeners[event].splice(index, 1);
      }while(index != -1);
    }
    
    
    function FireEventListener(event, data){
      data.type = event;
      data.target = self;
      if(!listeners[event]) return;
      for(var i=0,funct; funct=listeners[event][i++];)
        funct(data);
    }
    
    
    function TouchStart(event){
      // if a scroll animation is running, stop it
      if(animation.isRunning) animation.forceStop = true;
    
      // record the initial touch
      var touch = event.touches[0];
      mouse.lastx = touch.pageX;
      mouse.lasty = touch.pageY;
      
      // reset the time to now
      mouse.time = {};
      mouse.time.lastTouch = Date.now();
      
      // reset the velocity and direction
      mouse.velocity = {x:0,y:0};
      mouse.direction = {x:null,y:null,xcounts:0,ycounts:0};
      
      // set hasMoved to false, as no touch moves have registered yet
      mouse.hasMoved = false;
    
      // add event listeners to the document, so that the touches aren't
      // bounded by the provided element
      document.addEventListener('touchmove', TouchMove);
      document.addEventListener('touchend', TouchEnd);
    }
    
    
    function TouchMove(event){
      mouse.hasMoved = true;
      
      var touch = event.touches[0],
          // the difference in pixels between the last touch and the current one
          delta = {
            x: mouse.lastx-touch.pageX,
            y: mouse.lasty-touch.pageY
          },
          // converts the touch motion from pixels to screen lengths
          deltaPageUnit = {
            x: delta.x / elem.offsetWidth,
            y: delta.y / elem.offsetHeight
          },
          // time difference from last touch event in seconds
          timediff = (Date.now()-mouse.time.lastTouch) / 1000,
          // converts the touch motion into screen lengths per second
          touch_velocity = {
            x: deltaPageUnit.x / timediff,
            y: deltaPageUnit.y / timediff
          },
          // The velocity is either the previous velocity if it is greater, or
          // the current velocity just calculated if it is greater. This is done
          // so that velocity will be accurate since most gestures lose velocity
          // as the finger leaves the screen, this maintains the maximum velocity.
          // However, the next lines do reset the velocity if the motion stops.
          velocity = {
            x: Math.max(Math.abs(mouse.velocity.x), Math.abs(touch_velocity.x)),
            y: Math.max(Math.abs(mouse.velocity.y), Math.abs(touch_velocity.y))
          };
      // If the motion made is less than the min required to be considered a gesture
      // reset the velocity as the gesture has stopped but not been released yet.
      mouse.velocity = {
        x: Math.abs(delta.x) < MIN_MOTION_GESTURE ? 0 : velocity.x,
        y: Math.abs(delta.y) < MIN_MOTION_GESTURE ? 0 : velocity.y
      };
    
      // The velocity is always positive, however mouse.direction indicates
      // whether it is positive or negative. Since upward gestures end in a slight
      // downward motion due to the hand's bone structure, the direction requires
      // a few touches to be flipped. This computes that using the
      // TOUCHES_TO_CHANGE_DIRECTION constant.
      var direction = {
        x: delta.x < 0 ? -1 : 1,
        y: delta.y < 0 ? -1 : 1
      }
      mouse.direction.xcounts = direction.x != mouse.direction.lastx ? 1 : mouse.direction.xcounts+1;
      mouse.direction.ycounts = direction.y != mouse.direction.lasty ? 1 : mouse.direction.ycounts+1;
      if(mouse.direction.xcounts > TOUCHES_TO_CHANGE_DIRECTION) mouse.direction.x = mouse.direction.lastx;
      if(mouse.direction.ycounts > TOUCHES_TO_CHANGE_DIRECTION) mouse.direction.y = mouse.direction.lasty;
      mouse.direction.lastx = direction.x;
      mouse.direction.lasty = direction.y;
      if(mouse.direction.x == null) mouse.direction.x = mouse.direction.lastx;
      if(mouse.direction.y == null) mouse.direction.y = mouse.direction.lasty;
    
      // Update the current positions of the touch as the last ones made
      mouse.lastx = touch.pageX;
      mouse.lasty = touch.pageY;
      mouse.time.lastTouch = Date.now();
    
      // scroll with the finger but stop at 0 or the max scroll height
      elem.scrollTop = Math.max(0, Math.min(elem.scrollTop+delta.y, elem.scrollHeight-elem.offsetHeight));
      
      // fire the onscroll event
      FireEventListener('scroll', {
        scroll: {
          y: elem.scrollTop,
          height: elem.scrollHeight - elem.offsetHeight
        },
        velocity: {
          y: mouse.direction.y * mouse.velocity.y
        },
        animating: false
      });
    
      // prevent native scrolling
      event.preventDefault();
    }
    
    
    function TouchEnd(){
      // in case the TouchEnd event fires twice, which does happen
      // on some devices
      if(animation.isRunning) return;
    
      // if the person only tapped the screen, ie: to stop the scrolling
      // action, default to scroll to the closest object downward.
      if(!mouse.hasMoved){
        mouse.lastTouch = Infinity;
        mouse.direction.x = mouse.direction.y = 1;
      }
    
      // remove event listeners as to not confuse the program
      document.removeEventListener('touchmove', TouchMove);
      document.removeEventListener('touchend', TouchEnd);
     
      // If there is no velocity, use a default 0.2 screen lengths per second
      // which is enough to gently ease to a close neighbor. This is especially
      // important when a gesture is ended forcebly by the finger as opposed
      // to animated
      mouse.velocity.y = Math.max(mouse.velocity.y, 0.2);
      mouse.velocity.x = Math.max(mouse.velocity.x, 0.2);
    
      // animate the scrolling
      Animate();
    }
    
    
    function Animate(){
      // stop the animation and reset if forced to stop
      // cuased by the animation.forceStop flag
      if(animation.forceStop) return StopAnimation();
      
      // If the animation starttime isn't set, then it hasn't
      // started yet and this block will setup the animation variables.
      if(!animation.starttime){
        animation.isRunning = true;
        animation.starttime = Date.now();
        animation.startposition = elem.scrollTop;
        animation.modifier = 1;
        
        // this is the velocity at which point the scrolling stops.
        // otherwise it would indefinetly scroll in minute proportion.
        var endVelocity = 0.07;
        
        // this is how long (in seconds) that the animation will take to
        // reach it's completion.
        animation.finaltime = (Math.log(endVelocity) - Math.log(mouse.velocity.y)) / Math.log(self.FRICTION);
        
        // this is the final position the the scroll will reach
        var finalposition = PositionAtTime(animation.finaltime),
            // the scroll position of the closest object to snap to
            closest = ClosestSnapPosition(finalposition);
        
        // fire the prescrollevent
        FireEventListener('prescroll', {
          expected: {
            time: animation.finaltime,
            scroll: {
              y: finalposition
            },
            element: closest
          },
          scroll: {
            y: elem.scrollTop,
            height: elem.scrollHeight - elem.offsetHeight
          }
        });
        
        // recalulate the closest snap position in case the prescroll event
        // listener changed the snapMap. Also, if the final scroll position
        // will be more than a page length over the scroll boundaries,
        // the velocity will not be curbed to land at the boundary, instead
        // it will slam into it.
        closest = finalposition > elem.scrollHeight ? {
          pixels: finalposition,
          element: elem.children[elem.children.length-1]
        } : finalposition < -elem.offsetHeight ? {
          pixels: finalposition,
          element: elem.children[0]
        }: ClosestSnapPosition(finalposition);
        
        animation.closest = closest.element;
        // a small value that the velocity is multiplied by to insure that the animation finishes
        // on a child of the element provided. It's so close to 1 that the small change is
        // barely noticable.
        animation.modifier = (closest.pixels-animation.startposition) / (PositionAtTime(animation.finaltime) - animation.startposition);
      }
      
      // the elapsed animation time in seconds
      var elapsedTime = (Date.now() - animation.starttime) / 1000,
          position = PositionAtTime(elapsedTime);
     
      // if the elapsed time exceeds the amount of time needed to complete
      // the animation or the scroller is at the end or beginning, stop.
     if(elapsedTime >= animation.finaltime || elem.scrollTop == 0 || elem.scrollTop == elem.scrollHeight-elem.offsetHeight){
       elem.scrollTop = Math.round(PositionAtTime(animation.finaltime));
       // fire the onchange event
       FireEventListener('change', {
         index: [].indexOf.call(elem.children, animation.closest),
         element: animation.closest
       });
       // stop the animation
       return StopAnimation();
     };
     
     // update the scroll position
     elem.scrollTop = Math.max(0, Math.min(Math.round(position), elem.scrollHeight-elem.offsetHeight));
     
     // fire the onscroll event
     FireEventListener('scroll', {
       scroll: {
         y: elem.scrollTop,
         height: elem.scrollHeight - elem.offsetHeight
       },
       velocity: {
         y: mouse.direction.y * VelocityAtTime(elapsedTime)
       },
       animating: true
     });
    
     // continue the animation
     requestAnimationFrame(Animate);
    }
    
    
    function StopAnimation(){
      // resets necessary to stop animation
      animation.forceStop = false;
      animation.isRunning = false;
      animation.starttime = null;
    }
    
    
    // the velocity at time 'seconds'
    function VelocityAtTime(seconds){
      return mouse.velocity.y * Math.pow(self.FRICTION, seconds) * animation.modifier;
    }
    
    
    // the position at time 't' is figured out by adding the intergral from 0 to 't' of the continous
    // application of friction to velocity so figure out how far it has moved from time 0 to 't'.
    function PositionAtTime(seconds){
      return animation.startposition + animation.modifier * IntergrateVelocity(0, seconds) * elem.offsetHeight;
    }
    function IntergrateVelocity(start, end){
      var Intergral = function(t){
        return Math.pow(self.FRICTION, t) / Math.log(self.FRICTION) * mouse.velocity.y * mouse.direction.y;
      }
      return Intergral(end) - Intergral(start);
    }
    
    
    function BindTouchEvents(){
      elem.addEventListener('touchstart', TouchStart);
    }
    
    
    function ClosestSnapPosition(position){
      if(snapMap.length == 0) return null;
      var pixels = Helper_ClosestSnapPosition(position, 0, snapMap.length-1);
      return {
        pixels: pixels,
        element: elem.children[snapMap.indexOf(pixels)]
      };
    }
    function Helper_ClosestSnapPosition(item, start, end){
      if(start == end) return tree[start];
      if(end-start == 1) return item-snapMap[start] < snapMap[end]-item ? snapMap[start] : snapMap[end];
      var middle = Math.floor((start+end)/2);
      if(item == snapMap[middle]) return item;
      if(item >  snapMap[middle]) return Helper_ClosestSnapPosition(item, middle, end);
      if(item <  snapMap[middle]) return Helper_ClosestSnapPosition(item, start, middle);
    }
    
    
    function BindSnapMap(){
      elem.appendChild = (function(){
        this.apply(elem, arguments);
        snapMap.push(arguments[0].offsetTop);
      }).bind(elem.appendChild);
      
      elem.removeChild = (function(){
        this.apply(elem, arguments);
        ResetSnapMap();
      }).bind(elem.removeChild);
      
      elem.clearChildren = ClearHTML;
    }
    
    function ClearHTML(){
      elem.innerHTML = '';
      ResetSnapMap();
    }
    
    function AppendChild(){
      elem.appendChild.apply(elem, arguments);
    }
    
    function RemoveChild(){
      elem.removeChild.apply(elem, arguments);
    }
    
    function ResetSnapMap(){
      snapMap = [];
      BuildInitialSnapMap();
    }
    
    function BuildInitialSnapMap(){
      for(var i=0,child; child=elem.children[i++];)
        snapMap.push(child.offsetTop);
    }
    
    
  };
  
  
  // -------------------------------------------- library meta data -------------------------------------------- //
  
  snapscroller.AUTHOR = 'Hunter John Larco';
  snapscroller.VERSION = 'v0.0.0';
  snapscroller.DEPENDANCIES = 'None';
  
  
  // -------------------------------------------- factory builder -------------------------------------------- //
  
  
  window.SnapScroller = snapscroller;
  
})();