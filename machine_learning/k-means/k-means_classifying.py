# Joe Arriaga
# CS 445 - Machine Learning
# August 19, 2019 - August 25, 2019
#
# ("Object-Oriented") K-means Clustering
# File 2
#
# This program implements the K-means Clustering algorithm to identify digits
# from the optdigits data set.
# This is file 2, the testing file, and uses the clusters produced in file 1 to
# classify test data and visualize the results.

# Steps:
# --------------------------------
# File 2:
# x Classify test data
#   x each non-empty center gets its most common class
#   x assign each test example to its closest center
# x Calculate performance metrics
#   x accuracy
#   x confusion matrix
# x Visualize non-empty centers (can do this after training)


import numpy as np
import random # randomly select label for cluster, ln. 67
from example import Example # User-defined class for data points
import matplotlib.pyplot as plt
import os


##### User options
num_classes = 10
num_clusters = 10
data_file = 'data/optdigits/optdigits.test' # input file with test data

# formatting variables for PGM visualizations
num_features = 64
row_length = 8

##### Load data
### Copy and paste centroids from training results file into array
centroids = np.array(
[[0.00000000e+00, 4.73684211e-02, 4.40526316e+00, 1.21526316e+01,
  4.58947368e+00, 5.78947368e-01, 0.00000000e+00, 0.00000000e+00,
  0.00000000e+00, 4.89473684e-01, 1.15947368e+01, 1.16210526e+01,
  2.18421053e+00, 3.73684211e-01, 0.00000000e+00, 0.00000000e+00,
  0.00000000e+00, 2.06315789e+00, 1.44947368e+01, 4.87368421e+00,
  1.89473684e-01, 1.05263158e-01, 1.05263158e-02, 0.00000000e+00,
  0.00000000e+00, 3.60526316e+00, 1.44052632e+01, 4.86315789e+00,
  3.60526316e+00, 1.87894737e+00, 2.52631579e-01, 0.00000000e+00,
  0.00000000e+00, 4.90526316e+00, 1.44473684e+01, 1.18473684e+01,
  1.27263158e+01, 1.08736842e+01, 2.41052632e+00, 0.00000000e+00,
  0.00000000e+00, 3.29473684e+00, 1.53157895e+01, 1.03421053e+01,
  6.03684211e+00, 1.09368421e+01, 8.93157895e+00, 4.73684211e-02,
  0.00000000e+00, 1.01578947e+00, 1.31210526e+01, 1.14210526e+01,
  6.15263158e+00, 1.21421053e+01, 9.70526316e+00, 2.10526316e-01,
  0.00000000e+00, 8.42105263e-02, 4.16842105e+00, 1.27631579e+01,
  1.46157895e+01, 1.12315789e+01, 3.01052632e+00, 2.63157895e-02,],
 [0.00000000e+00, 1.50093809e-01, 4.93245779e+00, 1.27636023e+01,
  1.19887430e+01, 4.73921201e+00, 3.20825516e-01, 0.00000000e+00,
  9.38086304e-03, 1.52720450e+00, 1.08180113e+01, 1.29756098e+01,
  1.25084428e+01, 1.01163227e+01, 1.38836773e+00, 0.00000000e+00,
  2.62664165e-02, 2.37523452e+00, 1.05778612e+01, 1.05215760e+01,
  1.16960600e+01, 9.15009381e+00, 1.28893058e+00, 0.00000000e+00,
  7.50469043e-03, 1.36022514e+00, 9.15196998e+00, 1.43095685e+01,
  1.37636023e+01, 5.87617261e+00, 4.99061914e-01, 0.00000000e+00,
  0.00000000e+00, 5.79737336e-01, 7.87617261e+00, 1.51651032e+01,
  1.27054409e+01, 3.78236398e+00, 2.68292683e-01, 0.00000000e+00,
  0.00000000e+00, 7.99249531e-01, 9.65103189e+00, 1.22814259e+01,
  1.20544090e+01, 5.76360225e+00, 4.57786116e-01, 0.00000000e+00,
  9.38086304e-03, 9.02439024e-01, 1.00956848e+01, 1.18536585e+01,
  1.15966229e+01, 8.04502814e+00, 9.84990619e-01, 0.00000000e+00,
  1.87617261e-03, 1.72607880e-01, 5.19699812e+00, 1.27936210e+01,
  1.22307692e+01, 5.75797373e+00, 6.54784240e-01, 3.75234522e-03,],
 [0.00000000e+00, 3.47593583e-02, 4.59893048e+00, 1.32139037e+01,
  1.09572193e+01, 2.62299465e+00, 5.88235294e-02, 0.00000000e+00,
  0.00000000e+00, 1.20588235e+00, 1.30320856e+01, 1.30508021e+01,
  1.22165775e+01, 1.07379679e+01, 7.27272727e-01, 0.00000000e+00,
  0.00000000e+00, 3.91978610e+00, 1.43930481e+01, 4.62032086e+00,
  2.98128342e+00, 1.27326203e+01, 3.29679144e+00, 0.00000000e+00,
  0.00000000e+00, 5.25401070e+00, 1.27700535e+01, 1.64171123e+00,
  3.20855615e-01, 9.18983957e+00, 6.62299465e+00, 0.00000000e+00,
  0.00000000e+00, 5.46524064e+00, 1.19358289e+01, 8.98395722e-01,
  1.47058824e-01, 8.64705882e+00, 7.38502674e+00, 0.00000000e+00,
  0.00000000e+00, 3.34224599e+00, 1.35614973e+01, 1.68449198e+00,
  1.37967914e+00, 1.13716578e+01, 6.46791444e+00, 0.00000000e+00,
  0.00000000e+00, 7.67379679e-01, 1.32192513e+01, 1.05106952e+01,
  1.06122995e+01, 1.34812834e+01, 2.66577540e+00, 0.00000000e+00,
  0.00000000e+00, 1.87165775e-02, 4.62566845e+00, 1.36122995e+01,
  1.33074866e+01, 5.52941176e+00, 1.84491979e-01, 0.00000000e+00,],
 [0.00000000e+00, 5.01597444e-01, 7.84345048e+00, 1.28881789e+01,
  1.39169329e+01, 1.17667732e+01, 3.51757188e+00, 6.70926518e-02,
  9.58466454e-03, 3.23642173e+00, 1.42971246e+01, 1.30415335e+01,
  9.49201278e+00, 8.33226837e+00, 2.59744409e+00, 2.23642173e-02,
  1.59744409e-02, 4.72204473e+00, 1.39105431e+01, 5.82747604e+00,
  1.59424920e+00, 7.02875399e-01, 2.52396166e-01, 3.19488818e-03,
  0.00000000e+00, 4.86581470e+00, 1.40351438e+01, 1.21948882e+01,
  8.42492013e+00, 3.03514377e+00, 3.38658147e-01, 0.00000000e+00,
  0.00000000e+00, 1.50159744e+00, 7.40575080e+00, 8.95207668e+00,
  1.04313099e+01, 7.34824281e+00, 9.07348243e-01, 0.00000000e+00,
  0.00000000e+00, 8.30670927e-02, 8.01916933e-01, 2.93610224e+00,
  8.23961661e+00, 9.54313099e+00, 1.23642173e+00, 0.00000000e+00,
  0.00000000e+00, 4.98402556e-01, 5.52715655e+00, 8.49840256e+00,
  1.21341853e+01, 8.21086262e+00, 5.97444089e-01, 0.00000000e+00,
  0.00000000e+00, 3.92971246e-01, 8.86261981e+00, 1.43546326e+01,
  9.67412141e+00, 2.19488818e+00, 2.87539936e-02, 0.00000000e+00,],
 [0.00000000e+00, 9.72899729e-01, 1.06097561e+01, 1.38292683e+01,
  6.79403794e+00, 8.80758808e-01, 1.08401084e-02, 0.00000000e+00,
  0.00000000e+00, 4.98373984e+00, 1.44010840e+01, 1.27479675e+01,
  1.19728997e+01, 3.33333333e+00, 5.96205962e-02, 0.00000000e+00,
  0.00000000e+00, 4.51761518e+00, 8.27642276e+00, 4.86449864e+00,
  1.14634146e+01, 4.55013550e+00, 1.02981030e-01, 0.00000000e+00,
  0.00000000e+00, 1.14363144e+00, 2.72357724e+00, 5.21951220e+00,
  1.15826558e+01, 3.71815718e+00, 3.79403794e-02, 0.00000000e+00,
  0.00000000e+00, 7.58807588e-02, 1.15176152e+00, 8.40379404e+00,
  1.05555556e+01, 1.87533875e+00, 0.00000000e+00, 0.00000000e+00,
  0.00000000e+00, 2.16802168e-01, 4.23848238e+00, 1.12845528e+01,
  7.65040650e+00, 1.49593496e+00, 3.11653117e-01, 0.00000000e+00,
  0.00000000e+00, 1.42818428e+00, 1.16205962e+01, 1.45962060e+01,
  1.23089431e+01, 1.09945799e+01, 7.27642276e+00, 5.17615176e-01,
  0.00000000e+00, 9.72899729e-01, 1.06856369e+01, 1.40894309e+01,
  1.33089431e+01, 1.25013550e+01, 9.44986450e+00, 1.55826558e+00,],
 [0.00000000e+00, 3.69330454e-01, 6.95464363e+00, 1.33304536e+01,
  1.37213823e+01, 1.15809935e+01, 5.84233261e+00, 9.26565875e-01,
  0.00000000e+00, 1.13390929e+00, 9.46436285e+00, 1.00539957e+01,
  9.69114471e+00, 1.30647948e+01, 7.80993521e+00, 8.05615551e-01,
  0.00000000e+00, 1.02159827e+00, 3.15334773e+00, 1.28941685e+00,
  6.34341253e+00, 1.28444924e+01, 4.69330454e+00, 1.10151188e-01,
  0.00000000e+00, 9.56803456e-01, 4.42116631e+00, 7.16630670e+00,
  1.27105832e+01, 1.25010799e+01, 3.95032397e+00, 4.31965443e-03,
  0.00000000e+00, 1.42332613e+00, 7.96976242e+00, 1.32699784e+01,
  1.51317495e+01, 1.16436285e+01, 4.13390929e+00, 0.00000000e+00,
  0.00000000e+00, 6.63066955e-01, 3.64578834e+00, 1.18596112e+01,
  1.08228942e+01, 3.49892009e+00, 5.93952484e-01, 0.00000000e+00,
  0.00000000e+00, 1.61987041e-01, 4.85529158e+00, 1.33628510e+01,
  5.36717063e+00, 5.37796976e-01, 1.94384449e-02, 0.00000000e+00,
  0.00000000e+00, 3.77969762e-01, 8.21382289e+00, 1.16371490e+01,
  2.03455724e+00, 2.98056156e-01, 2.80777538e-02, 0.00000000e+00,],
 [0.00000000e+00, 0.00000000e+00, 5.30516432e-01, 9.68075117e+00,
  1.08826291e+01, 1.60093897e+00, 0.00000000e+00, 0.00000000e+00,
  0.00000000e+00, 4.22535211e-02, 5.17840376e+00, 1.52910798e+01,
  8.88732394e+00, 1.25352113e+00, 0.00000000e+00, 0.00000000e+00,
  0.00000000e+00, 2.06572770e-01, 1.07464789e+01, 1.23427230e+01,
  1.38967136e+00, 7.51173709e-02, 0.00000000e+00, 0.00000000e+00,
  0.00000000e+00, 1.09859155e+00, 1.32112676e+01, 9.27699531e+00,
  2.38967136e+00, 7.65258216e-01, 4.69483568e-02, 0.00000000e+00,
  0.00000000e+00, 1.82159624e+00, 1.43286385e+01, 1.18638498e+01,
  1.04741784e+01, 7.74647887e+00, 1.74647887e+00, 0.00000000e+00,
  0.00000000e+00, 1.02347418e+00, 1.38075117e+01, 1.22910798e+01,
  9.15492958e+00, 1.10281690e+01, 8.69953052e+00, 2.81690141e-01,
  4.69483568e-03, 2.67605634e-01, 8.47417840e+00, 1.38309859e+01,
  6.82159624e+00, 1.01596244e+01, 1.24647887e+01, 1.30516432e+00,
  0.00000000e+00, 2.34741784e-02, 6.80751174e-01, 8.72769953e+00,
  1.44413146e+01, 1.40234742e+01, 7.78403756e+00, 5.49295775e-01,],
 [0.00000000e+00, 1.44927536e-02, 3.47826087e-01, 4.20289855e+00,
  1.20108696e+01, 1.14601449e+01, 3.21014493e+00, 1.88405797e-01,
  0.00000000e+00, 3.15217391e-01, 4.27898551e+00, 1.05181159e+01,
  1.25615942e+01, 1.28586957e+01, 5.42753623e+00, 3.33333333e-01,
  0.00000000e+00, 1.84420290e+00, 9.46739130e+00, 1.10289855e+01,
  1.14202899e+01, 1.26159420e+01, 4.17028986e+00, 1.05072464e-01,
  0.00000000e+00, 3.72463768e+00, 1.21666667e+01, 1.25326087e+01,
  1.36159420e+01, 1.28260870e+01, 3.51811594e+00, 0.00000000e+00,
  0.00000000e+00, 2.16666667e+00, 6.67391304e+00, 7.39130435e+00,
  1.19275362e+01, 1.23695652e+01, 2.00724638e+00, 0.00000000e+00,
  0.00000000e+00, 2.64492754e-01, 9.27536232e-01, 2.88043478e+00,
  1.24347826e+01, 1.08840580e+01, 7.57246377e-01, 0.00000000e+00,
  0.00000000e+00, 2.53623188e-02, 2.60869565e-01, 4.07246377e+00,
  1.38949275e+01, 9.27173913e+00, 8.80434783e-01, 0.00000000e+00,
  0.00000000e+00, 0.00000000e+00, 2.10144928e-01, 4.73913043e+00,
  1.13007246e+01, 7.61231884e+00, 1.28260870e+00, 0.00000000e+00,],
 [0.00000000e+00, 0.00000000e+00, 1.63461538e-01, 5.64423077e+00,
  1.21250000e+01, 2.59294872e+00, 2.43589744e-01, 9.29487179e-02,
  0.00000000e+00, 3.20512821e-03, 1.89423077e+00, 1.20064103e+01,
  9.84935897e+00, 1.78846154e+00, 1.60256410e+00, 3.36538462e-01,
  0.00000000e+00, 3.65384615e-01, 7.51923077e+00, 1.27051282e+01,
  3.94230769e+00, 5.09935897e+00, 4.60897436e+00, 3.42948718e-01,
  0.00000000e+00, 3.23397436e+00, 1.32179487e+01, 8.23397436e+00,
  4.01602564e+00, 1.15032051e+01, 6.28525641e+00, 3.20512821e-02,
  1.60256410e-02, 7.37820513e+00, 1.50544872e+01, 9.81089744e+00,
  1.12660256e+01, 1.49423077e+01, 5.09294872e+00, 0.00000000e+00,
  3.36538462e-01, 7.16025641e+00, 1.15288462e+01, 1.18717949e+01,
  1.51025641e+01, 1.25801282e+01, 1.92307692e+00, 0.00000000e+00,
  1.98717949e-01, 2.16987179e+00, 3.49358974e+00, 7.10897436e+00,
  1.46826923e+01, 6.10897436e+00, 2.50000000e-01, 0.00000000e+00,
  0.00000000e+00, 3.20512821e-02, 2.59615385e-01, 6.59294872e+00,
  1.25064103e+01, 2.61538462e+00, 3.20512821e-03, 0.00000000e+00,],
 [0.00000000e+00, 4.55696203e-01, 7.55569620e+00, 1.37911392e+01,
  1.25202532e+01, 4.80379747e+00, 4.31645570e-01, 1.64556962e-02,
  0.00000000e+00, 3.40632911e+00, 1.34924051e+01, 9.55316456e+00,
  1.10797468e+01, 1.01962025e+01, 1.21772152e+00, 5.06329114e-03,
  0.00000000e+00, 3.23291139e+00, 8.65949367e+00, 4.68101266e+00,
  9.86455696e+00, 1.04455696e+01, 1.31265823e+00, 0.00000000e+00,
  0.00000000e+00, 1.18227848e+00, 6.72405063e+00, 1.11151899e+01,
  1.34443038e+01, 9.90506329e+00, 1.63797468e+00, 0.00000000e+00,
  0.00000000e+00, 1.32911392e-01, 2.47974684e+00, 6.39746835e+00,
  9.12405063e+00, 1.24949367e+01, 3.91898734e+00, 0.00000000e+00,
  0.00000000e+00, 1.86075949e-01, 1.70126582e+00, 8.91139241e-01,
  2.21772152e+00, 1.18962025e+01, 7.17721519e+00, 1.01265823e-02,
  0.00000000e+00, 8.54430380e-01, 7.71518987e+00, 6.25063291e+00,
  6.86202532e+00, 1.31898734e+01, 6.51772152e+00, 8.22784810e-02,
  0.00000000e+00, 3.73417722e-01, 8.02784810e+00, 1.40911392e+01,
  1.35177215e+01, 8.94303797e+00, 1.98227848e+00, 1.01265823e-01]])
