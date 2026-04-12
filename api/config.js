// api/config.js — store site-wide config (margin %, etc.) in Vercel Blob
const BLOB_KEY = 'wan-config';

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const blobToken = process.env.BLOB_READ_WRITE_TOKEN;
  const isCloud = !!blobToken;

  async function getConfig() {
    if (isCloud) {
      const r = await fetch(
        `https://blob.vercel-storage.com?prefix=${BLOB_KEY}&limit=5`,
        { headers: { authorization: `Bearer ${blobToken}` } }
      );
      if (!r.ok) return { margin: 0 };
      const { blobs } = await r.json();
      if (!blobs || blobs.length === 0) return { margin: 0 };
      blobs.sort((a, b) => new Date(b.uploadedAt) - new Date(a.uploadedAt));
      const data = await fetch(blobs[0].url, { cache: 'no-store' });
      if (!data.ok) return { margin: 0 };
      return await data.json();
    } else {
      const fs = require('fs'), path = require('path');
      const f = path.join(process.cwd(), 'data', 'config.json');
      if (!fs.existsSync(f)) return { margin: 0 };
      return JSON.parse(fs.readFileSync(f, 'utf8'));
    }
  }

  async function saveConfig(cfg) {
    if (isCloud) {
      // Delete old blobs
      const r = await fetch(
        `https://blob.vercel-storage.com?prefix=${BLOB_KEY}&limit=5`,
        { headers: { authorization: `Bearer ${blobToken}` } }
      );
      if (r.ok) {
        const { blobs } = await r.json();
        if (blobs && blobs.length > 0) {
          await fetch('https://blob.vercel-storage.com', {
            method: 'DELETE',
            headers: { authorization: `Bearer ${blobToken}`, 'content-type': 'application/json' },
            body: JSON.stringify({ urls: blobs.map(b => b.url) }),
          });
        }
      }
      await fetch(`https://blob.vercel-storage.com/${BLOB_KEY}.json`, {
        method: 'PUT',
        headers: {
          authorization: `Bearer ${blobToken}`,
          'content-type': 'application/json',
          'x-cache-control-max-age': '0',
        },
        body: JSON.stringify(cfg),
      });
    } else {
      const fs = require('fs'), path = require('path');
      const dir = path.join(process.cwd(), 'data');
      fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(path.join(dir, 'config.json'), JSON.stringify(cfg));
    }
  }

  try {
    if (req.method === 'GET') {
      res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
      return res.json(await getConfig());
    }
    if (req.method === 'POST') {
      const current = await getConfig();
      const updated = { ...current, ...req.body };
      await saveConfig(updated);
      return res.json({ success: true, config: updated });
    }
    res.status(405).json({ error: 'Method Not Allowed' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
};
