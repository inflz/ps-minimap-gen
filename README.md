# PS Minimap Gen v1.0

Generates a clone of ingame fixed minimap from raw PS2 LOD0 map tiles and puts it on a transparent 1080p canvas.

Currently only supports max zoom level (2x), true north (fixed) orientation, and 1080p.

I can't distribute the tiles, but if you need this script you probably know someone or somewhere you can get them from. This is designed to take raw LOD0.dds files from the game, but you can modify the tile_name function if you acquired them elsewhere.

For questions contact inflz#4000.

Works on windows & linux.

## Requirements

- python 3
- Python Imaging Library (PIL)

## Execution

1. Extract .zip somewhere
2. Add LOD0 tiles for each continent to their respective directory in map_tiles (should be 1024 per large continent)
3. Add a .ttf file with font to program directory (for minimap labels)
4. Rename .ttf file to mapfont.ttf
5. Open program directory in terminal
6. Run `python3 minimap-gen.py`
7. Collect your files in output

## Demystification

The script uses the same naming conventions as the game files. Renaming input files or directories could break stuff. Note these inconsistencies:

- "quickload" = Koltyr
- "OutfitWars" = Desolation
- "nexus" = Nexus
