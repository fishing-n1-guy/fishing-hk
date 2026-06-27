// Cloudflare Worker — 釣魚紀錄 Sync API
// 部署方法：
// 1. 去 https://dash.cloudflare.com/ 登入
// 2. Workers & Pages → Create Application → Create Worker
// 3. 俾個名 (e.g. fishing-sync)
// 4. Delete default code，貼上以下 code
// 5. 去 Settings → Variables → KV Namespace Binding
//    - 開個 KV namespace (e.g. FISHING_SYNC)
//    - Variable name: RECORDS_KV
// 6. Deploy

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    const path = url.pathname;
    const method = request.method;

    try {
      // POST /sync — save records
      if (method === 'POST' && path === '/sync') {
        const body = await request.json();
        const syncCode = body.syncCode;
        const catches = body.catches;
        
        if (!syncCode || !catches) {
          return new Response(JSON.stringify({ error: 'Missing syncCode or catches' }), {
            status: 400, headers: { 'Content-Type': 'application/json', ...corsHeaders }
          });
        }

        // Validate catches is array
        if (!Array.isArray(catches)) {
          return new Response(JSON.stringify({ error: 'catches must be an array' }), {
            status: 400, headers: { 'Content-Type': 'application/json', ...corsHeaders }
          });
        }

        // Save to KV
        await env.RECORDS_KV.put(syncCode, JSON.stringify(catches));
        
        return new Response(JSON.stringify({ success: true, count: catches.length }), {
          headers: { 'Content-Type': 'application/json', ...corsHeaders }
        });
      }

      // GET /sync?code=xxx — get records
      if (method === 'GET' && path === '/sync') {
        const syncCode = url.searchParams.get('code');
        if (!syncCode) {
          return new Response(JSON.stringify({ error: 'Missing code parameter' }), {
            status: 400, headers: { 'Content-Type': 'application/json', ...corsHeaders }
          });
        }

        const data = await env.RECORDS_KV.get(syncCode);
        const catches = data ? JSON.parse(data) : [];
        
        return new Response(JSON.stringify({ catches: catches }), {
          headers: { 'Content-Type': 'application/json', ...corsHeaders }
        });
      }

      // DELETE /sync?code=xxx — delete records
      if (method === 'DELETE' && path === '/sync') {
        const syncCode = url.searchParams.get('code');
        if (!syncCode) {
          return new Response(JSON.stringify({ error: 'Missing code parameter' }), {
            status: 400, headers: { 'Content-Type': 'application/json', ...corsHeaders }
          });
        }

        await env.RECORDS_KV.delete(syncCode);
        return new Response(JSON.stringify({ success: true }), {
          headers: { 'Content-Type': 'application/json', ...corsHeaders }
        });
      }

      // Health check
      if (path === '/') {
        return new Response(JSON.stringify({ status: 'ok', version: '1.0' }), {
          headers: { 'Content-Type': 'application/json', ...corsHeaders }
        });
      }

      return new Response('Not Found', { status: 404, headers: corsHeaders });

    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), {
        status: 500, headers: { 'Content-Type': 'application/json', ...corsHeaders }
      });
    }
  }
};
