function BinarySearchTree(options){
  
  
  var self = this,
      options = typeof options == 'object' ? options : {};
  
  
  self.add = Add;
  self.contains = Contains;
  self.closest = Closest;
  self.__getRoot__ = GetRoot;
  
  
  var root = {left:{}, right:{}, value:null},
      hashtable = {};
  
  
  function GetRoot(){
    return root;
  }
  
  
  function Add(item){
    if(options.isSet && hashtable[item]) return;
    hashtable[item] = true;
    _Add(item, root);
  }
  function _Add(item, node){
    if(node.value != null) return _Add(item, item >= node.value ? node.right : node.left);
    node.value = item;
    node.left = {};
    node.right = {};
  }
  
  
  function Contains(item){
    return _Contains(item, root);
  }
  function _Contains(item, node){
    if(node.value == null) return false;
    if(node.value == item) return true;
    return _Contains(item, item >= node.value ? node.right : node.left);
  }
  
  
  function Closest(item){
    return _Closest(item, root, root.value);
  }
  function _Closest(item, node, value){
    if(node.value == null) return value;
    if(Math.abs(item-node.value) < Math.abs(item-value)) value = node.value
    return _Closest(item, item >= node.value ? node.right : node.left, value);
  }
  
  
}