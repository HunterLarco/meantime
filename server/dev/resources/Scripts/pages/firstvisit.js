window.addEventListener('load', function(){
  document.getElementById('firstvisit_button').addEventListener('click', function(){
    app.hideshow(document.getElementById('firstvisit_frame'), document.getElementById('signup_frame'));
    app.cookies.set('firstvisit', 'done');
  });
  if(app.cookies.get('firstvisit') == 'done')
    app.cookies.set('firstvisit', 'done');
});