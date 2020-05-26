import sys

import random

#read data file
datafilef=sys.argv[1]
f=open(datafilef)
data = []
i = 0
l = f.readline()


while(l != '') :

    k = l.split()

    b = len(k)

    l2 = []

    for j in range(0, b, 1):

        l2.append(float(k[j]))

        if j == (b-1) :

            l2.append(float(1))  



    data.append(l2)

    l = f.readline()

rows = len(data)

cols = len(data[0])

f.close()

#read label

labelfile=sys.argv[2]

f=open(labelfile)

trainlabels = {}

n = []

n.append(0)

n.append(0)

l = f.readline()

while(l != '') :

    k = l.split()

    if int(k[0]) == 0:

        trainlabels[int(k[1])] = -1

    else:

        trainlabels[int(k[1])] = int(k[0])

    l = f.readline()

    n[int(k[0])] += 1

#initialize w

w = []

for j in range(cols):

    w.append(0)

    w[j] = (0.02 * random.uniform(0,1)) - 0.01

#define function dot_product

def dot_product(list1, list2):

    dp = 0

    refw = list1

    refx = list2

    for j in range (cols):

        dp += refw[j] * refx[j]

    return dp

#gradient descent iteration
flag = 0

k=0

while(flag != 1):

    k+=1

    delf = []

    for i in range(cols):

        delf.append(0)

    for i in range(rows):

        if(trainlabels.get(i) != None):

            dp = dot_product(w, data[i])

            for j in range (cols):

                if(dp*trainlabels.get(i)<1):

                    delf[j]+=-1*data[i][j]*trainlabels.get(i)

                else:

                    delf[j]+=0
    eta_list = [1, .1, .01, .001, .0001, .00001, .000001, .0000001, .00000001, .000000001, .0000000001, .00000000001]
    bestobj = 1000000000000
    for k in range(0, len(eta_list), 1):
        eta = eta_list[k]
        for j in range(0,cols,1):
            w[j] = w[j] - eta*delf[j]
        error = 0.0
        for i in range(rows):
            if (trainlabels.get(i) != None):
                error += max(0, 1 - trainlabels.get(i) * dot_product(w, data[i]))
#compute gradient

        obj = error
        if (obj < bestobj):
            besteta = eta
            bestobj = obj

        for j in range(cols):
            w[j] = w[j] + eta*delf[j]

    print("Besteta=",besteta)
    eta =besteta
    for j in range(cols):
        w[j] =w[j] - eta*delf[j]

    curr_error = 0
    for i in range (rows):
        if(trainlabels.get(i) != None):
            curr_error += max( 0,1-trainlabels.get(i)*dot_product(w,data[i]))

    print(error,k)
    if error - curr_error < 0.001:
        flag = 1
    error = curr_error



normw = 0

for j in range((cols-1)):

    normw += w[j]**2

    print(w[j])



normw = (normw)**0.5

print("||w||=", normw)
d_origin = w[(len(w)-1)]/normw
print(d_origin)



for i in range(rows):

    if(trainlabels.get(i) == None):

        dp = dot_product(w, data[i])

        if(dp > 0):

            print("1",i)

        else:

            print("0",i)
