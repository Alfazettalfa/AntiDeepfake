import cv2
import numpy as np
import matplotlib.pyplot as plt

images = []

cap = cv2.VideoCapture("Video/testvideo.mp4")
while not cap.isOpened():
    cap = cv2.VideoCapture("Video/testvideo.mp4")
    cv2.waitKey(1000)
    print("Wait for the header")

print("ok")
pos_frame = cap.get(1)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cnt = 0
_ = True
while _:
    img = cap.grab()
    _, img = cap.retrieve()
    print(cnt/total_frames)
    cnt += 1
    """""
    frame_ready, frame = cap.read()  # get the frame
    if frame_ready: # The frame is ready and already captured
        print(100 * pos_frame/total_frames)
        #images.append(frame)
        pos_frame = cap.get(1)
    else:
        # The next frame is not ready, so we try to read it again
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame - 1)
        print("frame is not ready")
        # It is better to wait for a while for the next frame to be ready
        cv2.waitKey(1000)
    if cv2.waitKey(10) == 27:
        break
    if cap.get(1) == total_frames:
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        break
        """

all_frames = np.array(images)
plt.imshow(all_frames[10])
plt.show()