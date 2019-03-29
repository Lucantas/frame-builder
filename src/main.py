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

def get_sheet_path(args):
    try:
        return args[args.index("-c") + 1]
    except ValueError:
        return ""

def get_available_frames(args):
    try:
        return args.index("-f") + 1
    except ValueError:
        return 0
        
def get_frame_dimension(args):
    try:
        return args.index("-d") + 1
    except ValueError:
        return 0


def crop_frames(file):
    # run identify to see the image size
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

    batch_crop(file, vertical_frames, horizontal_frames, square_side, square_side)
    
  
def crop_frames_with_dimension(file, dimension):
    # run identify to see the image size
    output = os.popen("identify -format '%[fx:w]x%[fx:h]' " + file).read()
    # find the width
    width = int(output.split("x")[0])
    #find the height
    height = int(output.split("x")[1])
    # get the frame width from the user's input
    frame_width = int(dimension.split("x")[0])
    # get the frame height from the user's input
    frame_height = int(dimension.split("x")[1])

    horizontal_frames = int(width/frame_width)
    vertical_frames = int(height/frame_height)

    max_frames = horizontal_frames * vertical_frames
    print(width, height, frame_width, frame_height)
    print(max_frames, horizontal_frames, vertical_frames)

    batch_crop(file, vertical_frames, horizontal_frames, frame_width, frame_height)

def crop_frames_with_max_frames(file, frames):
    pass

def batch_crop(file, vertical_frames, horizontal_frames, frame_width, frame_height):
    # Create the file if it doesn't exists
    try:
        os.mkdir(os.path.join(Path(file).parent, file.split(".")[0]) )
    except:
        print("dir exists")
    # loop over the frames
    for i in range(int(vertical_frames)):
        for j in range(int(horizontal_frames)):
            file_name = str(i) + "_" + str(j)
            destiny = os.path.abspath(os.path.join(Path(file).parent, file.split(".")[0], file_name))
            h_offset = frame_height * j
            w_offset = frame_width * i
            print("Executing: convert {0} -crop {1}x{2}+{3}+{4} {5}.png".format(
                    file,
                    frame_width,
                    frame_height,
                    h_offset,
                    w_offset,
                    destiny
                ))
            os.popen(
                "convert {0} -crop {1}x{2}+{3}+{4} {5}.png".format(
                    file,
                    frame_width,
                    frame_height,
                    h_offset,
                    w_offset,
                    destiny
                )
                )


args = sys.argv
sheet_path = get_sheet_path(args)
frames_available_index = get_available_frames(args)
frames_dimension_index = get_frame_dimension(args)

if (is_image(sheet_path)):
    if (frames_available_index > 0):
        crop_frames_with_max_frames(sheet_path, args[frames_available_index])
    elif (frames_dimension_index > 0):
        crop_frames_with_dimension(sheet_path, args[frames_dimension_index])
    else:
        crop_frames(sheet_path)
else:
    print("invalid image")




