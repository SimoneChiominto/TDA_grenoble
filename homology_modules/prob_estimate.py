'''
Prob_estimate.py 

In this modules, given the means and the variances of distances from a brain network to a small world random graph, 
we evaluate the best estimate for the probability of small world graph 
'''

import numpy as np
from gtda.diagrams import PairwiseDistance
from .random_graph_generation import *
from .from_corr_to_graph import *
from .filtration import *
from .homology_computation import *


'''
here we make the diagrams compatible to be worked by giotto PraiwiseDistance function
'''

def fill_holes(len_to_reach, array_to_fill): # dimension is deduced
    original_len = np.shape(array_to_fill)[0]
    diff = len_to_reach - original_len 
    new = np.ones([diff,3])*array_to_fill[0,2]
    return  np.concatenate((array_to_fill,new), axis = 0)

def len_to_reach(separated_diagrams1,separated_diagrams2):
    a=[len(separated_diagrams1[0][i]) for i in range(len(separated_diagrams1[0]))]
    b=[len(separated_diagrams2[0][i]) for i in range(len(separated_diagrams2[0]))]
    return [max(a[i],b[i]) for i in range(len(a))]


def equalize_and_concatenate(diagrams1, diagrams2):
    separated_diagrams1=separate(diagrams1)
    separated_diagrams2=separate(diagrams2)

    length_array = len_to_reach(separated_diagrams1,separated_diagrams2)
    diagram1_mod=[]
    for i,diagram in enumerate(separated_diagrams1):
        diagram1_mod.append([])
        for dim,dim_diagram in enumerate(diagram):
            diagram1_mod[i].append(fill_holes(length_array[dim],dim_diagram))


    diagram2_mod=[]
    for i,diagram in enumerate(separated_diagrams2):
        diagram2_mod.append([])
        for dim,dim_diagram in enumerate(diagram):
            diagram2_mod[i].append(fill_holes(length_array[dim],dim_diagram))

    diagrams1=[np.concatenate(tuple(diagram)) for diagram in diagram1_mod]
    diagrams2=[np.concatenate(tuple(diagram)) for diagram in diagram2_mod]

    return diagrams1 + diagrams2

'''
 we need to compute diagrams of a wide variety of probabilities for random graph ad save it somewhere
'''
def small_world_simulator(prob,homology_dimensions, costs,seed, n_samples_per_step=100): 

    rng=np.random.default_rng(seed)
    corr_mats=[generate_small_world_correlation_matrix(90,prob,rng.integers(0,100000)) for i in range(n_samples_per_step)]
    diagrams,VR=custom_vietoris_persistance (corr_mats,costs,homology_dimensions,plot=False)

    return diagrams


def compute_distances(brain_diagrams,small_worlds, homology_dimensions,costs,seed):

    distances=np.zeros([len(brain_diagrams),len(small_worlds)])
    variances=np.zeros([len(brain_diagrams),len(small_worlds)])
    for i,brain in enumerate(brain_diagrams):
        for j,small_world in enumerate(small_worlds):
            eq=equalize_and_concatenate([brain],small_world)
            D=PairwiseDistance().fit_transform(eq)
            d=D[0][1:]
            distances[i,j]=np.mean(d)
            variances[i,j]=np.var(d)

    return distances,variances





'''
simple function in the discretized case
'''
def prob_estimates(distances,probs):
    ''' 
    input:
    distances: 2 dimensional is a numpy array, each row are the mean distances from a brain network to all the random graph.
    probs: is the vector of the discretized probabilities where we evaluated the  distances
    '''
    indices=np.argmin(distances, axis=1)
    prob_estimates=probs[indices]
    return prob_estimates




'''
 now we want to make an estimate in a continuous framework
 the idea is to use splines to interpolate the points we have generated
 and find the best point on the splines we have found
'''
from scipy import interpolate
from scipy import optimize

def distance_spline(distances,probs):
    x_pts=probs
    y_pts=distances
    tks= interpolate.splrep(x_pts, y_pts)
    return tks

def optimize_spline(tks,probs):
    fun= lambda x : interpolate.splev(x,tks)
    bounds=(min(probs), max(probs))
    minimum=optimize.minimize_scalar(fun,bounds=bounds, method='bounded')
    return (minimum.x,minimum.fun)









    

