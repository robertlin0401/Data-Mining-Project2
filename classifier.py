import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import json, csv

# Build options encoding dictionary.
attributes = json.load(open("attributes.json"))
option_dict = []
for attr in attributes["attributes"]:
    new_dict = {}
    encoder = 0
    for option in attributes["options"][attr]:
        new_dict[option] = encoder
        encoder += 1
    option_dict.append(new_dict)

# Read training data.
data = []
data_reader = csv.reader(open("data.csv", newline=''))
for i in data_reader:
    data.append(i)
data.pop(0)
result = np.array(data).T[-1]

# Pre-process data.
for i in range(len(data)):
    for index, j in enumerate(data[i][:-1]):
        data[i][index] = option_dict[index][j]
    data[i].pop(-1)

# Train the decision tree.
model = DecisionTreeClassifier(random_state=0)
model.fit(data, result)

# Show the training result.
print(tree.export_text(model))
fig = plt.figure(figsize=(25,20))
tree.plot_tree(model, feature_names=attributes["attributes"], class_names=["0", "1"], filled=True)
fig.savefig("decistion_tree.png")
