import os
import glob
from html.parser import HTMLParser

class LinkFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'link':
            attrd = dict(attrs)
            rel = attrd.get('rel','')
            href = attrd.get('href')
            if href and 'stylesheet' in rel:
                self.links.append(href)

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
html_files = [os.path.join(root, f) for f in os.listdir(root) if f.endswith('.html')]
expected_css = os.path.join(root, 'css')
required_css_files = ['css/main.css', 'css/work.css', 'css/contact.css']
errors = []

print('Checking HTML files for stylesheet links...')
for hf in sorted(html_files):
    with open(hf, 'r', encoding='utf-8') as fh:
        content = fh.read()
    parser = LinkFinder()
    parser.feed(content)
    rel_paths = parser.links
    print(f"\n{os.path.basename(hf)}: found links -> {rel_paths}")
    # check for main.css in every file
    if './css/main.css' not in rel_paths and 'css/main.css' not in rel_paths and '/css/main.css' not in rel_paths:
        errors.append(f"{os.path.basename(hf)} missing link to css/main.css")
    # page-specific checks
    name = os.path.basename(hf)
    if name == 'work.html':
        if './css/work.css' not in rel_paths and 'css/work.css' not in rel_paths and '/css/work.css' not in rel_paths:
            errors.append('work.html missing link to css/work.css')
    if name == 'contact.html':
        if './css/contact.css' not in rel_paths and 'css/contact.css' not in rel_paths and '/css/contact.css' not in rel_paths:
            errors.append('contact.html missing link to css/contact.css')

print('\nChecking css folder and files...')
if not os.path.isdir(os.path.join(root, 'css')):
    errors.append('Missing css/ folder')
else:
    for rc in required_css_files:
        if not os.path.isfile(os.path.join(root, rc)):
            errors.append(f'Missing {rc}')

print('\nChecking img folder...')
if not os.path.isdir(os.path.join(root, 'img')):
    errors.append('Missing img/ folder')
else:
    print('img/ folder exists')

print('\nSummary:')
if errors:
    print('Issues found:')
    for e in errors:
        print('- ' + e)
    print('\nResult: FAIL')
    exit(1)
else:
    print('No issues found — all required files and links are present.')
    print('\nResult: PASS')
    exit(0)
