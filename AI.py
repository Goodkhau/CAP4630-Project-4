import numpy as np
from sklearn.utils import shuffle
import tensorflow as tf
from tensorflow import keras
import os.path



train_samples = np.load('mate_x.npy')
train_labels = np.load('mate_y.npy')
train_labels, train_samples = shuffle(train_labels, train_samples)

model = keras.models.Sequential()
model.add(keras.Input(shape=(71,)))
model.add(keras.layers.Dense(512))
model.add(keras.layers.LeakyReLU(negative_slope=0.01))
model.add(keras.layers.Dense(256))
model.add(keras.layers.LeakyReLU(negative_slope=0.01))
model.add(keras.layers.Dense(128))
model.add(keras.layers.LeakyReLU(negative_slope=0.01))
model.add(keras.layers.Dense(3, activation="softmax"))

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(train_samples, train_labels, validation_split = .1, epochs=10, batch_size=64, shuffle = True, verbose = 2)

if os.path.isfile('models/mate_model.keras') is False:
    model.save('models/mate_model.keras')


