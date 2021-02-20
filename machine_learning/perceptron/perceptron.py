# Joe Arriaga
# CS 445, Machine Learning
# January 17, 2019
#
# MNIST Perceptron
#
# This program implements 10 perceptrons (one for each digit) that learn to
# classify test from the MNIST testset. It also creates output files for various
# metrics.
#
# The datasets used and the learning rate can be changed in the 
# 'Initialize system' section starting on line 105.


import numpy as np
import random
import matplotlib.pyplot as plt
import time
import os


########## Define Classes and utility functions ##########
class Perceptron:
    eta = 0

    def __init__(self, eta, inputs):
        """ 'inputs' represents the number of input units the perceptron has."""
        self.weights = [0] * inputs
        for i in range(inputs):
            self.weights[i] = round(random.uniform(-0.05, 0.05), 3)
        self.eta = eta

    def learn(self, example):
        return np.dot(self.weights, example)

    def update(self, direction, example):
        """Updates the weights of the perceptron.
        'direction' is an integer, the result of the quantity (t-y).
        'example' is a list of the current inputs.
        """
        self.weights += self.eta * direction * example


# Define class to manage all 10 perceptrons as a single system
class Manager:
    # Create a perceptron for each digit
    perceptrons = []
    prediction_values = [0] * 10 # Prediction values for each perceptron, temporary for each example

    def __init__(self, eta, perceptrons, num_inputs):
        """ 'perceptrons' represents the number of perceptrons in the system.
        'inputs' represents the number of input units each perceptron has.
        """
        self.perceptrons = [Perceptron(eta, num_inputs) for _ in range(10)]


    def run(self, data):
        """Executes the Perceptron Learning Algorithm for all perceptrons for one
        epoch. Updates the weights for each perceptron, if needed.
        'data' is a 2d array of class labels and input values.
        """
        self.prediction_values = [0] * 10 # Clear values as a precaution
        successes = 0

        for ex in range(data.shape[0]):
            for p in range(len(self.perceptrons)):
                self.prediction_values[p] = self.perceptrons[p].learn(data[ex, 1:])
                # if perceptron is wrong, update weights
                if (self.prediction_values[p] > 0 and data[ex, 0] != p):
                    # perceptron predicts positively, but actual class is different
                    self.perceptrons[p].update(-1, data[ex, 1:])
                elif (self.prediction_values[p] <= 0 and data[ex, 0] == p):
                    # perceptron predicts negatively, but this is actual class
                    self.perceptrons[p].update(1, data[ex, 1:])
                #else prediction is correct, no need to change weights


    def accuracy(self, data, last=False):
        """Calculates the accuracy of the system with the given weight by
        calcuating each example.
        'data' is a 2d array of class labels and input values.
        Returns the accuracy for the 'data' given.
        """
        self.prediction_values = [0] * 10 # Clear values as a precaution
        successes = 0
        
        # Run each perceptron on each example in set 'data'
        for ex in range(data.shape[0]):
            for p in range(len(self.perceptrons)):
                self.prediction_values[p] = self.perceptrons[p].learn(data[ex, 1:])
            if np.argmax(self.prediction_values) == data[ex, 0]: #correct prediction
                # Record success
                successes += 1
            if last: # only for the last epoch
                # Enter result into confusion matrix
                conf_matrix[int(data[ex, 0]), np.argmax(self.prediction_values)] += 1
        
        return float(successes) / data.shape[0]


########## Initialize system ##########
# Read in data from file
fname = 'mnist_train.csv'
print("Reading in data from {}...".format(fname))
train = np.loadtxt(fname, delimiter=',')
fname = 'mnist_test.csv'
print("Reading in data from {}...".format(fname))
test = np.loadtxt(fname, delimiter=',')

# Preprocessing
train[:, 1:] /= 255 # Scale data
train = np.insert(train, 1, 1, axis=1) # Add bias unit
np.random.shuffle(train) # Shuffle training data

test[:, 1:] /= 255 # Scale data
test = np.insert(test, 1, 1, axis=1) # Add bias unit

# Define hyperparameters and compute commonly-used values
eta = 0.02
print("Learning rate eta = {}".format(eta))
epochs = 50
num_perceptrons = 10
num_inputs = train.shape[1] - 1 # number of inputs that each perceptron has
m = Manager(eta, num_perceptrons, num_inputs)
conf_matrix = np.zeros([num_perceptrons, num_perceptrons]) #indices are: [actual_class, predicted_class]

