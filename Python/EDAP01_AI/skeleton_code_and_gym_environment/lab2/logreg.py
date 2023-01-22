import csv
import random
import numpy as np
import matplotlib.pyplot as plt

def libsvm_reader(file):
	f = open(file,'r')
	arr = []
	lines = f.readlines()

	for line in lines:
		s = line.split(" ")
		l = [float(s[0])]
		for i in range(len(s[1:])):
			l.append(float(s[i + 1].split(":")[1]))
		arr.append(l)
	return np.array(arr)


#Normalize
data = libsvm_reader("libsvm")
datamean = data[:,1:].mean(axis=0)
data[:,1:] = data[:,1:] - datamean
datascale = np.abs(data).max(axis=0)
data /= datascale

data = np.concatenate((data,np.ones((len(data),1))), axis=1)

#sigmoid function
def sigmoid(x):
	return 1/(1 + np.exp(-x))

sig = np.vectorize(sigmoid)

#Logistic regression
def logreg(data, w, out, learning_rate):
	indx = list(range(out))
	indx.extend(list(range(out + 1, 30)))
	x = data[indx,1:]
	y = np.transpose(np.array([data[indx,0]]))
	m = len(x)
	
	for epoch in range(1000):
			y_pred = sig(np.matmul(x, w))

			e = y_pred - y
			grad = np.dot(e.T, x)
			w -= learning_rate*grad.T

			#cost function
			cost = -(np.dot(y.T,np.log(y_pred)) + np.dot((1-y).T,np.log(1 - y_pred)))

	return w


#Cross validation
wrong = 0
for i in range(30):
	w = np.random.rand(3,1)
	w = logreg(data,w,i,0.1)	
	wrong += np.round(abs(data[i,0] - sig(np.matmul(data[i,1:], w))))

print(wrong)
print(w)

ytilde = - w[2]/w[1] - (w[0]/w[1])*data[:,1]

plt.figure(1)
plt.plot(data[:,1], ytilde,c='r')
plt.scatter(data[data[:,0] == 1,1], data[data[:,0] == 1,2])
plt.scatter(data[data[:,0] == 0,1], data[data[:,0] == 0,2], c='g')

plt.xlabel("Normalized number of characters")
plt.ylabel("Normalized number of A's")
plt.title("Logistic regression")

plt.show()