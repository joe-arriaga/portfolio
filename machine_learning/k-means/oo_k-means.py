# Joe Arriaga
# CS 445 - Machine Learning
# August 9, 2019 - August 25, 2019
#
# "Object-Oriented" K-means Clustering
# File 1
#
# This program implements the K-means Clustering algorithm to identify digits
# from the optdigits data set.
# This is file 1, the training file, and calculates cluster ceners using randomly
# chosen points from the training data as seeds. It then calculates several
# performance metrics on the results and writes everything to an output file.

# Steps:
# --------------------------------
# File 1:
# x Run Clustering on data (5 times)
#   x Choose k centroids
#   x Until centroids stabilize
#       x assign each point to its nearest centroid
#       x recompute centroids as the mean of all associated points
#   - Associate each non-empty cluster center with the most frequent class it
#     contains (to be used later for classifying test data).
# x Choose run with smallest mse
#   x calculate mse for each run
#   x write mse and centroids to file
#
# x For run with smallest mse:
#   x Calculate evaluation metrics (leaving out empty clusters):
#     x mss
#     x entropy
#
# x write results to file
#
# File 2:
# - Classify test data
#   - each non-empty center gets its most common class
#   - assign each test example to its closest center
#   - calculate accuracy
#
# - Visualize non-empty centers (can do this after training)

import numpy as np
import random
#from math import sqrt
import matplotlib.pyplot as plt
import os
import sys # To print without newlines, in casting cluster values, line 153
            # Also, error checking for MSE, line 160
import csv # To write output, line 183
from math import log
from example import Example # User-defined class for data points


##### User options
num_classes = 10
#num_clusters = 30
num_clusters = 10
#num_clusters = 3
output_file_name = 'training_results.txt'
output_file = 'output/' + output_file_name



##### Create directory for program output
if not os.path.exists('output/'):
    os.makedirs('output/')



#NOTE:????? class Centroid(object):


####### Initalize objects
##### Load data
training_data = np.loadtxt('data/optdigits/optdigits.train', delimiter=',')
training_data = training_data.astype(int) #TODO: Remove and use \/\/ if data is all integers, I think it is

# Initialize representation of data
dimensions = training_data.shape[1]-1
examples = [ Example(x[:dimensions], x[dimensions]) for x in training_data ]


#examples = []
#for 


#print('examples:\n{}'.format(examples))
#print examples[0]
#print('examples[0]:\n{}'.format(examples[0]))
#print('examples[0].point = {}'.format(examples[0].point))
#print 'examples:'
#for ex in examples:
#    print ex
#print 'examples test:'
#print [ x.point for x in examples ]
#print [ x for x in examples ]

#for i in examples:
#    i.display_all()

#points = [ x.point for x in examples ]
#print('points = {}'.format(points))
#np_points = np.array(points)
#print('np_points:\n{}'.format(np_points))


#for run in range(5): # Run algorithm and evaluation 5 times
######### Algorithm ###########
####### To Find final centroids
### Select k points as initial centroids

#np_examples = np.array(examples, ndmin=2)
#print('np_examples:\n{}'.format(np_examples))
#print('np_examples[2] = {}'.format(np_examples[2]))
#centroids = np.array(examples[:num_clusters]).astype(np.float32)
#print('centroids:\n{}'.format(centroids))
#centroids = np.array(centroids, dtype=float)
#centroids = np.array(examples[:num_clusters], dtype=float) # take the first k examples as centroids
#centroids = np.array(np_examples[:num_clusters], dtype=float) # take the first k examples as centroids

#centroids = np.zeros((num_clusters))
#for i in range(num_clusters):
#    print('examples[{}].point = {}'.format(i, examples[i].point))
#    centroids[i] = examples[i].point

centroid_selection = random.sample(examples, k=num_clusters)
centroids = np.array( [x.point for x in centroid_selection], dtype=float)
#centroids = np.array( [x.point for x in examples[:num_clusters]], dtype=float) #NOTE: FOR TESTING - choose first k points as centroids