#print('centroids:\n{}'.format(centroids))
### Copy and paste number of classes per cluser from training results file into array
num_per_cluster = np.array(
[[  1.,   0.,   1.,   0.,   3.,   1., 177.,   0.,   6.,   0.],
 [  1., 218.,  11.,  11.,   3.,   6.,   1.,   7., 270.,   4.],
 [372.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.,   0.],
 [  0.,   0.,   0.,   6.,   6., 294.,   0.,   0.,   2.,   4.],
 [  0.,  15., 345.,   6.,   0.,   0.,   1.,   0.,   1.,   0.],
 [  0.,   3.,  10.,  12.,  32.,   0.,   0., 374.,   5.,  26.],
 [  0.,   6.,   0.,   0.,   5.,   0., 198.,   0.,   3.,   0.],
 [  1., 136.,   0.,   5.,  28.,   4.,   0.,   6.,   4.,  91.],
 [  1.,   0.,   0.,   0., 310.,   0.,   0.,   0.,   0.,   0.],
 [  0.,  11.,  13., 349.,   0.,  71.,   0.,   0.,  88., 257.]])
##print('centroids:\n{}'.format(centroids))

####### Classify test data
##### Assign the most common class to each cluster center
#for i in range(len(centroids)):
#    print('The most common class in cluster {} is {}'\
#            .format(centroids[i], np.argmax(num_per_cluster[i])))
to_remove = [] # centroids to remove because they are empty
cluster_labels = [-1] * len(centroids) # most common class in each cluster
for i in range(len(centroids)):
    most_common = np.max(num_per_cluster[i])
    #print('i = {}, num_per_cluster = {}, most_common = {}'.format(i, num_per_cluster[i], most_common))
    if (most_common == 0): # empty cluster
        to_remove.append(i)
    else:
        # get list of indices for most common labels in cluster
        indices = [j for (j,x) in enumerate(num_per_cluster[i]) if x == most_common]
        #print('indices: {}'.format(indices))
        # randomly select one label to apply to cluster for assignment in test phase
        cluster_labels[i] = random.choice(indices)
        #print('i = {}, cluster_labels: {}\n'.format(i, cluster_labels))
        #cluster_labels[i] = np.argmax(num_per_cluster[i]) # always picks the first label, biased
