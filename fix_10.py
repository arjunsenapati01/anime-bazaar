import os
import re
import json
import urllib.request

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

HEADERS = {'User-Agent': 'Mozilla/5.0'}

results = []
count = 137

for url in NEW_URLS:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        res = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        
        m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', res, flags=re.DOTALL)
        if m:
            data = json.loads(m.group(1))
            prod_id = url.split('/')[-1].split('?')[0]
            
            # recursive search for the product obj
            def find_p(d):
                if isinstance(d, dict):
                    if d.get('id') == prod_id: return d
                    for k, v in d.items():
                        res = find_p(v)
                        if res: return res
                elif isinstance(d, list):
                    for v in d:
                        res = find_p(v)
                        if res: return res
                return None
                
            p = find_p(data)
            if p:
                title = p.get('name', 'Action Figure').split('|')[0].strip().replace('Buy ', '').split(' online')[0].strip()
                price = p.get('sellingPrice', 'N/A')
                img_url = p.get('media', [{}])[0].get('url', '')
                
                # Check for logo issue, the logo was "OcFjAgAQ8z8fMu4YETU.jpg"
                if "OcFjAgAQ8z8fMu4YETU" in img_url and len(p.get('media', [])) > 1:
                    img_url = p.get('media', [{}])[1].get('url', '')
                    
                if img_url:
                    if not img_url.startswith('http'): img_url = 'https:' + img_url
                    ext = img_url.split('.')[-1].split('?')[0]
                    if ext.lower() not in ['jpg', 'jpeg', 'png', 'webp']: ext = 'jpg'
                    filename = f"product_{count}.{ext}"
                    filepath = f"images/{filename}"
                    
                    try:
                        img_data = urllib.request.urlopen(urllib.request.Request(img_url, headers=HEADERS)).read()
                        with open(filepath, 'wb') as f:
                            f.write(img_data)
                    except Exception as e:
                        filename = "default.jpg"
                else:
                    filename = "default.jpg"
                    
                results.append((filename, title, f"₹ {price}.00"))
                print(f"Got ok: {title} | {price}")
                count += 1
            else:
                print("Prod not in JSON", url)
        else:
            print("No next data", url)
    except Exception as e:
        print("Error fetching", url, e)

# Inject into index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

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

# Wipe the old Mini Figures and rebuild
start_idx = html.find('<div style="margin-top: 50px;')
if start_idx != -1:
    end_script_idx = html.find('<script>', start_idx)
    html = html[:start_idx] + html[end_script_idx:]
    
mini_html = '''
<div style="margin-top: 50px; text-align: center;">
    <h2>Mini Figures</h2>
    <div class="grid" id="minifigure-grid">'''

for img, title, price in manual_cards + results:
    mini_html += f'''
        <div class="card" style="display: block;">
            <img src="images/{img}" alt="{title}">
            <div class="title">{title}</div>
            <div class="price">{price}</div>
        </div>'''
        
mini_html += '''
    </div>
</div>
'''

target_pos = html.rfind('<script>')
if target_pos != -1:
    new_html = html[:target_pos] + mini_html + html[target_pos:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Fixed accurately!")
else:
    print("Failed finding script")
