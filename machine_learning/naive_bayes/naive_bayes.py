# Joe Arriaga, jarriaga@pdx.edu
# CS 445 - Machine Learning
# March 15, 2019
#
# Spambase Naive Bayes Classification
#
# This program implements a Naive Bayes Classifier designed to classify
# email messages from the Spambase dataset as spam or not spam
# <https://archive.ics.uci.edu/ml/datasets/Spambase>.
# It also serves to investigate the assumption of independent attributes made by
# the Naive Bayes Classifier.


from sklearn import preprocessing
from sklearn.metrics import accuracy_score, precision_score, recall_score,\
                            confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import os


##### User options
show_plots = False # Set to 'True' to show plots during program execution
                   # ***NOTE: Enabling this setting may cause some plots to not
                   # display correctly and not be saved correctly. If possible,
                   # it is recommended to leave this setting disabled and use a
                   # tool such as 'feh', 'eog', 'xdg-open', 
                   # or ImageMagick's 'display' command.
stat_output = True # Set to 'True' to show statistical output during execution


def prob_density(array, means, devs):
    index = ((array-means)**2) / (2*(devs**2))
    
    coefficient = 1/(np.sqrt(2*np.pi)*devs)

    return coefficient * np.exp(-index)


##### Create directory for program output
if not os.path.exists('output/'):
    os.makedirs('output/')

##### Load data
training_spam = np.loadtxt('data/train_spam.csv', delimiter=',')
training_legit = np.loadtxt('data/train_not_spam.csv', delimiter=',')
test_data = np.loadtxt('data/test_set.csv', delimiter=',')

##### Preprocess data
### Separate examples from labels
example_length = training_spam.shape[1]
(examples, labels) = np.split(training_spam, [example_length-1], axis=1)
training_spam = {'examples':examples, 'labels':labels.flatten()}

example_length = training_legit.shape[1]
(examples, labels) = np.split(training_legit, [example_length-1], axis=1)
training_legit = {'examples':examples, 'labels':labels.flatten()}

example_length = test_data.shape[1]
(examples, labels) = np.split(test_data, [example_length-1], axis=1)
test_data = {'examples':examples, 'labels':labels.flatten()}

### Calculate prior probabilities for each class
num_spam = len(training_spam['examples'])
num_legit = len(training_legit['examples'])
num_total = len(training_spam['examples']) + len(training_legit['examples'])
spam_class_prob = np.true_divide(num_spam, num_total)
legit_class_prob = np.true_divide(num_legit, num_total)

#### Compute Mean and Standard Deviation of each feature in training set
### Compute Means
#spam_means = np.mean(training_spam['examples'], axis=0, dtype=np.float64)
spam_means = np.mean(training_spam['examples'], axis=0)
legit_means = np.mean(training_legit['examples'], axis=0)

### Compute Standard Deviations
spam_sds = np.std(training_spam['examples'], axis=0)
legit_sds = np.std(training_legit['examples'], axis=0)

# add epsilon value to avoid division by zero when calculating probability densities
spam_sds += 0.0001 
legit_sds += 0.0001

##### Compute probability densities of each class for each example
spam_densities = []
legit_densities = []
for ex in test_data['examples']:
    temp = prob_density(ex, spam_means, spam_sds)
    if np.any(temp == 0): # Check for 0 probability which causes error in log()
        for i in range(len(temp)):
            if temp[i] < 0.000000001:
                temp[i] = 0.000000001
    spam_densities.append(temp)

    temp = prob_density(ex, legit_means, legit_sds)
    if np.any(temp == 0): # Check for 0 probability which causes error in log()
        for i in range(len(temp)):
            if temp[i] < 0.000000001:
                temp[i] = 0.000000001
    legit_densities.append(temp)

# Classify instances
spam_probabilities = np.log(spam_class_prob) \
                        + np.sum(np.log(spam_densities), axis=1)
legit_probabilities = np.log(legit_class_prob) \
                        + np.sum(np.log(legit_densities), axis=1)

predictions = []
for s, l in zip(spam_probabilities, legit_probabilities):
    predictions.append(int(s > l))


##### Evaluate performance
### Calculate Accuracy, Precision, and Recall
accuracy = accuracy_score(test_data['labels'], predictions)
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

### Create Confusion Matrix
# Grphics code modified from: https://stackoverflow.com/questions/37511277/how-to-plot-confusion-matrix-with-gridding-without-color-using-matplotlib

cm = confusion_matrix(test_data['labels'], predictions)
if stat_output:
    print('Confusion_matrix:\n{}'.format(cm))

height, width = cm.shape

fig = plt.figure('confusion matrix')
fig.subplots_adjust(top=0.8)
ax = fig.add_subplot(111, aspect='equal')
for x in range(width):
    for y in range(height):
        ax.annotate(str(cm[x][y]), xy=(y, x), ha='center', va='center')

offset = .5    
ax.set_xlim(-offset, width - offset)
ax.set_ylim(-offset, height - offset)

ax.hlines(y=np.arange(height+1)- offset, xmin=-offset, xmax=width-offset)
ax.vlines(x=np.arange(width+1) - offset, ymin=-offset, ymax=height-offset)

plt.xticks(range(width), ['Not Spam', 'Spam'])
ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()
plt.yticks(range(height), ['Not Spam', 'Spam'])
plt.title('Confusion Matrix of Naive Bayes Classifier on Spambase dataset', y = 1.14)
plt.xlabel("Predicted Class")
plt.gca().invert_yaxis()
plt.ylabel("Actual Class")
if show_plots:
   plt.show()
plt.savefig('output/confusion_matrix.png', format='png')

