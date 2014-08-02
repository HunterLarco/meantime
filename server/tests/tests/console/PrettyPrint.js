function PrettyPrint(data, elem){
  var innerHTML = '';
  var singletab = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
  function recurse(object, tabs){
    for(key in object){
      if(object[key] == null){
        innerHTML += tabs+key+' : \<label class="nl">null\</label>\<br/>';
        continue;
      }
      switch(object[key].constructor){
        case String:
          innerHTML += tabs+key+' : \<label class="s">'+object[key]+'\</label>\<br/>';
        break;
        case Array:
          innerHTML += tabs+key+' : \<label class="o"> Array ['+object[key].length+']\</label>\<br/>';
          recurse(object[key], tabs+singletab)
        break;
        case Number:
          innerHTML += tabs+key+' : \<label class="n">'+object[key]+'\</label>\<br/>';
        break;
        case Boolean:
          innerHTML += tabs+key+' : \<label class="b">'+object[key]+'\</label>\<br/>';
        break;
        case Object:
          innerHTML += tabs+key+' : \<label class="o"> Object {'+Object.keys(object[key]).length+'}\</label>\<br/>';
          recurse(object[key], tabs+singletab)
        break;
      }
    }
  }
  if(data.constructor == Array || data.constructor == Object){
    var innerHTML = '\<label class="o"> Object {'+Object.keys(data).length+'}\</label> {\<br/>';
    recurse(data, singletab)
    return innerHTML+'}';
  }else{
    switch(data.constructor){
      case String:
        return '\<label class="s">'+data+'\</label>\<br/>';
      break;
      case Number:
        return '\<label class="n">'+data+'\</label>\<br/>';
      break;
      case Boolean:
        return '\<label class="b">'+data+'\</label>\<br/>';
      break;
    }
  }
}