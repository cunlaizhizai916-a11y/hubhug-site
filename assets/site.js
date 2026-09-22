/* HubHug portal — shared behaviour */
(function(){
  /* header: solid after scroll */
  var hd=document.getElementById('hd');
  function hdState(){hd.classList.toggle('solid',scrollY>40)}
  addEventListener('scroll',hdState,{passive:true});hdState();

  /* drawer */
  var hamb=document.getElementById('hamb'),drawer=document.getElementById('drawer');
  function closeDrawer(){hamb.classList.remove('open');drawer.classList.remove('open');
    document.body.classList.remove('lock');hamb.setAttribute('aria-expanded','false');}
  hamb.addEventListener('click',function(){
    var open=!drawer.classList.contains('open');
    hamb.classList.toggle('open',open);drawer.classList.toggle('open',open);
    document.body.classList.toggle('lock',open);hamb.setAttribute('aria-expanded',String(open));});
  drawer.querySelectorAll('a').forEach(function(a){a.addEventListener('click',closeDrawer)});
  addEventListener('keydown',function(e){if(e.key==='Escape')closeDrawer()});

  /* Safari has no word-break:auto-phrase — split body copy at particles/punctuation */
  var RE=/(?:[、。！？]|(?:を|に|は|へ|から|まで|より)(?=[^ぁ-ゖ]))/g;
  function phrases(t){
    var out=[],last=0,m;RE.lastIndex=0;
    while((m=RE.exec(t))){out.push(t.slice(last,m.index+m[0].length));last=m.index+m[0].length;}
    if(last<t.length)out.push(t.slice(last));
    var r=[];
    out.forEach(function(p){if(r.length&&p.replace(/\s/g,'').length<=2)r[r.length-1]+=p;else r.push(p);});
    return r;
  }
  document.querySelectorAll('p,li,dd,td').forEach(function(el){
    [].slice.call(el.childNodes).forEach(function(node){
      if(node.nodeType!==3)return;
      var t=node.nodeValue;
      if(!/[、。をにはへ]/.test(t)||t.trim().length<8)return;
      var ps=phrases(t);if(ps.length<2)return;
      var frag=document.createDocumentFragment();
      ps.forEach(function(p){var sp=document.createElement('span');sp.className='np';sp.textContent=p;frag.appendChild(sp);});
      node.parentNode.replaceChild(frag,node);
    });
  });

  /* reveal on scroll */
  var rv=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){
      if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
    rv.forEach(function(el){io.observe(el)});
  }else rv.forEach(function(el){el.classList.add('in')});

  /* mobile sticky bar: show after hero, hide at form/footer */
  var spbar=document.getElementById('spbar');
  if(spbar){
    var stop=document.getElementById('cform')||document.querySelector('.cta');
    function spState(){
      var past=scrollY>innerHeight*.6;
      var at=stop&&stop.getBoundingClientRect().top<innerHeight*.8;
      spbar.classList.toggle('show',past&&!at);
    }
    addEventListener('scroll',spState,{passive:true});spState();
  }

  /* contact form */
  var cform=document.getElementById('cform');
  if(cform){
    var q=new URLSearchParams(location.search).get('type');
    if(q){var pre=cform.querySelector('input[name="立場"][data-k="'+q+'"]');if(pre)pre.checked=true;}
    var isMail=function(v){return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim())};
    function check(inp){
      var box=inp.closest('[data-f]');if(!box)return true;var ok=true;
      if(inp.hasAttribute('required')&&!inp.value.trim())ok=false;
      if(ok&&inp.type==='email'&&inp.value.trim()&&!isMail(inp.value))ok=false;
      box.classList.toggle('bad',!ok);return ok;
    }
    cform.querySelectorAll('input[required],input[type=email]').forEach(function(i){
      i.addEventListener('blur',function(){check(i)});});
    cform.addEventListener('submit',async function(e){
      e.preventDefault();
      var ts=[].slice.call(cform.querySelectorAll('input[required],input[type=email]'));
      var bad=ts.filter(function(t){return !check(t)});
      if(bad.length){bad[0].closest('[data-f]').scrollIntoView({behavior:'smooth',block:'center'});
        bad[0].focus({preventScroll:true});return;}
      var data={};new FormData(cform).forEach(function(v,k){data[k]=v});
      var ep=cform.dataset.endpoint,mt=cform.dataset.mailto;
      try{
        if(ep){await fetch(ep,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)});}
        else if(mt){
          var body=Object.keys(data).map(function(k){return '【'+k+'】 '+data[k]}).join('\n');
          location.href='mailto:'+mt+'?subject='+encodeURIComponent('HubHugへのお問い合わせ')+'&body='+encodeURIComponent(body);}
      }catch(err){}
      cform.hidden=true;var d=document.getElementById('cdone');d.hidden=false;
      if(!ep&&!mt){var n=document.createElement('p');n.className='fnote';
        n.textContent='※デモ表示です。送信先（data-endpoint）が未設定のため、実際には送信されていません。';d.appendChild(n);}
      d.scrollIntoView({behavior:'smooth',block:'center'});
    });
  }
})();
