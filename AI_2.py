import numpy as np
from sklearn.utils import shuffle
import tensorflow as tf
from tensorflow import keras
import os.path



train_samples = np.load('eval_big_x.npy')
train_labels = np.load('eval_big_y.npy')
train_labels, train_samples = shuffle(train_labels, train_samples)

model = keras.models.Sequential()
model.add(keras.Input(shape=(71,)))
model.add(keras.layers.Dense(512))
model.add(keras.layers.LeakyReLU(negative_slope=0.01))
model.add(keras.layers.Dense(256))
model.add(keras.layers.LeakyReLU(negative_slope=0.01))
model.add(keras.layers.Dense(128))
model.add(keras.layers.LeakyReLU(negative_slope=0.01))
model.add(keras.layers.Dense(1)) 

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001), loss='mean_squared_error', metrics=['mse','mae'])

early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True )

model.fit(train_samples, train_labels, validation_split = .02, epochs=30, batch_size=64, shuffle = True, verbose = 2, callbacks=[early_stopping])

if os.path.isfile('models/eval_big_model_v3.keras') is False:
    model.save('models/eval_big_model_v3.keras')
