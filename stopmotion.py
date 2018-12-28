# doel: script dat door op 'j' te drukken een volgend plaatje opslaat en door op 'l' te drukken een plaatje terug gaat
# als je op 'k' drukt toggled het programma tussen laatste tien plaatjes loopen en overlap tussen vorig plaatje en huidige camera

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import time

def getnum(string):
    return int(str(string).split('_')[-1].split('.')[0])

def get_last_n_images(n):
    p = Path('.')
    pathlist = p.glob('*.jpg')
    pathlist = list(pathlist)
    pathlist.sort(key=getnum)
    if len(pathlist) > n:
        return pathlist[-n:]
    else:
        return pathlist

def get_last_iterator(im_list):
    return int(str(im_list[-1]).split("_")[-1].split('.')[0])

def show_single_im(path, frame_duration=0.5):
    img = cv2.imread(str(path))
    cv2.imshow('image',img)
    cv2.waitKey(int(frame_duration*1000))

def get_single_image(channel=0):
    img_counter = 0
    cam = cv2.VideoCapture(channel)
    while True:
        ret, frame = cam.read()
        cv2.imshow("image", frame)
        cv2.waitKey(1)
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC to break
            break
        elif k%256 == 32:
            # 'SPACE'; save image, update img_counter and update im_list
            img_name = "filmpje_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            img_counter += 1
            play_sound()
            break
    cam.release()

def play_sound(duration=0.1, freq = 440):
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' %(duration, freq))

def run_last_n_images_with_camframe(n, frame_duration=0.5, channel=0):
    """
    plays last n images 
    """
    im_list = get_last_n_images(n)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    if im_list == []:
        get_single_image()
    im_list = get_last_n_images(n)
    img_counter = get_last_iterator(im_list)
    while True:
        cam = cv2.VideoCapture(channel)
#         cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
#         cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280);
#         cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720);
        for path in im_list:
            show_single_im(path, frame_duration)
        cam.grab()
        retval, frame = cam.retrieve(0)
        cv2.imshow('image', frame)
        cv2.waitKey(int(frame_duration*1000))
        cam.release()
        k = cv2.waitKey(30)
        if k%265 == 27:
            # ESC to break
            break
        elif k%265 == 32:
            # 'SPACE'; save new image, update img_counter and update im_list
            play_sound()
            img_name = "filmpje_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            img_counter += 1
            im_list = get_last_n_images(n)
            time.sleep(0.5)
        elif k%265 == 106:
            # 'j'; remove last image, update img_counter and update im_list
            remove = im_list[-1]
            os.remove(remove)
            play_sound(0.1, 800)
            img_counter -= 1
            im_list = get_last_n_images(n)
    cv2.destroyAllWindows()

run_last_n_images_with_camframe(10, 0.1)