# fish-eye-simulator
Convert rectilinear images to fish-eye/wide angle lenses distortion. Also works with videos or image folders. Inspired from 
https://docs.opencv.org/4.x/db/d58/group__calib3d__fisheye.html and Fish-eye lens effect from Instagram

Example usage:

python fish_eye.py -i input_image.jpg -o output_image.png


<img src="https://github.com/haohua13/fish-eye-simulator/blob/main/SDC10726.JPG"  alt="Original Image" width="400">
<img src="https://github.com/haohua13/fish-eye-simulator/blob/main/test1.png" alt="0.5 Distortion Image" width="500">


Example usage: 

python fish_eye.py -v input_video.avi -o output_images_folder/

python fish_eye.py -f image_folder -o output_images_folder/
-vary -randomize


Video example with randomize RGB/BGR effects


[<img src="https://github.com/haohua13/fish-eye-simulator/blob/main/test1.png" width="30%">](https://github.com/haohua13/fish-eye-simulator/assets/57109967/7c25519b-72d6-498c-aea7-c2ae8b2f3873)



