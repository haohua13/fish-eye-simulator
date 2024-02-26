import cv2
import os

def images_to_video(image_folder, video_name, fps = 30, video_format = 'DIVX'):
    # Get the list of image files in the directory in sorted order
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images = sorted(images, key=lambda x: int(x.split('.')[0]))

    # Get image dimensions to set the video size
    img = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, _ = img.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*video_format)
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    # Iterate through the images and write them to the video
    for image in images:
        frame = cv2.imread(os.path.join(image_folder, image))
        video.write(frame)

    # Release the video writer
    video.release()

# Example usage:
current_directory = os.getcwd()  # Get current directory
images_directory = os.path.join(current_directory, 'images')  # Assuming images are in 'images' subdirectory
output_video_path = os.path.join(current_directory, 'project.mp4')
images_to_video(images_directory, output_video_path)