(function(){
  
  function Page(frame){
    var self = this;
    self.super(frame);
    
    
    self.getDate = GetSelectedDateTime;
    self.getContacts = GetSelectedContacts;
    
    self.reset = new Function();
    
    
    function GetSelectedDateTime(){
      if(self.elements.picker.frame.classList.contains('show')) return GetDatePickerDate();
      else return GetQuickDate();
    }
    
    function ShowDatePicker(){
      self.elements.picker.frame.classList.add('show');
      ResetQuickPicker();
      GenerateDays();
    }
    function HideDatePicker(){
      self.elements.picker.frame.classList.remove('show');
    }
    
    function CheckContinueButton(){
      var date = GetSelectedDateTime(),
          contacts = GetSelectedContacts();
      if(!date || contacts.length == 0) self.elements.buttons.continue.classList.remove('ready');
      else self.elements.buttons.continue.classList.add('ready');
    }
    function Continue(){
      if(!self.elements.buttons.continue.classList.contains('ready')) return;
      app.pages['sendmessage'].focus();
    }
    
    function Reset(){
      ResetDatePicker();
      ResetQuickPicker();
      self.elements.frames.contacts.innerHTML = '';
      checkboxes = [];
      HideDatePicker();
      self.elements.buttons.continue.classList.remove('ready');
    }
    
    
    // ------------------- BEGINNING OF CONTACT CODE ------------------- //
    
    var checkboxes = [];
    
    function GetSelectedContacts(){
      var list = [];
      for(var i=0,checkbox; checkbox=checkboxes[i++];){
        if(!checkbox.checked) continue;
        list.push(checkbox.contact);
      }
      return list;
    }
    
    function LoadContacts(){
      var contacts = app.pages['contacts'].getContacts();
      for(var i=0,contact; contact=contacts[i++];){
        var title = contact.name || contact.email || contact.mobile;
        
        var div = document.createElement('div');
        div.classList.add('contact');
          var checkbox = document.createElement('input');
          checkbox.setAttribute('type', 'checkbox');
          checkbox.contact = contact;
          checkbox.addEventListener('click', CheckContinueButton);
          checkbox.checked = true;
          checkboxes.push(checkbox);
          div.appendChild(checkbox);
          var text = document.createElement('div');
          text.classList.add('text');
          text.innerHTML = title;
          div.appendChild(text);
        
        self.elements.frames.contacts.appendChild(div);
      }
    }
    
    // ------------------- END OF CONTACT CODE ------------------- //
    
    
    // ------------------- BEGINNING OF QUICK PICKER CODE ------------------- //
    
    var unit, unitElem,
        value, valueElem,
        onquickchange = new Function();
    
    function BindQuickPicker(){
      for(var key in self.elements.picker.quick.value){
        var elem = self.elements.picker.quick.value[key];
        (function(elem){
          elem.addEventListener('click', function(){
            if(elem.classList.contains('selected')) return;
            HideDatePicker();
            value = parseInt(elem.innerHTML);
            elem.classList.add('selected');
            if(!!valueElem) valueElem.classList.remove('selected');
            valueElem = elem;
            onquickchange();
          });
        })(elem);
      }
      
      for(var key in self.elements.picker.quick.unit){
        var elem = self.elements.picker.quick.unit[key];
        (function(elem){
          elem.addEventListener('click', function(){
            if(elem.classList.contains('selected')) return;
            HideDatePicker();
            if(elem.innerHTML == 'minutes')    unit = 1000*60;
            else if(elem.innerHTML == 'hours') unit = 1000*60*60;
            else if (elem.innerHTML == 'days') unit = 1000*60*60*24;
            elem.classList.add('selected');
            if(!!unitElem) unitElem.classList.remove('selected');
            unitElem = elem;
            onquickchange();
          });
        })(elem);
      }
    }
    function ResetQuickPicker(){
      if(!!valueElem) valueElem.classList.remove('selected');
      if(!!unitElem) unitElem
      .classList.remove('selected');
      unit  = unitElem  =
      value = valueElem = undefined;
    }
    
    function GetQuickDate(){
      if(!unit || !value) return null;
      var date = new Date();
      date.setSeconds(0);
      date.setMilliseconds(0);
      return new Date(date.getTime() + unit*value);
    }
    
    // ------------------- End OF QUICK PICKER CODE ------------------- //
    
    
    // ------------------- BEGINNING OF DATE PICKER CODE ------------------- //
    
    var selecteddate = new Date(),
        viewingdate = new Date(selecteddate.getTime());
    
    var framelevel = 0, ondatechange = new Function();
    
    function GetDatePickerDate(){
      var date = new Date(selecteddate.getTime());
      date.setHours((self.elements.picker.time.hour.selectedIndex+1)%12 + 12*self.elements.picker.time.ampm.selectedIndex);
      date.setMinutes(self.elements.picker.time.minute.selectedIndex);
      date.setMilliseconds(0);
      date.setSeconds(0);
      return date;
    }
    
    function BindDatePicker(){
      self.elements.picker.buttons.left.addEventListener('click', Prev);
      self.elements.picker.buttons.right.addEventListener('click', Next);
      self.elements.picker.buttons.header.addEventListener('click', NextLevel);
    }
    function ResetDatePicker(){
      selecteddate = new Date();
      viewingdate = new Date(selecteddate.getTime());
    }
    
    function ShowDays(){
      GenerateDays();
      self.elements.picker.frames.calendar.classList.remove('gone');
      self.elements.picker.frames.months.parentElement.classList.add('gone');
    }
    function GenerateDays(){
      var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      self.elements.picker.buttons.header.innerHTML = months[viewingdate.getMonth()]+' '+viewingdate.getFullYear();
      self.elements.picker.frames.days.innerHTML = '';
      var startdate = new Date(viewingdate.getTime());
      startdate.setDate(1);
      startdate.setDate(1-startdate.getDay());
      var enddate = new Date(viewingdate.getTime());
      enddate.setMonth(enddate.getMonth()+1);
      enddate.setDate(0);
      enddate.setDate(enddate.getDate()+6-enddate.getDay());
      var totaldays = (enddate.getTime() - startdate.getTime()) / (1000*60*60*24);
      for(var i=0; i<=totaldays; i++){
        var day = document.createElement('div');
        day.classList.add('day')
        if (startdate.getMonth() != viewingdate.getMonth()) day.classList.add('not-allowed');
        if (startdate.getTime() == selecteddate.getTime()) day.classList.add('selected');
        day.innerHTML = startdate.getDate();
        
        (function(date){
          if (startdate.getMonth() != viewingdate.getMonth()) return;
          day.addEventListener('click', function(){
            viewingdate.setDate(date);
            selecteddate.setDate(viewingdate.getDate());
            selecteddate.setMonth(viewingdate.getMonth());
            selecteddate.setFullYear(viewingdate.getFullYear());
            ondatechange();
            GenerateDays();
          });
        })(startdate.getDate());
        
        self.elements.picker.frames.days.appendChild(day);
        startdate.setDate(startdate.getDate()+1);
      }
    }
    function PrevMonth(){
      viewingdate.setMonth(viewingdate.getMonth()-1);
      GenerateDays();
    }
    function NextMonth(){
      viewingdate.setMonth(viewingdate.getMonth()+1);
      GenerateDays();
    }
    
    function NextLevel(){
      switch(framelevel++){
        case 0: return ShowMonths();
        case 1: return ShowYears();
        default: return;
      }
    }
    function PrevLevel(){
      switch(--framelevel){
        case 0: return ShowDays();
        case 1: return ShowMonths();
        default: return;
      }
    }
    function Prev(){
      switch(framelevel){
        case 0: return PrevMonth();
        case 1: return PrevYear();
        case 2: return PrevYears();
      }
    }
    function Next(){
      switch(framelevel){
        case 0: return NextMonth();
        case 1: return NextYear();
        case 2: return NextYears();
      }
    }
    
    function ShowMonths(){
      GenerateMonths();
      self.elements.picker.frames.calendar.classList.add('gone');
      self.elements.picker.frames.years.parentElement.classList.add('gone');
      self.elements.picker.frames.months.parentElement.classList.remove('gone');
    }
    function GenerateMonths(){
      self.elements.picker.buttons.header.innerHTML = viewingdate.getFullYear();
      self.elements.picker.frames.months.innerHTML = '';
      
      var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      for(var i=0, month; month=months[i++];){
        var div = document.createElement('div');
        div.setAttribute('class', 'table-item');
        div.innerHTML = month;
        
        if(i-1 == selecteddate.getMonth() && viewingdate.getFullYear() == selecteddate.getFullYear())
          div.classList.add('selected');
        
        (function(month){
          div.addEventListener('click', function(){
            viewingdate.setMonth(month);
            selecteddate.setMonth(viewingdate.getMonth());
            selecteddate.setFullYear(viewingdate.getFullYear());
            ondatechange();
            PrevLevel();
          });
        })(i-1);
        
        self.elements.picker.frames.months.appendChild(div);
      }
    }
    function NextYear(){
      viewingdate.setFullYear(viewingdate.getFullYear()+1);
      GenerateMonths();
    }
    function PrevYear(){
      viewingdate.setFullYear(viewingdate.getFullYear()-1);
      GenerateMonths();
    }
    
    function ShowYears(){
      GenerateYears();
      self.elements.picker.frames.months.parentElement.classList.add('gone');
      self.elements.picker.frames.years.parentElement.classList.remove('gone');
    }
    function GenerateYears(){
      self.elements.picker.buttons.header.innerHTML = viewingdate.getFullYear() + ' - ' + (viewingdate.getFullYear()+12);
      self.elements.picker.frames.years.innerHTML = '';
      
      for(var i=0; i<12; i++){
        var year = viewingdate.getFullYear()+i;
        
        var div = document.createElement('div');
        div.setAttribute('class', 'table-item');
        div.innerHTML = year;
        
        if(year == selecteddate.getFullYear())
          div.classList.add('selected');
        
        (function(year){
          div.addEventListener('click', function(){
            viewingdate.setFullYear(year);
            selecteddate.setFullYear(viewingdate.getFullYear());
            ondatechange();
            PrevLevel();
          });
        })(year);
        
        self.elements.picker.frames.years.appendChild(div);
      }
    }
    function NextYears(){
      viewingdate.setFullYear(viewingdate.getFullYear()+13);
      GenerateYears();
    }
    function PrevYears(){
      viewingdate.setFullYear(viewingdate.getFullYear()-13);
      GenerateYears();
    }
    
    // ------------------- END OF DATE PICKER CODE ------------------- //
    
    (function Constructor(){
      self.addEventListener('focus', function(){
        Reset();
        LoadContacts();
      });
      BindDatePicker();
      BindQuickPicker();
      onquickchange = CheckContinueButton;
      ondatechange = CheckContinueButton;
      self.elements.picker.button.addEventListener('click', ShowDatePicker);
      self.elements.buttons.back.addEventListener('click', function(){app.pages['contacts'].focus()});
      self.elements.buttons.continue.addEventListener('click', Continue);
    })();
  }
  
  
  if(!window.pages) window.pages = {};
  window.pages['datepicker'] = Page;
  
})();