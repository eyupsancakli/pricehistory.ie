import re

with open('search_results.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

matches = re.findall(r'/cars-for-sale/[^"\']+', content)
for m in matches:
    print("https://www.donedeal.ie" + m)