#cluster_labels = [np.argmax(x) for x in num_per_cluster if np.max(x) != 0]
# ^^^ Doesn't work because it doesn't flag empty clusters, they just disappear
#       and indices get squashed together
##print('to_remove: {}'.format(to_remove))
##print('cluster_labels: {}'.format(cluster_labels))

### Remove empty centroids
for i in to_remove:
    centroids = np.delete(centroids, i, axis=0)
    del cluster_labels[i]
##print('centroids after removing empties :\n{}'.format(centroids))
##print('cluster_labels: {}'.format(cluster_labels))

##### Load test data
data = np.loadtxt(data_file, delimiter=',')
data = data.astype(int) #TODO: Remove and use \/\/ if data is all integers, I think it is

# Initialize representation of data
dimensions = data.shape[1]-1
examples = [ Example(x[:dimensions], x[dimensions]) for x in data ]
##print('examples:\n{}'.format(examples))

##### Assign test data to clusters
cluster_membership = np.array([])
min_distance = np.array([])
clusters = [[None]]*num_clusters
cluster_empty = [True]*num_clusters

for ex in examples:
    #print ex
    distance_to_centroids = np.array([])
    for i in range(centroids.shape[0]):
        distance_to_centroids = np.append(distance_to_centroids, ex.distance(centroids[i]))
    #cluster_index = distance_to_centroids.argmin()
