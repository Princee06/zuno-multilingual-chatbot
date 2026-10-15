/* login and sign up, kept in this browser only */
function setMode(m){mode=m;$("at").textContent=m==="login"?"Log in":"Sign up";$("nm").hidden=m==="login";$("sw").textContent=m==="login"?"New here? Sign up":"Have an account? Log in";$("err").textContent="";show("auth")}
document.querySelectorAll("[data-go]").forEach(b=>b.onclick=()=>setMode(b.dataset.go));
$("sw").onclick=()=>setMode(mode==="login"?"signup":"login");
const sha=async s=>[...new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(s)))].map(x=>x.toString(16).padStart(2,"0")).join("");
$("af").onsubmit=async e=>{
  e.preventDefault();
  const em=$("em").value.trim().toLowerCase(),h=await sha($("pw").value),u=users();
  if(mode==="signup"){
    if(u[em]){$("err").textContent="This email already has an account. Log in instead.";return}
    u[em]={name:$("nm").value.trim()||em.split("@")[0],h};LS.setItem("zuno:users",JSON.stringify(u));enter(em,true);
  }else{
    if(!u[em]||u[em].h!==h){$("err").textContent="Email or password is incorrect.";return}
    enter(em,false);
  }
};
function enter(em,fresh){
  me=em;LS.setItem("zuno:me",em);
  data=JSON.parse(LS.getItem("zuno:d:"+em)||'{"chats":[],"pref":""}');
  fresh||!data.pref?show("pick"):openApp();
}
L.forEach(l=>{const b=document.createElement("button");b.className="btn";b.textContent=l[2];b.lang=l[0];b.onclick=()=>{data.pref=l[0];save();openApp()};$("langs").appendChild(b)});
