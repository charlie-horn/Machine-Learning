import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
import math

def sigmoid(x):
	return 1/(1 + np.exp(-x))

def softmax(x):
	expX = np.exp(x)
	return expX / expX.sum(axis=1, keepdims=True)

def relu(x):
	if x<0:
		return 0
	else:
		return x

def cost(T,Y):
  return -(T*np.log(Y)).sum()

#weight = weight - learning_rate*gradient

def forward(X, W1, W2):
  Z = sigmoid(X.dot(W1))
  Y = softmax(Z.dot(W2))
  return Y,Z

def grad_W2(Z,T,Y):
  return Z.T.dot(Y - T)

def grad_W1(X,Z,T,Y,W2):
  return X.T.dot(((Y - T).dot(W2.T)*(Z*(1 - Z))))


#x_train is 60000 samples, 28x28 pixel images
#y_train is the 60000 targets, with values 0-9
#x_test is 10000 samples
(x_train, y_train), (x_test, y_test) = mnist.load_data()
num_pixels = x_train.shape[1] * x_train.shape[2]

#Flatten into Nx784 arrays
x_train = x_train.reshape(x_train.shape[0], num_pixels).astype('float32')
x_test = x_test.reshape(x_test.shape[0], num_pixels).astype('float32')

#Normalize pixel intensity values
x_train = x_train / 255
x_test = x_test / 255

#Transform y into index vectors
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]



# M is the size of hidden layer
# K is the number of classes
# D is the size of a sample
D = num_pixels
K = num_classes
M = D


# Instantiate Weights
W1 = np.random.randn(D,M)
W2 = np.random.randn(M,K)

Z = sigmoid(x_train.dot(W1))
Y = softmax(Z.dot(W2))

#Training

epochs = 10
learning_rate = 0.0000000001
C = 0

while(not math.isnan(C)):
    for i in range(epochs):
        Y, Z = forward(x_train, W1, W2)
        W2 -= learning_rate*grad_W2(Z, y_train, Y)
        W1 -= learning_rate*grad_W1(x_train, Z, y_train, Y, W2)
        C = cost(y_train, Y)
        print(C)
    learning_rate = learning_rate*10
    print("New rate : " + string(learning_rate))
