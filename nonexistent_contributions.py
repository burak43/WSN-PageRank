'''
Edge weights are passed to f(x) = e^x to determine new edge weights. 
Contributions of non-existent edges, i.e. edges between the nodes 
that have no interaction(rating) between them, are also taken into 
account while calculating the PageRanks, i.e. e^0 = 1  is added 
K times to each node n_i, where K = N - num_of_indegree(n_i)
N is total number of nodes in the network.

This is nonsense because line 52 and 67 must consider all other nodes'
rank values which is not implemented below.
'''

import networkx as nx
import math
import operator
from math import exp

#def initialize_scores(G):
#	N = G.number_of_nodes()
#
#	nodes = G.nodes()
#	for node in nodes:
#		fairness[node] = 1
#		try:
#			goodness[node] = G.in_degree(node, weight='weight')*1.0/G.in_degree(node)
#		except:
#			goodness[node] = 0
#	return fairness, goodness

def compute_pageRank(G):
	
 	'''inedge = G.in_edges('1', data='weight')
	for e in inedge:
		print e[2]
	raw_input()'''
	
	#initialize
	N = G.number_of_nodes()
	r = {}	#[1.0/N] * N
	B = 0.85
	d = {}

	nodes = G.nodes()
	for node in nodes:
		r[node] = 1.0 / N
		d[node] = 0.0
		
		outedges = G.out_edges(node, data='weight')
		for edge in outedges:
			d[node] += exp(edge[2])		# edge = ('from_ind', 'to_ind', weight)
		
		# take non-existent edges into account also
		d[node] += N - 1 - len(outedges) # * e^0 (which is 1)
	
	itr = 0
	r_new_prime = {}
	while itr < 1000:
		epsilon = 0.0
		S = 0.0

		print '-----------------'
		print "Iteration number", itr
		
		for node in nodes:
			inedges = G.in_edges(node, data='weight')
			
			# start with non-existent edge's contributions
			r_new_prime[node] = N - 1 - len(inedges) # * e^0 (which is 1) 

			for edge in inedges:
				r_new_prime[node] += exp(edge[2]) * r[edge[0]] / d[edge[0]]

			r_new_prime[node] *= B

			S += r_new_prime[node]
		
		for node in nodes:
			r_new = r_new_prime[node] + (1.0 - B) / N
			epsilon += abs(r_new - r[node])
			r[node] = r_new

		print 'epsilon = %.11f' % epsilon
		if epsilon < math.pow(10, -10):
			print 'ExitReason: epsilon become too small =', epsilon
			break
		itr+=1
    
	return r


G = nx.DiGraph()

f = open("./wsn-db/OTCNet.csv","r")
for l in f:
	ls = l.strip().split(",")
	G.add_edge(ls[0], ls[1], weight = int(float(ls[2]) * 10)) # float(ls[2])) ## the weight should already be in the range of -1 to 1
f.close()

# r has the rank values
r = compute_pageRank(G)

# descending sort
sorted_r = sorted(r.items(), key=operator.itemgetter(1), reverse=True)	# key = lambda tuple: tuple(1)


sum = 0
print '\nPageRanks:'
for rank in sorted_r:
	print rank
	sum += rank[1]

print sum
