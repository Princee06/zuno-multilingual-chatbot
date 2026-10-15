/* chat */
const mk=()=>{const c={s:newId(),t:"New chat",m:[]};data.chats.unshift(c);return c};
function openApp(){
  $("who").textContent=(users()[me]||{}).name||"";
  $("app").dataset.t=LS.getItem("zuno:theme")||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light");
  show("app");cur=data.chats[0]||mk();list();draw();
}
function list(){
  const h=$("hist");h.innerHTML="";
  data.chats.filter(c=>c.m.length||c===cur).forEach(c=>{const b=document.createElement("button");b.className="ch"+(c===cur?" on":"");b.textContent=c.t;b.onclick=()=>{cur=c;list();draw()};h.appendChild(b)});
}
function draw(){
  const log=$("log");log.innerHTML="";
  if(!cur.m.length){log.innerHTML='<div class="empty" lang="'+(data.pref||"en")+'">'+find(data.pref)[3]+"</div>";return}
  cur.m.forEach((m,i)=>{
    const d=document.createElement("div");d.className=m.r;
    if(m.r==="u")d.textContent=m.t;
    else{
      d.innerHTML=md(m.ro?roman(m.t,m.l):m.t)+'<span class="tag">'+find(m.l)[2]+(m.ro?", romanized":"")+'</span><button class="dots" aria-label="Message options">⋯</button>';
      d.querySelector(".dots").onclick=e=>{e.stopPropagation();menu(d,i)};
    }
    log.appendChild(d);
  });
  log.scrollTop=log.scrollHeight;
}
function menu(d,i){
  document.querySelectorAll(".menu").forEach(x=>x.remove());
  const m=cur.m[i],mn=document.createElement("div");mn.className="menu";
  const add=(t,f)=>{const b=document.createElement("button");b.textContent=t;b.onclick=f;mn.appendChild(b)};
  add("Regenerate",()=>{const u=cur.m.slice(0,i).reverse().find(x=>x.r==="u");if(u)ask(u.t,i)});
  add("Read aloud",()=>{speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(m.t);u.lang=find(m.l)[4];speechSynthesis.speak(u)});
  if(IND.test(m.t))add(m.ro?"Show original":"Romanize to "+find(m.l)[1],()=>{m.ro=!m.ro;save();draw()});
  d.appendChild(mn);
}
document.onclick=()=>document.querySelectorAll(".menu").forEach(x=>x.remove());

async function ask(text,redo){
  const body=new FormData();body.append("message",text);body.append("session_id",cur.s);
  if(pending&&redo==null)body.append("file",pending);
  if(redo==null){cur.m.push({r:"u",t:text});if(cur.t==="New chat")cur.t=text.slice(0,32)}
  draw();list();
  const w=document.createElement("div");w.className="b";w.textContent="Reading and thinking...";$("log").appendChild(w);
  $("send").disabled=true;
  try{
    const r=await fetch(API_BASE+"/chat",{method:"POST",body});
    if(!r.ok)throw Error("server returned "+r.status);
    const j=await r.json();
    const m={r:"b",t:j.response,l:j.language,ro:!IND.test(text)&&IND.test(j.response)};
    redo==null?cur.m.push(m):cur.m[redo]=m;
    pending=null;$("file").value="";$("chip").textContent="";
  }catch(e){
    if(redo==null)cur.m.push({r:"b",t:"Zuno could not answer. Check that the server is running and try again. Details: "+e.message,l:"en"});
  }
  $("send").disabled=false;save();draw();
}
$("bar").onsubmit=e=>{e.preventDefault();const t=$("text").value.trim();if(!t)return;$("text").value="";ask(t)};
$("file").onchange=e=>{
  pending=e.target.files[0]||null;$("chip").textContent=pending?pending.name:"";
  if(pending&&/\.pdf$/i.test(pending.name)){$("frame").src=URL.createObjectURL(pending);$("pdf").hidden=false}
};
$("nc").onclick=()=>{cur=cur.m.length?mk():cur;$("pdf").hidden=true;list();draw()};
$("th").onclick=()=>{const a=$("app"),t=a.dataset.t==="dark"?"light":"dark";a.dataset.t=t;LS.setItem("zuno:theme",t)};
$("lg").onclick=()=>show("pick");
$("out").onclick=()=>{LS.removeItem("zuno:me");me=null;show("land")};
