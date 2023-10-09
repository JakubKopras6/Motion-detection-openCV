# Motion-detection-openCV
This script captures video from a webcam, detects motion, records the start and end times of the detected motion, and saves this information to a CSV file. It's a simple example of motion detection using computer vision techniques. 

An infinite loop captures frames from the webcam and performs the following operations on each frame:
Convert the color image to grayscale.
Apply GaussianBlur to the grayscale image.
Compute the absolute difference between the static background and the current frame.
Threshold the difference frame to identify regions of significant change.
Find contours in the thresholded frame to identify moving objects.
If the area of a contour exceeds a certain threshold, a green rectangle is drawn around the moving object.
Status of motion is updated in the motion_list.
Start and end times of motion are recorded in the time list.

To exit program press q.
