# Joe Arriaga, jarriaga@pdx.edu
# CS 445 - Machine Learning
# February 5, 2019
#
# MNIST Neural Network
#
# This program implements a neural network designed to classify handwritten
# digits from the MNIST dataset.
#
# The user can specify the data sets to be used as well as the values for
# various hyperparameters in the 'user-defined variables' section.
#
# Function definitions are at the beginning of the file; the program execution
# routine is at the end of the file.


import numpy as np
from random import random
import time
import os
import make_graphs # Local file containing functions to create graphics of plots


################# INTERACTIVE PROMPTS ##################################
print("These prompts allow you to enter values for various program variables.\n\
Any value you enter will override the value hard-coded in the script.\n\
NOTE: The program does not check your user input in any way so invalid entries\n\
will likely result in a program crash.\n\
If you want to use the values defined in the script simply leave the fields blank and press 'Enter'.\n\
*** Remember to end all paths with a terminating '/' ***\n")

training_data = raw_input("Enter the path to the training set (default = data/mnist_train.csv): ")
test_data = raw_input("Enter the path to the test set (default = data/mnist_test.csv): ")
num_hidden_units = raw_input("Enter the number of hidden units (not including the bias unit) (default = 100): ")
momentum = raw_input("Enter a value for the momentum (default = 0.9): ")
output_path = raw_input("Enter the path to the desired location for output (default = output/): ")
dump_results = raw_input("Would you like to dump the results in CSV format?(y/n)  ")
create_graphics = raw_input("Would you like to generate graphics?(y/n) ")

################# USER-DEFINED VARIABLES ###############################
# Use these variables to specify the data files to be used
# and to set hyperparameters

if not training_data: 
    training_data = 'data/mnist_train.csv' # File path of csv training data
if not test_data: 
    test_data = 'data/mnist_test.csv' # File path of csv test data

if not output_path:
    output_path = "output/" # Set path of output directory, terminating with '/'
                        # Entering './' will save files in the current directory
                        # with no enclosing directory

if dump_results.lower() == 'y':
    dump_results = True
else:
    dump_results = False # Set to 'True' to output csv files of data for 
                         # final accuracies and confusion matrices

if create_graphics.lower() == 'y':
    create_graphics = True
else:
    create_graphics = False # Set to 'True' to render graphics of accuracis and 
                            # confusion matrices

epochs = 50
learning_rate = .1

if momentum: 
    momentum = float(momentum) # Convert string to float
else:
    momentum = .9

if num_hidden_units:
    num_hidden_units = int(num_hidden_units) # Convert string to int
else:
    num_hidden_units = 100 # don't include the bias unit

num_output_units = 10

# Activation function
def sigmoid(z):
  return (1 / (1 + np.exp(-z)))
########################################################################


def scale(data):
    """Prepare the raw data to be used by the neural network by scaling the
        input values and adding the input bias unit.
    """
    # Scale data, add bias unit
    (labels,inputs) = np.split(data,[1],axis=1)
    inputs /= 255 # scale data
    inputs = np.insert(inputs,0,1,axis=1) # add bias unit
    # Recombine labels and input values so they stay together during shuffling
    data = np.concatenate((labels,inputs),axis=1)

    return data


