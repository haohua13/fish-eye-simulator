import cv2
import os

# concatenate videos
def concat_videos(video_files, output):
    if not video_files:
        raise ValueError("No video files provided")

    # initialize the first video to get properties
    cap = cv2.VideoCapture(video_files[0])
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    # create video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output, fourcc, fps, (width, height))

    # read and write each video file
    for video in video_files:
        cap = cv2.VideoCapture(video)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                break
        cap.release()

    # release resources
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_folder = r'C:\Users\haohu\OneDrive\Imagens\Digital\Videos'
    output = "video_output.avi"

    # get all .AVI files in the folder
    video_files = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.lower().endswith('.avi')]
    video_files.sort()  # sort the files if needed

    concat_videos(video_files, output)
    print("Video concatenation completed successfully")