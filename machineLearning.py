#!usr/bin/python

import combineData
import openfile

import numpy as np


import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers import Conv1D, GlobalMaxPooling1D, Flatten
from keras.optimizers import SGD


# prepare data for training
# input: null
# output: two lists, training data and it's labels
def prepare_training_dataset():
    x_train = []
    y_train = []
    dataDic = openfile.get_train_data()  # to find y_train

    # used to fetch data from memory
    # in order to avoid problems occurred on remote computer, I changed the 'combineData.get_result()' method \
    # so that I can read data from file
    # all_data = combineData.get_result()  # from memory

    all_data = eval(open('result.txt', 'r').read())
    for i in range(len(all_data)):
        # to avoid mathematical problem, I changed label '1' into '0.99'
        y_train.append([int(dataDic[all_data[i]['name']]) > 1 and 0.99 or 0])
        x_train.append(all_data[i]['values'])

    # for some reasons I found some valid data in final dictionary
    # so I find them out and delete it from training data
    x_fore = x_train[:428]
    x_after = x_train[444:]
    y_fore = y_train[:428]
    y_after = y_train[444:]
    x_train = x_fore + x_after
    y_train = y_fore + y_after
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    return x_train, y_train

"""
# just to reduce calculating time  
def prepare_naive_dataset():
    x_train = []
    y_train = []
    dataDic = openfile.get_train_data()  # to find y_train
    all_data = eval(open('result.txt', 'r').read())

    for i in range(len(all_data)):
        y_train.append([int(dataDic[all_data[i]['name']]) > 1 and 0.99 or 0])  # label
        x_train.append(all_data[i]['values'])
    x_fore = x_train[:428]
    x_after = x_train[444:]
    y_fore = y_train[:428]
    y_after = y_train[444:]
    x_train = x_fore + x_after
    y_train = y_fore + y_after
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    return x_train[:100], y_train[:100]
"""


# creating neural network and training
# input: training data and its' label
# output: save well-trained model into file
def train(x_train, y_train):
    """
    In keras, model was created as a queue, \
    in which each node can be treated as a neural network layer contains many neural cells
    My neural network was designed mainly using one dimension convolution method.
    The structure can be described like:
        one dimension convolution layer
        + pooling layer
        + dropout layer
        + full connected layer
        + full connected layer
    """
    model = Sequential()
    """
    In the first layer, no matter what kind of type it is, 
    we have to initialize the network by point out the input shape and some other parameters required 
    """
    model.add(Conv1D(filters=128,
                     kernel_size=10,
                     padding='same',
                     input_shape=(2880, 2),
                     activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dropout(0.25))

    # model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))

    model.add(Dense(1, activation='sigmoid'))

    # model.summary() will print out the detailed structure of your network
    model.summary()

    """
    model.compile() will compile the whole network to check if there is anywhere logically wrong.
    Basically, model.compile() needs two inputs to build the network -- loss function and optimizer.
    Metrices can be used to evaluate the model while training dynamically
    """
    # opt = keras.optimizers.rmsprop(lr=0.001, rho=0.9, epsilon=1e-6)
    # opt = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    # opt = keras.optimizers.adagrad(lr=0.01, epsilon=1e-6)
    opt = keras.optimizers.adam()
    model.compile(loss='binary_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    """
    model.fit() will try to fit data into the model and start the training process.
    During this process, it will check if the shape of your input data could fit the one being required or not.
    Also, we can try to optimize the network by specify other parameters to avoid problems such as overfitting
    """
    model.fit(x_train, y_train,
              batch_size=10,
              epochs=500,
              verbose=1)
    # save the network into file
    # correspondingly we can reload the model using model.load(path)
    model.save('first_model.h5')

if __name__ == '__main__':
    x_train, y_train = prepare_training_dataset()
    # x_train, y_train = prepare_naive_dataset()
    train(x_train, y_train)