def train(labels, training_set, inputs_to_hidden_weights, hidden_to_output_weights):
    """Train the neural network.
        
        Keyword arguments:
        labels -- list of the true class of each example
        training_set -- matrix of the input values for each example
        inputs_to_hidden_weights -- matrix of the weights from the input layer
                                    to the hidden layer
        hidden_to_output_weights -- matrix of the weights from the hidden layer
                                    to the output layer
    """
    hidden_to_output_deltas = np.zeros_like(hidden_to_output_weights)
    inputs_to_hidden_deltas = np.zeros_like(inputs_to_hidden_weights)

    num_examples = training_examples.shape[0]
    for ex in range(num_examples):
        #### Forward Propagation
        hidden_activations = np.array(map(sigmoid,np.dot(inputs_to_hidden_weights,training_set[ex])))
        # Insert hidden layer bias unit and calculate dot product from hidden layer
        output_activations = np.dot(hidden_to_output_weights,np.insert(hidden_activations,0,1))

        if num_output_units == 1:
            output_activations = sigmoid(output_activations)
        else:
            output_activations = np.array(map(sigmoid,output_activations))

        #### Calculate Error
        ## Output errors
        targets = [.1] * num_output_units
        targets[labels[ex]] = .9
        
        if num_output_units == 1:
            output_errors = (output_activations
                            *(1-output_activations)
                            *(targets-output_activations))
        else:
            output_errors = (output_activations
                            *[1-x for x in output_activations]
                            *(targets-output_activations))
        
        ## Hidden errors    
        # Create vectors out of the weights from each hidden unit into the output units,
        # and delete the weights from the hidden layer bias unit
        weights_to_outputs = np.squeeze(
                                np.split(
                                    np.delete(hidden_to_output_weights,0,1),
                                                num_output_units))
      
        hidden_errors = (hidden_activations
                        *[1-x for x in hidden_activations]
                        *np.transpose(np.dot(output_errors,weights_to_outputs)))
      
        #### Calculate Weight Deltas
        # Add bias unit
        hidden_activations = np.insert(hidden_activations,0,1)
        # Flatten output error matrix to allow matrix multiplication with
        # the matrix of hidden unit activations
        reshaped_errors = np.reshape(output_errors,(num_output_units,1))
        hidden_to_output_deltas = (learning_rate*reshaped_errors*hidden_activations
                                  + momentum*hidden_to_output_deltas)

        if num_output_units == 1:
            hidden_to_output_deltas = np.reshape(hidden_to_output_deltas,(3,))

        # Flatten hidden error matrix to allow matrix multiplication with
        # the matrix of input unit values
        reshaped_errors = np.reshape(hidden_errors,(num_hidden_units,1))
        inputs_to_hidden_deltas = (learning_rate*reshaped_errors*training_set[ex]
                                  + momentum*inputs_to_hidden_deltas)

        #### Update Weights
        hidden_to_output_weights += hidden_to_output_deltas
        inputs_to_hidden_weights += inputs_to_hidden_deltas

    return (inputs_to_hidden_weights,hidden_to_output_weights)


def get_accuracy(labels, inputs, inputs_to_hidden_weights, hidden_to_output_weights):
    """Compute the accuracy of the current model over all examples given in
        'labels' and 'inputs'.
        
        Keyword arguments:
        labels -- list of the true class of each example
        inputs -- matrix of the input values for each example
        inputs_to_hidden_weights -- matrix of the weights from the input layer
                                    to the hidden layer
        hidden_to_output_weights -- matrix of the weights from the hidden layer
                                    to the output layer
    """

    num_examples = inputs.shape[0]
    successes = 0
    for ex in range(num_examples):
        #### Forward Propagation
        hidden_activations = np.array(map(sigmoid,np.dot(inputs_to_hidden_weights,inputs[ex])))
        # Insert hidden layer bias unit and calculate dot product from hidden layer
        output_activations = np.dot(hidden_to_output_weights,np.insert(hidden_activations,0,1))

        if num_output_units == 1:
            output_activations = sigmoid(output_activations)
        else:
            output_activations = np.array(map(sigmoid,output_activations))

        #### Check Prediction
        prediction = np.argmax(output_activations)
        if prediction == labels[ex]:
            successes += 1

    return float(successes)/num_examples


