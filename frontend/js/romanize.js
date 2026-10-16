/* romanizer: Indic scripts share one Unicode layout, so one table covers them all */
const C={},M={},V={5:"a",6:"aa",7:"i",8:"ii",9:"u",10:"uu",11:"ri",14:"e",15:"e",16:"ai",18:"o",19:"o",20:"au"},S={1:"n",2:"m",3:"h"},CH={122:"n",123:"n",124:"r",125:"l",126:"l",127:"k"};
"k kh g gh ng ch chh j jh ny t th d dh n t th d dh n n p ph b bh m y r r l l l v sh sh s h".split(" ").forEach((x,i)=>C[21+i]=x);
"aa i ii u uu ri".split(" ").forEach((x,i)=>M[62+i]=x);
Object.assign(M,{69:"e",70:"e",71:"e",72:"ai",73:"o",74:"o",75:"o",76:"au"});
function roman(t,l){
  const dev=l==="hi"||l==="mr";let o="",p=false;
  const flush=()=>{if(p&&!dev)o+="a";p=false};
  for(const ch of t){
    const c=ch.codePointAt(0),b=[2304,2432,2560,2688,2944,3072,3200,3328].find(x=>c>=x&&c<x+128),k=c-b;
    if(b===undefined){flush();o+=ch}
    else if(C[k]){if(p)o+="a";o+=C[k];p=true}
    else if(M[k]){o+=M[k];p=false}
    else if(k===77)p=false;else if(b===3328&&CH[k]){if(p)o+="a";o+=CH[k];p=false}
    else if(V[k]||S[k]){if(p)o+="a";o+=V[k]||S[k];p=false}
    else{flush();o+=ch}
  }
  flush();
  return o.replace(/(^|[.?!]\s+)([a-z])/g,(x,a,b)=>a+b.toUpperCase());
}
