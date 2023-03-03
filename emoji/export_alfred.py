from config import *
from hashlib import sha256
from uuid import UUID
from emoji import EMOJI_DATA
import json
import os
from pprint import pprint

emojis = dict()
for e, data in EMOJI_DATA.items():
    if e in ['❤', '♥', '❣']:
        continue
    name = data['en']
    if 'alias' in data:
        for n in data['alias']:
            emojis[f'{n[:-1]}_{name[1:]}'] = e
    emojis[data['en']] = e

emojis ={**emojis, **extra} # emoji library + user config

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

for name, uni_char in emojis.items(): # iterate over all name:emoji pairs
    snippet = make_snippet(name, uni_char)
    contents = snippet['alfredsnippet']
    file = f"{contents['keyword']} - {contents['uid']}.json"
    with open(f'{path}/{file}', 'w+') as f:
        json.dump(snippet, f, indent=4)
    # exit()
