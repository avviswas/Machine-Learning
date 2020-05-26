#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[7]:


import sys
import math
import random


# Read Data File -------------------------------------
datafile = sys.argv[1]
f = open(datafile)
data = []
i = 0
l = f.readline()


while (l != ''):
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    data.append(l2)
    l = f.readline()
    data[i].append(1)
    i += 1
rows = len(data)
cols = len(data[0])
f.close()
#print("rows: ", rows, "cols: ", cols)


# Read Labels files in ---------------------------------
label_data = sys.argv[2]
f = open(label_data)
labels = {}

l = f.readline()
while(l != ''):
    a = l.split()
    labels[int(a[1])] = int(a[0])
    l = f.readline()
f.close()


#define dot product function to be used below-------------
def dot_product(refw, refx):
    dot_product = 0
    for j in range(0, cols, 1):
        dot_product += refw[j]*refx[j]
    return dot_product

def sig(a1, b1):
    dp = dot_product(a1, b1)
    sig = 1 / (1 + math.exp(-1 * dp))
    if (sig >= 1):
        sig = 0.999999
    return sig


#Randomly Initialize w to be used below--------------------
w = []
for j in range(0, cols, 1):
    w.append(float(0.02*random.random() - 0.01))


# dellf descent iteration ----------------------------------
# eta = 0.01
eta = 0.001
diff = 1
error = 0
# stop = 0.0000001
stop = 0.001

#compute dellf and error------------------------------------
while (diff > stop):
    dellf = []
    dellf.extend(0 for _ in range(cols))

    for i in range(0, rows, 1):
        if (labels.get(i) != None):
            a = sig(w, data[i]) - labels[i]
            for j in range(0, cols):
                dellf[j] += a * data[i][j]



    #Updating w ----------------------------------------
    for j in range(0, cols, 1):
        w[j] -= eta*dellf[j]

    prevObj = error
    error = 0

    #Computing error------------------------------------
    for i in range(0, rows, 1):
        if (labels.get(i) != None):
            error += -1 * (labels[i] * math.log(sig(w, data[i])) +
                           ((1 - labels[i]) * math.log(1 - sig(w, data[i]))))

        diff = abs(prevObj - error)

    # print(f'diff: {diff}')
    # print("error: ", error)

print(f'w =  {w[0:2]}')



normw = 0
for j in range(0, cols-1, 1):
    normw += w[j]**2


normw = math.sqrt(normw)
print(f'||w|| = {normw}')

origin_distance = w[len(w)-1]/normw
print('distance from origin = ', origin_distance)

# prediction
for i in range(0, rows, 1):
    if (labels.get(i) == None):
        dp = dot_product(w, data[i])
        if dp > 0:
            print("1,", i)
        else:
            print("0,", i)





