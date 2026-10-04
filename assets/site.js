(function(){
  /* Contact details: fill these in and each row appears on the contact page */
  var CONTACT = {
    whatsapp: '',   // digits only, international format, e.g. '9715XXXXXXXX'
    phone: '',      // e.g. '+971 5X XXX XXXX'
    email: '',      // e.g. 'hello@example.com'
    instagram: ''   // handle without @
  };
  var build = {
    whatsapp:function(v){var d=v.replace(/\D/g,'');return ['https://wa.me/'+d,'+'+d]},
    phone:function(v){return ['tel:'+v.replace(/[^\d+]/g,''),v]},
    email:function(v){return ['mailto:'+v,v]},
    instagram:function(v){var h=v.replace(/^@/,'');return ['https://instagram.com/'+h,'@'+h]}
  };
  Object.keys(CONTACT).forEach(function(k){
    var v=CONTACT[k], row=document.querySelector('[data-contact="'+k+'"]');
    if(!v||!row) return;
    var r=build[k](v), a=row.querySelector('[data-value]');
    a.href=r[0]; a.textContent=r[1]; row.hidden=false;
  });
  var year=document.getElementById('year');
  if(year) year.textContent=new Date().getFullYear();

  /* header hairline once the page moves */
  var header=document.getElementById('header');
  function onScroll(){header.classList.toggle('is-scrolled',window.scrollY>8)}
  onScroll(); window.addEventListener('scroll',onScroll,{passive:true});

  /* mobile menu */
  var root=document.documentElement, burger=document.querySelector('.burger'), menu=document.getElementById('menu');
  function setMenu(open){
    root.classList.toggle('menu-open',open);
    burger.setAttribute('aria-expanded',open);
    burger.setAttribute('aria-label',open?'Close menu':'Open menu');
    menu.inert=!open;
  }
  setMenu(false);
  burger.addEventListener('click',function(){setMenu(!root.classList.contains('menu-open'))});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&root.classList.contains('menu-open')){setMenu(false);burger.focus()}});
  window.matchMedia('(min-width:1180px)').addEventListener('change',function(m){if(m.matches)setMenu(false)});

  /* booking form (contact page only) */
  var form=document.querySelector('form[name="booking"]');
  if(!form) return;

  /* "Enquire about Pilates" etc. arrive as /contact/?interest=Pilates */
  var interest=new URLSearchParams(location.search).get('interest');
  var select=document.getElementById('f-interest');
  if(interest&&[].some.call(select.options,function(o){return o.value===interest})) select.value=interest;

  var status=form.querySelector('.form__status');
  var messages={'f-name':'Please add your name.','f-email':'Please enter an email address Lia can reply to.'};
  function check(input){
    var ok=input.checkValidity()&&(input.type!=='email'||/.+@.+\..+/.test(input.value));
    input.closest('.field').classList.toggle('is-invalid',!ok);
    input.setAttribute('aria-invalid',String(!ok));
    document.getElementById(input.id+'-err').textContent=ok?'':messages[input.id];
    return ok;
  }
  var required=[].slice.call(form.querySelectorAll('[required]'));
  required.forEach(function(i){
    i.addEventListener('blur',function(){if(i.value||i.dataset.touched)check(i)});
    i.addEventListener('input',function(){if(i.dataset.touched)check(i)});
  });
  form.addEventListener('submit',function(e){
    e.preventDefault();
    required.forEach(function(i){i.dataset.touched='1'});
    var bad=required.filter(function(i){return !check(i)});
    if(bad.length){bad[0].focus();return}
    var btn=form.querySelector('button[type="submit"]');
    btn.disabled=true; btn.textContent='Sending…'; status.hidden=true;
    fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(form)).toString()})
      .then(function(r){if(!r.ok)throw new Error(r.status);
        form.reset(); required.forEach(function(i){delete i.dataset.touched});
        status.textContent='Thank you. Your request has been sent and Lia will be in touch personally.'; status.hidden=false;})
      .catch(function(){status.textContent='Sorry, the request didn’t go through. Please try again in a moment.'; status.hidden=false;})
      .finally(function(){btn.disabled=false; btn.textContent='Send request';});
  });
})();
