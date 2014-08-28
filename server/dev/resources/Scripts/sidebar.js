function Sidebar(sidebar, trigger){
  var self = this;
  
  
  self.toggle = ToggleVisiblity;
  self.show = Show;
  self.hide = Hide;
  self.tree = GetTree;
  
  var root = new Node({
    'menu': {
      'element': sidebar.children[0].children[0],
      'back': document.createElement('div')
    },
    'self': trigger
  });
  
  
  LoadNodeTree();
  
  
  trigger.addEventListener('click', self.toggle);
  
  
  function GetTree(){
    return root;
  }
  function ToggleVisiblity(){
    sidebar.children[0].children[0].parentElement.classList.toggle('opened');
  }
  function Show(){
    sidebar.children[0].children[0].parentElement.classList.add('opened');
  }
  function Hide(){
    sidebar.children[0].children[0].parentElement.classList.remove('opened');
  }
  
  
  function BindMenu(node){
    if(!node.hasMenu) return;
    
    if(!!node.menu.back)
      node.menu.back.addEventListener('click', function(event){
        event.stopPropagation();
        node.menu.element.classList.remove('opened');
        node.parent.menu.element.classList.remove('covered');
      });
    
    node.self.addEventListener('click', function(){
      if(node.menu.element.classList.contains('opened')) return;
      // fixes the scrolling messing up absolute positioning
      var scrollTop = node.parent.menu.element.children[0].scrollTop;
      node.menu.element.style.top = scrollTop+'px';
      node.menu.element.classList.add('opened');
      node.parent.menu.element.classList.add('covered');
    });
    
  }
  
  
  function Node(data){
    var self = this;
    
    
    var notifications = 0;
    
    
    self.self = data.self;
    self.parent = data.parent;
    
    
    self.hasMenu = !!data.menu.element;
    if(self.hasMenu){
      self.menu = {
        element: data.menu.element,
        back: data.menu.back,
        children: []
      }
    }
    
    
    self.setNotifications = SetNotifications;
    self.getNotifications = function(){return notifications;};
    
    
    function SetNotifications(newn){
      var diff = newn-notifications;
      notifications = newn;
      UpdateNotificationHTML();
      if(!self.parent) return;
      self.parent.setNotifications(self.parent.getNotifications()+diff);
    }
    
    
    function UpdateNotificationHTML(){
      var elem = self.self,
          value = notifications;
      if(!elem.hasNotificationElement){
        elem.hasNotificationElement = true;
        var notification = document.createElement('div');
        notification.setAttribute('class', 'notification');
        elem.appendChild(notification);
      }else{
        var notification;
        for(var j=0,child; child=elem.children[j++];)
          if(child.classList.contains('notification')){
            notification = child;
            break;
          }
      }
      notification.innerHTML = value;
      notification.style.display = value == 0 ? 'none' : 'block';
    }
  }
  
  
  function LoadNodeTree(){
    function Recurse(parentnode, menuelement){
      for(var i=0,elem; elem=menuelement.children[0].children[i++];){
        
        if(elem.classList.contains('back'))
          parentnode.menu.back = elem;
        
        if(!elem.classList.contains('menuitem') && elem != sidebar.children[0].children[0]) continue;
        
        var buzzword = elem.getAttribute('name');
        if(!buzzword) continue;
        
        var menu = elem.getElementsByClassName('menu').length == 0 ? null : elem.getElementsByClassName('menu')[0],
            back = null;
        
        var data = {
          'menu': {
            'element': menu,
            'back': null,
            'items': {}
          },
          'self': elem,
          'parent': parentnode
        }
        
        var node = new Node(data);
        parentnode.menu.children.push(node);
        parentnode.menu.children[buzzword] = node;
        
        if(!!menu) Recurse(node, menu);
        
        BindMenu(node);
      }
    }
    Recurse(root, sidebar.children[0].children[0]);
  }
  
  
}
