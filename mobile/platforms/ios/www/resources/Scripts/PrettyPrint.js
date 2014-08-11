function PrettyPrint(data){
  var innerHTML = '',
      singletab = '&nbsp;&nbsp;';
  function recurse(object, tabs){
    for(var key in object){
      if(object[key] == null){
        innerHTML += tabs+key+' : \<label class="nl">null\</label>\<br/>';
        continue;
      }
      if(object[key] == undefined){
        innerHTML += tabs+key+' : \<label class="nl">undefined\</label>\<br/>';
        continue;
      }
      switch(typeof object[key]){
        case 'string':
          innerHTML += tabs+key+' : \<label class="s">'+object[key]+'\</label>\<br/>';
        break;
        case 'number':
          innerHTML += tabs+key+' : \<label class="n">'+object[key]+'\</label>\<br/>';
        break;
        case 'boolean':
          innerHTML += tabs+key+' : \<label class="b">'+object[key]+'\</label>\<br/>';
        break;
        case 'object':
          var len, nm;
          try{
            len = Object.keys(object[key]).length;
            nm = 'Object';
          }catch(e){
            len = object[key].length;
            nm = 'Array';
          }
          innerHTML += tabs+key+' :\<label class="o"> '+nm+' {'+len+'}\</label>\<br/>';
          recurse(object[key], tabs+singletab)
        break;
      }
    }
  }
  if(typeof data == 'object'){
    var len, nm;
    try{
      len = Object.keys(data).length;
      nm = 'Object';
    }catch(e){
      len = data.length;
      nm = 'Array';
    }
    var innerHTML = '\<label class="o"> '+nm+' {'+len+'}\</label> {\<br/>';
    recurse(data, singletab)
    return innerHTML+'}';
  }else{
    if(data == null) return '\<label class="nl">null\</label>\<br/>';
    if(data == undefined) return '\<label class="nl">undefined\</label>\<br/>';
    switch(typeof data){
      case 'string':
        return '\<label class="s">'+data+'\</label>\<br/>';
      break;
      case 'number':
        return '\<label class="n">'+data+'\</label>\<br/>';
      break;
      case 'boolean':
        return '\<label class="b">'+data+'\</label>\<br/>';
      break;
    }
    return PrettyPrint(data+'');
  }
}