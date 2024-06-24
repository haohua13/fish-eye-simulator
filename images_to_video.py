import cv2
import os

def images_to_video(image_folder, video_name, fps=10, video_format='DIVX'):
    # get the list of image files in the directory in sorted order
    images = [img for img in os.listdir(image_folder) if img.lower().endswith(".jpg")]
    if not images:
        raise ValueError("No images found in the directory")
    
    images = sorted(images, key=lambda x: int(''.join(filter(str.isdigit, x))))

    # get image dimensions to set the video size
    img = cv2.imread(os.path.join(image_folder, images[0]))
    if img is None:
        raise ValueError("The first image could not be read")
    height, width, _ = img.shape

    # define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*video_format)
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    # iterate through the images and write them to the video
    for image in images:
        frame = cv2.imread(os.path.join(image_folder, image))
        if frame is None:
            print(f"Warning: Skipping image {image} as it could not be read")
            continue
        video.write(frame)

    # release the video writer
    video.release()


if __name__ == '__main__':
    current_directory = os.getcwd()  # get current directory
    images_directory = r'C:\Users\haohu\OneDrive\Imagens\Digital\Favoritos-24-06-2024'  # raw string to handle backslashes

    output_video_path = os.path.join(current_directory, 'video_insta_10fps.mp4')
    images_to_video(images_directory, output_video_path)
    print("Video created successfully")