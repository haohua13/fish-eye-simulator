# fish-eye-simulator
Convert rectilinear images to fish-eye/wide angle lenses distortion. Also works with videos or image folders. Inspired from 
https://docs.opencv.org/4.x/db/d58/group__calib3d__fisheye.html and Fish-eye lens effect from Instagram

Example usage:
python fish_eye.py -i input_image.jpg -o output_image.png

![Original image](https://github.com/haohua13/fish-eye-simulator/blob/main/SDC10726.JPG)
![Fish-eye image with 0.5 distortion coefficient](https://github.com/haohua13/fish-eye-simulator/blob/main/test1.png)

python fish_eye.py -v input_video.avi -o output_images_folder/
python fish_eye.py -f image_folder -o output_images_folder/

![Video example with randomize effects](https://github.com/haohua13/fish-eye-simulator/blob/main/project.mp4)
