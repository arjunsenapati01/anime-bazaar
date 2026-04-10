// api/orders.js — Vercel Serverless Function
// Storage: GitHub Gist (production DB) | orders.json file (local dev)

module.exports = async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  try {
    const isCloud = !!process.env.GITHUB_TOKEN && !!process.env.GITHUB_GIST_ID;
    const GIST_URL = isCloud ? `https://api.github.com/gists/${process.env.GITHUB_GIST_ID}` : null;
    const authHeaders = isCloud ? {
      'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'X-GitHub-Api-Version': '2022-11-28'
    } : {};

    async function getAll() {
      if (isCloud) {
        const r = await fetch(GIST_URL, { headers: authHeaders, cache: 'no-store' });
        if (!r.ok) return [];
        const data = await r.json();
        const content = data.files['orders.json']?.content;
        return content ? JSON.parse(content) : [];
      } else {
        const fs = require('fs'), path = require('path');
        const f = path.join(process.cwd(), 'data', 'orders.json');
        if (!require('fs').existsSync(f)) return [];
        return JSON.parse(require('fs').readFileSync(f, 'utf8'));
      }
    }

    async function saveAll(orders) {
      if (isCloud) {
        const r = await fetch(GIST_URL, {
          method: 'PATCH',
          headers: { ...authHeaders, 'Content-Type': 'application/json' },
          body: JSON.stringify({
            files: { 'orders.json': { content: JSON.stringify(orders, null, 2) } }
          })
        });
        if (!r.ok) console.error('Gist update failed:', await r.text());
        return;
      } else {
        const fs = require('fs'), path = require('path');
        const dir = path.join(process.cwd(), 'data');
        fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(path.join(dir, 'orders.json'), JSON.stringify(orders, null, 2));
      }
    }

    // GET all orders
    if (req.method === 'GET') {
      return res.json(await getAll());
    }

    // POST — save new order
    if (req.method === 'POST') {
      const orders = await getAll();
      orders.unshift(req.body);
      await saveAll(orders);
      return res.json({ success: true, id: req.body.id });
    }

    // PATCH — update order status  (body: { id, status })
    if (req.method === 'PATCH') {
      const orders = await getAll();
      const o = orders.find(x => x.id === req.body.id);
      if (o) { o.status = req.body.status; await saveAll(orders); }
      return res.json({ success: true });
    }

    // DELETE — ?id=ORD-xxx  or  ?id=all
    if (req.method === 'DELETE') {
      const id = req.query.id || (req.url.split('/').pop());
      if (id === 'all') {
        await saveAll([]);
      } else {
        await saveAll((await getAll()).filter(o => o.id !== id));
      }
      return res.json({ success: true });
    }

    res.status(405).json({ error: 'Method Not Allowed' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
};
