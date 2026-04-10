import json

manual_cards = [
    {"img": "product_126.jpeg", "title": "Demon Slayer-A Sitting Miniature Set", "price": "₹ 250.00"},
    {"img": "product_127.jpg", "title": "shinchan regular set", "price": "₹ 210.00"},
    {"img": "product_128.jpg", "title": "Shinychan Duck Yellow Face changing", "price": "₹ 180.00"},
    {"img": "product_129.jpg", "title": "6 pc set PVC Kuromi Flower Season", "price": "₹ 449.00"},
    {"img": "product_130.jpg", "title": "10 pc mini on Set", "price": "₹ 349.00"},
    {"img": "product_131.jpg", "title": "Hari Putter Hp set of 8 Pop", "price": "₹ 439.00"},
    {"img": "product_132.jpg", "title": "Pokimon set of 8", "price": "₹ 399.00"},
    {"img": "product_133.jpg", "title": "Kuromi set New B (Set of 8)", "price": "₹ 390.00"},
    {"img": "product_134.jpg", "title": "Kuromi Car figure set", "price": "₹ 589.00"},
    {"img": "product_135.jpg", "title": "6 PC DBZ set Dragon Ballz", "price": "₹ 489.00"},
    {"img": "product_136.jpg", "title": "Mario Set of 18", "price": "₹ 550.00"},
    
    # Newly fixed data bypassing Next.js obfuscation:
    {"img": "https://do9uy4stciz2v.cloudfront.net/-OcFjAgAQ8z8fMu4YETT/products_600/-OdxM7a0jv4IgWrUEo3j.jpg", "title": "BTS Mini Figures (Set of 7)", "price": "₹ 1300.00"},
    {"img": "https://do9uy4stciz2v.cloudfront.net/-OcFjAgAQ8z8fMu4YETT/products_600/-Od8jTtHkgFvJhmhXStC.jpg", "title": "6 Pcs/Set Pokemon Figure", "price": "₹ 750.00"},
    {"img": "https://do9uy4stciz2v.cloudfront.net/-OcFjAgAQ8z8fMu4YETT/products_600/-Od8jTtu_oQ3o3hG7d1d.jpg", "title": "Dragon Ball Z Anime 21 Pcs", "price": "₹ 1100.00"},
    {"img": "https://do9uy4stciz2v.cloudfront.net/-OcFjAgAQ8z8fMu4YETT/products_600/-Od8jTtu_oQ3o3hG7d1e.jpg", "title": "ONE Piece Set of 8 Action Figures", "price": "₹ 850.00"},
    {"img": "https://do9uy4stciz2v.cloudfront.net/-OcFjAgAQ8z8fMu4YETT/products_600/-OdIuXlx2k2Atz0rwHFp.jpg", "title": "Spider Man - Set of 8 Small Figures", "price": "₹ 550.00"},
    {"img": "https://do9uy4stciz2v.cloudfront.net/-OcFjAgAQ8z8fMu4YETT/products_600/-OdIuXlyOQ2m0H_64K0q.jpg", "title": "Naruto Anime 12 Pcs Action Figure", "price": "₹ 1050.00"},
    {"img": "https://do9uy4stciz2v.cloudfront.net/-OcFjAgAQ8z8fMu4YETT/products_600/-Odr872RsHXaqPnXqIp0.jpg", "title": "Dragon Ball Z 12 Pice Set", "price": "₹ 420.00"},
    {"img": "https://do9uy4stciz2v.cloudfront.net/-OcFjAgAQ8z8fMu4YETT/products_600/-OiS94iFkZh7fh13FZH0.jpg", "title": "16 Pcs Minion Set", "price": "₹ 1300.00"},
    {"img": "https://do9uy4stciz2v.cloudfront.net/-OcFjAgAQ8z8fMu4YETT/products_600/-OiIpHtqGH2_PG63DYGq.jpg", "title": "Tom & Jerry Miniature Action Figure-5Cm", "price": "₹ 550.00"},
    {"img": "https://do9uy4stciz2v.cloudfront.net/-OcFjAgAQ8z8fMu4YETT/products_600/-OdIuXlx2k2Atz0rwHFq.jpg", "title": "Avengers 6pcs Miniature Action Figure Set - Marvel", "price": "₹ 620.00"}
]

with open('index.html', 'r', encoding='utf-8') as f:
    original_html = f.read()

start = original_html.find('<div class="grid" id="product-grid">')
script_tag = original_html.find('<script>', start)
keychains_html = original_html[start:script_tag]
last_div = keychains_html.rfind('</div>', 0, keychains_html.rfind('</div>'))
keychain_products = keychains_html[len('<div class="grid" id="product-grid">'):last_div]

