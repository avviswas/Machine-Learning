#!/usr/bin/env python
# coding: utf-8

# In[4]:


import sys
import random
import math



#define best split function--------------------------------
def bestsplit(data, labels, col):
    covals = {}
    indicies = []
    rows = 0
    minus = 0
    for i in range(0, len(data), 1):
        if(labels.get(i) != None):
            covals[i] = data[i][col]
            indicies.append(i)
            rows += 1
            if(labels[i] == 0):
                minus += 1
    sorted_indicies = sorted(indicies, key=covals.__getitem__)

    lsize = 1
    rsize = rows - 1
    lp = 0
    rp = minus
    if(labels[sorted_indicies[0]] == 0):
        lp += 1
        rp -= 1

    best_s = -1
    bestgini = 10000
    for i in range(1, len(sorted_indicies), 1):
        s = (covals[sorted_indicies[i]] + covals[sorted_indicies[i-1]])/2
        gini = (lsize/rows)*(lp/lsize)*(1 - lp/lsize) +             (rsize/rows)*(rp/rsize)*(1 - rp/rsize)
        if(gini < bestgini):
            bestgini = gini
            best_s = s
        if(labels[sorted_indicies[i]] == 0):
            lp += 1
            rp -= 1
        lsize += 1
        rsize -= 1

    return(best_s, bestgini)


#Read in Data file ------------------------------------
datafile = sys.argv[1]
f = open(datafile)
data = []
i = 0
l = f.readline()

while (l != ''):
    l = l.strip('\n')
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    data.append(l2)
    l = f.readline()
rows = len(data)
cols = len(data[0])
f.close()

#Read in Label File -----------------------------------
labelfile = sys.argv[2]
f = open(labelfile)
trainlabels = {}
n = []
n.append(0)
n.append(0)
l = f.readline()
while(l != ''):
    a = l.split()
    trainlabels[int(a[1])] = int(a[0])
    l = f.readline()
    n[int(a[0])] += 1
f.close()


#Main Part ------------------------------------------------
boots = 100
test_predictions = {}
for i in range(0, rows, 1):
    if(trainlabels.get(i) == None):
        test_predictions[i] = 0

        
        
#Bagging ---------------------------------------------------
for k in range(0, boots, 1):
    i = 0
    boot_data = []
    boot_trainlabels = {}
    while(i < len(data)):
        r = random.randint(0, rows-1)
        if(trainlabels.get(r) != None):
            boot_data.append(data[r])
            boot_trainlabels[i] = trainlabels[r]
            i += 1

    best_split = -1
    best_col = -1
    best_gini = 100000
    for j in range(0, cols, 1):
        [s, gini] = bestsplit(boot_data, boot_trainlabels, j)
        print("Split: ",s, " ", "Gini: ",gini)
        if(gini < best_gini):
            best_gini = gini
            best_split = s
            best_col = j

    m = 0
    p = 0
    for i in range(0, rows, 1):
        if(trainlabels.get(i) != None):
            if(data[i][best_col] < best_split):
                if(trainlabels[i] == 0):
                    m += 1
                else:
                    p += 1
    if(m > p):
        left = -1
        right = 1
    else:
        left = 1
        right = -1

    for i in range(0, rows, 1):
        if(trainlabels.get(i) == None):
            if(data[i][best_col] < best_split):
                test_predictions[i] += left
            else:
                test_predictions[i] += right

print("Output Predictions: ")                
#Print out predictions of missing data 
for i in range(0, rows, 1):
    if(trainlabels.get(i) == None):
        if(test_predictions[i] > 0):
            print("1 ", i)
        else:
            print("0 ", i)


# In[ ]:




