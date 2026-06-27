export default {
  async fetch(request, env, ctx) {
    const url=new URL(request.url);
    const c={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Methods":"GET,POST,OPTIONS","Access-Control-Allow-Headers":"Content-Type"};
    if(request.method==="OPTIONS") return new Response(null,{headers:c});
    try{
      if(request.method==="POST"&&url.pathname==="/sync"){
        const b=await request.json();
        const code=b.syncCode||"master";
        const catches=b.catches;
        if(!catches) return new Response(JSON.stringify({error:"missing catches"}),{status:400,headers:{"Content-Type":"application/json",...c}});
        await env.RECORDS_KV.put(code,JSON.stringify(catches));
        return new Response(JSON.stringify({ok:true,count:catches.length}),{headers:{"Content-Type":"application/json",...c}});
      }
      if(request.method==="GET"&&url.pathname==="/sync"){
        const code=url.searchParams.get("code")||"master";
        const d=await env.RECORDS_KV.get(code);
        return new Response(JSON.stringify({catches:d?JSON.parse(d):[]}),{headers:{"Content-Type":"application/json",...c}});
      }
      return new Response(JSON.stringify({status:"ok"}),{headers:{"Content-Type":"application/json",...c}});
    }catch(e){return new Response(JSON.stringify({error:e.message}),{status:500,headers:{"Content-Type":"application/json",...c}});}
  }
}
