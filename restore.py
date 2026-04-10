import os
import requests
from bs4 import BeautifulSoup
import json
import re

HEADERS = {'User-Agent': 'Mozilla/5.0'}

NEW_URLS = [
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OdxM7_wTnXOE2wcn89K?returnUri=https%3A%2F%2Fwww.giftzystore.in%2F%3FsearchTerm%3Dmini%2520figures',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-Od8jTru_86XvKQyeYqp?returnUri=https%3A%2F%2Fwww.giftzystore.in%2F%3FsearchTerm%3Dmini%2520figures',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-Od8jTru_86XvKQyeYqt?returnUri=https%3A%2F%2Fwww.giftzystore.in%2F%3FsearchTerm%3Dmini%2520figures',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-Od8jTrs5RkmoRxqHwWy?returnUri=https%3A%2F%2Fwww.giftzystore.in%2F%3FsearchTerm%3Dmini%2520figures',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OdIuXlXwnamP-O7uGeZ?returnUri=https%3A%2F%2Fwww.giftzystore.in%2F%3FsearchTerm%3Dmini%2520figures',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OdIuXlWPVD7ujiQZXWF?returnUri=https%3A%2F%2Fwww.giftzystore.in%2F%3FsearchTerm%3Dmini%2520figures',
    'https://www.giftzystore.in/s/gallery/gala-collection/dragon-ball-z-collection/dol/product/-Odr872PzczT_RYv2ZSn?returnUri=https%3A%2F%2Fwww.giftzystore.in%2F%3FsearchTerm%3Dmini%2520figures',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OeWe5IemREIUqRgPDVV?returnUri=https%3A%2F%2Fwww.giftzystore.in%2F%3FsearchTerm%3Dmini%2520figures',
    'https://www.giftzystore.in/s/gallery/undefined/undefined/undefined/product/-OeW4eTBiUP15nuHHLjA?returnUri=https%3A%2F%2Fwww.giftzystore.in%2F%3FsearchTerm%3Dmini%2520figures',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OfUc5I-ox79mhr_u93j?returnUri=https%3A%2F%2Fwww.giftzystore.in%2F%3FsearchTerm%3Dmini%2520figures',
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OdIuXlYUj9Q4eqc1TIg?returnUri=https%3A%2F%2Fwww.giftzystore.in%2F%3FsearchTerm%3Dmini%2520figures',
]

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Make sure we scope the javascript pagination to #product-grid .card again
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
            <div class=\"card\" style=\"display: block;\">
                <img src=\"images/{img}\" alt=\"{title}\">
                <div class=\"title\">{title}</div>
                <div class=\"price\">{price}</div>
            </div>'''
            
    count = 137
    
    for url in NEW_URLS:
        try:
            prod_id = url.split('product/')[-1].split('?')[0]
            res = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(res.content, 'html.parser')
            
            # Extract standard stuff
            og_title = soup.find('meta', property='og:title')
            title = og_title.get('content', 'Unknown Action Figure').replace('Buy ', '').split(' online at ')[0]
            
            og_img = soup.find('meta', property='og:image')
            img_url = og_img.get('content', '')
            
            # Find the actual price from the Next.js payload using the product ID
            price = "N/A"
            for script in soup.find_all('script'):
                if script.string and prod_id in script.string:
                    m = re.search(r'\"' + re.escape(prod_id) + r'\".*?\"sellingPrice\"\s*:\s*(\d+)', script.string)
                    if m: 
                        price = f"₹ {m.group(1)}.00"
                        break
                    m2 = re.search(r'\"' + re.escape(prod_id) + r'\".*?\"price\"\s*:\s*(\d+)', script.string)
                    if m2:
                        price = f"₹ {m2.group(1)}.00"
                        break
            
            # If still nothing, fallback
            if price == "N/A":
                m3 = re.search(r'\"sellingPrice\":(\d+)', res.text)
                if m3: price = f"₹ {m3.group(1)}.00"
            
            if img_url:
                if not img_url.startswith('http'):
                    img_url = 'https:' + img_url
                    
                ext = img_url.split('.')[-1].split('?')[0]
                if ext.lower() not in ['jpg', 'jpeg', 'png', 'webp']: ext = 'jpg'
                filename = f"product_{count}.{ext}"
                
                # Download
                if not os.path.exists(f'images/{filename}'):
                    try:
                        data = requests.get(img_url, headers=HEADERS).content
                        with open(f'images/{filename}', 'wb') as f:
                            f.write(data)
                    except: pass
                
                mini_html += f'''
            <div class=\"card\" style=\"display: block;\">
                <img src=\"images/{filename}\" alt=\"{title}\">
                <div class=\"title\">{title}</div>
                <div class=\"price\">{price}</div>
            </div>'''
                print(f"Prepared: {title} | {price}")
                count += 1
                
        except Exception as e:
            print(f"Error processing {url}: {e}")

    mini_html += '''
        </div>
    </div>'''
            
    # Inject it before the script tag
    target_pos = html.rfind('<script>')
    if target_pos != -1:
        new_html = html[:target_pos] + mini_html + '\n    ' + html[target_pos:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        print("Restored Mini Figures and injected new URLs successfully!")
    else:
        print("Error: Could not find script tag in index.html")

if __name__ == "__main__":
    main()