def compute_confusion_matrix(labels, inputs, inputs_to_hidden_weights, hidden_to_output_weights):
    """Collect the prediction values and the labels for each example and create
        a confusion matrix graphic.
        
        Keyword arguments:
        labels -- list of the true class of each example
        inputs -- matrix of the input values for each example
        inputs_to_hidden_weights -- matrix of the weights from the input layer
                                    to the hidden layer
        hidden_to_output_weights -- matrix of the weights from the hidden layer
                                    to the output layer
    """

    num_examples = inputs.shape[0]
    successes = 0
    confusion_matrix = np.zeros((num_output_units,num_output_units))
    for ex in range(num_examples):
        #### Forward Propagation
        hidden_activations = np.array(map(sigmoid,np.dot(inputs_to_hidden_weights,inputs[ex])))
        # Insert hidden layer bias unit and calculate dot product from hidden layer
        output_activations = np.dot(hidden_to_output_weights,np.insert(hidden_activations,0,1))

        if num_output_units == 1:
            output_activations = sigmoid(output_activations)
        else:
            output_activations = np.array(map(sigmoid,output_activations))

        #### Add prediction to confusion matrix
        prediction = np.argmax(output_activations)
        confusion_matrix[labels[ex],prediction] += 1 # indices are (actual class, predicted class)

    return confusion_matrix
    


############## Program Execution ################

# Read in data
training_examples = np.loadtxt(training_data, delimiter=',')
num_inputs = training_examples.shape[1]
training_examples = scale(training_examples)
test_examples = np.loadtxt(test_data, delimiter=',')
test_examples = scale(test_examples)

# Initialize weights to random values
inputs_to_hidden_weights = .1 * np.random.random((num_hidden_units,num_inputs)) - .05
hidden_to_output_weights = .1 * np.random.random((num_output_units,num_hidden_units+1)) - .05

# Initialize lists of accuracies for plot
training_accuracies = np.zeros(epochs+1)
test_accuracies = np.zeros(epochs+1)

### Collect accuracies with random weights before training as baseline
(training_labels,training_inputs) = np.split(training_examples,[1],axis=1)
training_labels = np.ravel(np.asarray(training_labels,dtype=int))
training_accuracies[0] = get_accuracy(training_labels, 
                                training_inputs, 
                                inputs_to_hidden_weights, 
                                hidden_to_output_weights)

(test_labels,test_inputs) = np.split(test_examples,[1],axis=1)
test_labels = np.ravel(np.asarray(test_labels,dtype=int))
test_accuracies[0] = get_accuracy(test_labels, 
                            test_inputs, 
                            inputs_to_hidden_weights, 
                            hidden_to_output_weights)

for i in range(epochs):
    print(time.strftime("%H:%M:%S") + " starting epoch {}".format(i))
    np.random.shuffle(training_examples)
    (training_labels,training_inputs) = np.split(training_examples,[1],axis=1)
    training_labels = np.ravel(np.asarray(training_labels,dtype=int))

    ### Train neural network, collect accuracies
    (inputs_to_hidden_weights, hidden_to_output_weights) = train(training_labels, 
                                                                training_inputs, 
                                                                inputs_to_hidden_weights, 
                                                                hidden_to_output_weights)

    ### Collect accuracies after training in each epoch
    training_accuracies[i+1] = get_accuracy(training_labels, 
                                    training_inputs, 
                                    inputs_to_hidden_weights, 
                                    hidden_to_output_weights)

    test_accuracies[i+1] = get_accuracy(test_labels, 
                                test_inputs, 
                                inputs_to_hidden_weights, 
                                hidden_to_output_weights)

    #### Create confusion matrix on last epoch
    if i == epochs-1:
        confusion_data = compute_confusion_matrix(test_labels,
                                                    test_inputs,
                                                    inputs_to_hidden_weights,
                                                    hidden_to_output_weights)

# Output csv files of final accuracies and confusion matrices
if (dump_results):
    make_graphs.dump_results(output_path, "training_accuracy", training_accuracies)
    make_graphs.dump_results(output_path, "test_accuracy", test_accuracies)
    make_graphs.dump_results(output_path, "test_confusion_data", confusion_data)
        
# Create Graphics
if (create_graphics):
    make_graphs.create_accuracy_plot(output_path, training_accuracies, test_accuracies, epochs)
    make_graphs.create_confusion_matrix(output_path, confusion_data)



