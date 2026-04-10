import os
import requests
from bs4 import BeautifulSoup
import re

URLS = [
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

headers = {'User-Agent': 'Mozilla/5.0'}

with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

count = len([f for f in os.listdir('images') if os.path.isfile(os.path.join('images', f))])

for url in URLS:
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    # Title
    og_title = soup.find('meta', property='og:title')
    title = og_title.get('content') if og_title else 'Giftzy Store Action Figure'
    title = title.replace('Buy ', '').split(' online at ')[0]
    
    # Price
    price = 'N/A'
    price_match = re.search(r'₹\s*([\d,]+)', res.text)
    if price_match:
        price = '₹ ' + price_match.group(1)
    else:
        pm2 = re.search(r'"sellingPrice":(\d+)', res.text)
        if pm2:
            price = '₹ ' + pm2.group(1)
            
    # Image
    og_img = soup.find('meta', property='og:image')
    img_url = og_img.get('content') if og_img else ''
    
    if img_url:
        if not img_url.startswith('http'):
            img_url = 'http:' + img_url
        ext = img_url.split('.')[-1].split('?')[0]
        if ext.lower() not in ['jpg', 'jpeg', 'png', 'gif', 'webp']: ext = 'jpg'
        
        filename = f"images/product_{count}.{ext}"
        print(f"Downloading image from {img_url}...")
        img_data = requests.get(img_url, headers=headers).content
        with open(filename, 'wb') as f:
            f.write(img_data)
        count += 1
        
        card_html = f'''
            <div class="card" style="display: block;">
                <img src="{filename}" alt="{title}">
                <div class="title">{title}</div>
                <div class="price">{price}</div>
            </div>'''
            
        target = '<div class="grid" id="minifigure-grid">'
        html_content = html_content.replace(target, target + card_html)
        print(f"Added: {title} | {price}")
    else:
        print(f"Failed to find image for {url}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully processed all urls!")
