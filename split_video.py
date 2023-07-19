import cv2
import os
from pathlib import Path
import time
from tqdm import tqdm

#Set minimum frame diference parameter
diff_thresh = 3.5

# Define the path to the directory
main_dir = "VideoFrames/"
video_path = "/Users/ilyapetrov/Desktop/Biz/Neuronflo/Software/Videos_Images/Tenneco_1st_batch/VID_5_goggle_ok_shoe_ok.mp4"
video_name = video_path.rsplit('/',1)[1]
video_name = video_name.split(".")[0]
output_path = main_dir + video_name + "/"

print("Output path: ", output_path)

# Check if the directory exists
Path(output_path).mkdir(parents=True, exist_ok=True)

if os.path.exists(output_path) and os.path.isdir(output_path):
    if len(os.listdir(output_path)) > 0:
        print("Output directory is not empty.")
        answer = input("Clear the directory? (Y/N) ")
        if answer.upper() == 'Y':
            for filename in os.listdir(output_path):
                file_path = os.path.join(output_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
        else:
            print("Aborted.")
            exit()

# Open the video file
cap = cv2.VideoCapture(video_path)

# Get the total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f'The video has {total_frames} frames.')

# Prompt the user to continue
while True:
    proceed = input('Do you want to continue? (Y/N) ').upper()
    if proceed == 'Y':
        break 
    elif proceed == 'N':
        cap.release()
        exit()
    else:
        print('Please enter Y or N.')

# Initialize the frame counter
frame_count = 0
save_cnt = 0


# Initialize the previous frame
prev_frame = None

# Loop through the frames
# while cap.isOpened():
for frame_number in tqdm(range(total_frames)):
    # Read a frame from the video
    ret, frame = cap.read()

    # If the frame is read correctly, process it
    if ret:
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # If this is not the first frame, compare it to the previous frame
        if prev_frame is not None:
            # Compute the absolute difference between the frames
            diff = cv2.absdiff(gray, prev_frame)

            # Compute the mean value of the difference
            # frame_test_count += 1
            mean_diff = diff.mean()
            # print(f"mean difference for {frame_test_count} is {mean_diff}")

            # # Save the frame if it is different from the previous frame
            # if mean_diff > diff_thresh:
            #     frame_count += 1
            #     filename = f'frame_{frame_count:04d}.jpg'
            #     cv2.imwrite(output_path+filename, frame)
            # Save the frame if it is different from the previous frame
            if mean_diff > diff_thresh:
                frame_count += 1
                if frame_count % 2 == 1:  # save only odd numbered frames
                    save_cnt +=1
                    filename = f'frame_{save_cnt:04d}.jpg'
                    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                    cv2.imwrite(output_path+filename, frame)


        # Store the current frame as the previous frame for the next iteration
        prev_frame = gray.copy()


        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

print(f"Saved {save_cnt} different frames")
# Release the resources
cap.release()
cv2.destroyAllWindows()
