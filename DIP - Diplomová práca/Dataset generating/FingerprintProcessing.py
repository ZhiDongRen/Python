import os
from PIL import Image
import PIL
from random import seed
from random import randint
import numpy as np
from matplotlib import pyplot as plt
from scipy.misc import toimage
import math

#width and height of image
width = 256
height = 400

#function for inserting warts to image
wartsDirectory="warts"
def insertWart(image):
    seed(2)
    #random wart is choosen from directory
    rand = np.random.randint(1, 40)
    #placed to random position(x,y)
    x = np.random.randint(20, 160)
    y = np.random.randint(20, 310)
    wart = Image.open(wartsDirectory+"\\" + rand.__str__() + ".png").convert("RGBA")
    #paste wart to image
    newImage = image.copy()
    newImage.paste(wart, (x, y), wart)
    return newImage

#function for removing third channel from image
#only grayscale images can be used (8bit)
def removeThirdChannel(image):
    global height
    global width
    newImage=np.zeros((height, width))
    for i in range (height):
        for j in range (width):
            newImage[i][j]=image[i][j][0]
    return newImage

#function for processing fingerprint
i=1
#directory of original warts
fingerprintDirectory= "fpingerprints"
#number of warts to insert
numberOfWarts=10
for filename in os.listdir(fingerprintDirectory):
    #remowing third channel and resizing image
    image = Image.open(fingerprintDirectory+"\\"+i.__str__()+".jpg").convert("RGBA")
    image = image.resize((width, height))
    image = np.asarray(image)
    image = removeThirdChannel(image)
    image=toimage(image)

    #save original fingerprint without damage
    pure=os.getcwd()+"\\pure\\"+(i).__str__()+".png"
    image.save(pure,dpi=(500,500))

    #insert warts
    for j in range(numberOfWarts):
        image=insertWart(image)

    #sawe damaged fingerprint
    damaged=os.getcwd()+"\\damaged\\"+(i).__str__()+".png"
    image.save(damaged,dpi=(500,500))
    print("Image: "+i.__str__()+" processed")
    i+=1


