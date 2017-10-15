# format images for Alyssa Davis Gallery 
# run script in a directory that contains a directory called "original_images"
# with all original images inside. these won't be deleted

from __future__ import print_function
from __future__ import division
import os, sys
from PIL import Image

# size = (235,157)
print("~ starting script ~")
directory = "original_images"
thumbdir = "thumbnails"
carouseldir = "carousel_images"

transparent_box = Image.new('RGBA', (40,80), (0,0,0,0))
transparent_box.save("test.png", "PNG")

if not os.path.exists(thumbdir):
    os.makedirs(thumbdir)
if not os.path.exists(carouseldir):
    os.makedirs(carouseldir)

for infile in os.listdir(directory):
    outfile = thumbdir + "/" + os.path.splitext(infile)[0] + "-thumbnail.png"
    print(infile)
    print(outfile)
    if infile != outfile:
        try:
            im = Image.open(directory + "/" + infile)
            width, height = im.size
            if width > height:
            	new_width = 235
            	new_height = new_width/(width/height)
            	print("width greater")
            elif width <= height:
            	new_height = 157
            	new_width = (width/height)*new_height
            	print("height greater")
            print(width)
            print(height)
            print(int(round(new_height)))
            print(int(round(new_width)))
            size = (new_width, new_height)
            im.thumbnail(size)
            im.save(outfile, "PNG")
        except IOError:
            print("cannot create thumbnail for", infile)