# Create Alfred Snippets for Emojis

 - running `export_alfred.py` will add all emojis to Alfred Snippets
   - snippets will replace an emoji name with that emoji
   - `:grinning_face: will be replaced by 😀`
 - see `config.py` for settings
 - tested used Python 3.8.5
 - only needs `emoji` package to run
   - `pip3 install emoji` to install
 - `testing` directory was an attempt at parsing [Unicode's emoji list](https://unicode.org/emoji/charts/full-emoji-list.html)

Thanks to https://github.com/derickfay/import-alfred-snippets for showing me where to save the snippet JSON files