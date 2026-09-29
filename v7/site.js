/* HubHug v7 — 共通の動き */
(function(){
  /* ヘッダー：スクロールしたら下線 */
  var hd=document.getElementById('hd');
  function hdState(){hd.classList.toggle('solid',scrollY>8)}
  addEventListener('scroll',hdState,{passive:true});hdState();

  /* メニュー（ドロワー） */
  var mb=document.getElementById('menu-btn'),dr=document.getElementById('drawer'),
      scrim=document.getElementById('scrim'),dc=document.getElementById('drawer-close');
  function setMenu(open,restore){
    dr.classList.toggle('open',open);scrim.classList.toggle('open',open);
    document.body.classList.toggle('lock',open);
    mb.setAttribute('aria-expanded',String(open));dr.setAttribute('aria-hidden',String(!open));
    if(open)setTimeout(function(){dc.focus()},60);else if(restore)mb.focus();
  }
  mb.addEventListener('click',function(){setMenu(true)});
  dc.addEventListener('click',function(){setMenu(false,true)});
  scrim.addEventListener('click',function(){setMenu(false,true)});
  dr.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){setMenu(false)})});
  addEventListener('keydown',function(e){if(e.key==='Escape'&&dr.classList.contains('open'))setMenu(false,true)});

  /* 本文の文節折り返し（Safari は word-break:auto-phrase 未対応） */
  var RE=/(?:[、。！？]|(?:を|に|は|へ|が|で|と|も|の|や|から|まで|より)(?=[^ぁ-ゖ、。」』）]))/g;
  function phrases(t){
    var out=[],last=0,m;RE.lastIndex=0;
    while((m=RE.exec(t))){out.push(t.slice(last,m.index+m[0].length));last=m.index+m[0].length;}
    if(last<t.length)out.push(t.slice(last));
    var r=[];
    out.forEach(function(p){if(r.length&&p.replace(/\s/g,'').length<=2)r[r.length-1]+=p;else r.push(p);});
    return r;
  }
  document.querySelectorAll('main p,main li,main dd,.t').forEach(function(el){
    if(/flex|grid/.test(getComputedStyle(el).display))return; /* 横並びの中は包むと崩れる（.t で包んでおく） */
    [].slice.call(el.childNodes).forEach(function(node){
      if(node.nodeType!==3)return;
      var t=node.nodeValue;
      if(!/[、。をにはへがでとものやら]/.test(t)||t.trim().length<8)return;
      var ps=phrases(t);if(ps.length<2)return;
      var frag=document.createDocumentFragment();
      ps.forEach(function(p){var sp=document.createElement('span');sp.className='np';sp.textContent=p;frag.appendChild(sp);});
      node.parentNode.replaceChild(frag,node);
    });
  });

  /* 数字は明朝（本文中の数字も <span class="n"> で包む） */
  var tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,{acceptNode:function(n){
    if(!/[0-9]/.test(n.nodeValue))return NodeFilter.FILTER_REJECT;
    return n.parentNode.closest('script,style,textarea,svg,.n,b.num')?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT;}});
  var nodes=[];while(tw.nextNode())nodes.push(tw.currentNode);
  nodes.forEach(function(node){
    var t=node.nodeValue,re=/[0-9]+(?:[,.][0-9]+)*%?/g,m,last=0,frag=document.createDocumentFragment();
    while((m=re.exec(t))){
      if(m.index>last)frag.appendChild(document.createTextNode(t.slice(last,m.index)));
      var s=document.createElement('span');s.className='n';s.textContent=m[0];frag.appendChild(s);
      last=m.index+m[0].length;
    }
    if(last<t.length)frag.appendChild(document.createTextNode(t.slice(last)));
    node.parentNode.replaceChild(frag,node);
  });

  /* 追従ボタン：ヒーローを過ぎたら出す／CTA・フォームが見えたら隠す */
  var fab=document.getElementById('fab');
  if(fab){
    var stop=document.getElementById('cform')||document.querySelector('.cta-box,.cta2');
    /* ページ内の相談ボタンが見えている間は出さない（同じボタンが二重に見えないように） */
    var seen=[];
    if('IntersectionObserver' in window){
      var io2=new IntersectionObserver(function(es){
        es.forEach(function(e){var i=seen.indexOf(e.target);if(e.isIntersecting&&i<0)seen.push(e.target);if(!e.isIntersecting&&i>=0)seen.splice(i,1);});
        fabState();});
      document.querySelectorAll('main .btns,main .aud-act').forEach(function(el){io2.observe(el)});
    }
    function fabState(){
      var past=scrollY>innerHeight*.5;
      var at=stop&&stop.getBoundingClientRect().top<innerHeight*.9;
      fab.classList.toggle('show',past&&!at&&!seen.length);
    }
    addEventListener('scroll',fabState,{passive:true});addEventListener('resize',fabState);fabState();
  }

  /* お問い合わせフォーム */
  var cform=document.getElementById('cform');
  if(cform){
    var q=new URLSearchParams(location.search).get('type');
    if(q){var pre=cform.querySelector('input[name="立場"][data-k="'+q+'"]');if(pre)pre.checked=true;}
    var isMail=function(v){return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim())};
    function check(inp){
      var box=inp.closest('[data-f]');if(!box)return true;var ok=true;
      if(inp.hasAttribute('required')&&!inp.value.trim())ok=false;
      if(ok&&inp.type==='email'&&inp.value.trim()&&!isMail(inp.value))ok=false;
      box.classList.toggle('bad',!ok);inp.setAttribute('aria-invalid',String(!ok));return ok;
    }
    cform.querySelectorAll('input[required],input[type=email]').forEach(function(i){
      i.addEventListener('blur',function(){check(i)});
      i.addEventListener('input',function(){if(i.closest('[data-f]').classList.contains('bad'))check(i)});
    });
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
      if(!ep&&!mt){var n=document.createElement('p');n.className='note';
        n.textContent='※デモ表示です。送信先（data-endpoint）が未設定のため、実際には送信されていません。';d.appendChild(n);}
      d.scrollIntoView({behavior:'smooth',block:'center'});
    });
  }
})();
