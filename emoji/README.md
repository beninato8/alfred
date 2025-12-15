# Create Alfred Snippets for Emojis

Generate an `.alfredsnippets` file containing emoji snippets for Alfred.

## Installation

Just run `install.sh` - it will:
1. Set up a Python virtual environment
2. Install required dependencies
3. Generate `emoji.alfredsnippets`
4. Open the file to import it into Alfred

## Usage

- Running `export_alfred.py` generates an `.alfredsnippets` file containing all emoji snippets
- Snippets will replace an emoji name with that emoji
- Example: `:grinning_face:` will be replaced by 😀
- The generated file can be imported into Alfred by double-clicking it

## Configuration

See `config.py` for settings:
- `extra`: User-defined name:emoji pairs
- `collection_name`: Name of the snippet collection
- `dontautoexpand`: Whether to disable auto-expansion (default: False)

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt` (installed automatically by `install.sh`)

## Notes

- The `testing` directory contains an attempt at parsing [Unicode's emoji list](https://unicode.org/emoji/charts/full-emoji-list.html)
- The script generates a `.alfredsnippets` file (a zip archive) compatible with Alfred 5+