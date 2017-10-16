# format images for Alyssa Davis Gallery 
# run script in a directory that contains a directory called "original_images"
# with all original images inside. these won't be deleted
# run python resize-img.py width height

from __future__ import print_function
from __future__ import division
import os, sys
from PIL import Image

# size = (235,157)
print("~ starting script ~")
directory = "original_images"
thumbdir = "thumbnails"
carouseldir = "carousel_images"
desired_w = int(sys.argv[1])
desired_h = int(sys.argv[2])
print("desired width: ", desired_w, "desired height: ", desired_h)

if not os.path.exists(thumbdir):
    os.makedirs(thumbdir)
if not os.path.exists(carouseldir):
    os.makedirs(carouseldir)

for infile in os.listdir(directory):
    outfile = thumbdir + "/" + os.path.splitext(infile)[0] + "-thumbnail.png"
    print(infile)
    # print(outfile)
    if infile != outfile:
        try:
            im = Image.open(directory + "/" + infile)
            width, height = im.size
            # add case to only resize if aspect ratio matches
            print("w/h: ", width/height)
            print("aspect ratio: ", round(desired_w/desired_h, 1))
            if (round(width/height,1)) == round(desired_w/desired_h, 1):
                print("aspect ratio matches")
                new_width = desired_w
                new_height = desired_h
                final_img = im
                final_img.thumbnail((new_width, new_height), Image.ANTIALIAS)
            else:   
                if width > height:
                    print("width greater than height")
                    new_width = desired_w
                    new_height = int(round(new_width/(width/height)))
                    print("new h: ", new_height) 
                    transparent_h = (desired_h - new_height)/2
                    transparent_h = int(round(transparent_h))
                    transparent_w = desired_w
                    print("new width w transparency", new_width)
                    print('new height with transparency:', transparent_h+new_height+transparent_h)
                    if (transparent_h+new_height+transparent_h) != desired_h:
                        print('height doesnt match')
                elif width <= height:
                    print("height greater than width")
                    new_height = desired_h
                    new_width = int(round((width/height)*new_height))
                    transparent_h = desired_h
                    transparent_w = (desired_w - new_width)/2
                    transparent_w = int(round(transparent_w))
                    print("new height w transparency", new_height)
                    print('new width w transparency:', transparent_w+new_width+transparent_w)
                    if (transparent_w+new_width+transparent_w) != desired_w:
                        print('height doesnt match')
                # save resized image then overwrite with transparency
                size = (new_width, new_height)
                print("size of resized img: ", size)
                im.thumbnail(size)
                im.save(outfile, "PNG")

                # make transparent images
                transparent_box = Image.new('RGBA', (transparent_w,transparent_h), (0,0,0,0))
                t_box_path = os.path.splitext(infile)[0] + "-t-box.png"
                transparent_box.save(t_box_path, "PNG")
                print("transparent_box: ", transparent_box)

                # concatenate images
                images = map(Image.open, [t_box_path, outfile, t_box_path])
                print("images: ", images)

                os.remove(t_box_path)
                widths, heights = zip(*(i.size for i in images))

                if width > height:
                    total_height = sum(heights)
                    max_width = max(widths)
                    final_img = Image.new('RGBA', (max_width, total_height))
                    y_offset = 0
                    # print(final_img)
                    for im in images:
                      final_img.paste(im, (y_offset,0))
                      y_offset += im.size[1]
                elif width <= height:
                    total_width = sum(widths)
                    max_height = max(heights)
                    final_img = Image.new('RGBA', (total_width, max_height))
                    x_offset = 0
                    for im in images:
                      final_img.paste(im, (x_offset,0))
                      x_offset += im.size[0]

            print(final_img.size)
            final_img.save(outfile, 'PNG')
            
        except IOError:
            print("cannot create thumbnail for", infile)