#TODO: Make sure class labels are assigned correctly, not just based on indices
    ex.assigned_label = cluster_labels[distance_to_centroids.argmin()]
    #print('cluster_index = {}'.format(cluster_index))
    if (cluster_empty[ex.assigned_label]):
        cluster_empty[ex.assigned_label] = False
        clusters[ex.assigned_label] = [ex.point]
    clusters[ex.assigned_label].append(ex.point)

    # Debugging signals
    #min_distance = np.append(min_distance, distance_to_centroids[cluster_index])
    cluster_membership = np.append(cluster_membership, ex.assigned_label)
##print('clusters:\n{}'.format(clusters))

##print('examples:\n{}'.format(examples))

####### Calculate performance metrics
##### Calculate accuracy
#num_correct = 0.0
#for i in range(len(examples)):
#    if assigned_labels[i] == true_classes[i]:
#        num_correct += 1

#num_correct = 0.0
#for ex in examples:
#    if (ex.assigned_label == ex.true_class):
#        num_correct += 1
#accuracy = num_correct / len(examples)

num_correct = [x for x in examples if x.true_class == x.assigned_label]
accuracy = float(len(num_correct)) / len(examples)
print('accuracy = {}'.format(accuracy))

##### Create confusion matrix
#assigned_labels = [x.assigned_label for x in examples]
#true_classes = [x.true_class for x in examples]

