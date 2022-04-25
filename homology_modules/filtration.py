### FILTRATION.PY
'''
In this module we define all the function about the filtrations.
First we work on the filtration induced by threshold eps, then on nighborhods
'''



import numpy as np
from .from_corr_to_graph import adj_matrix_connected
import networkx as nx
from timeit import default_timer as timer




###
# General use function that gives us a matrix in the format needed to compute the diagrams by giotto tda
###

def from_filtration_to_adjacency(graph_filtration):
  
  # pre allocate output
  # we create an array with non feasible weigth
  adjacency_matrix=np.ones(np.shape(graph_filtration[0]))*(-1)

  # for each graph in the filtration if a new link appears, the weigth is the 
  # number of the filtration.
  for i,graph in enumerate(graph_filtration):
    cond=np.logical_and(adjacency_matrix==-1,graph==1)
    adjacency_matrix[cond]=i
  
  # diagonal entries need to be 0
  adjacency_matrix+= np.identity(np.shape(adjacency_matrix)[0])
  # all non feasible weight becomes infinite 
  adjacency_matrix[adjacency_matrix==-1]=np.inf
  return adjacency_matrix




###
# FILTRATION FROM THE THRESHOLDS
###

def generate_graph_sequence(corr_matrix, costs):

  # input:
  #   correlation matrix: is the correlation matrix where we need to extract 
  #                       using the function provided to us
  #   costs: is the list of cost where we decided to make the filtration
  # output:
  #   graph_sequence: it is a list of numpy matrices, each being an adjacency 
  #                   matrix of a graph of hte filtration
  
  graph_sequence=list()
  for eps in costs:
    graph_sequence.append(adj_matrix_connected(corr_matrix,eps))
  return graph_sequence


###
# NEIGHBORHOOD (not done)
###


###
# New filtration
###

from .c import *

def custom_filtration(adjacency_matrix, homology_dimensions):
    max_dim=max(homology_dimensions)
    np.savetxt("DATA/data1.csv", adjacency_matrix, 
              delimiter = " ")
    FindCliques(max_dim+2, "DATA/data1.csv")
    cliques=[]
    with open ('DATA/cliques.txt') as f:
        for i,line in enumerate(f):
            cliques.append([])
            cliques[i]=line.strip("\n").split(",")
            cliques=[list(map(int,clique)) for clique in cliques]
        cliques = sorted(cliques, key=len)
    
    filtration=[(clique,len(clique)-1) for clique in cliques]
    return filtration
  















