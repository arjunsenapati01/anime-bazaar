import re

def fix_admin():
    with open('admin.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix base64 function to handle broken Vercel URLs
    old_b64 = "if(!url) return resolve('');"
    new_b64 = "if(!url) return resolve('');\n        if(url.includes('vercel.app/images/')) url = 'images/' + url.split('images/')[1];"
    content = content.replace(old_b64, new_b64)

    # Fix viewOrder to handle broken Vercel URLs for the UI Modal
    old_view = "const imgHtml = i.img\\n            ? `<img src=\"${i.img}\""
    new_view = "let safeImg = i.img; if(safeImg && safeImg.includes('vercel.app/images/')) safeImg = 'images/' + safeImg.split('images/')[1];\n        const imgHtml = safeImg\n            ? `<img src=\"${safeImg}\""
    content = content.replace(old_view, new_view)

    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(content)

fix_admin()
print("Done")
