import re

def fix_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix addToCart to grab relative paths
    content = content.replace("const img = card.querySelector('img').src;", "const img = card.querySelector('img').getAttribute('src');")

    # 2. Add Base64 function and update exportCartPDF
    base64_logic = """
        function getBase64Image(url) {
            return new Promise((resolve, reject) => {
                if(!url) return resolve('');
                let img = new Image();
                img.crossOrigin = 'Anonymous';
                img.onload = () => {
                    let canvas = document.createElement('canvas');
                    canvas.width = img.width; canvas.height = img.height;
                    let ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);
                    resolve(canvas.toDataURL('image/jpeg'));
                };
                img.onerror = () => resolve('');
                if(url.startsWith('images/')) url = window.location.origin + '/' + url;
                img.src = url;
            });
        }

        async function exportCartPDF() {"""

    content = content.replace("function exportCartPDF() {", base64_logic)

    # Now make the cart loop async
    old_loop = """            cart.forEach(item => {
                total += item.price * item.qty;
                html += `
                    <tr>
                        <td style="padding:15px; border-bottom: 1px solid #e2e8f0;">
                            <img src="${item.img}" style="width: 60px; height: 60px; border-radius: 6px; object-fit: cover;">
                        </td>"""
    new_loop = """            for(let item of cart) {
                total += item.price * item.qty;
                let b64 = await getBase64Image(item.img);
                html += `
                    <tr>
                        <td style="padding:15px; border-bottom: 1px solid #e2e8f0;">
                            <img src="${b64}" style="width: 60px; height: 60px; border-radius: 6px; object-fit: cover;">
                        </td>"""
    content = content.replace(old_loop, new_loop)
    content = content.replace("            });\n            html += `</table>", "            }\n            html += `</table>")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

def fix_admin():
    with open('admin.html', 'r', encoding='utf-8') as f:
        content = f.read()

    base64_logic = """
function getBase64Image(url) {
    return new Promise((resolve) => {
        if(!url) return resolve('');
        let img = new Image();
        img.crossOrigin = 'Anonymous';
        img.onload = () => {
            let canvas = document.createElement('canvas');
            canvas.width = img.width; canvas.height = img.height;
            let ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            resolve(canvas.toDataURL('image/jpeg'));
        };
        img.onerror = () => resolve('');
        if(url.startsWith('images/')) url = window.location.origin + '/' + url;
        img.src = url;
    });
}

async function printOrder(orderId) {"""

    content = content.replace("function printOrder(orderId) {", base64_logic)

    old_loop = """    order.items.forEach((item, n) => {
        html += `
            <tr style="background:${n % 2 ? '#f1f5f9' : 'white'}">
                <td style="padding:10px;">
                    <img src="${item.img || ''}" style="width:60px;height:60px;border-radius:6px;object-fit:cover;">
                </td>"""
    new_loop = """    for(let n=0; n<order.items.length; n++) {
        let item = order.items[n];
        let b64 = await getBase64Image(item.img);
        html += `
            <tr style="background:${n % 2 ? '#f1f5f9' : 'white'}">
                <td style="padding:10px;">
                    <img src="${b64}" style="width:60px;height:60px;border-radius:6px;object-fit:cover;">
                </td>"""
    content = content.replace(old_loop, new_loop)
    content = content.replace("    });\n    html += `</table>", "    }\n    html += `</table>")

    # In viewOrder, let's also fix the img paths to ensure they work if absolute urls are broken
    # Actually if they use relative paths now, viewOrder will just work.
    
    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(content)

fix_index()
fix_admin()
print("Done")
