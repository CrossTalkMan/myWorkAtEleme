from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers import Conv1D, MaxPooling1D, Flatten
from keras.optimizers import SGD

import keras
import numpy as np
import random

x_total = []
y_total = []
for i in range(1500):
    # training dataset structure is a list of (x, y), representing coordinate
    x_total.append([(random.uniform(-1, 1), random.uniform(-1, 1)) for i in range(50)])
    tmp = 0
    for j in range(len(x_total[i])):
        tmp += (x_total[i][j][0]**2 + x_total[i][j][1]**2) ** 0.5
    y_total.append([tmp > 37.5 and 1 or 0])

x_train, y_train = x_total[:1000], y_total[:1000]
x_test, y_test = x_total[1000:], y_total[1000:]

print(x_train[0])

x_train = np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test = np.array(y_test)


model = Sequential()

model.add(Conv1D(input_shape=(50, 2),
                 filters=32,
                 kernel_size=5,
                 padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=2))

model.add(Flatten())

model.add(Dense(16))
model.add(Activation('tanh'))

model.add(Dense(1, activation='sigmoid'))

model.summary()
sgd = SGD(lr=0.1)
opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)
model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=2,
          epochs=500)

score = model.evaluate(x_test, y_test)
print('\n', score)
