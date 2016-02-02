import pandas as pd 
import numpy as np 
from sklearn import manifold

def run_mds(distance_matrix, top_sim):
	# filter distance matrix for the top podcasts
	sub_matrix = distance_matrix[top_sim.index, :][:, top_sim.index]

	# run mds 
	mds = manifold.MDS(dissimilarity="precomputed")
	mds2d = mds.fit(sub_matrix).embedding_

	# add mds coords to df 
	top_sim['x_coord'] = mds2d[:,0].tolist()
	top_sim['y_coord'] = mds2d[:,1].tolist()

	return top_sim