old_centroids = centroids - 1 # Used to determine when centroids stabilize, 
                       # initialize to something different from initial centroids
#print('initial centroids:\n{}'.format(centroids))
#print('old_centroids:\n{}'.format(old_centroids))

iterations = 0 #TODO: for testing only

##### Until centroids stabilize:
while (not (centroids == old_centroids).all()):
    iterations += 1 #TODO: for testing only
    cluster_membership = np.array([])
    min_distance = np.array([])
    clusters = [[None]]*num_clusters
    cluster_empty = [True]*num_clusters

    # Assign points to clusters
    for ex in examples:
        #print ex
        distance_to_centroids = np.array([])
        for i in range(centroids.shape[0]):
            distance_to_centroids = np.append(distance_to_centroids, ex.distance(centroids[i]))
        #cluster_index = distance_to_centroids.argmin()
        ex.assigned_label = distance_to_centroids.argmin()
        #print('cluster_index = {}'.format(cluster_index))
        if (cluster_empty[ex.assigned_label]):
            cluster_empty[ex.assigned_label] = False
            clusters[ex.assigned_label] = [ex.point]
        clusters[ex.assigned_label].append(ex.point)

#TODO: Make sure class labels are assigned correctly, not just based on indices

        # Debugging signals
        #min_distance = np.append(min_distance, distance_to_centroids[cluster_index])
        cluster_membership = np.append(cluster_membership, ex.assigned_label)

    # Recompute centroids
    old_centroids = np.array(centroids)
    for i in range(len(centroids)):
        centroids[i] = np.average(clusters[i], axis=0)

##### Associate each non-empty cluster with the most frequent class it contains
#TODO??? accomplished in testing file


#print 'examples test:'
#print [ x.point for x in examples ]
#print [ x for x in examples if x.assigned_label == 1 ]

#print('\nAfter stabilizing:')
#print('# of iterations = {}'.format(iterations))
#print('centroids:\n{}'.format(centroids))

#print('clusters, raw:\n{}'.format(clusters))
#clusters = np.array(clusters)
#print('clusters, numpy array:\n{}'.format(clusters))

#print('cluster_membership:\n{}'.format(cluster_membership))

#print('object clusters:')
#for i in range(num_clusters):
#    print [ x for x in examples if x.assigned_label == i ]
#for i in range(num_clusters):
#    for ex in examples:
#        if (ex.assigned_label == i):
#            print ex,; print ', ',
#    print

#print('labels:')
#for i in range(num_clusters):
#    print [x.assigned_label for x in examples if x.assigned_label == i]

# --> Want to get clustered examples?

# ----- Calculate Mean Square Error -----
mses = []
if (len(clusters) != len(centroids)):
    print('***ERROR: Different numbers of clusters and centroids\
    \n***       Found when finding the average MSE')
    sys.exit(1)
else:
    for i in range(len(clusters)):
        norms = [np.linalg.norm(x) for x in clusters[i] - centroids[i]]
        norms = np.array(norms)
        mses.append(sum(norms**2)/len(norms))
        #print('norms = {}'.format(norms))
        #print('squares = {}'.format(norms**2))
        #print('#{} avg = {}'.format(i, sum(norms**2)/len(norms)))

print('mses = {}'.format(mses))
avg_mse = sum(mses) / len(mses)
print('avg_mse = {}'.format(avg_mse))

# ----- Calculate Mean Square Separation -----
total = 0
num_centroids = len(centroids)
for i in range(num_centroids):
    for j in range(i+1,num_centroids):
        #print('({},{})'.format(i,j))
        #print('i - j = {}'.format(centroids[i] - centroids[j]))
        distance = np.linalg.norm(centroids[i] - centroids[j])**2
        #print('distance^2 = {}'.format(distance))
        total += np.linalg.norm(centroids[i] - centroids[j])**2
        #print('total = {}'.format(total))

mss = total / (num_centroids * (num_centroids-1) / 2)
print('mss = {}'.format(mss))

