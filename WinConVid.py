# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 21:12:33 2020

@author: lefin
"""

import cv2
import time

finish = [False]

def camVid():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.flip(gray, 1)
    for _  in range(100):
        finish[0] = False
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.flip(gray, 1)
        cv2.imwrite('temp.jpg',gray)
        finish[0] = True
        time.sleep(0.1)
        #cv2.imshow('a', gray)
        # Display the resulting frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

#camVid()