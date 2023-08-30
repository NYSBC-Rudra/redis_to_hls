import cv2
import time
import subprocess as sp 
import glob
import os
from collections import deque
from redis_image_getter import getImage


class ImagetoVideoStreamer():
    def __init__(self) -> None:
        self.img_width = 1224
        self.img_height = 1024
        self.ffmpeg_cmd = 'ffmpeg'
        #making 20 frame buffer
        self.imglist = [None] * 2
        self.fps = 20
        self.command = [self.ffmpeg_cmd,
           '-re',
           '-f', 'rawvideo',  # Apply raw video as input - it's more efficient than encoding each frame to PNG
           '-s', f'{self.img_width}x{self.img_height}',
           '-pixel_format', 'bgr24',
           '-r', f'{self.fps}',
           '-i', '-',
           '-pix_fmt', 'yuv420p',
           '-c:v', 'libx264',
           '-vf', 'scale=640:512',
           '-f', 'hls', '-hls_time', '1', '-hls_list_size', '5', '-hls_flags', 'delete_segments', 'live_server/live.m3u8'
           ]
        self.process = sp.Popen(self.command, stdin=sp.PIPE)
        self.buffer = deque(self.imglist)
        self.fillBuffer()

        self.run()




    def fillBuffer(self):
        for i in range(0,3):
            self.buffer.pop()
            pyimage, self.image_data = getImage()
            self.cv2_image = cv2.cvtColor(self.image_data, cv2.COLOR_RGB2BGR)
            self.buffer.appendleft(self.cv2_image)
    
    def run(self):
        while True:
            current_img = self.buffer.pop() 
            pyimage, self.image_data = getImage()
            self.cv2_image = cv2.cvtColor(self.image_data, cv2.COLOR_RGB2BGR)
            self.buffer.appendleft(self.cv2_image)
            print(type(current_img))
            self.process.stdin.write(current_img.tobytes())  # Write raw frame to stdin pipe.

            #cv2.imshow('current_img', current_img)  # Show image for testing

            time.sleep(1/self.fps)
            #key = cv2.waitKey(int(round(1000/fps)))  # We need to call cv2.waitKey after cv2.imshow

            #if key == 27:  # Press Esc for exit
            #    break
