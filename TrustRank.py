'''
Edge weights are passed to f(x) = e^x to determine new edge weights.
For teleportation, seed set(trust set) is chosen as top K elements
that receives least number of negative ratings(edges).
'''

import networkx as nx
import math
import operator
from math import exp

def compute_pageRank(G, seed_set, K):
	
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
	
	itr = 0
	r_new_prime = {}
	while itr < 1000:
		epsilon = 0.0
		S = 0.0

		print '-----------------'
		print "Iteration number", itr
		
		for node in nodes:
			inedges = G.in_edges(node, data='weight')
			
			r_new_prime[node] = 0.0

			for edge in inedges:
				r_new_prime[node] += exp(edge[2]) * r[edge[0]] / d[edge[0]]

			r_new_prime[node] *= B
			S += r_new_prime[node]
		
		ss = q = c = w = 0
		dic = {}
		for node in nodes:
			r_new = r_new_prime[node] + (1.0 - S) / K if (node in seed_set) else r_new_prime[node]
			epsilon += abs(r_new - r[node])
			ss += r[node]
			r[node] = r_new
		
		print 'epsilon = %.11f' % epsilon
		if epsilon < math.pow(10, -10):
			print 'ExitReason: epsilon became too small =', epsilon
			break
		itr+=1
    
	return r

count = {}
G = nx.DiGraph()

f = open("./wsn-db/OTCNet.csv","r")
for l in f:
	ls = l.strip().split(",")
	G.add_edge(ls[0], ls[1], weight = float(ls[2])) #int(float(ls[2]) * 10)) # float(ls[2])) ## the weight should already be in the range of -1 to 1
	
	if '-' in ls[2]:	# rating is negative
		count[ls[1]] = count[ls[1]]+1 if (ls[1] in count) else 1
f.close()

# ascending sort
sorted_count = sorted(count.items(), key=operator.itemgetter(1))

# determine seed set by taking top K elements
K = 1034	# first 1034 entries rated negatively have max 3 times
seed_set = sorted_count[:K]
seed_set, _ = zip(*seed_set)

# r has the rank values
r = compute_pageRank(G, seed_set, K)

# descending sort
sorted_r = sorted(r.items(), key=operator.itemgetter(1), reverse=True)	# key = lambda tuple: tuple(1)


sum = 0
print '\nPageRanks:'
for rank in sorted_r:
	print rank
	sum += rank[1]

print sum
