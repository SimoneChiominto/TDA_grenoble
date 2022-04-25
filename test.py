
    
import numpy as np
import networkx as nx
import math
import gtda as gtda
from gtda.homology import VietorisRipsPersistence
from gtda.diagrams import PairwiseDistance
from igraph import Graph
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import os
import pickle    
from homology_modules import *
from persim import plot_diagrams

with open("DATA/data.custom_diagrams_coma","rb") as f:
        custom_dgms_coma=pickle.load(f)

n1=0
n2=6

dgm=custom_dgms_coma[n1][n2]
print(dgm)
plot_diagrams(dgm)
plt.show()

def count_inf(dgm,dim):
        if (len(dgm)<=dim):
                return 0
        out=dgm[dim]
        return len(out[out[:,1]==np.inf])

print(count_inf(dgm,1))
inf0=[[count_inf(dgm,0) for dgm in brain] for brain in custom_dgms_coma]
inf1=[[count_inf(dgm,1) for dgm in brain] for brain in custom_dgms_coma]
inf2=[[count_inf(dgm,2) for dgm in brain] for brain in custom_dgms_coma]
print(inf1)
print(inf2)
print(inf0)
  
#corr_mat=generate_Erdos_Renyi_correlation_matrix(10,0)
#print(corr_mat)    
