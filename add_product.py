import os
import sys
import requests
import re
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 add_product.py <url>")
        return
        
    URL = sys.argv[1]
    HEADERS = {'User-Agent': 'Mozilla/5.0'}

    print(f"Fetching {URL}...")
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    title_elem = soup.find('h1', class_=re.compile(r'product_title'))
    if not title_elem:
        print("Could not find product title.")
        return
        
    title = title_elem.text.strip()
    
    price_elem = soup.find('p', class_='price')
    price = price_elem.text.strip() if price_elem else ""
    
    img_wrapper = soup.find('div', class_='woocommerce-product-gallery__image')
    if not img_wrapper or not img_wrapper.find('img'):
        print("Could not find product image.")
        return
        
    img_elem = img_wrapper.find('img')
    img_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-lazy-src')

    if not img_url.startswith('http'):
        img_url = 'https:' + img_url if img_url.startswith('//') else 'https://apkastore.in' + img_url

    ext = img_url.split('.')[-1].split('?')[0]
    if ext.lower() not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
        ext = 'jpg'

    os.makedirs('images', exist_ok=True)
    count = len([f for f in os.listdir('images') if os.path.isfile(os.path.join('images', f))])
    
    filename = f"product_{count}.{ext}"
    filepath = os.path.join('images', filename)

    if not os.path.exists(filepath):
        print(f"Downloading image from {img_url}...")
        img_data = requests.get(img_url, headers=HEADERS, timeout=10).content
        with open(filepath, 'wb') as f:
            f.write(img_data)

    card_html = f'''
        <div class="card">
            <img src="{filepath}" alt="{title}">
            <div class="title">{title}</div>
            <div class="price">{price}</div>
        </div>'''

    print("Updating index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the current count and update it
    match = re.search(r'<h1>Keychains \((\d+) Products\)</h1>', html)
    current_count = int(match.group(1)) if match else count
    new_count = current_count + 1
    
    html = re.sub(r'<h1>Keychains \(\d+ Products\)</h1>', f'<h1>Keychains ({new_count} Products)</h1>', html)
    
    # Insert the card right before the closing of the grid div
    html = html.replace('    </div>\n    \n    <div class="pagination">', card_html + '\n    </div>\n    \n    <div class="pagination">')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Added '{title}' successfully! Total products is now {new_count}.")

if __name__ == "__main__":
    main()
