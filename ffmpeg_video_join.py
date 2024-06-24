import os
import subprocess

def create_file_list(video_folder, file_list_path):
    video_files = [f for f in os.listdir(video_folder) if f.lower().endswith('.avi')]
    video_files.sort()  # sort the files if needed

    with open(file_list_path, 'w') as file_list:
        for video_file in video_files:
            file_list.write(f"file '{os.path.join(video_folder, video_file)}'\n")

def concat_videos_ffmpeg(file_list_path, output):
    command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', file_list_path, '-c', 'copy', output]
    subprocess.run(command)

if __name__ == "__main__":
    video_folder = r'C:\Users\haohu\OneDrive\Imagens\Digital\Videos'
    file_list_path = "file_list.txt"
    output = "video_output_with_sound.avi"

    create_file_list(video_folder, file_list_path)
    concat_videos_ffmpeg(file_list_path, output)
    print("Video concatenation completed successfully")