# Joe Arriaga
# CS 445 - Machine Learning
# Febrary 5, 2019
#
# MNIST Neural Network
#
# This is a utility program to create graphical output for the MNIST Neural
# Network program. It creates accuracy graphs and confusion matrices.


import numpy as np
import matplotlib.pyplot as plt
import time
import os


def dump_results(path, filename, data):
    # Make directory for output, create scheme for naming output files
    if not path: # user has not specified a location to place output
        path = time.strftime("%Y-%m-%d_%H:%M:%S/")

    if not os.path.exists(path):
        os.makedirs(path)

    np.savetxt(path+filename+".csv", data, delimiter=",")

########## Create graphics ##########

### Line graph
def create_accuracy_plot(path, train_accuracies, test_accuracies, epochs):
    plt.plot(range(epochs+1), train_accuracies*100, label="Accuracy on training data")
    plt.plot(range(epochs+1), test_accuracies*100, label="Accuracy on test data")
    plt.title('Accuracy of Two-layer Neural Network\non classifying MNIST Handwritten Digits')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    plt.grid(True)
    #plt.show()  # toggle to your preference
    plt.savefig(path+"accuracy.png")


def create_confusion_matrix(path, data):
##### Confusion Matrices #####
# N.B. Confusion matrix code modified primarily from a Stack Overflow thread[1] and other sources:
# [1] https://stackoverflow.com/questions/5821125/how-to-plot-confusion-matrix-with-string-axis-rather-than-integer-in-python
# [2] https://stackoverflow.com/questions/37511277/how-to-plot-confusion-matrix-with-gridding-without-color-using-matplotlib

### Plain confusion matrix
    norm_conf = []
    for i in data:
        a = 0
        tmp_arr = []
        a = sum(i)
        for j in i:
            if a == 0:
                tmp_arr.append(0)
            else:
                tmp_arr.append(float(j)/float(a))
        norm_conf.append(tmp_arr)

    plt.clf()
    fig = plt.figure()
    fig.subplots_adjust(top=0.8)
# Formatting appearance
    ax = fig.add_subplot(111, aspect='equal') #[2]
    ax.xaxis.tick_top()
    ax.set_xlabel("Predicted Class")
    ax.xaxis.set_label_position('top')
    ax.xaxis.set_ticks(np.arange(0, 10, 1))
    ax.yaxis.set_ticks(np.arange(0, 10, 1))

    height, width = data.shape
    offset = .5 #[2]
    ax.set_xlim(-offset, width - offset) #[2]
    ax.set_ylim(-offset, height - offset) #[2]

    ax.hlines(y=np.arange(height+1) - offset, xmin=-offset, xmax=width - offset) #[2]
    ax.vlines(x=np.arange(width+1) - offset, ymin=-offset, ymax=height - offset) #[2]

    for i,j in ((x,y) for x in xrange(len(data))
                      for y in xrange(len(data[0]))):
        ax.annotate(str(int(data[i][j])), xy=(j,i), ha='center', va='center')

    plt.gca().invert_yaxis()
    plt.title('Confusion Matrix for MNIST Handwritten Digits', y=1.14)
    plt.ylabel("Actual Class")
    #fig.show() # toggle to your preference
    plt.savefig(path+"confusion_matrix_plain.png")


### Heat Map of Total Occurrences confusion matrix
    norm_conf = []
    for i in data:
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
    fig.subplots_adjust(top=0.8)#, left=0.05, right=0.95)
    ax = fig.add_subplot(111)
    ax.xaxis.tick_top()
    plt.title('Heatmap Confusion Matrix for MNIST Handwritten Digits', y=1.14)
    ax.set_xlabel("Predicted Class")
    plt.ylabel("Actual Class")
    ax.xaxis.set_label_position('top')
    ax.xaxis.set_ticks(np.arange(0, 10, 1))
    ax.yaxis.set_ticks(np.arange(0, 10, 1))
    res = ax.imshow(np.array(data), cmap=plt.cm.jet, interpolation='nearest')

    width, height = data.shape
# Annotates with numbers
    for x in xrange(width):
        for y in xrange(height):
            ax.annotate(str(int(data[x][y])), xy=(y,x), ha='center', va='center')

    cb = fig.colorbar(res)
    cb.set_label("Occurrences")
    #fig.show() # toggle to your preference
    plt.savefig(path+"confusion_matrix_heatmap.png")
# End Stack Overflow code



