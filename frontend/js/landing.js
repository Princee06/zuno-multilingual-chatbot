/* screens */
const screens=["land","auth","pick","app"];
function show(id){screens.forEach(s=>$(s).hidden=s!==id);$("bg").hidden=id==="app"}
const G=Array.from("अआकगतनमसఅఆకతనమసஅகதநமவಅಕತನಮಸഅകതനമവঅকতনমসઅકતનમસਅਕਤਨਮਸ");
for(let i=0;i<26;i++){const s=document.createElement("span");s.textContent=G[Math.random()*G.length|0];s.style.cssText=`left:${Math.random()*96}%;top:${Math.random()*92}%;font-size:${28+Math.random()*70}px;animation-duration:${7+Math.random()*7}s;animation-delay:-${Math.random()*9}s`;$("bg").appendChild(s)}
function cycle(){const g=L[gi++%L.length],h=$("hello");h.textContent=g[3];h.lang=g[0];h.classList.remove("in");void h.offsetWidth;h.classList.add("in")}
cycle();setInterval(cycle,2400);
