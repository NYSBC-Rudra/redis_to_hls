import cv2

vcap = cv2.VideoCapture("http://localhost:8000/live.m3u8")

while(1):
     ret, frame = vcap.read()
     cv2.imshow('VIDEO', frame)
     cv2.waitKey(25)