##### Confusion Matrices #####
# N.B. Confusion matrix code modified primarily from a Stack Overflow thread[1] and other sources:
# [1] https://stackoverflow.com/questions/5821125/how-to-plot-confusion-matrix-with-string-axis-rather-than-integer-in-python
# [2] https://stackoverflow.com/questions/37511277/how-to-plot-confusion-matrix-with-gridding-without-color-using-matplotlib

conf_arr = np.zeros((num_classes,num_classes))
for ex in examples:
    conf_arr[ex.true_class][ex.assigned_label] += 1
print('conf_arr:\n{}'.format(conf_arr))

### Plain confusion matrix
norm_conf = []
for i in conf_arr:
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

height, width = conf_arr.shape
offset = .5 #[2]
ax.set_xlim(-offset, width - offset) #[2]
ax.set_ylim(-offset, height - offset) #[2]

ax.hlines(y=np.arange(height+1) - offset, xmin=-offset, xmax=width - offset) #[2]
ax.vlines(x=np.arange(width+1) - offset, ymin=-offset, ymax=height - offset) #[2]

for i,j in ((x,y) for x in xrange(len(conf_arr))
                  for y in xrange(len(conf_arr[0]))):
    ax.annotate(str(int(conf_arr[i][j])), xy=(j,i), ha='center', va='center')

