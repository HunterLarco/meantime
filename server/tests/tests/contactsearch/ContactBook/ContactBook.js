function ContactBook(){
  var self = this;
  
  
  self.add = AddContact;
  self.bind = Bind;
  
  
  var tree = new ModifiedTrieTree();
  
  
  function Bind(inputframe){
    var input = document.createElement('input'),
        div = document.createElement('div');
  
  
    input.setAttribute('type', 'text');
    input.addEventListener('keyup', CheckSuggestions);
    
    inputframe.appendChild(div);
    inputframe.appendChild(input);
    
    CheckSuggestions();
  
    function CheckSuggestions(){
      var value = input.value,
          suggestions = tree.getSuggestions(value);
      if(value.length == 0){
        div.innerHTML = inputframe.getAttribute('placeholder');
        return;
      };
      var least = Infinity, lValue;
      for(var i=0, suggestion; suggestion=suggestions[i++];){
        var dist = levenshteinDistance(value, suggestion);
        if(dist < least){
          least = dist;
          lValue = suggestion;
        }
      }
      if(!lValue){
        div.innerHTML = '\<label>'+value+'\</label>';
        return;
      };
      if(!!value.match(/^[0-9]*$/))
        value = value.slice(0,3)+(value.length>3?' '+value.slice(3,6)+(value.length>6?'-'+value.slice(6,10):''):'');
      var index = lValue.toLowerCase().indexOf(value.toLowerCase());
      if(index == -1)
        div.innerHTML = lValue;
      else
        div.innerHTML = lValue.slice(0,index) + '\<label>'+value+'\</label>' + lValue.slice(value.length+index);
    }
  }
  
  
  function AddContact(contact){
    tree.add(contact);
  }
}