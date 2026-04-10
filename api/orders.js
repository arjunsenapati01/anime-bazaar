// api/orders.js — Vercel Serverless Function
// Storage: Vercel KV (production) | orders.json file (local dev via server.js)

module.exports = async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const KEY = 'anime_bazaar_orders';

  try {
    // Use Vercel KV when deployed; fallback to filesystem for local dev
    const useKV = !!process.env.KV_REST_API_URL;
    let kv;
    if (useKV) kv = require('@vercel/kv').kv;

    async function getAll() {
      if (useKV) return (await kv.get(KEY)) || [];
      const fs = require('fs'), path = require('path');
      const f = path.join(process.cwd(), 'data', 'orders.json');
      if (!require('fs').existsSync(f)) return [];
      return JSON.parse(require('fs').readFileSync(f, 'utf8'));
    }

    async function saveAll(orders) {
      if (useKV) { await kv.set(KEY, orders); return; }
      const fs = require('fs'), path = require('path');
      const dir = path.join(process.cwd(), 'data');
      fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(path.join(dir, 'orders.json'), JSON.stringify(orders, null, 2));
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
