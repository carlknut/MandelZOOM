from MandelClass import Mandel
from numba import jit, prange
import cv2
import time

"""""""""""""""""
---ZOOM POINTS---
"""""""""""""""""
#ZOOM_POINT_1 = complex(-math.e/7,-math.e/20)
ZOOM_POINT_2 = complex(-0.75,0.1)
ZOOM_POINT_3 = complex(-1.249274351,0.060542975) #1/31502649967
ZOOM_POINT_4 = complex(-0.749809928,-0.024218808)
ZOOM_POINT_5 = complex(-1.786059972,0.000208514) #1/9733047.1368 #great spot for blooming
ZOOM_POINT_6 = complex(-0.239716191,0.845503313) #1.5768819.076489

ZOOM_FACTOR = 1/1574597.28239619

INITIAL_ITERS = 100
MAX_ITERS = 750
dimensions = (920,540) #(920,540)
TOTAL_FRAMES = 300#1500
STARTING_FRAME = 0#1230#247


@jit(parallel=True)
def mandelanim(zoomPoint,zoomFactor):
    mandelZoom = Mandel(zoomPoint,zoomFactor,dimensions=dimensions,iters=INITIAL_ITERS,maxIters=MAX_ITERS,totalFrames=TOTAL_FRAMES)
    for frame in prange(TOTAL_FRAMES):
        #t_0 = time.time()
        frame += STARTING_FRAME
        mandel = mandelZoom.mandelzoom(frame)
        img = cv2.cvtColor(mandel, cv2.COLOR_HSV2RGB)
        cv2.imwrite('C:\\Users\\thorr\\OneDrive\\Desktop\\MandelZoom\\MZF9_Frames\\mandelbrot_'+str(frame)+'.png', img)
        if frame == TOTAL_FRAMES: return;
        #dt = time.time() - t_0
        #print("Frame " + str(frame) + " -- " + str(dt) + " s"+ " -- ")

def mandelPic(zoomPoint,zoomFactor,totalFrames):
    mandelZoom = Mandel(zoomPoint,zoomFactor, maxIters=MAX_ITERS, totalFrames=totalFrames)
    mandel = mandelZoom.mandelzoom(totalFrames-1)
    img = cv2.cvtColor(mandel, cv2.COLOR_HSV2RGB)
    name = "zoom_" + str(zoomPoint.real) + "+" + str(zoomPoint.imag) + "i_" + str(zoomFactor) + ".png"
    cv2.imwrite(name, img)

def main():
    start_time = time.time()
    mandelanim(ZOOM_POINT_6,ZOOM_FACTOR)
    #mandelPic(ZOOM_POINT_5, ZOOM_FACTOR, 300)
    duration = time.time() - start_time
    print("Total duration: " + str(duration) + " s")

main()
