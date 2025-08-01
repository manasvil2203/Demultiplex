#!/usr/bin/env python
import matplotlib.pyplot as plt

labels = ['Matched(91.33%)', 'Hopped(0.19%)', 'Unknown(8.47%)']
sizes = [91.33, 0.19, 8.47]
colors = ['green', 'yellow', 'red']   

# Plot
plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, colors=colors,startangle=90)
plt.title("Proprtion of records")
plt.axis('equal')
plt.savefig('piechart.png')
plt.close() 


#Heatmap

import numpy as np

matrix = []
index_names = []

with open("./RESULTS/matrix.txt", "r") as f:
    lines = f.readlines()

# First line = column headers...so we shall skip ittttt
for line in lines[1:]:
    parts = line.strip().split()         # Splits on any whitespace
    row_label = parts[0]                 # First item = row index
    index_names.append(row_label)        # Save the row label
    row_values = list(map(int,parts[1:]))  # Convert rest of line to integers
    matrix.append(row_values)

matrix = np.array(matrix)
    
#Heatmap
fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(matrix, cmap = "plasma", norm = "log")

# Show all ticks and label them with the respective list entries
ax.set_xticks(range(len(index_names)), labels=index_names,
              rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticks(range(len(index_names)), labels=index_names)

plt.colorbar(im, ax=ax)
ax.set_title("Log Heatmap of Index Combination Counts")
fig.tight_layout()
plt.savefig("heatmap.png")





















































