from bs4 import BeautifulSoup
import re

with open('full-emoji-list.html') as f:
    html = f.read()
html = re.sub(r"<td class.*?src='data:image/png;base64.*?</td>", '', html)
html = re.sub(r"\n{2,}", '\n', html)
soup = BeautifulSoup(html, 'html.parser')

lines = []
rows = soup.find_all('tr')
size = len(rows)
for i, row in enumerate(rows):
    if row.find('th', {'class':['bighead', 'mediumhead']}):
        continue
    if 'CLDR Short Name' in row.text.split('\n'):
        continue
    lines.append([x for x in row.text.split('\n') if x not in ('', '-', '—')])
    if i % 100 == 0:
        print(f'{i/size:.4f}')
print(lines)
print(len(lines))