(function(){
  
  window.addEventListener('load', function(){
    document.getElementById('header_capturebutton').addEventListener('click', function(){
      app.pages['capture'].focus();
    });
  });
  
})();