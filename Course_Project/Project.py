import sys
import array
import copy
import random
from sklearn import svm



print("Program Started!")


#set size and gamma

size = 0.1
gamma = 0.001

def data_set(feature, data):
    newData = [[row[feature[0]]] for row in data]

    feature.remove(feature[0])
    length = len(feature)
    for _ in range(0, length, 1):
        data_set = [[row[feature[0]]] for row in data]
        newData = [x + y for x, y in zip(newData, data_set)]
        feature.remove(feature[0])
    return newData

#defining pearson correlation
def pearson_correlation(x, y, fi):
    sumX = 0
    sumX2 = 0
    ro = len(x)
    co = len(x[0])
    switch = 0
    pc = array.array("f")
    for i in range(0, co, 1):
        switch += 1
        sumY = 0
        sumY2 = 0
        sumXY = 0
        for j in range(0, ro, 1):
            if (switch == 1):
                sumX += y[j]
                sumX2 += y[j] ** 2
            sumY += x[j][i]
            sumY2 += x[j][i] ** 2
            sumXY += y[j] * x[j][i]
        r = (ro * sumXY - sumX * sumY) / ((ro * sumX2 - (sumX ** 2)) * (ro * sumY2 - (sumY ** 2))) ** (0.5)
        pc.append(abs(r))

    savedforPrinting = array.array("f")
    myFeatures = array.array("i")
    for i in range(0, fi, 1):
        selectedFeatures = max(pc)
        savedforPrinting.append(selectedFeatures)
        featureIndex = pc.index(selectedFeatures)
        pc[featureIndex] = -1
        myFeatures.append(featureIndex)
    return myFeatures

#Set seed
seed = 777
#Split data
def split(data, labels, test_size=size):
    random.seed(seed)
    num_of_test_data = len(data) * test_size
    indicies = random.sample(range(len(data)), int(num_of_test_data))
    x_train = []
    x_test = []
    y_train = []
    y_test = []
    for feat_i in range(len(data)):
        if feat_i not in indicies:
            x_train.append(data[feat_i])
            y_train.append(labels[feat_i])
        else:
            x_test.append(data[feat_i])
            y_test.append(labels[feat_i])
    return x_train, x_test, y_train, y_test






# Reading data file

data_file = sys.argv[1]
data = []
with open(data_file, "r") as file:
    for line in file:
        s = line.split()
        l = array.array("i")
        for i in s:
            l.append(int(i))
        data.append(l)

# Reading labels from file
print("\nReading Data......", end="")
labels = sys.argv[2]
trainlabels = array.array("i")
with open(labels, "r") as file:
    for line in file:
        s = line.split()
        trainlabels.append(int(s[0]))

print("\nReading Data - Completed", end="")


#Setting Feature Count 
feature_count = 15
rows = len(data)
cols = len(data[0])
rows = len(trainlabels)

#Dimension Reduction
print("\nFeature Selection in progress......")
pc_features = pearson_correlation(data, trainlabels, 2000)
print("\nFeature Selection Complete!", end="")

saved_features = copy.deepcopy(pc_features)
updated_data = data_set(pc_features, data)

svc = svm.SVC(gamma=gamma)

accuracy_array = array.array("f")
feature_array = []

accuracy_svm = 0
accuracy_score = 0



print("\n")

#Set Iterations
iterations = 2 
for i in range(iterations):

    print("Iteration# ", i + 1)
    x_train, x_test, y_train, y_test = split(updated_data, trainlabels, test_size=0.3)

    corr_features = pearson_correlation(x_train, y_train, feature_count)

    feature_array.append(corr_features)
    argument = copy.deepcopy(corr_features)

    data_fea = data_set(argument, x_train)

    svc.fit(data_fea, y_train)

    features = pearson_correlation(x_test, y_test, feature_count)

    test_features = data_set(features, x_test)

    len_test_features = len(test_features)
    counter_svm = 0
    my_counter = 0

    for j in range(0, len_test_features, 1):
        svc_predicted_labels = int(svc.predict([test_features[j]]))

        if (svc_predicted_labels >= 3):
            final_predicted_labels = 1
        elif (svc_predicted_labels <= 1):
            final_predicted_labels = 0
        else:
            final_predicted_labels = svc_predicted_labels

        if (svc_predicted_labels == y_test[j]):
            counter_svm += 1

    accuracy_svm += counter_svm / len_test_features
    accuracy_array.append(my_counter / len_test_features)


bestAc = max(accuracy_array)
bestInd = accuracy_array.index(bestAc)
bestFeatures = feature_array[bestInd]

print("\nNumber of Features: ", feature_count)

original_features = array.array("i")
for i in range(0, feature_count, 1):
    realIndex = saved_features[bestFeatures[i]]
    original_features.append(realIndex)

print("\nThe features are: ", original_features)

#Write Features to output file
feature_output = open("Features", "w+")
feature_output.write(str(original_features))


# Calculating Accuracy of the model
feature_copies = copy.deepcopy(original_features)
accuracies = data_set(feature_copies, data)

svc.fit(accuracies, trainlabels)

svm_counter = 0

k = len(accuracies)
for i in range(0, k, 1):
    svc_predicted_labels = int(svc.predict([accuracies[i]]))

    if (svc_predicted_labels <= 1):
        final_predicted_labels = 0
    else:
        final_predicted_labels = svc_predicted_labels

    if (svc_predicted_labels == trainlabels[i]):
        svm_counter += 1

accuracy = svm_counter / k
print("Accuracy: ", accuracy * 100)

# Reading in Test data
testfile = sys.argv[3]
testdata = []
with open(testfile, "r") as file:
    for line in file:
        s = line.split()
        l = array.array("i")
        for i in s:
            l.append(int(i))
        testdata.append(l)

deep_copy = copy.deepcopy(original_features)
updated_test_data = data_set(deep_copy, testdata)

# creating a file
testlabels = open("testLabels", "w+")

for i in range(0, len(updated_test_data), 1):
    lab1 = int(svc.predict([updated_test_data[i]]))
    testlabels.write(str(lab1) + " " + str(i) + "\n")

print("\nPredicted labels file has been created")
print("\nProgram Finished!")

