from PIL import Image
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from matplotlib import pyplot
from keras.layers import Input,Conv2D,MaxPooling2D,UpSampling2D,Dropout
from keras.models import Model
import keras
import numpy
from scipy.misc import toimage
import sklearn
import os

#learning on graphic card
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

#image resolution, X(width), Y(height)
X=256
Y=400

#function for preparing images to training
def read_images(path,ext):
    global X
    global Y
    #array of processed images
    images = []

    i=1
    for filename in os.listdir(path):
        image = Image.open(path+i.__str__()+ext)
        image = image.resize((X,Y))
        image = numpy.asarray(image)
        #append image to array
        image = image.astype('float32')
        images.append(image)
        i+=1

    #reshape array to suitable form for training
    images = numpy.array(images)
    print(images.shape)
    images = images.reshape(-1, Y, X, 1)
    images = images / (255.0)
    return images


#function for saving predicted images
def save(images):
    print('saving')
    for i in range(len(images)):
        image = numpy.reshape(images[i], (Y, X))
        image =toimage(image)
        image.save(os.getcwd()+"\predicted\\"+(i+1).__str__()+ ".png",dpi=(500,500))

####################################################################
#read images from folders
print("start")
pure=read_images('pure/',".png")
damaged=read_images('damaged/',".png")
print("images loaded")

#split images to training and validation setst
train_x,valid_x,train_y,valid_y = sklearn.model_selection.train_test_split(damaged,pure,test_size=0.2,shuffle=True)
#####################################################################
#training parameters
batch =21
epochs = 300
input = Input(shape = (Y, X, 1))
def autoencoder(input):
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(input)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Dropout(0.35)(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)

    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Dropout(0.35)(x)
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(32, (3, 3), activation='relu',padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)
    return decoded
########################################################################
#compile model
autoencoder = Model(input, autoencoder(input))
autoencoder.compile(loss='mean_squared_error', optimizer = keras.optimizers.RMSprop())
#load weights for net
#autoencoder.load_weights('weights.hdf5')

#save weights of best epochs
filepath = "weights/saved-model-{epoch:02d}-{val_loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='auto',period=1,save_weights_only=True)
autoencoder.summary()
#training
trained_model = autoencoder.fit(train_x, train_y, batch_size=batch,epochs=epochs,callbacks=[checkpoint],validation_data=(valid_x, valid_y))
#########################################################################
#plot loss function
printLoss=True
#printLoss=False
if(printLoss):
    validation = trained_model.history['val_loss']
    training = trained_model.history['loss']
    n_epochs = len(trained_model.history['loss'])
    epochs = range(n_epochs)

    pyplot.figure()
    pyplot.plot(epochs, validation, 'b', label='Validačná sada')
    pyplot.plot(epochs, training, 'r', label='Trénovacia sada')
    pyplot.title('Priebeh loss funkcií')
    pyplot.legend()
    pyplot.show()

#########################################################################
#save trained weights to file
autoencoder.save_weights('weights.hdf5')
#try to reconstruct images
print('reconstructing')
#print(len(damaged[damagedLen]))
predicted=autoencoder.predict(damaged)
#save images
save(predicted)
#show results of prediction
showResults()