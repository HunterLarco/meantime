function Sidebar(root){
  var self = this;
  
  
  self.toggle = ToggleVisiblity;
  self.tree = GetTree;
  
  
  var itemtree = {};
  
  
  ShowRoot();
  LoadItemTree();
  
  
  
  function GetTree(){
    return itemtree;
  }
  function ToggleVisiblity(){
    root.parentElement.classList.toggle('opened');
  }
  
  
  function BindMenu(node){
    if(!node.menu.exists) return;
    
    if(!!node.menu.back)
      node.menu.back.addEventListener('click', function(event){
        event.stopPropagation();
        node.menu.element.classList.remove('opened');
        node.parent.menu.element.classList.remove('covered');
      });
    
    node.self.addEventListener('click', function(){
      node.menu.element.classList.add('opened');
      node.parent.menu.element.classList.add('covered');
    });
    
  }
  
  
  function ShowRoot(){
    root.classList.add('opened');
    root.setAttribute('name', 'root');
  }
  
  
  function LoadItemTree(){
    function Recurse(treenode, nodemenu){
      for(var i=0,elem; elem=nodemenu.children[i++];){
        if(elem.classList.contains('back'))
          treenode.menu.back = elem;
        if(!elem.classList.contains('menuitem') && elem != root) continue;
        var buzzword = elem.getAttribute('name');
        if(!buzzword) continue;
        var menu = elem.children.length == 0 ? null : elem.children[0],
            back = null;
        treenode.menu.items[buzzword] = {
          'menu': {
            'exists': !!menu,
            'element': menu,
            'back': null,
            'items': {}
          },
          'self': elem,
          'parent': treenode
        }
        if(!!menu) Recurse(treenode.menu.items[buzzword], menu);
        BindMenu(treenode.menu.items[buzzword]);
      }
    }
    itemtree.menu = {
      'exists': true,
      'element': root,
      'back': null,
      'items': {}
    }
    itemtree.parent = null;
    itemtree.self = root;
    Recurse(itemtree, root);
  }
  
  
}






window.addEventListener('load', function(){
	var sidebar = new Sidebar(document.getElementById('settings_root'));
  document.getElementById('header_settingsbutton').addEventListener('click', sidebar.toggle);
  app.data.sidebar = sidebar;
});