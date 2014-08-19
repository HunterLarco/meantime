function ContactField(frame, book){
  var self = this;
  
  self.complete = Complete;
  self.contact = null;
  
  var input, div;
  Bind();
  
  function IsPhoneNumber(num){
    return (/^[0-9]+$/).test(num.replace(/\s|-/,''));
  }
  
  function IsEmail(email){
    return /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
  }
  
  function Complete(){
    match = book.suggest(input.value);
    input.blur();
    if(!match){
      if(IsPhoneNumber(input.value))
        self.contact = {numbers:[input.value]};
      if(IsEmail(input.value))
        self.contact = {emails:[input.value]};
      return;
    };
    input.value = match.alias;
    div.innerHTML = '<label>'+match.alias+'</label>';
    self.contact = match.contact;
  }
  
  function UpdateSuggestion(){
    self.contact = null;
    var value = input.value;
    if(value.length == 0){
      div.innerHTML = frame.getAttribute('placeholder');
      return;
    };
    lValue = book.suggest(value);
    if(!lValue){
      div.innerHTML = '<label>'+value+'</label>';
      return;
    };
    lValue = lValue.alias;
    if(!!value.match(/^[0-9]*$/))
      value = value.slice(0,3)+(value.length>3?' '+value.slice(3,6)+(value.length>6?'-'+value.slice(6,10):''):'');
    var index = lValue.toLowerCase().indexOf(value.toLowerCase());
    if(index == -1)
      div.innerHTML = lValue;
    else
      div.innerHTML = lValue.slice(0,index) + '<label>'+value+'</label>' + lValue.slice(value.length+index);
  }
  
  function Bind(){
    input = document.createElement('input');
    div = document.createElement('div');
  
    input.setAttribute('type', 'text');
    input.addEventListener('keyup', UpdateSuggestion);
    
    frame.appendChild(div);
    frame.appendChild(input);
    
    UpdateSuggestion();
  }
}