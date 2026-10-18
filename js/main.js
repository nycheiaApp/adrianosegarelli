/* Adriano Segarelli — script del sito.
   1) Filigrana e sfondo home: a ogni arrivo in home si sceglie un'opera diversa (elenco in js/data/opere.js).
   2) Carosello foto nelle pagine evento.  3) Modulo contatti (apre il programma di posta). */
(function(){
var BASE=new URL('../',document.currentScript.src).href;
var body=document.body;
function get(){try{return parseInt(sessionStorage.getItem('wm')||'-1',10)}catch(e){return -1}}
function set(i){try{sessionStorage.setItem('wm',i)}catch(e){}}
function pick(different){var n=OPERE.length,last=get(),i;
 if(!different&&last>=0&&last<n)return last;
 do{i=Math.floor(Math.random()*n)}while(n>1&&i===last);
 set(i);return i}
function apply(i){var o=OPERE[i],s=body.style;
 s.setProperty('--wm','url("'+BASE+o.filigrana+'")');
 s.setProperty('--wms',o.orizzontale?'cover':'auto 108%');
 s.setProperty('--wmp',o.orizzontale?'center':'68% 50%');
 s.setProperty('--wmm',o.punto);s.setProperty('--wmo',o.opacita);
 s.setProperty('--hb','url("'+BASE+o.sfondo+'")');s.setProperty('--hp',o.punto);
 s.setProperty('--ho1',o.velo1);s.setProperty('--ho2',o.velo2)}
if(typeof OPERE!=='undefined'&&OPERE.length)apply(pick(body.classList.contains('home')));

var car=document.querySelector('.car');
if(car){var fs=[].slice.call(car.querySelectorAll('figure')),cur=0,cn=car.querySelector('.cnt');
 car.classList.add('js');
 function show(i){cur=(i+fs.length)%fs.length;fs.forEach(function(f,k){f.classList.toggle('on',k===cur)});cn.textContent=(cur+1)+' / '+fs.length}
 car.querySelector('.pv').onclick=function(){show(cur-1)};car.querySelector('.nx').onclick=function(){show(cur+1)};show(0)}

var tb=document.querySelector('.tabs');
if(tb){var tabs=[].slice.call(tb.querySelectorAll('[role=tab]')),pn=[].slice.call(tb.querySelectorAll('.tp'));tb.classList.add('js');
 function sel(i,focus){tabs.forEach(function(t,k){var on=k===i;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;pn[k].classList.toggle('on',on)});if(focus)tabs[i].focus()}
 tabs.forEach(function(t,i){t.onclick=function(){sel(i);try{history.replaceState(null,'','#'+t.dataset.k)}catch(e){}};
  t.onkeydown=function(e){if(e.key==='ArrowRight')sel((i+1)%tabs.length,1);else if(e.key==='ArrowLeft')sel((i-1+tabs.length)%tabs.length,1)}});
 var h=location.hash.slice(1),k=tabs.findIndex(function(t){return t.dataset.k===h});sel(k>=0?k:0)}

var zs=document.querySelectorAll('a.zoom');
if(zs.length){var ov=document.createElement('div');ov.className='lb';ov.hidden=true;ov.setAttribute('role','dialog');ov.setAttribute('aria-modal','true');ov.setAttribute('aria-label','Immagine ingrandita');
 ov.innerHTML='<button type="button" class="btn lb-back">\u2190 Torna indietro</button><figure><img alt=""><figcaption></figcaption></figure>';
 document.body.appendChild(ov);
 var li=ov.querySelector('img'),lc=ov.querySelector('figcaption'),bk=ov.querySelector('.lb-back'),last=null,sy=0,pushed=false;
 function openLb(a){last=a;sy=window.scrollY;li.src=a.href;li.alt=a.querySelector('img').alt;lc.innerHTML=a.parentNode.querySelector('figcaption').innerHTML;
  ov.hidden=false;document.body.classList.add('lb-open');bk.focus();
  try{history.pushState({lb:1},'');pushed=true}catch(e){pushed=false}}
 function closeLb(){if(ov.hidden)return;ov.hidden=true;document.body.classList.remove('lb-open');window.scrollTo(0,sy);if(last)last.focus({preventScroll:true})}
 zs.forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();openLb(a)})});
 bk.onclick=function(){if(pushed){pushed=false;history.back()}else closeLb()};
 window.addEventListener('popstate',function(){pushed=false;closeLb()});
 ov.addEventListener('click',function(e){if(e.target===ov)bk.onclick()});
 document.addEventListener('keydown',function(e){if(!ov.hidden&&e.key==='Escape')bk.onclick()})}

var f=document.getElementById('f');
if(f)f.addEventListener('submit',function(e){e.preventDefault();var d=new FormData(f);
 var b='Nome: '+d.get('n')+'\nEmail: '+d.get('e')+'\nRichiesta: '+d.get('t')+'\n\n'+d.get('m');
 document.getElementById('ok').style.display='block';
 location.href='mailto:adrianosegarelli.art@gmail.com?subject='+encodeURIComponent(d.get('t'))+'&body='+encodeURIComponent(b)});
})();
