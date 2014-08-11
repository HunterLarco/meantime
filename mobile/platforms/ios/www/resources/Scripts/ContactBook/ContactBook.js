function ContactBook(){
  var self = this;
  
  var tree = new ModifiedTrieTree();
  
  self.add = AddContact;
  self.suggest = Suggest;
  
  function Suggest(value){
    var suggestions = tree.getSuggestions(value);
    var least = Infinity, lValue = null;
    for(var i=0, suggestion; suggestion=suggestions[i++];){
      var dist = levenshteinDistance(value, suggestion.alias);
      if(dist < least){
        least = dist;
        lValue = suggestion;
      }
    }
    return lValue;
  }
  
  function AddContact(contact){
    tree.add(contact);
  }
}