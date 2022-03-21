'''
Random Graph generation:

This modules has all the function necessaries to create colleration graph for Erdos-Renyi, ring lattice and watts strogattz random small world graph
'''

# importing useful packages
import numpy as np
import networkx as nx
import math



###
#
# Erdos Renyi
#
###

def generate_Erdos_Renyi_correlation_matrix(n, seed=np.nan):
    '''
    Input:
    n -> number of nodes
    seed -> seed for pseudo-random number generation

    Output:
    corr_matrix -> correlation matrix for Erdos Renyi graph
    '''

    # Preallocate output
    corr_matrix=np.zeros([n,n])

    # set seed
    if not np.isnan(seed):
        rng=np.random.default_rng(seed)
    else:
        rng=np.random.default_rng()

    # generate upper triangle
    for i in range(0,n-1):
        for j in range(i+1,n):
            corr_matrix[i,j] = rng.uniform()

    # generate whole matrix
    corr_matrix = corr_matrix+ corr_matrix.transpose()

    return corr_matrix


###
#
# Ring lattice
#
###

def generate_ring_lattice_correlation_matrix(n, seed=np.nan):
    '''
    Input:
    n -> number of nodes
    seed -> seed for pseudo-random number generation

    Output:
    corr_matrix -> correlation matrix for Erdos Renyi graph
    '''

    #max number of indirect edges
    max_edge = n*(n-1)/2

    # preallocate output
    corr_matrix=np.zeros([n,n])

    # set seed
    if not np.isnan(seed):
        rng=np.random.default_rng(seed)
    else:
        rng=np.random.default_rng()


    G=nx.watts_strogatz_graph(n, 2, 0)
    G_adjacency=nx.to_numpy_array(G)
    G_adjacency=np.triu(G_adjacency)
    length=sum(sum(G_adjacency==1))
    G_adjacency[G_adjacency==1]=rng.uniform(1-length/max_edge,1,length)
    a=1-length/max_edge

    corr_matrix+=G_adjacency

    for k in range(1,int(np.floor(n/2))):
        #creo ring lattice con 2*k e 2*(k+1) edges
        G=nx.watts_strogatz_graph(n, 2*k, 0)
        H=nx.watts_strogatz_graph(n, 2*(k+1), 0)
        H_adjacency=nx.to_numpy_array(H)
        G_adjacency=nx.to_numpy_array(G)
        diff_adjacency=H_adjacency-G_adjacency
        diff_adjacency=np.triu(diff_adjacency)
        # prendo la differenza, conto quanti sono
        diff_adjacency=H_adjacency-G_adjacency
        diff_adjacency=np.triu(diff_adjacency)

        length=sum(sum(diff_adjacency==1))
        #faccio unif nella parte nell'intervallo dalla fine del precedente a la porzione di nodi da inserire rispetto al totale
        diff_adjacency[diff_adjacency==1]=rng.uniform(a-length/max_edge,a,length)
        a=a-length/max_edge
        corr_matrix+=diff_adjacency


    return corr_matrix+np.transpose(corr_matrix)



###
#
# Small world
#
###

# auxiliary functions
def old_nodes(old_graph, upper=False):
    n=len(old_graph)
    nodes=np.arange(n)
    col,row=np.meshgrid(nodes,nodes)
    old_nodes=old_graph>0
    if upper:
        return np.logical_and(col>row,old_nodes)
    return old_nodes

def new_nodes(old_graph,new_graph, upper=False):
    n=len(old_graph)
    nodes=np.arange(n)
    col,row=np.meshgrid(nodes,nodes)
    old=old_nodes(old_graph)
    new_nodes=np.logical_and(new_graph>0,np.logical_not(old))
    if upper:
        return np.logical_and(col>row,new_nodes)
    return new_nodes

def possible_nodes(new_graph, upper=False):
    n=len(new_graph)
    nodes=np.arange(n)
    col,row=np.meshgrid(nodes,nodes)
    possible_nodes= new_graph==0
    if upper:
        return np.logical_and(possible_nodes,col>row)
    return possible_nodes

def create_random_small_world_link(old_graph, new_graph,p,rng=0):
    # set seed
    if rng==0:
        rng=np.random.default_rng()

    n=len(old_graph)
    nodes=np.arange(n)
    cols,rows=np.meshgrid(nodes,nodes)

    olds=old_nodes(old_graph, upper=True)
    news=new_nodes(old_graph, new_graph, upper=True)
    possibles=possible_nodes(new_graph, upper=True)
    #shuffled is a np array where we save all the nodes of the newgraph after a shuffle
    shuffled=np.zeros(np.shape(news))
    shuffled[olds]=1
    shuffled[news]=rng.uniform(0,1,len(shuffled[news]))
    shuffled[shuffled>p]=1

    #now i remain with all the nodes I need to change
    for row in range(n):
        for col in range(n):
            if shuffled[row,col]>0 and shuffled[row,col]<1:

                if np.any(possibles[row]):

                    appo_index=rng.integers(0,len(shuffled[possibles[row]]))
                    index=cols[row,possibles[row]][appo_index]

                    shuffled[row,index]=1
                    shuffled[row,col]=0
                    possibles=possible_nodes(shuffled, upper=True)


    return shuffled+np.transpose(shuffled)


def generate_small_world_correlation_matrix(n,p, seed=np.nan):
    max_edge=n*(n-1)/2

    # preallocate output
    corr_matrix=np.zeros([n,n])

    # generate random correlation

    # set seed
    if not np.isnan(seed):
        rng=np.random.default_rng(seed)
    else:
        rng=np.random.default_rng()
        seed=1792 #we put this number as seed

    a=1
    G1=np.zeros([n,n])
    G_adjacency=np.zeros([n,n])

    for k in range(int(np.floor(n/2))):
        #generate closest
        G1=G_adjacency
        G2=closest_nodes(n,dist=k+1).astype(int)#,upper=True)

    #shuffle
        G_adjacency=create_random_small_world_link(G1,G2,p,rng)

        G_appo=np.triu(G_adjacency)-np.triu(G1)

        length=sum(sum(G_appo==1))
        G_appo[G_appo==1]=rng.uniform(a-length/max_edge,a,length)
        a=a-length/max_edge

        corr_matrix+=G_appo
    #creo ring lattice con 2*k e 2*(k+1) edges

    return corr_matrix+np.transpose(corr_matrix)
