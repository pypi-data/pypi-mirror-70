# k-mxt-w3
The k-mxt-w3 library contains an implementation of the k-mxt and k-mxt-w algorithms.
Using clustering algorithms can identify clusters on a dataset.

## Installation
```bash
pip install k-mxt-w3
```

## Parameters
 * The larger the parameter k, the more vertices will be in each cluster, and the number of clusters will be less.
 * The eps parameter indicates the maximum distance between the vertices at which these vertices are connected.
 
 ## Usage
 ```python
import k_mxt_w3.clustering_algorithms
import k_mxt_w3.clusters_data
import k_mxt_w3.data
import pandas as pd

filename = 'dataset.csv'
df = pd.read_csv(filename)                                          # reading csv-file data
dataset = k_mxt_w3.data.DataPropertyImportSpace(df=df)
features_list = ['column_x']                                        # list of the dataset columns
x, y, features = dataset.get_data(name_latitude_cols='latitude',    # name of the column containing the latitude values
                                   name_longitude_cols='longitude',  # name of the column containing the longitude values
                                   features_list=features_list)      # list of others
clusters = k_mxt_w3.clusters_data.ClustersDataSpaceFeaturesEuclidean(x_init=x, 
                                                                     y_init=y,
                                                                     features_init=features)  # creating an object 
                                                                                              # containing clusters
alg = k_mxt_w3.clustering_algorithms.K_MXT_gauss(k=5, eps=0.05, clusters_data=clusters)       # creating an object 
                                                                                               # with k=5, eps=0.05
alg()                               # run the clustering algorithm
print(clusters.cluster_numbers)     # print cluster number for each vertex
```