# ----- Calculate Entropy -----
#num_per_cluster = [[0]*num_classes] * k
#for i in range(k):
#    for j in range(num_classes):
#        num_per_cluster.append([0])
num_per_cluster = np.zeros((num_classes, num_clusters))
#print('num_per_cluster:\n{}'.format(num_per_cluster))
#print('num_per_cluster[0][1]: {}'.format(num_per_cluster[0][1]))

#for cluster in range(len(clustered)):
#    for point in clustered[cluster]:
#        #print('cluster = {}, point[1] = {}'.format(cluster, point[1]))
#        num_per_cluster[cluster][point[1]] += 1
#        #print('class = {}'.format(point[1]))
#        #print('num_per_cluster: {}\n'.format(num_per_cluster))

#print('object clusters len:')
#for i in range(num_clusters):
#    print len([x for x in examples if x.assigned_label == i])

#print('clusters:\n{}'.format(clusters))
#for i in range(num_clusters):
#    for j in range(num_classes):
#        num_per_cluster[i][j] = len( [x for x in clusters if x.assigned_label == j] )
#print('num_per_cluster:\n{}'.format(num_per_cluster))

for i in range(num_clusters):
    for j in range(num_classes):
        num_per_cluster[i][j] = len( [x for x in examples if x.assigned_label == i and x.true_class == j] )
print('num_per_cluster:\n{}'.format(num_per_cluster))

#numer = num_per_cluster[i][j]
ex_per_cluster = [sum(x) for x in num_per_cluster]
#print('ex_per_cluster = {}'.format(ex_per_cluster))
total_examples = sum(ex_per_cluster)

entropies = []

## Method 1
#for i in range(len(clustered)):
#    denom = ex_per_cluster[i]
#    total = 0
#    for j in num_per_cluster[i]:
#        if j == 0: continue
#        #print('j = {}'.format(j))
#        #print('denom = {}'.format(denom))
#        total += -(j/denom * log(j/denom, 2))
#    entropies.append(total)

# Method 2
for i in range(num_clusters):
    denom = ex_per_cluster[i]
    #entropies.append(-sum([x/denom * log(x/denom, 2) for x in num_per_cluster[i] if x != 0]))
    entropies += [-sum( [x/denom * log(x/denom, 2) for x in num_per_cluster[i] if x != 0] )]
    #print('inside entropies = {}'.format(entropies))

print('entropies = {}'.format(entropies))

mean_entropy = 0
for i in range(len(entropies)):
    mean_entropy += ex_per_cluster[i]/total_examples * entropies[i]

print('mean_entropy = {}'.format(mean_entropy))

### Write centroids and metrics(mse, mss, entropies) of each run to file
with open(output_file, 'ab') as file_out:
    file_out.write('Run # \n')
    
    #file_out.write('tofile()\n')
    #centroids.tofile(output_file, sep=',')
    #file_out.write('\n')
    #file_out.write('savetxt()\n')
    #np.savetxt(output_file, centroids, delimiter=',')
    
    file_out.write('Centroids:\n{}\n'.format(centroids))
    file_out.write('Number of each class per Cluster:\n{}\n'.format(num_per_cluster))
    file_out.write('MSEs = {}\n'.format(mses))
    file_out.write('Avg. MSE  = {}\n'.format(avg_mse))
    file_out.write('MSS = {}\n'.format(mss))
    file_out.write('Entropies = {}\n'.format(entropies))
    file_out.write('Mean Entropy = {}\n'.format(mean_entropy))
    file_out.write('\n')
print('output file: {}'.format(output_file))

#with open('array_out.txt', 'ab') as file_out:
#    file_out.write('tofile()\n')
#centroids.tofile('array_out.txt', sep=',')
#with open('array_out.txt', 'ab') as file_out:
#    file_out.write('\n')
#    file_out.write('savetxt()\n')
#print('centroids:\n{}'.format(centroids))
#np.savetxt('array_out.txt', centroids, delimiter=',')




