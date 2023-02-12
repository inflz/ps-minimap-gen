#
# READ THE README.md please!
# This script was written in a hurry so expect jankiness.
#
# Notes:
# - Assumes 1080p resolution
# - x axis (N/S ingame) = y axis here
# - z axis (W/E ingame) = x axis here
#

from PIL import Image, ImageDraw, ImageFont
from os import path, getcwd

FONT_NAME = "mapfont.ttf"

# Function to determine tile filename from tile coordinates and selected continent
def tile_name(contstr: str, x_tile: int, y_tile: int, tilecount: int):

    # Convert 0-31 tile coord (based) to PS2 tile coord system (wtf)
    tilecount = int(tilecount/2)
    x_tile = str((x_tile-tilecount)*4).zfill(3)
    y_tile = str((y_tile-tilecount)*4).zfill(3)

    # Generate name string
    return f"{contstr}_Tile_{x_tile}_{y_tile}_LOD0.dds"

# Banner
CONSOLE_WIDTH = 50
print("#"*CONSOLE_WIDTH)
print("#    P S    M I N I M A P    G E N    v 1 . 0    #")
print("#"*CONSOLE_WIDTH)

# Collect params (continent selection)
print("1 - Indar\n2 - Esamir\n3 - Amerish\n4 - Hossin\n5 - Oshur\n6 - Desolation\n7 - Nexus\n8 - Koltyr")
cont = int(input("Select continent (int 1 to 8): "))
while not (cont >= 1 and cont <=8): # basic input validation
    print(f"Error: invalid selection ({cont})!")
    cont = int(input("Select continent (int 1 to 8): "))
cont_string = ""
cont_tilecount = 32 # sq root of total number of tiles per continent
if (cont == 1):
    cont_string = "Indar"
elif (cont == 2):
    cont_string = "Esamir"
elif (cont == 3):
    cont_string = "Amerish"
elif (cont == 4):
    cont_string = "Hossin"
elif (cont == 5):
    cont_string = "Oshur"
elif (cont == 6):
    cont_string = "OutfitWars"
elif (cont == 7):
    cont_string = "nexus" # this lowercase pisses me off
    cont_tilecount = 16
elif (cont == 8):
    cont_string = "quickload" # tf is a quickload
    cont_tilecount = 16

cont_dir = path.join(getcwd(), "map-tiles", cont_string)

print("-"*CONSOLE_WIDTH)

# Collect params (location entry)
max_coord = int((cont_tilecount*256)/2 - 225) # make sure image doesn't go off edge of map
loc_y = int(input(f"Enter /loc x positon (int -{max_coord} to +{max_coord}): "))
while not (loc_y >= -max_coord and loc_y <= max_coord): # basic input validation
    print(f"Error: invalid selection ({loc_y})!")
    loc_y = int(input(f"Enter /loc x positon (int -{max_coord} to +{max_coord}): "))
loc_x = int(input(f"Enter /loc z positon (int -{max_coord} to +{max_coord}): "))
while not (loc_x >= -max_coord and loc_x <= max_coord):
    print(f"Error: invalid selection ({loc_x})!")
    loc_x = int(input(f"Enter /loc z positon (int -{max_coord} to +{max_coord}): "))

print("-"*CONSOLE_WIDTH)
border = False
border_sel = "x"
border_sel = str(input("Add border? (y/n): "))
while not (border_sel == "y" or border_sel == "n"):
    print(f"Error: invalid selection ({border_sel})!")
    border_sel = str(input("Add border? (y/n): "))

if (border_sel == "y"):
    border = True

print("-"*CONSOLE_WIDTH)
border_text = ""

if (border):
    border_text = str(input("Enter map border text (base name): "))

print("-"*CONSOLE_WIDTH)

zoom_coefficient = 2.0 # breaks if you use anything else

print("Generating map...")

# Generate blank 32x32 tileset canvas for cropping
tileset32x32 = Image.new(mode = "RGB",
                             size = (256*cont_tilecount, 256*cont_tilecount),
                             color = (0, 0, 0))

