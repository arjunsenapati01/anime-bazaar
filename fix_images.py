import urllib.request
import urllib.parse
import re
import json

def get_image(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        m = re.search(r'vqd=([\d-]+)', html)
        if not m: return None
        vqd = m.group(1)
        
        search_url = f"https://duckduckgo.com/i.js?q={urllib.parse.quote(query)}&o=json&vqd={vqd}"
        req2 = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        res2 = urllib.request.urlopen(req2, timeout=10).read().decode('utf-8')
        data = json.loads(res2)
        return data['results'][0]['image']
    except Exception as e:
        print(f"Failed {query}: {e}")
        return None

items = [
    "BTS Mini Figures (Set of 7) 7cm pvc",
    "6 Pcs/Set Pokemon Figure action",
    "Dragon Ball Z Anime 21 Pcs figure set dbz",
    "ONE Piece Set of 8 Action Figures 7-8cm",
    "Spider Man - Set of 8 Small Figures",
    "Naruto Anime 12 Pcs Action Figure",
    "Dragon Ball Z 12 Pice Set",
    "16 Pcs Minion Set figures",
    "Tom & Jerry Miniature Action Figure-5Cm",
    "Avengers 6pcs Miniature Action Figure Set - Marvel"
]

images = []
for t in items:
    img = get_image(t)
    images.append(img)
    print(f"Title: {t[:20]} -> {img}")

with open('scraped_images.json', 'w') as f:
    json.dump(images, f)
