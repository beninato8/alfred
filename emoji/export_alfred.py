from config import *
from hashlib import sha256
from uuid import UUID
from emoji import EMOJI_DATA
import json
import os
from pprint import pprint
from collections import Counter

emojis = dict()
for e, data in EMOJI_DATA.items():
    if e in ['❤', '♥', '❣']:
        continue
    name = data['en']
    if 'alias' in data:
        for n in data['alias']:
            emojis[f'{n[:-1]}_{name[1:]}'] = e
    emojis[data['en']] = e

# from https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-annotations-full/annotations/en/annotations.json
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

home = os.path.expanduser('~') # home directory
path = f'{home}/.config/alfred/Alfred.alfredpreferences/snippets/{collection_name}'

if not os.path.exists(path):
    os.makedirs(path)

for name, uni_char in emojis.items(): # iterate over all name:emoji pairs
    snippet = make_snippet(name, uni_char)
    contents = snippet['alfredsnippet']
    file = f"{contents['keyword']} - {contents['uid']}.json"
    with open(f'{path}/{file}', 'w+') as f:
        json.dump(snippet, f, indent=4)
    # exit()