# Load all 1024 tiles into memory (this probably isn't very efficien but I was tired of dealing with tile coordinates!!!)
print(f"Loading tileset...")
for x in range(0,cont_tilecount):
    for y in range(0,cont_tilecount):
        cur_img = Image.open(path.join(cont_dir, f"{tile_name(cont_string, x, y, cont_tilecount)}")).copy()
        tileset32x32.paste(cur_img,(x*256,y*256))
        cur_img.close()
print(f"Tileset loaded")

# Flip upside down because game tiles are vertically inverted for... some reason?
tileset32x32 = tileset32x32.transpose(Image.FLIP_TOP_BOTTOM)

# Convert cartesian game coords to screen space coords of full res LOD0 map
coord_offset = (cont_tilecount*256)/2

loc_x_scrn = int(loc_x)+coord_offset
loc_y_scrn = coord_offset-int(loc_y) # Invert vertical coordinates

print(f"Calculated screenspace position: ({loc_x_scrn},{loc_y_scrn})")

# Some resizing stuff that was supposed to be dynamic but didn't quite work so now it's just pointless abstraction (basically don't change the coefficient)
zoom_mult = int(450*zoom_coefficient)
zoom_div = int(450/zoom_coefficient)

minimap = tileset32x32.crop((loc_x_scrn-zoom_div, loc_y_scrn-zoom_div, loc_x_scrn+zoom_div, loc_y_scrn+zoom_div))
tileset32x32.close()

minimap = minimap.resize((zoom_mult, zoom_mult))

minimap = minimap.crop((zoom_div, zoom_div, (zoom_mult-zoom_div), (zoom_mult-zoom_div)))

print(f"Cropped and scaled tileset")

# Make transparent 1080p canvas
canvas1080p = Image.new(mode = "RGBA",
                             size = (1920, 1080),
                             color = (0, 0, 0, 0))

canvas1080p_small = Image.new(mode = "RGBA",
                             size = (1920, 1080),
                             color = (0, 0, 0, 0))

# Paste maps over final 1080p canvas
canvas1080p.paste(minimap, (29, 589))

minimap_small = minimap.crop((96, 96, 353, 353))

canvas1080p_small.paste(minimap_small, (29, 782))

fname_large = f"{cont_string}_LMM_{loc_y}x_{loc_x}z.png"
fname_small = f"{cont_string}_SMM_{loc_y}x_{loc_x}z.png"

if border:
    border1080p_small = Image.open(path.join(getcwd(),"SMM_border.png"))
    canvas1080p_small = Image.alpha_composite(canvas1080p_small, border1080p_small)
    border1080p_small.close()
    draw = ImageDraw.Draw(canvas1080p_small)
    font = ImageFont.truetype(path.join(getcwd(),FONT_NAME), 12)
    bbox = font.getsize(border_text)
    center_x = 158
    center_y = 770
    x = center_x - bbox[0] / 2
    y = center_y - bbox[1] / 2
    draw.text((x, y), border_text, font=font, fill=(255, 255, 255, 255))

    border1080p = Image.open(path.join(getcwd(),"LMM_border.png"))
    canvas1080p = Image.alpha_composite(canvas1080p, border1080p)
    border1080p.close()
    draw = ImageDraw.Draw(canvas1080p)
    font = ImageFont.truetype(path.join(getcwd(),FONT_NAME), 12)
    bbox = font.getsize(border_text)
    center_x = 255
    center_y = 577
    x = center_x - bbox[0] / 2
    y = center_y - bbox[1] / 2
    draw.text((x, y), border_text, font=font, fill=(255, 255, 255, 255))

canvas1080p.save(path.join(getcwd(), "output", fname_large))
canvas1080p_small.save(path.join(getcwd(), "output", fname_small))

canvas1080p.close()
canvas1080p_small.close()

# Close things out
print(f"Maps successfully generated!")
print("Saved files to output folder:")
print(fname_large)
print(fname_small)
print("#"*CONSOLE_WIDTH)
