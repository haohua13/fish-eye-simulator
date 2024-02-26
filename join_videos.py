import cv2
import numpy as np

# concatenate videos
def concat_videos(video1, video2, output):
    # read videos
    cap1 = cv2.VideoCapture(video1)
    cap2 = cv2.VideoCapture(video2)
    # get video properties
    fps = cap1.get(cv2.CAP_PROP_FPS)
    width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # create video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output, fourcc, fps, (width, height))
    # read and write video1
    while cap1.isOpened():
        ret, frame = cap1.read()
        if ret:
            out.write(frame)
        else:
            break
    # read and write video2
    while cap2.isOpened():
        ret, frame = cap2.read()
        if ret:
            out.write(frame)
        else:
            break
    # release resources
    cap1.release()
    cap2.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video1 = "video1.mp4"
    video2 = "video2.mp4"
    output = "output.mp4"
    concat_videos(video1, video2, output)
