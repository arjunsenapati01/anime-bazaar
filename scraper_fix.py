import os
import re
import json
import urllib.request

NEW_URLS = [
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-OdxM7_wTnXOE2wcn89K', # BTS
    'https://www.giftzystore.in/s/gallery/gala-collection/action-figure/k3p/product/-Od8jTru_86XvKQyeYqp', # Pokemon
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

def extract_safe(data, p_id):
    # Search for product object where id == p_id
    if isinstance(data, dict):
        if data.get('id') == p_id: return data
        for v in data.values():
            res = extract_safe(v, p_id)
            if res: return res
    elif isinstance(data, list):
        for v in data:
            res = extract_safe(v, p_id)
            if res: return res
    return None

for url in NEW_URLS:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        res = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        m = re.search(r'<script\s+type=application/json\s+id=amalgam-json>(.*?)</script>', res, flags=re.DOTALL)
        if m:
            data = json.loads(m.group(1))
            prod_id = url.split('/')[-1].split('?')[0]
            prod = extract_safe(data, prod_id)
            
            if prod:
                title = prod.get('name', 'Action Figure').split('|')[0].strip().replace('Buy ', '').split(' online')[0].strip()
                price = prod.get('sellingPrice', 'N/A')
                
                # Check media
                media = prod.get('media', [])
                img_url = ""
                # skip logo logic isn't needed if we pull from 'media' array, usually index 0 is valid.
                for m_obj in media:
                    u = m_obj.get('url', '')
                    if "OcFjAgAQ8z8fMu4YETU" not in u: # Ignore logo
                        img_url = u
                        break
                if not img_url and media: img_url = media[0].get('url', '')
                
                print(f"Product: {title} | ₹{price} | img={img_url}")
                results.append((title, price, img_url))
            else:
                print("Could not find product in JSON", url)
        else:
            print("Could not find script amalgam-json", url)
    except Exception as e:
        print("Error fetching", url, e)

# Save dict
import pickle
with open('results.pkl', 'wb') as f:
    pickle.dump(results, f)
print("Saved to results.pkl")
