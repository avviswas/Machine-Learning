#!/usr/bin/env python
# coding: utf-8

# In[4]:


import sys
import math

datafile = sys.argv[1]
f = open(datafile)
data = []
i = 0
l = f.readline()

####to read data

while(l != ''):
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    data.append(l2)
    l = f.readline()
    
rows = len(data)
cols = len(data[0])
f.close

### Read label file 
labelfile = sys.argv[2]
f = open(labelfile)
trainlabels = {}
n = []
n.append(0)
n.append(0)
l = f.readline()

#Count total number of records
while(l != ''):
    a= l.split()
    trainlabels[int(a[1])] = int(a[0])
    l = f.readline()
    n[int(a[0])] += 1
    
    
m0 = []
for j in range(0, cols, 1):
    m0.append(.1)
    
m1 = []
for j in range(0, cols, 1):
    m1.append(.1)
    
#find sums of both dataset of 0s and 1s   
for i in range(0, rows, 1):
    if(trainlabels.get(i) != None and trainlabels[i] == 0):
        for j in range(0, cols, 1):
            m0[j] = m0[j] + data[i][j]
            
    if(trainlabels.get(i) != None and trainlabels[i] == 1):
        for j in range(0, cols, 1):
            m1[j] = m1[j] + data[i][j]

#Find Means
for j in range(0, cols, 1):
    m0[j] = m0[j]/n[0]
    m1[j] = m1[j]/n[1]



s0 = []
s1 = []

for j in range(0, cols, 1):
    s0.append(0)
    s1.append(0)
    

for i in range(rows):
    if(trainlabels.get(i) != None and trainlabels[i] == 0):
        for j in range(0, cols, 1):
            s0[j] += (data[i][j] - m0[j]) ** 2
        
    
    if(trainlabels.get(i) != None and trainlabels[i] == 1):
        for j in range(0, cols, 1):
            s1[j] += (data[i][j] - m1[j]) ** 2
            

for i in range(cols):
    s0[i] = s0[i]/ n[0]
    s1[i] = s1[i]/ n[1]
    
for i in range(0, rows, 1):
    if(trainlabels.get(i) == None):
        d0 = 0
        d1 = 0
        for j in range( 0, cols, 1):
            d0 = d0 + ((data[i][j] - m0[j])**2 / (s0[j]))
            d1 = d1 + ((data[i][j] - m1[j])**2 / (s1[j]))
        
        if(d0 < d1):
            print("0", i)
        
        else:
            print("1", i)







