window.__store = {}; window.__log = [];
(function(){
  const store = window.__store; const subs = [];
  const notify = () => subs.forEach(s => s());
  function collSnap(path){ const pre = path + '/'; const docs = Object.keys(store).filter(k => k.startsWith(pre) && !k.slice(pre.length).includes('/')).map(k => ({id:k.slice(pre.length), exists:true, data:()=>JSON.parse(JSON.stringify(store[k]))})); return {docs, size:docs.length, empty:!docs.length}; }
  const db = {
    collection(path){ return { onSnapshot(next){ const f=()=>next(collSnap(path)); subs.push(f); setTimeout(f,10); return ()=>{}; }, doc(id){ return db.doc(path+'/'+id); } }; },
    doc(path){ return {
      async set(d){ if(JSON.stringify(d).includes('undefined')) throw new Error('undefined value'); store[path]=JSON.parse(JSON.stringify(d)); __log.push(['set',path]); setTimeout(notify,5); },
      async delete(){ delete store[path]; __log.push(['del',path]); setTimeout(notify,5); },
      onSnapshot(next){ const f=()=>next({exists:path in store, data:()=>store[path]}); subs.push(f); setTimeout(f,10); return ()=>{}; } }; }
  };
  const mcp = {
    async callTool(server, tool, input){ __log.push(['mcp',tool]);
      if(tool==='find_securities') return {payload:[{results:[{id:'BADID1', listing_values:['XETR:'+input.query]},{id:input.query==='NVDA'?'E09E2B':'384423', listing_values:['XNAS:'+input.query,'ARCX:'+input.query]}]}]};
      if(tool==='bigdata_search') return {payload:{results:[{id:'x1',headline:'Headline about '+input.request.query.text,timestamp:'2026-10-13T08:00:00',source:{name:'MT Newswires'},chunks:[{text:'Body text of the article '.repeat(20)}],url:'https://app.bigdata.com/documents/'+Math.random().toString(36).slice(2)}]}};
      throw {code:'bad_request'}; },
    watchTool(server, tool, input, handler){ __log.push(['watch',input.rp_entity_ids.join(',')]); setTimeout(()=>handler({type:'data', result:{payload:{structured: input.rp_entity_ids.map(id=>({rp_entity_id:id, price:{value: id==='E09E2B'?226.32:715.13, currency: id==='E09E2B'?'USD':null}, change_1d_pct:-1.2}))}}}),30); return ()=>{}; }
  };
  const sample = async (p, o) => { const t = '### สรุปพอร์ตตอนนี้\nพอร์ตรวม **ทดสอบ** ตัวเลข\n- ข้อหนึ่ง\n- ข้อสอง'; o?.onText?.({text:t, delta:t}); return {text:t, truncated:false}; };
  window.claude = { use: async name => ({db, mcp, sample})[name] ?? null };
})();
