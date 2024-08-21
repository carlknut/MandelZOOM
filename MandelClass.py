import numba as nb
from numba import *
from numba.experimental import jitclass
import numpy as np
import cv2
import colorsys
import time
import math

"""""""""""""""
---Variables---
"""""""""""""""

WIDTH = 1920
HEIGHT = 1080
#W = 600
#H = 400

ITERATIONS = 100
ZOOM_FACTOR = 1/31502649967
TOTAL_FRAMES = 600


"""""""""""""""""
---ZOOM POINTS---
"""""""""""""""""
ZOOM_POINT_1 = complex(-math.e/7,-math.e/20)
ZOOM_POINT_2 = complex(-0.75,0.1)
ZOOM_POINT_3 = complex(-1.249274351,0.060542975) #1/5167898196
ZOOM_POINT_4 = complex(-0.749809928,-0.024218808)

"""""""""""""""
---Equations---
"""""""""""""""
@njit
def e_val(n):
    e = (1+1/n)**n
    return e

@njit
def ease_in_ease_out(x,xf,inc_or_dec):
    if inc_or_dec == 1:
        y = 0.5*(1 - math.cos(math.pi*x/xf) )
    elif inc_or_dec == -1:
        y = 0.5*(1 + math.cos(math.pi*x/xf) )
    else:
        print("ERROR: ease_in_ease_out must input 1 for increase or -1 for decrease")
        return
    return y

@njit
def ease_in_easier_out(x,xf,inc_or_dec,factor):
    if inc_or_dec == 1:
        y = 0.5*(1+math.cos(math.pi*((x-xf)/xf)**factor))
    elif inc_or_dec == -1:
        y = 0.5*(1-math.cos(math.pi*((x-xf)/xf)**factor))
    else:
        print("ERROR: ease_in_ease_out must input 1 for increase or -1 for decrease")
        return
    return y

@njit
def easier_in_ease_out(x,xf,inc_or_dec,factor):
    if inc_or_dec == 1:
        y = 0.5*(1-math.cos(math.pi*((x)/xf)**factor))
    elif inc_or_dec == -1:
        y = 0.5*(1+math.cos(math.pi*((x)/xf)**factor))
    else:
        print("ERROR: ease_in_ease_out must input 1 for increase or -1 for decrease")
        return
    return y

@njit
def cycle_eq(x,X,cycles):
    n = cycles * 2
    equation = (1-math.cos(math.pi/n*x/X))
    return equation

@njit
def slow_down(x,xf):
    y = 1-((x-xf)/xf)**2
    return y


"""""""""""""""
---Main Class---
"""""""""""""""


@jitclass([ ('zoomPoint', complex128),
            ('zoomFactor', float64),
            ('width', int64),
            ('height', int64),
            ('iters', int64),
            ('maxIters', int64),
            ('totalFrames', int64),
            ('colorRange', int32[:]) ])


class Mandel:
    def __init__(self, zoomPoint, zoomFactor, dimensions, iters, maxIters, totalFrames, colorRange):
        self.zoomPoint = zoomPoint
        self.zoomFactor = zoomFactor
        self.width = int(dimensions[0])
        self.height = int(dimensions[1])
        self.iters = iters
        self.maxIters = maxIters
        self.totalFrames = totalFrames
        self.colorRange = colorRange

    def mandelcolor(self, c, ITER, frame):
        color_range = self.colorRange
        color_len = self.colorRange[1] - self.colorRange[0]
        
        z = complex(0)
        done = 0
        for i in range(ITER):
            z = z**2 + c
            if abs(z) > 2:
                hue = i**( 1.2+.8*ease_in_easier_out(frame,self.totalFrames,-1,1) ) / ITER
                val = 255
                
                xf = color_len/2
                hue = hue*180 + 180*cycle_eq(frame,self.totalFrames,2) #+ frame 
                if hue > 180: hue = hue % 180;
                hue = (hue/180 * color_len) + color_range[0]
                val = int(100*(1+math.cos(math.pi*((hue-color_range[0]-xf)/xf)**3)))
                done = 1
            if i == ITER-1:
                hue = ITER
                val = 0
                done = 1
            if done==1:
                sat = 200
                return hue, sat, val

    def mandelbrot(self,xStart,xDist,yStart,yDist,ITER,frame):
        array = np.empty( (self.height, self.width,3), dtype=np.uint8 )
        for x in prange(0,self.width):
            c_r = float(x/self.width) * xDist + xStart
            for y in prange(0,self.height):
                c_i = -( float(y/self.height) * yDist + yStart )
                hue, sat, val = self.mandelcolor(complex(c_r,c_i), ITER, frame)
                color = [hue,sat,val]
                array[y,x] = color
        return array
    
    def mandelzoom(self, frame):
        equation = ease_in_easier_out(frame,self.totalFrames,1,8)
        zoom = 1 - (1-self.zoomFactor) * equation
        #print(zoom)
    
        if frame != self.totalFrames:
            zoom_point_multiplier = equation
            zoom_point = complex(self.zoomPoint.real * zoom_point_multiplier - 0.5*(1-zoom_point_multiplier), self.zoomPoint.imag * zoom_point_multiplier)
            print( zoom_point )
            xDist = 3 * zoom 
            xStart = zoom_point.real - xDist/2
            yDist = 2 * zoom 
            yStart = zoom_point.imag - yDist/2
            ITER = int( self.iters + (self.maxIters-self.iters)*easier_in_ease_out(frame,self.totalFrames,1,4))
            #print(ITER)
        else:
            xDist = 3 - ( (3-self.zoomFactor)*equation)
            xStart = self.zoomPoint.real - xDist/2
            yDist = 2 - ( (2-self.zoomFactor)*equation)
            yStart = self.zoomPoint.imag - yDist/2
            ITER = self.maxIters
        if frame == self.totalFrames - 1:
            print(xDist)

        if frame == 0:
            print("xDist:")
            print(xStart)
            print(yStart)
        array = self.mandelbrot(xStart,xDist,yStart,yDist,ITER,frame)
        return array

    '''
    def mandelanim(self):
        #start_time = time.time()
        for frame in range(self.totalFrames):
            #t_0 = time.time()
            mandel = self.mandelzoom(frame)
            img = cv2.cvtColor(mandel, cv2.COLOR_HSV2RGB)
            cv2.imwrite('C:\\Users\\thorr\\OneDrive\\Desktop\\MandelZoom\\Frames_2\\mandelbrot_'+str(frame)+'.png', img)
            #dt = time.time() - t_0
            #print("Frame " + str(frame) + " -- " + str(dt) + " s"+ " -- ")

        #duration = time.time() - start_time

        #print("Total duration: " + str(duration) + " s")
    '''

#MandelZoom = Mandel(ZOOM_POINT_3,ZOOM_FACTOR)
#print(type(MandelZoom.mandelcolor(complex(0,0),100,100)[0]))