########## Run Perceptron Learning Algorithm and record accuracies for 50 epochs ##########
# Record initial accuracies
print("Calculating initial accuracies...")
train_accuracy = np.zeros(1)
test_accuracy = np.zeros(1)
train_accuracy[0] = m.accuracy(train)
test_accuracy[0] = m.accuracy(train)

for i in range(epochs):
    print("{} - Running epoch {}...".format(time.strftime("%H:%M:%S", time.localtime()), i))
    m.run(train)
    print("         - {} - Calculating accuracies...".format(time.strftime("%H:%M:%S", time.localtime())))
    train_accuracy = np.append(train_accuracy, m.accuracy(train))
    test_accuracy = np.append(test_accuracy, m.accuracy(test, i==49))

# Make directory for output, create scheme for naming output files
file_num = str(eta).split('.')[1]

if not os.path.exists('output'):
    os.makedirs('output')

np.savetxt("output/"+file_num+"_train_acc.csv", train_accuracy, delimiter=",")
np.savetxt("output/"+file_num+"_test_acc.csv", test_accuracy, delimiter=",")
np.savetxt("output/"+file_num+"_conf_matrix.csv", conf_matrix, delimiter=",")

########## Create graphics ##########
### Line graph
plt.plot(range(epochs+1), train_accuracy*100, label="Accuracy on the training data")
plt.plot(range(epochs+1), test_accuracy*100, label="Accuracy on the test data")
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.legend()
plt.grid(True)
#plt.show()  # toggle to your preference
plt.savefig("output/"+file_num+"_accuracy.png")

##### Confusion Matrices #####
# N.B. Confusion matrix code modified primarily from a Stack Overflow thread[1] and other sources:
# [1] https://stackoverflow.com/questions/5821125/how-to-plot-confusion-matrix-with-string-axis-rather-than-integer-in-python
# [2] https://stackoverflow.com/questions/37511277/how-to-plot-confusion-matrix-with-gridding-without-color-using-matplotlib

### Plain confusion matrix
plt.clf()
fig = plt.figure()
# Formatting appearance
ax = fig.add_subplot(111, aspect='equal') #[2]
ax.xaxis.tick_top()
ax.set_xlabel("Predicted Class")
ax.xaxis.set_label_position('top')
ax.xaxis.set_ticks(np.arange(0, 10, 1))
ax.yaxis.set_ticks(np.arange(0, 10, 1))

height, width = conf_matrix.shape
offset = .5 #[2]
ax.set_xlim(-offset, width - offset) #[2]
ax.set_ylim(-offset, height - offset) #[2]

ax.hlines(y=np.arange(height+1) - offset, xmin=-offset, xmax=width - offset) #[2]
ax.vlines(x=np.arange(width+1) - offset, ymin=-offset, ymax=height - offset) #[2]

for i,j in ((x,y) for x in xrange(len(conf_matrix))
                  for y in xrange(len(conf_matrix[0]))):
    ax.annotate(str(int(conf_matrix[i][j])), xy=(j,i), ha='center', va='center')

plt.gca().invert_yaxis()
plt.ylabel("Actual Class")
#fig.show() # toggle to your preference
plt.savefig("output/"+file_num+"_confusion_matrix_plain.png")

### Heat Map of Proportion confusion matrix
norm_conf = []
for i in conf_matrix:
    a = 0
    tmp_arr = []
    a = sum(i)
    for j in i:
        if a == 0:
            tmp_arr.append(0)
        else:
            tmp_arr.append(round(float(j)/float(a), 2))
    norm_conf.append(tmp_arr)

fig = plt.figure()
plt.clf()
ax = fig.add_subplot(111)
ax.xaxis.tick_top()
ax.set_xlabel("Predicted Class")
plt.ylabel("Actual Class")
ax.xaxis.set_label_position('top')
ax.xaxis.set_ticks(np.arange(0, 10, 1))
ax.yaxis.set_ticks(np.arange(0, 10, 1))
res = ax.imshow(np.array(norm_conf), cmap=plt.cm.jet, interpolation='nearest')

width, height = conf_matrix.shape
# Annotates with numbers
for x in xrange(width):
    for y in xrange(height):
        ax.annotate(str(norm_conf[x][y]), xy=(y,x), ha='center', va='center')

cb = fig.colorbar(res)
cb.set_label("Proportion of Occurrences of Actual Class")
#fig.show() # toggle to your preference
plt.savefig("output/"+file_num+"_confusion_matrix_heatmap.png")

# End Stack Overflow code
