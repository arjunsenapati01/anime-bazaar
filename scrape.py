import os
import requests
from bs4 import BeautifulSoup
import re

URLS = [
    "https://apkastore.in/product-category/keychains/",
    "https://apkastore.in/product-category/keychains/page/2/",
    "https://apkastore.in/product-category/keychains/page/3/",
    "https://apkastore.in/product-category/keychains/page/4/",
    "https://apkastore.in/product-category/keychains/page/5/"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def main():
    os.makedirs('images', exist_ok=True)
    count = 0
    seen_titles = set()
    
    html_cards = ""
    
    for url in URLS:
        print(f"Fetching page {url}...")
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Woo commerce classes usually include 'product' in the class list of li or div
        products = soup.find_all('li', class_=re.compile(r'\bproduct\b'))
        if not products:
            products = soup.find_all('div', class_=re.compile(r'\bproduct-inner\b'))
            if not products:
                products = soup.find_all('div', class_=re.compile(r'\bproduct\b'))
        
        print(f"Found {len(products)} product elements.")
        
        for i, prod in enumerate(products):
            # find title
            title_elem = prod.find(['h2', 'h3'])
            if not title_elem:
                title_elem = prod.find(class_=re.compile(r'title'))
            title = title_elem.text.strip() if title_elem else f"Product {count+1}"
            
            # SKIP empty or default titles
            if "Product" in title or not title:
                continue
                
            # DEDUPLICATE
            if title in seen_titles:
                continue
            seen_titles.add(title)
            
            # find price
            price_elem = prod.find(class_=re.compile(r'price'))
            price = price_elem.text.strip() if price_elem else "N/A"
            
            # find image
            img_elem = prod.find('img')
            img_url = ""
            local_img = ""
            if img_elem:
                # handle lazy loading
                img_url = img_elem.get('data-src') or img_elem.get('data-lazy-src') or img_elem.get('src')
                if img_url:
                    if not img_url.startswith('http'):
                        img_url = 'https:' + img_url if img_url.startswith('//') else 'https://apkastore.in' + img_url
                        
                    # download image
                    try:
                        ext = img_url.split('.')[-1].split('?')[0]
                        if ext.lower() not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                            ext = 'jpg'
                        filename = f"product_{count}.{ext}"
                        filepath = os.path.join('images', filename)
                        
                        if not os.path.exists(filepath):
                            img_data = requests.get(img_url, headers=HEADERS, timeout=10).content
                            with open(filepath, 'wb') as f:
                                f.write(img_data)
                        local_img = filepath
                        
                    except Exception as e:
                        print(f"Failed to download {img_url}: {e}")
            
            # SKIP if no image
            if not local_img:
                continue
                
            count += 1
            html_cards += f'''
            <div class="card">
                <img src="{local_img}" alt="{title}">
                <div class="title">{title}</div>
                <div class="price">{price}</div>
            </div>'''
            print(f"Processed: {title} | {price}")

    # Generate the full HTML with pagination JS
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scraped Keychains</title>
    <style>
        body {{ font-family: sans-serif; background: #f4f4f4; margin: 0; padding: 20px; text-align: center; }}
        h1 {{ color: #333; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; text-align: left; }}
        .card {{ background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; display: none; }}
        .card img {{ max-width: 100%; height: auto; border-radius: 4px; object-fit: cover; max-height: 250px; }}
        .title {{ font-size: 1.1em; margin: 10px 0; color: #333; }}
        .price {{ font-weight: bold; color: #e44d26; }}
        .pagination {{ margin: 30px 0; }}
        .pagination button {{ padding: 10px 20px; margin: 0 5px; cursor: pointer; border: none; background: #007bff; color: white; border-radius: 4px; font-size: 16px; }}
        .pagination button:disabled {{ background: #ccc; cursor: not-allowed; }}
        #page-info {{ font-size: 18px; margin: 0 15px; }}
    </style>
</head>
<body>
    <h1>Keychains ({count} Products)</h1>
    <div class="grid" id="product-grid">
        {html_cards}
    </div>
    
    <div class="pagination">
        <button id="prev-btn" onclick="changePage(-1)">Previous</button>
        <span id="page-info">Page 1</span>
        <button id="next-btn" onclick="changePage(1)">Next</button>
    </div>

    <script>
        const cards = document.querySelectorAll('.card');
        const itemsPerPage = 20;
        let currentPage = 1;
        const totalPages = Math.ceil(cards.length / itemsPerPage) || 1;

        function showPage(page) {{
            if (page < 1) page = 1;
            if (page > totalPages) page = totalPages;
            currentPage = page;

            cards.forEach((card, index) => {{
                card.style.display = 'none';
                if (index >= (page - 1) * itemsPerPage && index < page * itemsPerPage) {{
                    card.style.display = 'block';
                }}
            }});

            document.getElementById('page-info').innerText = `Page ${{currentPage}} of ${{totalPages}}`;
            document.getElementById('prev-btn').disabled = currentPage === 1;
            document.getElementById('next-btn').disabled = currentPage === totalPages;
            window.scrollTo(0, 0);
        }}

        function changePage(direction) {{
            showPage(currentPage + direction);
        }}

        // Initialize first page
        showPage(1);
    </script>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Saved {count} products to index.html with JS pagination.")

if __name__ == "__main__":
    main()
