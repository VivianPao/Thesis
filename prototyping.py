
# GOAL: Save dictionary data to JSON file.
# Load dictionary from JSON file

import json

randomList = [1,2,3,4]
with open("info_summary.txt", "w") as f:
    f.write(str(randomList))

# listOfDicts = []
# with open('sample.json', 'w') as f:
    # json.dump(randomList,f)

# Read dictionary from JSON
# with open('sample.json', 'r') as f:
#     sample = json.load(f)
# print(sample)
