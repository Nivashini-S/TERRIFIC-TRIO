from collections import deque
from imutils import *
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import time
import testquadrant
import csv

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
args = vars(ap.parse_args())
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])
if not args.get("video", False):
	vs = VideoStream(src=0).start()
else:
	vs = cv2.VideoCapture(args["video"])
time.sleep(2.0)
st=0
et=0
ttime=0
c=0
r=open("results.csv","w")
r1 = csv.writer(r, delimiter=',')        
r1.writerow(['bounce_number', 'time_of_bounce','quadrant_of_bounce'])
sno=0
qd=""
while True:        
	frame = vs.read()
	st=time.time()#start time
	frame = frame[1] if args.get("video", False) else frame
	if frame is None:
		break	
	frame = resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)	
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)	
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = grab_contours(cnts)
	center = None		
	if len(cnts) > 0:		
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)		
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))		
		if radius > 10:			
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)						
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
		qd=testquadrant.test(x,y)		
	pts.appendleft(center)	
	et=time.time()#end time
	ttime=et-st #total time       
	for i in range(1, len(pts)):		
		if pts[i - 1] is None or pts[i] is None:
			continue		
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF	
	if key == ord("q"):
		break	
	if(ttime):    
                sno=sno+1
                r1.writerow([sno,ttime,qd])                
r.close()
if not args.get("video", False):
	vs.stop()
else:
	vs.release()
cv2.destroyAllWindows()


'''
In Command Prompt:
        To Run :  python testball.py --video Hackathon-video.mov
'''
