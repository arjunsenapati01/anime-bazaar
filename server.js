const express = require('express');
const cors    = require('cors');
const fs      = require('fs');
const path    = require('path');

const app  = express();
const PORT = process.env.PORT || 3000;
const DATA = path.join(__dirname, 'data', 'orders.json');

// ── Middleware ────────────────────────────────────────────────────────────────
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Serve ALL static files (index.html, admin.html, images/) with CORS headers
app.use((req, res, next) => {
  res.setHeader('Cross-Origin-Resource-Policy', 'cross-origin');
  res.setHeader('Access-Control-Allow-Origin', '*');
  next();
});
app.use(express.static(__dirname, {
  index: 'index.html',
  setHeaders: (res) => {
    res.setHeader('Cross-Origin-Resource-Policy', 'cross-origin');
  }
}));

// ── Helpers ───────────────────────────────────────────────────────────────────
function readOrders() {
  try {
    if (!fs.existsSync(DATA)) return [];
    return JSON.parse(fs.readFileSync(DATA, 'utf8'));
  } catch { return []; }
}

function writeOrders(orders) {
  fs.mkdirSync(path.dirname(DATA), { recursive: true });
  fs.writeFileSync(DATA, JSON.stringify(orders, null, 2));
}

// ── API Routes ────────────────────────────────────────────────────────────────

// GET all orders
app.get('/api/orders', (req, res) => {
  res.json(readOrders());
});

// POST new order
app.post('/api/orders', (req, res) => {
  const orders = readOrders();
  orders.unshift(req.body);
  writeOrders(orders);
  res.json({ success: true, id: req.body.id });
});

// PATCH — update order status
app.patch('/api/orders/:id', (req, res) => {
  const orders = readOrders();
  const o = orders.find(x => x.id === req.params.id);
  if (o) { o.status = req.body.status; writeOrders(orders); }
  res.json({ success: true });
});

// DELETE one order
app.delete('/api/orders/:id', (req, res) => {
  if (req.params.id === 'all') {
    writeOrders([]);
  } else {
    writeOrders(readOrders().filter(o => o.id !== req.params.id));
  }
  res.json({ success: true });
});

// ── Start ─────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`✅ Wholesale Action Nook running → http://localhost:${PORT}`);
  console.log(`🔐 Admin panel        → http://localhost:${PORT}/admin.html`);
});
