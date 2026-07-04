// Cloudflare Worker — Multi-user sync backend for 香港釣魚資訊站
// Each user gets a unique 6-char sync code
// Records stored in KV: key = sync code, value = JSON array of catches
// Max: 500 records per user, 2KB per photo (Base64 thumbnail), videos as URL only

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const headers = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Content-Type": "application/json"
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers });
    }

    try {
      // POST /sync — save records for a sync code
      if (request.method === "POST" && url.pathname === "/sync") {
        const body = await request.json();
        const syncCode = (body.code || "master").slice(0, 20); // sanitize
        const records = body.records;

        if (!Array.isArray(records)) {
          return new Response(JSON.stringify({ error: "records must be array" }), 
            { status: 400, headers });
        }

        // Limit to 500 records per user
        const trimmed = records.slice(-500);

        // Strip large base64 photos (>3KB) to prevent KV bloat
        const cleaned = trimmed.map(r => {
          const c = { ...r };
          if (c.photo && c.photo.length > 3000) {
            c.photoPreview = c.photo.slice(0, 100) + "..."; // keep thumbnail reference
            delete c.photo;
          }
          if (c.video && c.video.length > 1000) {
            delete c.video; // videos too large for KV
          }
          return c;
        });

        await env.RECORDS_KV.put(syncCode, JSON.stringify(cleaned));

        return new Response(JSON.stringify({ 
          ok: true, 
          count: cleaned.length,
          code: syncCode
        }), { headers });
      }

      // GET /sync?code=xxx — load records
      if (request.method === "GET" && url.pathname === "/sync") {
        const code = (url.searchParams.get("code") || "master").slice(0, 20);
        const raw = await env.RECORDS_KV.get(code);
        const records = raw ? JSON.parse(raw) : [];
        return new Response(JSON.stringify({ 
          ok: true, 
          records: records,
          code: code
        }), { headers });
      }

      // POST /code — generate new unique sync code
      if (request.method === "POST" && url.pathname === "/code") {
        const code = generateCode();
        // Check not already in use
        const exists = await env.RECORDS_KV.get(code);
        if (exists) {
          // Try again (very unlikely collision)
          const code2 = generateCode();
          return new Response(JSON.stringify({ code: code2 }), { headers });
        }
        // Pre-create with empty array
        await env.RECORDS_KV.put(code, "[]");
        return new Response(JSON.stringify({ code: code }), { headers });
      }

      // Health check
      return new Response(JSON.stringify({ 
        status: "ok",
        name: "fishing-hk-sync",
        version: "2.0"
      }), { headers });

    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), 
        { status: 500, headers });
    }
  }
};

// Generate a friendly 6-char sync code
function generateCode() {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"; // no I,O,0,1 for readability
  let code = "";
  for (let i = 0; i < 6; i++) {
    code += chars[Math.floor(Math.random() * chars.length)];
  }
  return code;
}
