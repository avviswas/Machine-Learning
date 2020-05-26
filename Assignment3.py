#!/usr/bin/env python
# coding: utf-8

# In[8]:



import sys
import math
import random 

### Defining Dot Product Function
def dot(w,data):
    ans=0
    for j in range(0,len(w),1):
        ans = ans + w[j]*data[j]
    return ans


### Reading in Data file
datafile =  sys.argv[1]
f = open(datafile)
data = []
i = 0
l = f.readline()

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



### Read Label File 
labelfile =  sys.argv[2]
f = open(labelfile)
trainlabels = {}
l = f.readline()
n=[]
n.append(0)
n.append(0)

while(l != ''):
    a= l.split()
    trainlabels[int(a[1])] = int(a[0])
    if(trainlabels[int(a[1])] == 0):
        trainlabels[int(a[1])] = -1
    l = f.readline()
    n[int(a[0])] += 1
    

w = []
### initalizing w 
for j in range(0,cols):
    w.append(0)
    w[j] = (0.02 * random.uniform(0,1)) - 0.01



#setting eta and stopping condition
### Gradient Decent 
#gradient descent iteration
eta=0.001
stop_condition=.001
error=0
prevobj = 1000000
error = prevobj - 10
dellf = []
for j in range(0, cols):
    dellf.append(0)


while abs(prevobj-error) > stop_condition:
    prevobj=error
    
    #reset dellf to 0
    dellf = [0]*cols

    #compute gradient and error
    error=0

    for i in range (rows):
        if (trainlabels.get(i) != None):
            dp=dot(w,data[i])
            for j in range (cols):
                if((trainlabels[i]*(dp) < 1)):
                    dellf[j] += data[i][j]*trainlabels[i]
                    
                else:
                    dellf[j] += 0

                    
                    
                    
    #update w
    for j in range (cols):
        w[j]+=eta*dellf[j]
    
                   
    for i in range(rows):
        if(trainlabels.get(i) != None):
            dp = dot(w,data[i])
            error += max(0, (1 - (trainlabels[i] * dp)))
    
    print("objective is:", error)
    


print("w = ", w)

#Norm of W
normw = 0
for j in range (0, (cols-1), 1):
    normw += w[j]**2
    print(f'w{j}: {abs(w[j])}')
    
normw = math.sqrt(normw)
origin_distance = abs(w[len(w)-1]/normw)
print ("Distance from Origin= ", origin_distance)


for i in range (0, rows):
    if (trainlabels.get(i) == None):
        dp = 0
        for j in range (0, cols):
            dp += data[i][j]*w[j]
        if dp > 0:
            print ("1,", i)
        else:
            print ("0,", i)


# In[ ]:




