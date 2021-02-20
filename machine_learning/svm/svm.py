# Joe Arriaga, jarriaga@pdx.edu
# CS 445 - Machine Learning
# March 15, 2019
#
# Spambase SVM
#
# This program implements a Support Vector Machine (SVM) designed to classify
# email messages from the Spambase dataset as spam or not spam.
# <https://archive.ics.uci.edu/ml/datasets/Spambase>
#
# It also investigates the effects of feature selection by comparing two methods
# of selecting features: selecting based on the importance of the feature, and
# random selection.


from sklearn import svm, preprocessing
from sklearn.metrics import precision_score, recall_score, roc_curve, auc
import numpy as np
import matplotlib.pyplot as plt
from random import random
import os


##### User options
show_plots = False # Set to 'True' to show plots during program execution
                   # ***NOTE: Enabling this setting may cause some plots to not
                   # display correctly and not be saved correctly. If possible,
                   # it is recommended to leave this setting disabled and use a
                   # tool such as 'feh', 'eog', 'xdg-open', 
                   # or ImageMagick's 'display' command.
stat_output = False # Set to 'True' to show statistical output during execution


##### Create directory for program output
if not os.path.exists('output/'):
    os.makedirs('output/')

##### Load data
training_data = np.loadtxt('data/training_set.csv', delimiter=',')
test_data = np.loadtxt('data/test_set.csv', delimiter=',')

##### Prepare data for SVM
np.random.shuffle(training_data)
np.random.shuffle(test_data)

### Separate examples from labels
example_length = training_data.shape[1]
(examples, labels) = np.split(training_data, [example_length-1], axis=1)
training_data = {'examples':examples, 'labels':labels.flatten()}

(examples, labels) = np.split(test_data, [example_length-1], axis=1)
test_data = {'examples':examples, 'labels':labels.flatten()}

### Scale data
scaler = preprocessing.StandardScaler().fit(training_data['examples'])
training_data['examples'] = scaler.transform(training_data['examples'])
test_data['examples'] = scaler.transform(test_data['examples'])


############################## Experiment 1 ####################################
# Basic SVM: Train SVM using a linear kernel on all 57 features.

### Train SVM
classifier = svm.SVC(kernel='linear')
classifier.fit(training_data['examples'], training_data['labels'])

### Test model on test data
predictions = classifier.predict(test_data['examples'])
scores = classifier.decision_function(test_data['examples'])

### Calculate accuracy, precision, recall
accuracy = classifier.score(test_data['examples'], test_data['labels'])
precision = precision_score(test_data['labels'], predictions)
recall = recall_score(test_data['labels'], predictions)

stats = {'accuracy':accuracy, 'precision':precision, 'recall':recall}
if stat_output:
    print("Accuracy = {}".format(accuracy))
    print("Precision = {}".format(precision))
    print("Recall = {}".format(recall))
file = open('output/stats.txt', 'w')
for key, val in stats.items():
    file.write(key + ' = ' + str(val) + '\n')
file.close()

### Create ROC curve
# Compute ROC curve
fpr, tpr, _ = roc_curve(test_data['labels'], scores)
roc_auc = auc(fpr, tpr)
np.savetxt("output/fpr.csv", fpr, delimiter=",")
np.savetxt("output/tpr.csv", tpr, delimiter=",")

# Plot ROC curve
plt.title('ROC curve')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0,1], [0,1], 'r--')
plt.xlim([0,1])
plt.ylim([0,1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
if show_plots:
    plt.show()
plt.savefig('output/roc.png')


############################## Experiment 2 ####################################
# Weighted Feature Selection: Train SVM using only the m most important
# features, as determined by the absolute value of the weight for each feature
# determined in Experiment 1. m varies from 2 to 57.

##### Order Examples
### Collect ordering
weights = classifier.coef_.flatten() # SVM weight vector
if stat_output:
    print("Weights:\n{}".format(weights))
file = open('output/stats.txt', 'a')
file.write("\nWeights:\n" + str(weights) + '\n')
file.close()

# get indices of weights in descending order of absolute value
ordered_weight_indices = np.argsort(np.absolute(weights))[::-1]
if stat_output:
    print("Weight-ordered Indices:\n{}".format(ordered_weight_indices))
file = open('output/stats.txt', 'a')
file.write("\nWeight-ordered Indices:\n" + str(ordered_weight_indices) + '\n')
file.close()

# write out weights in descending order
ordered_weights = []
for i in ordered_weight_indices:
    ordered_weights.append(weights[i])
if stat_output:
    print("Ordered Weights:\n{}".format(ordered_weights))
file = open('output/stats.txt', 'a')
file.write("\nOrdered Weights:\n" + str(ordered_weights) + '\n')
file.close()


### Order Training Examples
# Re-order the inputs in each training example according to the SVM weights
# ie. the input corresponding to the weight with the greatest absolute value is
# first, the input corresponding to the weight with the least absolute value is
# last, etc.
# The re-ordered data is stored in 'training_data['weight_ordered']
training_data['weight_ordered'] = []
for example in training_data['examples']:
    ordered_features = []
    for weight in ordered_weight_indices:
        ordered_features.append(example[weight])
    training_data['weight_ordered'].append(ordered_features)

### Order Test Examples
# re-order the inputs in each test example according to the SVM weights
# same as for the training data above
# The re-ordered data is stored in 'test_data['weight_ordered']
test_data['weight_ordered'] = []
for example in test_data['examples']:
    ordered_features = []
    for weight in ordered_weight_indices:
        ordered_features.append(example[weight])
    test_data['weight_ordered'].append(ordered_features)

### Collect Accuracies
# using the [2, 57] most important features, train the SVM and collect its accuracy
accuracies = []
for m in range(1,58):
    # Train SVM
    classifier.fit(training_data['weight_ordered'], training_data['labels'])

    # Test model
    accuracies.append(classifier.score(test_data['weight_ordered'], test_data['labels']))

np.savetxt("output/ordered_accuracy.csv", accuracies, delimiter=",")
accuracies = np.array(accuracies)

### Plot Accuracy vs. Ordered Features
plt.clf()
plt.title('Accuracy vs. Ordered Features')
plt.plot(range(1,58), accuracies*100)
plt.ylabel('Accuracy (%)')
plt.xlabel('# of Features')
plt.grid(True)
if show_plots:
    plt.show()
plt.savefig('output/ordered_features_zoomed.png')

plt.ylim(0,100)
if show_plots:
    plt.show()
plt.savefig('output/ordered_features.png')


############################## Experiment 3 ####################################
# Random Feature Selection: Train SVM using only m randomly-selected features;
# m varies from 2 to 57.

selection = range(57) # represents the indices of the features to be selected

# using the [2, 57] random weights, train the SVM and collect its accuracy
### Randomize features
# Sort training data into order selected by randomizer
accuracies = []
training_data['random'] = []
test_data['random'] = []
num_training_examples = training_data['examples'].shape[0]
num_test_examples = test_data['examples'].shape[0]
for m in range(1,58): # select [2,57] random features
    np.random.shuffle(selection) # randomize order of features
    random_example = []
    for i in selection[:m]: # use the first m indices from the shuffled list
        # extract the 'i'th column from the 2D array of examples
        random_example.append(training_data['examples'][:,[i]])
    # recombine the features from each example into a single array
    training_data['random'] = np.reshape(np.ravel(random_example, order='F'), (num_training_examples, m))

    # Sort test data into order selected by randomizer
#for m in range(1,58): # select [2,57] random features
    random_example = []
    for i in selection[:m]: # use the first m indices from the shuffled list
        # extract the 'i'th column from the 2D array of examples
        random_example.append(test_data['examples'][:,[i]])
    # recombine the features from each example into a single array
    test_data['random'] = np.reshape(np.ravel(random_example, order='F'), (num_test_examples, m))

    ### Train SVM and Collect Accuracies
    # Train SVM
    classifier.fit(training_data['random'], training_data['labels'])

    # Test model
    accuracies.append(classifier.score(test_data['random'], test_data['labels']))

accuracies = np.array(accuracies)
np.savetxt("output/random_accuracy.csv", accuracies, delimiter=",")

### Plot Accuracy vs. Random Features
plt.clf()
plt.title('Accuracy vs. Random Features')
plt.plot(range(1,58), accuracies*100)
plt.ylabel('Accuracy (%)')
plt.xlabel('# of Features')
plt.grid(True)
if show_plots:
    plt.show()
plt.savefig('output/random_features_zoomed.png')

plt.ylim(0,100)
if show_plots:
    plt.show()
plt.savefig('output/random_features.png')