import re
def add_button(match):
    return match.group(0) + '\n<button class="add-to-cart-btn" onclick="addToCart(this)">Add to Cart</button>'

keychain_products = re.sub(r'<div class="price">.*?</div>', add_button, keychain_products)

mini_products = ""
for item in manual_cards:
    img_src = item['img'] if item['img'].startswith('http') else "images/" + item['img']
    mini_products += '<div class="card" data-category="mini">\n'
    mini_products += '    <img src="' + img_src + '" alt="' + item['title'] + '" onclick="openLightbox(this.src)">\n'
    mini_products += '    <div class="title">' + item['title'] + '</div>\n'
    mini_products += '    <div class="price">' + item['price'] + '</div>\n'
    mini_products += '    <button class="add-to-cart-btn" onclick="addToCart(this)">Add to Cart</button>\n'
    mini_products += '</div>\n'

NEW_INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anime Bazaar Collections</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --bg-color: #f7f9fa;
            --text-color: #222;
            --card-bg: #ffffff;
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        body { 
            font-family: 'Inter', sans-serif; 
            background: var(--bg-color); 
            color: var(--text-color);
            margin: 0; 
            padding: 0; 
            padding-top: 80px;
        }

        nav {
            position: fixed;
            top: 0; width: 100%;
            display: flex; justify-content: space-between; align-items: center;
            padding: 15px 40px; background: var(--card-bg);
            box-shadow: 0 2px 10px rgba(0,0,0,0.05); z-index: 1000; box-sizing: border-box;
        }
        .nav-links { display: flex; gap: 20px; }
        .nav-links button {
            background: none; border: none; font-size: 16px; font-weight: 600; cursor: pointer;
            padding: 10px 15px; border-radius: 6px; transition: 0.2s; color: #555;
        }
        .nav-links button.active { background: var(--primary); color: white; }
        
        .cart-btn {
            position: relative; background: #111; color: white; border: none; padding: 10px 20px;
            border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: 600;
            display: flex; align-items: center; gap: 8px;
        }
        .cart-count { background: #ef4444; color: white; padding: 2px 8px; border-radius: 50%; font-size: 12px; font-weight: bold; }

        .container { max-width: 1300px; margin: 0 auto; padding: 20px; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 25px; display: none; }
        .grid.active { display: grid; }

        .card { 
            background: var(--card-bg); padding: 15px; border-radius: 12px; 
            box-shadow: var(--shadow); text-align: center; transition: transform 0.2s ease, box-shadow 0.2s ease;
            display: flex; flex-direction: column;
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }
        .card img { width: 100%; height: 220px; border-radius: 8px; object-fit: cover; cursor: zoom-in; }
        .title { font-size: 15px; margin: 12px 0 6px; font-weight: 600; line-height: 1.4; flex-grow: 1; }
        .price { font-weight: bold; color: var(--primary); font-size: 17px; margin-bottom: 15px; }
        
        .add-to-cart-btn {
            width: 100%; padding: 10px; background: #f1f5f9; color: #334155; border: none; border-radius: 6px;
            font-weight: 600; cursor: pointer; transition: 0.2s;
        }
        .add-to-cart-btn:hover { background: var(--primary); color: white; }

        #lightbox {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8); backdrop-filter: blur(5px);
            display: none; justify-content: center; align-items: center; z-index: 2000;
        }
        #lightbox img { max-width: 90%; max-height: 90%; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        #lightbox .close-btn { position: absolute; top: 20px; right: 30px; color: white; font-size: 40px; cursor: pointer; }

        #cart-sidebar {
            position: fixed; top: 0; right: -400px; width: 350px; height: 100%;
            background: white; box-shadow: -5px 0 25px rgba(0,0,0,0.15); transition: right 0.3s ease;
            z-index: 1500; display: flex; flex-direction: column;
        }
        #cart-sidebar.open { right: 0; }
        .cart-header { padding: 20px; background: #f8fafc; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; }
        .cart-header h3 { margin: 0; font-size: 18px; }
        .close-cart { background: none; border: none; font-size: 20px; cursor: pointer; }
        
        .cart-items { flex-grow: 1; overflow-y: auto; padding: 20px; }
        .cart-item { display: flex; align-items: center; gap: 15px; margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #e2e8f0; }
        .cart-item img { width: 60px; height: 60px; object-fit: cover; border-radius: 6px; }
        .cart-item-info { flex-grow: 1; }
        .cart-item-title { font-size: 13px; font-weight: 600; margin-bottom: 5px; }
        .cart-item-price { font-size: 14px; color: var(--primary); font-weight: bold; }
        .remove-item { background: none; border: none; color: #ef4444; cursor: pointer; }
        
        .cart-footer { padding: 20px; border-top: 1px solid #e2e8f0; background: #f8fafc; }
        .cart-total { display: flex; justify-content: space-between; font-size: 18px; font-weight: bold; margin-bottom: 15px; }
        .export-pdf-btn {
            width: 100%; padding: 14px; background: #10b981; color: white; border: none; border-radius: 8px;
            font-size: 16px; font-weight: bold; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 10px;
        }
        .export-pdf-btn:hover { background: #059669; }
        
        .pagination { margin: 40px 0; text-align: center; }
        .pagination button { padding: 10px 20px; margin: 0 5px; cursor: pointer; border: none; background: var(--primary); color: white; border-radius: 6px; font-size: 15px; }
        .pagination button:disabled { background: #ccc; cursor: not-allowed; }
        #page-info { font-size: 16px; margin: 0 15px; font-weight: bold; }
    </style>
</head>
<body>

    <nav>
        <div class="nav-links">
            <button id="tab-keychains" class="active" onclick="switchTab('keychains')">Keychains</button>
            <button id="tab-minifigures" onclick="switchTab('minifigures')">Mini Figures</button>
        </div>
        <button class="cart-btn" onclick="toggleCart()">
            <i class="fa-solid fa-cart-shopping"></i> Cart 
            <span class="cart-count" id="cartCount">0</span>
        </button>
    </nav>

    <div id="lightbox" onclick="closeLightbox()">
        <span class="close-btn">&times;</span>
        <img id="lightbox-img" src="" alt="Zoomed">
    </div>

    <div class="container">
        <div id="section-keychains" class="grid active">
            ###KEYCHAINS###
        </div>
        
        <div id="pagination-controls" class="pagination">
            <button id="prev-btn" onclick="changePage(-1)">Previous</button>
            <span id="page-info">Page 1</span>
            <button id="next-btn" onclick="changePage(1)">Next</button>
        </div>

        <div id="section-minifigures" class="grid">
            ###MINIFIGURES###
        </div>
    </div>

    <div id="cart-sidebar">
        <div class="cart-header">
            <h3>Your Cart</h3>
            <button class="close-cart" onclick="toggleCart()"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="cart-items" id="cart-items-container"></div>
        <div class="cart-footer">
            <div class="cart-total">
                <span>Total:</span>
                <span id="cart-total-price">₹ 0.00</span>
            </div>
            <button class="export-pdf-btn" onclick="exportCartPDF()">
                <i class="fa-brands fa-whatsapp"></i> Export Invoice (PDF)
            </button>
        </div>
    </div>

    <script>
        function switchTab(tab) {
            document.getElementById('section-keychains').classList.remove('active');
            document.getElementById('section-minifigures').classList.remove('active');
            document.getElementById('tab-keychains').classList.remove('active');
            document.getElementById('tab-minifigures').classList.remove('active');
            
            document.getElementById('section-' + tab).classList.add('active');
            document.getElementById('tab-' + tab).classList.add('active');
            
            if(tab === 'minifigures') {
                document.getElementById('pagination-controls').style.display = 'none';
            } else {
                document.getElementById('pagination-controls').style.display = 'block';
            }
        }

        const keychainCards = Array.from(document.querySelectorAll('#section-keychains .card'));
        const itemsPerPage = 30;
        let currentPage = 1;
        const totalPages = Math.ceil(keychainCards.length / itemsPerPage) || 1;

        function showPage(page) {
            if (page < 1) page = 1;
            if (page > totalPages) page = totalPages;
            currentPage = page;

            keychainCards.forEach((card, index) => {
                if (index >= (page - 1) * itemsPerPage && index < page * itemsPerPage) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
            document.getElementById('page-info').innerText = `Page ${currentPage} of ${totalPages}`;
            document.getElementById('prev-btn').disabled = currentPage === 1;
            document.getElementById('next-btn').disabled = currentPage === totalPages;
            window.scrollTo({top: 0, behavior: 'smooth'});
        }

        function changePage(direction) { showPage(currentPage + direction); }
        
        document.querySelectorAll('.card img').forEach(img => {
            img.onclick = () => openLightbox(img.src);
        });

        showPage(1);

        function openLightbox(src) {
            document.getElementById('lightbox-img').src = src;
            document.getElementById('lightbox').style.display = 'flex';
        }
        function closeLightbox() {
            document.getElementById('lightbox').style.display = 'none';
        }

        let cart = [];
        function toggleCart() { document.getElementById('cart-sidebar').classList.toggle('open'); }

        function addToCart(btn) {
            const card = btn.closest('.card');
            const title = card.querySelector('.title').innerText;
            const priceText = card.querySelector('.price').innerText;
            const img = card.querySelector('img').src;
            const priceVal = parseFloat(priceText.replace(/[^0-9.]/g, '')) || 0;
            
            const existing = cart.find(item => item.title === title);
            if(existing) { existing.qty++; } else { cart.push({ title, price: priceVal, img, qty: 1 }); }
            updateCartUI();
            
            btn.innerText = "Added ✓";
            btn.style.background = "#10b981"; btn.style.color = "white";
            setTimeout(() => {
                btn.innerText = "Add to Cart";
                btn.style.background = "#f1f5f9"; btn.style.color = "#334155";
            }, 1000);
        }

        function removeFromCart(title) {
            cart = cart.filter(item => item.title !== title);
            updateCartUI();
        }

        function updateCartUI() {
            const container = document.getElementById('cart-items-container');
            container.innerHTML = '';
            let total = 0; let totalQty = 0;
            
            cart.forEach(item => {
                total += item.price * item.qty;
                totalQty += item.qty;
                container.innerHTML += `
                    <div class="cart-item">
                        <img src="${item.img}" alt="img">
                        <div class="cart-item-info">
                            <div class="cart-item-title">${item.title} (x${item.qty})</div>
                            <div class="cart-item-price">₹ ${(item.price * item.qty).toFixed(2)}</div>
                        </div>
                        <button class="remove-item" onclick="removeFromCart('${item.title.replace(/'/g, "\\'")}')"><i class="fa-solid fa-trash"></i></button>
                    </div>
                `;
            });
            document.getElementById('cartCount').innerText = totalQty;
            document.getElementById('cart-total-price').innerText = `₹ ${total.toFixed(2)}`;
        }

        function exportCartPDF() {
            if(cart.length === 0) { alert('Your cart is empty!'); return; }
            
            const invoice = document.createElement('div');
            invoice.style.padding = '40px'; invoice.style.background = 'white'; invoice.style.width = '800px'; invoice.style.color = 'black';
            
            let html = `
                <h1 style="text-align:center; color:#6366f1; margin-bottom: 5px;">Anime Bazaar Invoice</h1>
                <p style="text-align:center; color:#666; margin-bottom: 40px;">Send this PDF via WhatsApp to place your order</p>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                    <tr style="background:#f1f5f9; text-align:left;">
                        <th style="padding:15px; border-bottom: 2px solid #cbd5e1;">Image</th>
                        <th style="padding:15px; border-bottom: 2px solid #cbd5e1;">Product</th>
                        <th style="padding:15px; border-bottom: 2px solid #cbd5e1;">Qty</th>
                        <th style="padding:15px; border-bottom: 2px solid #cbd5e1;">Price</th>
                    </tr>
            `;
            let total = 0;
            cart.forEach(item => {
                total += item.price * item.qty;
                html += `
                    <tr>
                        <td style="padding:15px; border-bottom: 1px solid #e2e8f0;">
                            <img src="${item.img}" style="width: 60px; height: 60px; border-radius: 6px; object-fit: cover;">
                        </td>
                        <td style="padding:15px; border-bottom: 1px solid #e2e8f0; font-weight: 600;">${item.title}</td>
                        <td style="padding:15px; border-bottom: 1px solid #e2e8f0;">${item.qty}</td>
                        <td style="padding:15px; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #6366f1;">₹ ${(item.price * item.qty).toFixed(2)}</td>
                    </tr>
                `;
            });
            html += `</table><h2 style="text-align: right; margin-top:30px;">Total: ₹ ${total.toFixed(2)}</h2>`;
            invoice.innerHTML = html;
            
            var opt = {
              margin:       [0.5, 0.5, 0.5, 0.5],
              filename:     'AnimeBazaar_Order.pdf',
              image:        { type: 'jpeg', quality: 0.98 },
              html2canvas:  { scale: 2, useCORS: true },
              jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
            };
            html2pdf().set(opt).from(invoice).save();
        }
    </script>
</body>
</html>"""

NEW_INDEX = NEW_INDEX.replace('###KEYCHAINS###', keychain_products)
NEW_INDEX = NEW_INDEX.replace('###MINIFIGURES###', mini_products)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(NEW_INDEX)

print("Regeneration complete!")
