import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove HTML Section
html_start = text.find('<!-- NEW: Document Validation Section -->')
html_end = text.find('</div><!-- End Col -->', html_start)
if html_start != -1 and html_end != -1:
    text = text[:html_start] + text[html_end:]
    print("Removed HTML Section")
else:
    print("Could not find HTML section markers")

# 2. Remove JS Section
js_start = text.find('// --- New Feature Functions ---')
js_end = text.find('// --- INITIALIZATION ---', js_start)
if js_start != -1 and js_end != -1:
    text = text[:js_start] + text[js_end:]
    print("Removed JS Section")
else:
    print("Could not find JS section markers")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated index.html")
