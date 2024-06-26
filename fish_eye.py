import imageio.v2 as imageio
import imageio.v3 as iio
import numpy as np
from math import sqrt
import sys
import argparse
import os
import cv2
from images_to_video import images_to_video
import re
import random

def extract_numeric_part(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    else:
        return float('inf')  # Return a large number for non-numeric filenames

def process_folder(input_folder, output_folder, distortion, vary_distortion=False, randomize_rgb=False):
    # get the list of image files in the directory in sorted order
    images = [img for img in os.listdir(input_folder)]
    images = sorted(images, key=lambda x: extract_numeric_part(x))
    distortion_value = -1.2
    distortion_step = 0.2
    distortion_limit = 1.2
    # no distortion
    distortion_value = 0
    distortion_step = 0
    distortion_limit = 0

    flag = False
    iterator = 0
    for image in images:
        imgobj = imageio.imread(os.path.join(input_folder, image))
        iterator += 1
        # randomize RGB/BGR for each image frame
        if randomize_rgb:
            imgobj = cv2.cvtColor(imgobj, random.choice([cv2.COLOR_BGR2RGB, cv2.COLOR_RGB2BGR]))
        else:
            imgobj = cv2.cvtColor(imgobj, cv2.COLOR_BGR2RGB)
        if vary_distortion:
            if flag:
                distortion_value += distortion_step
                if distortion_value >= distortion_limit:
                    flag = False
            else:
                distortion_value -= distortion_step
                if distortion_value <= -distortion_limit:
                    flag = True
        else:
            distortion_value = distortion

        # Call fish function here
        distorted_frame = fish(imgobj, distortion_value)
        # Write the distorted frame to the output folder
        cv2.imwrite(os.path.join(output_folder, f"{iterator}.png"), distorted_frame)
    

def process_video(new_video_path, input_video, distortion, fps = 30, vary_distortion = False, randomize_rgb = False):
    # use the resolution of the input video
    cap = cv2.VideoCapture(input_video)
    resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("Resolution: ", resolution)
    distortion_value = -1
    distortion_step = 0.1
    end_distortion = 1
    flag = False
    iterator = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if vary_distortion:
            if flag:
                distortion_value += distortion_step
                if distortion_value >= 1:
                    flag = False
            else:
                distortion_value -= distortion_step
                if distortion_value <= -1:
                    flag = True
        else:
            distortion_value = distortion  # Use fixed distortion value
        # randomize RGB/BGR for each image frame
        if randomize_rgb:
            frame = cv2.cvtColor(frame, random.choice([cv2.COLOR_BGR2RGB, cv2.COLOR_RGB2BGR]))

        # call fish function here
        distorted_frame = fish(frame, distortion_value)
        # write the distorted frame to the new video
        # video.write(distorted_frame)
        cv2.imwrite(new_video_path + str(iterator) + ".png", distorted_frame)
        iterator += 1

    cap.release()
    # video.release()

def fish_distortion(x, y, distance, distortion):
    """
    Apply a fish-eye distortion to the given pixel coordinates (x, y)
    :param x: The x coordinate of the pixel
    :param y: The y coordinate of the pixel
    :param distance: The distance from the center of the image
    :param distortion: The distortion coefficient, in which moves pixels from/to the center
    """
    if 1-distortion*(distance**2) == 0:
        return x, y
    return x * (distance / (1 - distortion * (distance ** 2))), y * (distance / (1 - distortion * (distance ** 2)))

def fish(img, distortion):

    weight, height = img.shape[0], img.shape[1]
    if len(img.shape) == 2:
        bw_img = np.copy(img)
        img = np.dstack((img, bw_img, bw_img))
    if len(img.shape) == 3 and img.shape[2] == 3:
        print("RGB to RGBA")
        img = np.dstack((img, np.full((weight, height), 255)))
    # prepare for dst image
    dst = np.zeros_like(img)
    w, h = float(weight), float(height)
    for x in range(len(dst)):
        for y in range(len(dst[x])):

            # normalize x and y to be between -1 and 1
            normalized_x, normalized_y = (2 * x - w) / w, (2 * y - h) / h 

            # get the distance from the normalized center
            r = sqrt(normalized_x**2 + normalized_y**2)
            # new normalized pixel coordinates
            distorted_x, distorted_y = fish_distortion(normalized_x, normalized_y, r, distortion)

            # convert the normalized coordinates back to pixel coordinates
            new_x, new_y = int((distorted_x + 1) * w / 2), int((distorted_y + 1) * h / 2)

            # check if new coordinates are within the bounds of the image
            if 0 <= new_x < w and 0 <= new_y < h:
                dst[x, y] = img[new_x, new_y]
    return dst.astype(np.uint8)

def parse_args(args = sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description = "Apply a fish-eye distortion to images or videos",
        prog = 'python3 fish_eye.py'
    )
    # add the image argument
    parser.add_argument(
        "-i", "--image", help = "Path to the input image", required = False
    )
    # add the video argument
    parser.add_argument("-v", "--video", help="Path to the input video."
                        " If this argument is provided, the script will output a video instead of an image."
                        " The output video will be the same as the input video, but with the fish-eye effect applied."
                        " The output video will be saved to the path provided by the --outpath argument."
                        " The output video will have the same frame rate and resolution as the input video.",
                        required = False)
    
    # add image folder argument
    parser.add_argument("-f", "--folder", help="Path to the input image folder."
                        " If this argument is provided, the script will output a video instead of an image."
                        " The output video will be the same as the input video, but with the fish-eye effect applied."
                        " The output video will be saved to the path provided by the --outpath argument."
                        " The output video will have the same frame rate and resolution as the input video.",
                        required = False)
    
    # add the outpath argument
    parser.add_argument("-o", "--outpath", help="file path to write output to."
                        " format: <path>.<format(jpg,png,etc..)>", required = True)
    # add the distortion argument
    parser.add_argument("-d", "--distortion",
                        help="The distortion coefficient. How much the move pixels from/to the center."
                        " Recommended values are between -1 and 1."
                        " The bigger the distortion, the further pixels will be moved outwards from the center (fisheye)."
                        " The smaller the distortion, the closer pixels will be move inwards toward the center (rectilinear)."
                        " For example, to reverse the fisheye effect with --distoration 0.5,"
                        " You can run with --distortion -0.3."
                        " Note that due to double processing the result will be somewhat distorted.",
                        type=float, default=0.5)
    # add the variation of distortion argument
    parser.add_argument("-vary", "--vary_distortion", help="Vary the distortion coefficient over time."
                        " If this argument is provided, the script will apply a varying distortion coefficient to the input video."
                        " The distortion coefficient will start at -1, and increase each frame until it reaches 1."
                        " Then it will decrease each frame until it reaches -1 again."
                        " The cycle will then repeat.", action="store_true")
    
    parser.add_argument("-randomize", "--randomize_rgb", help="Randomize the RGB/BGR order for each frame."
                        " If this argument is provided, the script will randomize the order of the color channels for each frame in the input video."
                        " This can be used to create a psychedelic effect.", action="store_true")
    
    
    return parser.parse_args(args)

if __name__ == "__main__":
    args = parse_args()
    # check if argument image
    if args.image:
        try:
            imgobj = imageio.imread(args.image)
        except Exception as e:
            print(e)
            sys.exit(0)

    if os.path.exists(args.outpath):
        ans = input(args.outpath + " already exists. Overwrite? (y/n): ")
        if ans.lower() != "y":
            sys.exit(0)
    else:
        os.makedirs(args.outpath, exist_ok = True)
    
    # check if argument video
    if args.video:
        process_video(args.outpath, args.video, args.distortion, vary_distortion = args.vary_distortion, randomize_rgb = args.randomize_rgb)
        print("Output video saved to " + args.outpath)

    if args.image:
        output_img = fish(imgobj, args.distortion)    
        imageio.imwrite(args.outpath, output_img, format = 'png')
        print("Output image saved to " + args.outpath)

    if args.folder:
        process_folder(args.folder, args.outpath, args.distortion, vary_distortion = args.vary_distortion, randomize_rgb = args.randomize_rgb)
        print("Output images saved to " + args.outpath)

    # convert the images in args.outpath to a video
    current_directory = os.getcwd()  # get current directory
    images_directory = os.path.join(current_directory, args.outpath) 


    # check if mp4 file already exists, if so, create a new one
    output_video_path = os.path.join(current_directory, 'project.mp4')
    if os.path.exists(output_video_path):
        i = 1
        while os.path.exists(output_video_path):
            output_video_path = os.path.join(current_directory, 'project' + str(i) + '.mp4')
            i += 1

    images_to_video(images_directory, output_video_path)
    


        