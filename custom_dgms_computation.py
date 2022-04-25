


import pandas as pd
import networkx as nx
import numpy as np
from gtda.diagrams import PairwiseDistance
import pickle
from persim import plot_diagrams
import matplotlib.pyplot as plt
import cechmate as cm
import timeit
from timeit import default_timer as timer

from homology_modules import *
#G=nx.watts_strogatz_graph(90, 4, 0.1,np.random.randint(0,100))
#z=nx.to_numpy_matrix(G)
#print(z)
#filtration=custom_filtration(z,[1])
#print(filtration)    
















print("fine importazioni moduli")
path="regional-differentiation-based-on-graph-nodal-statistics-for-functional-brain-connectivity-networks-characterization/DATA/cor_mat_HCP_90"
files=os.listdir(path) #make a list of all the files' names at the path 
cor_mats_HCP_90_df=[pd.read_csv(path+"/"+file,delim_whitespace=True,header=None) for file in files]

path="regional-differentiation-based-on-graph-nodal-statistics-for-functional-brain-connectivity-networks-characterization/DATA/cor_mat_coma"
files=os.listdir(path) #make a list of all the files' names at the path 
cor_mats_coma_df=[pd.read_csv(path+"/"+file,delim_whitespace=True) for file in files]

cor_mats_HCP_90=[df.to_numpy() for df in cor_mats_HCP_90_df]
cor_mats_coma=[df.to_numpy() for df in cor_mats_coma_df]

print("importati i datasets")
costs=np.linspace(1/44,0.25,10)

#dgms,filtration=custom_filtration_persistance(cor_mats_coma,costs,[1,2])

#with open("data.custom_filtration_coma", "wb") as f:
#    pickle.dump((filtration), f, protocol=pickle.HIGHEST_PROTOCOL)
#with open("data.custom_diagrams_coma", "wb") as f:
#    pickle.dump((dgms), f, protocol=pickle.HIGHEST_PROTOCOL)

