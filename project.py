import numpy as np
from sklearn.preprocessing import normalize

def findMaxIndex(a):
    maxValue = a[0]
    index = 0
    for i in xrange(len(a)):
        if a[i] > maxValue:
            maxValue = a[i]
            index = i

    print "MaxValue: "  + str(maxValue)
    return index+1

def equalityCheck(a, b):
    x = a-b
    # return np.sqrt(x.dot(x)) < 0.1
    # print np.linalg.norm(x)
    sum = 0
    for i in xrange(len(x)):
        sum += np.square(x[i])
    # print np.sqrt(sum)
    return np.sqrt(sum) <= 0.0000001

def pageRank(M, maxID):
    r = np.ones((maxID,1))
    r = r/maxID
    rm = np.matrix(r)
    MM = np.matrix(M)
    max_itr = 3000
    r_new = MM*rm
    print np.array_equal(r,r_new)
    itr = 0
    beta = 0.8
    while(~equalityCheck(r, r_new) and itr < max_itr):
        r = np.matrix(r_new)
        #r = r / r.sum(axis=1)
        r_new = beta*MM*r + (1-beta)/maxID
        itr = itr + 1

    print "Number of iterations: " + str(itr)
    print r
    print r_new
    return r_new


def expPageRank(M, maxID):
    # M[:,n] = (np.exp(M[:,n]))
    # print M
    M_big = np.zeros((maxID, maxID))
    for elm in M:
        M_big[int(elm[1])-1][int(elm[0])-1] = np.exp(elm[2])

    beta = []
    #Normalizing
    for i in xrange(maxID):
        #M_big[:,i] = np.exp(M_big[:,i])
        tot = np.sum(M_big[:,i])
        #print tot
        if tot != 0:
            M_big[:,i] = M_big[:,i]/tot
            beta.append(0.8)
        else:
            beta.append(0)

    r = pageRank(M_big, maxID)
    print "Index: " + str(findMaxIndex(r))
    np.savetxt("result.csv", r, delimiter=",")


def main():
    # createGraph(4, 'sample_graph.csv')
    M = np.genfromtxt("data.csv", delimiter=',')
    # # Data Verification
    maxID = np.max(M[:,0])
    M = M[:,0:3]
    if np.max(M[:,1]) > maxID:
        maxID = np.max(M[:,1])
    maxID = int(maxID)
    #print maxID
    r = np.zeros((maxID,1))
    r = r/maxID
    PageTrust(M, r)
    # print maxID
    # users = np.zeros((int(maxID)+1, 1))
    # for i in M[:,0]:
    #     users[int(i)] = 1
    #
    # for i in M[:,1]:
    #     if users[int(i)] == 0:
    #         users[int(i)] = 1
    # print np.sum(users)
    # print M
    # exp_ranks = expPageRank(M, maxID)
    # r = np.genfromtxt("result.csv", delimiter=',')
    # x = r/np.sum(r)
    # #print "Max Value: " + str(np.max(x))
    # print "Max Value Index: " + str(findMaxIndex(x))
    # print np.sum(x)

def sumOfAllIncoming(G, r, i):
    dim = G.shape[0]
    sum = 0
    for k in xrange(dim):
        sum = sum + G[i][k]*r[k]
    return sum

def getDenom(A, d, r, beta, z, i):
    dim = A.shape[0]
    sum = 0
    for k in xrange(dim):
        if d[k] != 0:
            sum += A[k][i]*r[k]/d[k] + (1-beta)*z

    return beta*sum

def PageTrust(M, r):
    print "In Page Trust"
    #Initializations
    dim = r.shape[0]
    num_edges = M.shape[0]
    A_plus = np.zeros((dim, dim))
    A_minus = np.zeros((dim, dim))
    d = np.zeros(dim)
    beta = 0.8      #Teleportaion probability
    z = 1.0/dim     #Amout of teleported distribution
    # print num_edges
    for i in xrange(num_edges):
        voter = int(M[i][0])-1
        votee = int(M[i][1])-1
        vote = int(M[i][2])

        if vote >= 0:
            A_plus[voter][votee] = vote/10.0
            d[voter] += 1
        else:
            A_minus[voter][votee] = vote/-10.0

    # Initializing G
    print "Initialzing G"
    G = np.zeros((dim, dim))
    # print G
    for j in xrange(dim):
        for k in xrange(dim):
            if d[k] != 0:
                x = beta*A_plus[k][j]/d[k]
                G[j][k] = x + (1-beta)*z

    #Initializing P
    print "Initializing P"
    P = np.zeros((dim, dim))
    P_tilda = np.zeros((dim, dim))
    for i in xrange(dim):
        for j in xrange(dim):
            if A_minus[i][j] > 0:
                P[i][j] = A_minus[i][j]
                P_tilda[i][j] = A_minus[i][j]

    #Other Initializations
    r_new = np.ones((dim,1))/dim
    # print r
    # print r_new
    iters = 0
    max_iters = 1000
    # print "In the loop"
    # print r_new
    while ~equalityCheck(r, r_new) and iters <= max_iters:
        # print "Iter: " + str(iters)
        r = np.array(r_new, copy=True)
        for i in xrange(dim):
            # print "i: " + str(i)
            r_new[i] = (1-P_tilda[i][i])*sumOfAllIncoming(G, r, i)
            T = np.zeros((dim, dim))
            for j in xrange(dim):
                # print "T (j): " + str(j)
                for k in xrange(dim):
                    if d[k] != 0:
                        neum = beta*r[k]*A_plus[k][j]/d[k] + (1-beta)*z*r[k]
                        # print "Am i here i=" + str(i) + " j=" + str(j) + " k=" + str(k)
                        denom = getDenom(A_plus, d, r, beta, z, j)
                        if denom != 0:
                            T[i][j] = neum/denom
            for j in xrange(dim):
                for k in xrange(dim):
                    P_tilda[i][j] += T[i][k]*P[k][j]

                if A_minus[i][j] > 0:
                    P[i][j] = A_minus[i][j]
                elif i==j:
                    P[i][j] = 0
                else:
                    P[i][j] = P_tilda[i][j]
        # print r_new
        r_new = normalize(r_new)
        iters += 1

    # print r_new
    # print r
    # print np.sum(r_new)
    # print iters

    sorted_indices = sorted(range(dim),reverse=True, key=lambda k: r_new[k])
    # print sorted_indices
    for i in xrange(dim):
        sorted_indices[i] += 1
    np.savetxt("result_PT_values.csv", r_new, delimiter=",")
    np.savetxt("result_PT_indices.csv", sorted_indices, delimiter=",")

def normalize(r):
    # print "Chutyap " + str(r)
    dim = r.shape[0]
    sum = 0
    for x in xrange(dim):
        sum = sum + r[x]
    return r/sum

#Creates graph with n nodes and stores in the specified filename
def createGraph(n, filename):
    nodes = [i for i in xrange(n)]
    nodes = np.array(nodes)
    # print type(nodes)
    f = open(filename, "w")
    for i in xrange(n):
        for j in xrange(n):
            if i != j:
                f.write(str(i+1)+","+str(j+1)+","+str(int(np.random.uniform(-10, 10))) + "\n")
    f.close()

if __name__ == '__main__':
    main()