plt.gca().invert_yaxis()
plt.title('Confusion Matrix for OptDigits dataset', y=1.14)
plt.ylabel("Actual Class")
#fig.show() # toggle to your preference
plt.savefig('output/confusion_matrix_plain.png')


### Colored Heat Map confusion matrix
norm_conf = []
for i in conf_arr:
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
plt.title('Heatmap Confusion Matrix for OptDigits dataset', y=1.14)
ax.set_xlabel("Predicted Class")
plt.ylabel("Actual Class")
ax.xaxis.set_label_position('top')
ax.xaxis.set_ticks(np.arange(0, 10, 1))
ax.yaxis.set_ticks(np.arange(0, 10, 1))
res = ax.imshow(np.array(conf_arr), cmap=plt.cm.jet, interpolation='nearest')

width, height = conf_arr.shape
# Annotates with numbers
for x in xrange(width):
    for y in xrange(height):
        ax.annotate(str(int(conf_arr[x][y])), xy=(y,x), ha='center', va='center')

cb = fig.colorbar(res)
cb.set_label("Occurrences")
#fig.show() # toggle to your preference
plt.savefig('output/confusion_matrix_heatmap.png')
# End Stack Overflow code


####### Visualize clusters
### After writing file: view with GIMP, zoom in, take screenhsot, :(
### Visualize centroids
# Create directory for program output
if not os.path.exists('output/visualizations'):
    os.makedirs('output/visualizations')

### Values range 0 - 16
# format centroid vectors and write to file
count = 0
#for i in range(num_clusters):
for c in centroids:
    with open('output/visualizations/tens_'+str(count)+'.pgm', 'w') as fout:
        # PGM header
        fout.write('P2\n')
        fout.write('8 8\n')
        fout.write('16\n')
        # data
        for i in range(num_features):
            s = str(int(c[i]))
            if ((i+1) % row_length == 0):
                fout.write(s + '\n')
            else:
                fout.write(s + ' ')
    count += 1

### Values range 0 - 160
# format centroid vectors and write to file
count = 0
#for i in range(num_clusters):
for c in centroids:
    with open('output/visualizations/hund_'+str(count)+'.pgm', 'w') as fout:
        # PGM header
        fout.write('P2\n')
        fout.write('8 8\n')
        fout.write('160\n')
        # data
        for i in range(num_features):
            s = str(int(c[i]*10))
            if ((i+1) % row_length == 0):
                fout.write(s + '\n')
            else:
                fout.write(s + ' ')
    count += 1

### Values range 0 - 1600
# format centroid vectors and write to file
count = 0
#for i in range(num_clusters):
for c in centroids:
    with open('output/visualizations/thou_'+str(count)+'.pgm', 'w') as fout:
        # PGM header
        fout.write('P2\n')
        fout.write('8 8\n')
        fout.write('1600\n')
        # data
        for i in range(num_features):
            s = str(int(c[i]*100))
            if ((i+1) % row_length == 0):
                fout.write(s + '\n')
            else:
                fout.write(s + ' ')
    count += 1

