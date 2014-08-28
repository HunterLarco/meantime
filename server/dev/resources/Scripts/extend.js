(function(){
  
  
  function ApplyArguments(Constructor, args){
    var Temp = function(){}, // temporary constructor
    inst, ret; // other vars
    // Give the Temp constructor the Constructor's prototype
    Temp.prototype = Constructor.prototype;
    // Create a new instance
    inst = new Temp;
    // Call the original Constructor with the temp
    // instance as its context (i.e. its 'this' value)
    ret = Constructor.apply(inst, args);
    // If an object has been returned then return it otherwise
    // return the original instance.
    // (consistent with behaviour of the new operator)
    return Object(ret) === ret ? ret : inst;
  }




  Function.prototype.extend = function ExtendObject(Sub){
    var Super = this;
    function Wrapper(){
      var self = this;
    
      var empty = [],
          superArgs = empty;
    
      Sub.prototype.super = function(){
        superArgs = arguments;
        throw ('stop execution');
      };

      try{
        var sub = ApplyArguments(Sub, arguments);
        delete sub;
      }catch(error){}

      Sub.prototype = ApplyArguments(Super, superArgs);
      Sub.prototype.super = Sub.prototype;
      
      // changes to this effect App.Page.blure (reset call)
      Sub.prototype.derived = self;

      if(empty != superArgs)
        Sub.prototype.super = function(){
          Sub.prototype.super = Sub.prototype;
        }

      var sub = ApplyArguments(Sub, arguments);
      Sub.prototype = new Object();

      for(var propname in sub)
        self[propname] = sub[propname];
    
      // console.log(arguments.callee.caller.slice(0,30));
    
    }
    return Wrapper;
  }




  Function.prototype.extend.ABSTRACT = {};
  
  
})();