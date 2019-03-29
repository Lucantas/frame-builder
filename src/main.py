import sys
import imghdr
import subprocess
import os
import math
from pathlib import Path

def file_exists(path):
    try:
        open(path)
        return True
    except FileNotFoundError:
        print("file does not exist: " + path)
        return False

def is_image(file):
    if (file_exists(file)):
        if (imghdr.what(file) != None):
            return True

    return False

def crop_frames(file):
    # run identify to see the image size]
    output = os.popen("identify -format '%[fx:w]x%[fx:h]' " + file).read()
    # find the width
    width = int(output.split("x")[0])
    #find the height
    height = int(output.split("x")[1])
    #find the square side
    square_side = math.gcd(height,width) 
    print(square_side)
    # Number of squares. 
    max_frames = (height * width)/(square_side*square_side) 
    horizontal_frames = int(width/square_side)
    vertical_frames = int(height/square_side)
    # loop over the frames
    try:
        os.mkdir(os.path.join(Path(file).parent, file.split(".")[0]) )
    except:
        print("dir exists")

    for i in range(int(vertical_frames)):
        for j in range(int(horizontal_frames)):
            file_name = str(i) + "_" + str(j)
            destiny = os.path.abspath(os.path.join(Path(file).parent, file.split(".")[0], file_name))
            h_offset = square_side * j
            w_offset = square_side * i
            print("convert {0} -crop {1}x{1}+{2}+{3} {4}.png".format(
                    file,
                    square_side,
                    h_offset,
                    w_offset,
                    destiny
                ))
            os.popen(
                "convert {0} -crop {1}x{1}+{2}+{3} {4}.png".format(
                    file,
                    square_side,
                    h_offset,
                    w_offset,
                    destiny
                )
                )
  

  

def find_square_by_frame_dimension(width, height):
    size = math.max(width, height)
    columns = math.floor(width/size)
    rows = math.floor(height/size)
     

    
args = sys.argv
sheet_path = args[args.index("-c") + 1]

if (is_image(sheet_path)):
    print("seems to be an image")
    crop_frames(sheet_path)





