window.addEventListener('load', function(){
  var cookies = new (function(){
    var self = this;
    
    
    self.set = function(cookiename, value, days){
  		var days = days || 365,
  		    expirationDate = new Date(Date.now()+1000*60*60*24*days),
  		    cookie = escape(value) + '; expires=' + expirationDate.toUTCString() + '; path=/;';
  		document.cookie = cookiename + "=" + cookie;
    }
    
    
    self.get = function(cookiename){
      var ARRcookies = document.cookie.split(';');
      for (var i=0; i<ARRcookies.length; i++){
        var x = ARRcookies[i].substr(0, ARRcookies[i].indexOf('=')),
            y = ARRcookies[i].substr(ARRcookies[i].indexOf('=') + 1);
        x = x.replace(/^\s+|\s+$/g,"");
        if (x == cookiename) return unescape(y);
      }
    }
    
    
    self.delete = function(cookiename){
      self.set(cookiename, 'delete', -1);
    }
  })();
  if(!!cookies.get('disableegg')) return;
  var logo = [
    '      ___           ___           ___           ___       ___           ___     ',
    '     /\\  \\         /\\  \\         /\\  \\         /\\__\\     /\\  \\         /\\  \\    ',
    '    /::\\  \\       /::\\  \\       /::\\  \\       /:/  /    /::\\  \\       /::\\  \\   ',
    '   /:/\\ \\  \\     /:/\\:\\  \\     /:/\\:\\  \\     /:/  /    /:/\\:\\  \\     /:/\\:\\  \\  ',
    '  _\\:\\~\\ \\  \\   /::\\~\\:\\  \\   /::\\~\\:\\  \\   /:/  /    /::\\~\\:\\  \\   /:/  \\:\\__\\ ',
    ' /\\ \\:\\ \\ \\__\\ /:/\\:\\ \\:\\__\\ /:/\\:\\ \\:\\__\\ /:/__/    /:/\\:\\ \\:\\__\\ /:/__/ \\:|__|',
    ' \\:\\ \\:\\ \\/__/ \\:\\~\\:\\ \\/__/ \\/__\\:\\/:/  / \\:\\  \\    \\:\\~\\:\\ \\/__/ \\:\\  \\ /:/  /',
    '  \\:\\ \\:\\__\\    \\:\\ \\:\\__\\        \\::/  /   \\:\\  \\    \\:\\ \\:\\__\\    \\:\\  /:/  / ',
    '   \\:\\/:/  /     \\:\\ \\/__/        /:/  /     \\:\\  \\    \\:\\ \\/__/     \\:\\/:/  /  ',
    '    \\::/  /       \\:\\__\\         /:/  /       \\:\\__\\    \\:\\__\\        \\::/__/   ',
    '     \\/__/         \\/__/         \\/__/         \\/__/     \\/__/         ~~       '
  ];
  var text = [
    'Hi there, nice to meet you!',
    '',
    'Interested in writing code and having an impact on the web? Join',
    'Sealed and become part of our developing community.',
    '',
    'Email admin@trysealed.com to inquire about current job openings',
    'or simply spread the word and tell everyone you know about Sealed!',
    '',
    '---',
    '',
    'If you don\'t want to see this message again, run this JS statement:',
    '',
    '\tconsole.disableEasterEgg();'
  ];
  console.log('\n\n'+logo.join('\n')+'\n\n\n'+text.join('\n')+'\n\n');
  console.disableEasterEgg = function(){
    cookies.set('disableegg', 'true');
  }
});