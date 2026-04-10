import os
import requests
import re
import urllib.request

HEADERS = {'User-Agent': 'Mozilla/5.0'}

NEW_URLS = [
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OdxM7_wTnXOE2wcn89K',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-Od8jTru_86XvKQyeYqp',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-Od8jTru_86XvKQyeYqt',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-Od8jTrs5RkmoRxqHwWy',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OdIuXlXwnamP-O7uGeZ',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OdIuXlWPVD7ujiQZXWF',
    'https://www.giftzystore.in/s/gallery/gala-collection/dragon-ball-z-collection/dol/product/-Odr872PzczT_RYv2ZSn',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OeWe5IemREIUqRgPDVV',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OfUc5I-ox79mhr_u93j',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OdIuXlYUj9Q4eqc1TIg'
]

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# First, strip out the existing "Mini Figures" section completely to rewrite it fresh without duplicates
start_idx = html.find('<div style="margin-top: 50px;')
if start_idx != -1:
    end_script_idx = html.find('<script>', start_idx)
    if end_script_idx != -1:
        html = html[:start_idx] + html[end_script_idx:]

# Ensure pagination script uses correct selector
html = html.replace("document.querySelectorAll('.card');", "document.querySelectorAll('#product-grid .card');")

manual_cards = [
    ("product_126.jpeg", "Demon Slayer-A Sitting Miniature Set of 5pcs With Base", "₹ 250.00"),
    ("product_127.jpg", "shinchan regular set", "₹ 210.00"),
    ("product_128.jpg", "3 pcs - Shinychan Duck Yellow Face changing keychain", "₹ 180.00"),
    ("product_129.jpg", "6 pc set PVC Kuromi Flower Season action figures", "₹ 449.00"),
    ("product_130.jpg", "10 pc mini on Set", "₹ 349.00"),
    ("product_131.jpg", "Hari Putter Hp set of 8 Pop", "₹ 439.00"),
    ("product_132.jpg", "Pokimon set of 8", "₹ 399.00"),
    ("product_133.jpg", "Kuromi set New B (Set of 8)", "₹ 390.00"),
    ("product_134.jpg", "Kuromi Car figure set", "₹ 589.00"),
    ("product_135.jpg", "6 PC DBZ set Dragon Ballz", "₹ 489.00"),
    ("product_136.jpg", "Mario Set of 18", "₹ 550.00"),
]

mini_html = '''
<div style="margin-top: 50px; text-align: center;">
    <h2>Mini Figures</h2>
    <div class="grid" id="minifigure-grid">'''

for img, title, price in manual_cards:
    if os.path.exists(f'images/{img}'):
        mini_html += f'''
        <div class="card" style="display: block;">
            <img src="images/{img}" alt="{title}">
            <div class="title">{title}</div>
            <div class="price">{price}</div>
        </div>'''
        
count = 137

for url in NEW_URLS:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        res = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        
        title_match = re.search(r'<title>(.*?)</title>', res, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).split('|')[0].strip().replace('Buy ', '').split(' online')[0].strip()
        else:
            title = 'Action Figure'
            
        img_match = re.search(r'<meta\s+property=[\'"]?og:image[\'"]?\s+content=[\'"]?([^ \'">]+)', res, re.IGNORECASE)
        img_url = img_match.group(1) if img_match else ''
        
        # Scrape price
        p = re.search(r'\"sellingPrice\":(\d+)', res)
        # fallback to any 'price",' or similar if not found, since giftzy uses Next.js payload where sellingPrice could be absent
        if not p: p = re.search(r'\"price\":(\d+)', res)
        price = f"₹ {p.group(1)}.00" if p else "N/A"
        
        filename = "default.jpg"
        if img_url:
            if not img_url.startswith('http'): img_url = 'https:' + img_url
            ext = img_url.split('.')[-1].split('?')[0]
            if len(ext) > 4 or ext.lower() not in ['jpg', 'jpeg', 'png', 'webp']: ext = 'jpg'
            filename = f"product_{count}.{ext}"
            
            if not os.path.exists(f'images/{filename}'):
                try:
                    img_data = requests.get(img_url, headers=HEADERS, timeout=10).content
                    with open(f'images/{filename}', 'wb') as f: f.write(img_data)
                except Exception as e:
                    print(f"Img Error {img_url}: {e}")
                    filename = "default.jpg"
        
        mini_html += f'''
        <div class="card" style="display: block;">
            <img src="images/{filename}" alt="{title}">
            <div class="title">{title}</div>
            <div class="price">{price}</div>
        </div>'''
        count += 1
        print(f"Successfully added {title} | {price}")
    except Exception as e:
        print(f"Error on {url}: {e}")

mini_html += '''
    </div>
</div>
'''

target_pos = html.rfind('<script>')
if target_pos != -1:
    new_html = html[:target_pos] + mini_html + html[target_pos:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Injected successfully.")
else:
    print("Could not find script tag inside index.html")
