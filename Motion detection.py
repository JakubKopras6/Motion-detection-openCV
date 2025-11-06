# Webcam Motion Detector (Optimized + Adjustable Sensitivity)

import cv2
import pandas as pd
from datetime import datetime

# Initialize variables
static_back = None
motion_list = [None, None]
motion_times = []
motion_records = []

# Start video capture
video = cv2.VideoCapture(0)

# --- Create window and trackbar for threshold ---
cv2.namedWindow("Threshold Frame")
cv2.createTrackbar("Threshold", "Threshold Frame", 45, 255, lambda x: None)  # Default 45


while True:
    check, frame = video.read()
    if not check:
        break

    motion = 0

    # Convert to grayscale and blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Set initial background
    if static_back is None:
        static_back = gray
        continue

    # Get current threshold value from trackbar
    thresh_value = cv2.getTrackbarPos("Threshold", "Threshold Frame")

    # Compute difference between background and current frame
    diff_frame = cv2.absdiff(static_back, gray)

    # Apply threshold using the adjustable value
    thresh_frame = cv2.threshold(diff_frame, thresh_value, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Find contours
    cnts, _ = cv2.findContours(thresh_frame.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 5000:
            continue
        motion = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    motion_list.append(motion)
    motion_list = motion_list[-2:]

    # Record motion start time
    if motion_list[-1] == 1 and motion_list[-2] == 0:
        motion_times.append(datetime.now())

    # Record motion end time
    if motion_list[-1] == 0 and motion_list[-2] == 1:
        motion_times.append(datetime.now())

    # Display frames
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        if motion == 1:
            motion_times.append(datetime.now())
        break

    # Smoothly update background to adapt to lighting changes
    static_back = cv2.addWeighted(static_back, 0.97, gray, 0.03, 0)


# Save motion times to CSV
for i in range(0, len(motion_times), 2):
    if i + 1 < len(motion_times):
        motion_records.append({"Start": motion_times[i], "End": motion_times[i + 1]})

df = pd.DataFrame(motion_records)
df.to_csv("Time_of_movements.csv", index=False)

video.release()
cv2.destroyAllWindows()


