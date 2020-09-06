from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from PIL import Image, ImageDraw, ImageFilter
import os
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Dropout
from keras.models import Model
import keras
import numpy
from matplotlib import pyplot
from scipy.misc import toimage

class MainWindow():
    def __init__(self, main):
        #index of current weights from array
        self.weightsIndex = 0
        #array of pretrained weights for neural net
        self.weightsArray = []

        #################################################LABELS

        self.lbl1 = Label(main, text="Damaged")
        self.lbl1.place(relx=0.23, rely=0.03, anchor='nw')

        self.lbl2 = Label(main, text="Reconstructed")
        self.lbl2.place(relx=0.69, rely=0.03, anchor='nw')

        #################################################CANVASES

        self.canvas1 = Canvas(main,width=256, height=400, bg='white')
        self.canvas1.place(relx=0.11, rely=0.1, anchor='nw')

        self.canvas2 = Canvas(main,width=256, height=400, bg='white')
        self.canvas2.place(relx=0.57, rely=0.1, anchor='nw')


        #################################################BUTTONS
        self.btn0 = Button(main, text="Reconstruct wart", command=self.onButtonReconstruct)
        self.btn0.place(relx=0.44, rely=0.4, anchor='nw')

        self.btn1 = Button(main, text="Load image", command=self.onButtonLoad)
        self.btn1.place(relx=0.23, rely=0.85, anchor='nw')

        self.btn2 = Button(main, text="Save image", command=self.onButtonSave)
        self.btn2.place(relx=0.695, rely=0.85, anchor='nw')

        self.btn7 = Button(main, text="View original", command=self.onButtonViewOriginal)
        self.btn7.place(relx=0.452, rely=0.76, anchor='nw')

        #Class of fingerprints(master fingerprints(1x,6x,10x,imressions)
        #in different directories
        self.CLASS=0

        # for reconstructing the image again
        self.newImageToReconstruct = False
        self.reconstructedImage = []

    #----------------

    def setCanvas(self,image):
        #set image of canvas
        temp = ImageTk.PhotoImage(image)
        self.canvas2.create_image(0, 0, image=temp, anchor=NW)

    def onButtonViewOriginal(self):
        #get filename of reconstructed fingerprint
        head, tail = os.path.split(self.filename1)
        filename, file_extension = os.path.splitext(tail)

        #get path of original fingerprint
        original = Image.open(os.getcwd()+"\\"+self.CLASS + "\\pure\\" + filename + ".png")
        original = original.resize((256, 400))
        original = numpy.asarray(original)

        #show original fingerprint
        pyplot.figure(figsize=(5.1, 5.1))
        pyplot.imshow(original, cmap='gray')
        pyplot.show()

    def onButtonLoad(self):
        #select file
        self.filename1 = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                    title="Select file",
                                                    filetypes=(("all files", "*.*"), ("jpeg files", "*.jpg"),
                                                               ("png files", "*.png")))
        #get fingerprint class
        tmp=self.filename1.split("/")
        self.CLASS=tmp[-3]

        #show fingerprint
        self.image1 = ImageTk.PhotoImage(Image.open(self.filename1))
        self.canvas1.create_image(0, 0, image=self.image1, anchor=NW)

        #set weights index to zero
        self.weightsIndex=0
        #load weights
        path=os.getcwd()+"\\"+self.CLASS+"\\weights\\"
        self.weightsArray=[path+"weights1.hdf5",path+"weights2.hdf5",path+"weights3.hdf5",]

        #set reconstructing of new loaded image
        self.newImageToReconstruct=True


    def onButtonSave(self):
        #select filename
        self.filename2 = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                                    title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        #save fingerprint
        self.reconstructedImage.save(self.filename2+".jpg")


    def onButtonReconstruct(self,):
        images=[]

        #If image was loaded first time, reconstruct that image
        #else reconstruct the same image again
        if(self.newImageToReconstruct):
            self.imageToReconstruct=(Image.open(self.filename1))
            self.newImageToReconstruct=False
        else:
            self.imageToReconstruct=self.reconstructedImage

        #prepare image for neural net (normalize image pixels to <0,1> values
        self.imageToReconstruct = numpy.asarray(self.imageToReconstruct)
        self.imageToReconstruct = self.imageToReconstruct.astype('float32')
        images.append(self.imageToReconstruct)
        arr = numpy.array(images)
        arr = arr.reshape(-1, 400, 256, 1)
        arr = arr / (255.0)

        #neural net
        input = Input(shape=(400, 256, 1))
        x = Conv2D(32, (3, 3), activation='relu', padding='same')(input)
        x = MaxPooling2D((2, 2), padding='same')(x)
        x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = MaxPooling2D((2, 2), padding='same')(x)
        x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = MaxPooling2D((2, 2), padding='same')(x)

        x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = UpSampling2D((2, 2))(x)
        x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = UpSampling2D((2, 2))(x)
        x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
        x = UpSampling2D((2, 2))(x)
        decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

        #compile neurel net model
        autoencoder = Model(input, decoded)
        autoencoder.compile(loss='mean_squared_error', optimizer=keras.optimizers.RMSprop())

        #load next weight from weights array
        autoencoder.load_weights(self.weightsArray[self.weightsIndex])
        if(self.weightsIndex!=2):
            self.weightsIndex+=1

        #reconstruct image
        prediction = autoencoder.predict(arr)
        image = numpy.reshape(prediction[0], (400, 256))
        self.reconstructedImage=toimage(image)

        #show image in canvas
        self.image2 = ImageTk.PhotoImage(self.reconstructedImage)
        self.canvas2.create_image(0, 0, image=self.image2, anchor=NW)

#----------------------------------------------------------------------
#run main window of application
root = Tk()
root.title("Fingerprint reconstruction")
root.geometry('800x550')
MainWindow(root)
root.mainloop()