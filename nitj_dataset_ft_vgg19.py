# -*- coding: utf-8 -*-
"""NITJ_Dataset_FT_VGG19.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qpC9uZhoKZpZbSDGxLgCZYaAqkYcbC_V
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense,Conv2D,MaxPooling2D,Flatten,BatchNormalization,Dropout

from google.colab import drive
drive.mount('/drive')

test_path='/drive/MyDrive/Spliting of data (full sized Images)/test'
train_path='/drive/MyDrive/Spliting of data (full sized Images)/train'
val_path='/drive/MyDrive/Spliting of data (full sized Images)/val'

from keras.applications.vgg19 import VGG19
conv_base = VGG19(
    weights='imagenet',
    include_top = False,
    input_shape=(150,150,3)
)

conv_base.summary()

conv_base.trainable = True

set_trainable = False

for layer in conv_base.layers:
  if layer.name == 'block5_conv1':
    set_trainable = True
  if set_trainable:
    layer.trainable = True
  else:
    layer.trainable = False

for layer in conv_base.layers:
  print(layer.name,layer.trainable)

model = Sequential()

model.add(conv_base)
model.add(Flatten())
model.add(Dense(4096,activation='relu'))
model.add(Dense(36,activation='softmax'))

model.summary()

# generators
train_ds = keras.utils.image_dataset_from_directory(
    directory = train_path,
    batch_size=32,
    image_size=(150,150)
)

validation_ds = keras.utils.image_dataset_from_directory(
    directory = val_path,
    batch_size=32,
    image_size=(150,150)
)

# Normalize
def process(image,label):
    image = tf.cast(image/255. ,tf.float32)
    return image,label

train_ds = train_ds.map(process)
validation_ds = validation_ds.map(process)

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

from tensorflow.keras.callbacks import EarlyStopping
callback = EarlyStopping(
    monitor="val_loss",
    min_delta=0.0001,
    patience=10,
    verbose=1,
    mode="auto",
    baseline=None,
    restore_best_weights=False
)

history = model.fit(train_ds,epochs=100,validation_data=validation_ds,callbacks=callback)

test_ds = keras.utils.image_dataset_from_directory(
    directory = test_path,
    batch_size=32,
    image_size=(150,150)
)

test_ds = test_ds.map(process)

loss, accuracy = model.evaluate(test_ds, verbose=1)
print('Test loss:', loss)
print('Test accuracy:', accuracy)

import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='Validation')
plt.legend()
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Accuracy Plot of ResNet50')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train' , 'Val'], loc ='lower right')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss Plot of ResNet50')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train' , 'Val'], loc ='upper left')
plt.show()
