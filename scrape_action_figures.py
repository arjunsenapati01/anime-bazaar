import requests
from bs4 import BeautifulSoup
import os
import re
import time

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
BASE_URL = 'https://thegiftwholesalers.com/collections/action-figures-wholesaler?page={}'
PRODUCT_BASE = 'https://thegiftwholesalers.com'

os.makedirs('images', exist_ok=True)

# Count existing product images to avoid numbering conflicts
existing = [f for f in os.listdir('images') if f.startswith('product_') and '.' in f]
nums = []
for f in existing:
    try:
        n = int(f.replace('product_', '').split('.')[0])
        nums.append(n)
    except:
        pass
count = max(nums) + 1 if nums else 200
print(f"Starting image counter at: {count}")

products = []

for page in range(1, 13):
    print(f"\n--- Scraping page {page}/12 ---")
    url = BASE_URL.format(page)
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Shopify collection pages use li.grid__item or article
        items = soup.select('li.grid__item')
        if not items:
            items = soup.select('.product-item, .card-wrapper')
        
        print(f"  Found {len(items)} product items")
        
        for item in items:
            try:
                # Title
                title_el = item.select_one('.card__heading a, h3 a, .product-item__title, .full-unstyled-link')
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                if not title:
                    continue

                # Price - get sale price  
                price_el = item.select_one('.price-item--sale, .price-item--regular, .price__regular .price-item')
                if not price_el:
                    price_el = item.select_one('.price-item')
                price = price_el.get_text(strip=True) if price_el else 'N/A'
                # Clean price
                price = re.sub(r'\s+', ' ', price).strip()
                if 'Rs.' in price:
                    price = '₹ ' + price.split('Rs.')[-1].strip()

                # Image
                img_el = item.select_one('img')
                img_url = ''
                if img_el:
                    img_url = img_el.get('src', '') or img_el.get('data-src', '')
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    # Shopify images: get better quality
                    img_url = re.sub(r'_\d+x\d*\.', '_600x.', img_url)
                    img_url = re.sub(r'\?.*$', '', img_url)  # remove query params
                    if not img_url.startswith('http'):
                        img_url = ''

                # Download image
                filename = 'default.jpg'
                if img_url:
                    ext = img_url.split('.')[-1].lower()
                    if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                        ext = 'jpg'
                    filename = f'product_{count}.{ext}'
                    filepath = f'images/{filename}'
                    if not os.path.exists(filepath):
                        try:
                            img_data = requests.get(img_url, headers=HEADERS, timeout=10).content
                            if len(img_data) > 1000:  # valid image
                                with open(filepath, 'wb') as f:
                                    f.write(img_data)
                            else:
                                filename = 'default.jpg'
                        except:
                            filename = 'default.jpg'
                    count += 1

                products.append({'title': title, 'price': price, 'img': filename})
                print(f"  ✓ {title[:50]} | {price}")

            except Exception as e:
                print(f"  Item error: {e}")
                continue
        
        time.sleep(0.5)  # polite delay

    except Exception as e:
        print(f"Page {page} error: {e}")

print(f"\n\nTotal products scraped: {len(products)}")

# Now inject into index.html as new 'Action Figures' section
cards_html = ''
for p in products:
    img_src = f"images/{p['img']}"
    safe_title = p['title'].replace('"', '&quot;').replace("'", "&#x27;")
    cards_html += f'''            <div class="card" data-category="figures">
    <img src="{img_src}" alt="{safe_title}" onclick="openLightbox(this.src)">
    <div class="title">{p['title']}</div>
    <div class="price">{p['price']}</div>
    <button class="add-to-cart-btn" onclick="addToCart(this)">Add to Cart</button>
</div>
'''

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add 'Action Figures' nav tab button
html = html.replace(
    '<button id="tab-minifigures" onclick="switchTab(\'minifigures\')">Mini Figures</button>',
    '<button id="tab-minifigures" onclick="switchTab(\'minifigures\')">Mini Figures</button>\n            <button id="tab-actionfigures" onclick="switchTab(\'actionfigures\')">Action Figures</button>'
)

# 2. Add section div before cart sidebar
new_section = f'''        <div id="section-actionfigures" class="grid">
{cards_html}        </div>

'''
html = html.replace('    <div id="cart-sidebar">', new_section + '    <div id="cart-sidebar">')

# 3. Update switchTab JS to handle new tab
old_switchtab = """        function switchTab(tab) {
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
        }"""

new_switchtab = """        function switchTab(tab) {
            ['keychains', 'minifigures', 'actionfigures'].forEach(t => {
                const sec = document.getElementById('section-' + t);
                const btn = document.getElementById('tab-' + t);
                if(sec) sec.classList.remove('active');
                if(btn) btn.classList.remove('active');
            });
            document.getElementById('section-' + tab).classList.add('active');
            document.getElementById('tab-' + tab).classList.add('active');
            
            if(tab === 'keychains') {
                document.getElementById('pagination-controls').style.display = 'block';
            } else {
                document.getElementById('pagination-controls').style.display = 'none';
            }
        }"""

html = html.replace(old_switchtab, new_switchtab)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Done! Injected {len(products)} Action Figures into index.html as a new tab.")
