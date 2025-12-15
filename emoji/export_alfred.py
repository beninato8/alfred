from config import *
from hashlib import sha256
from uuid import UUID
from emoji import EMOJI_DATA
import json
import os
from pprint import pprint
from collections import Counter
import requests
from pathlib import Path
import zipfile
import time
from xml.etree import ElementTree as ET

emojis = dict()
for e, data in EMOJI_DATA.items():
    if e in ['❤', '♥', '❣']:
        continue
    name = data['en']
    if 'alias' in data:
        for n in data['alias']:
            emojis[f'{n[:-1]}_{name[1:]}'] = e
    emojis[data['en']] = e

url = "https://raw.githubusercontent.com/unicode-org/cldr-json/refs/heads/main/cldr-json/cldr-annotations-full/annotations/en/annotations.json"
dest = Path("annotations.json")

if not dest.exists():
    print("Downloading annotations.json...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()  # fails fast on HTTP errors
    dest.write_bytes(response.content)

with open('annotations.json', 'r') as f:
    cldr_data = json.load(f)['annotations']['annotations']

cldr = dict()
stats = []
ignore = {'face', 'animal', 'arrow', 'button', 'food', 'person', 'hand', 'right', 'mathematics'}
for i, (e, data) in enumerate(cldr_data.items()):
    if len(e) > 1 or ord(e) < 124:
        continue
    name = '_'.join(' '.join(data['tts']).split(' '))
    for alias in [f':{n}_{name}:' for n in set(data['default']) - ignore]:
        cldr[alias] = e
    for d in data['default']:
        stats.append(d)

# emoji library + user config + unicode annotations
emojis ={**emojis, **extra, **cldr}

def get_uuid(s):
    """use hash to keep uuid constant when re-running"""
    sha = sha256(s.encode('utf-8')).hexdigest()
    uuid = UUID(sha[:32])
    return str(uuid)

def make_snippet(name, uni_char):
    """create snippet as dictionary from name and unicode"""
    snippet = dict()
    snippet['snippet'] = uni_char
    if dontautoexpand:
        snippet['dontautoexpand'] = True
    snippet['uid'] = get_uuid(f'{uni_char} {name[1:-1]}')
    snippet['name'] = f'{uni_char} {name[1:-1]}'
    snippet['keyword'] = f'{name}'
    return {'alfredsnippet': snippet}

def create_info_plist():
    """create info.plist XML for Alfred snippet collection"""
    plist = ET.Element('plist', version='1.0')
    plist_dict = ET.SubElement(plist, 'dict')
    
    prefix_key = ET.SubElement(plist_dict, 'key')
    prefix_key.text = 'snippetkeywordprefix'
    prefix_string = ET.SubElement(plist_dict, 'string')
    prefix_string.text = ''
    
    suffix_key = ET.SubElement(plist_dict, 'key')
    suffix_key.text = 'snippetkeywordsuffix'
    suffix_string = ET.SubElement(plist_dict, 'string')
    suffix_string.text = ''
    
    # Pretty print the XML with indentation (using tabs like Alfred does)
    ET.indent(plist, space='\t')
    xml_string = ET.tostring(plist, encoding='unicode')
    # Add XML declaration and DOCTYPE
    return '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n' + xml_string

# Create the .alfredsnippets file (which is a zip file)
output_file = f'{collection_name}.alfredsnippets'

with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Create info.plist
    info_plist = create_info_plist()
    zipf.writestr('info.plist', info_plist)
    
    # Snippets go at the root level
    # Filename format: "name [uid].json"
    for name, uni_char in emojis.items():
        snippet = make_snippet(name, uni_char)
        contents = snippet['alfredsnippet']
        snippet_name = contents['name'].replace('/', ' / ')
        filename = f"{snippet_name} [{contents['uid']}].json"
        # Alfred expects compact JSON (no indentation)
        zipf.writestr(filename, json.dumps(snippet, separators=(',', ':')))

print(f"Created {output_file}")
