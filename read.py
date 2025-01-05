import pickle
import os
import numpy as np

# Change to your working directory
os.chdir('E:\\data works\\nse_data')
filename = 'ordered_filtered_120.pkl'

# Open a text file to store the output
with open('playersChoices.txt', 'w') as output_file:
    with open(filename, 'rb') as file:
        data = pickle.load(file)

        # Iterate over elements with index using np.ndenumerate
        for index, value in np.ndenumerate(data):
            output = f"Index {index}: {value}\n"
            output_file.write(output)  # Write to the file instead of printing

print("Output saved to playerChoices.txt")
