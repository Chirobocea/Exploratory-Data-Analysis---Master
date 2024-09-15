import numpy as np
import json
import numpy as np

with open("/mnt/d/University/EDA/archive/parsed_all_V3.jsonl", "r") as json_file:
    data = json.load(json_file)

data = np.array(data)

np.random.shuffle(data)

total_samples = len(data)
train_split = int(0.8 * total_samples)
val_split = int(0.1 * total_samples) + train_split

train_data = data[:train_split].tolist()
val_data = data[train_split:val_split].tolist()
test_data = data[val_split:].tolist()

with open("/mnt/d/University/EDA/archive/train_V2.jsonl", "w") as json_file:
    json.dump(train_data, json_file, indent=4)

with open("/mnt/d/University/EDA/archive/validation_V2.jsonl", "w") as json_file:
    json.dump(val_data, json_file, indent=4)

with open("/mnt/d/University/EDA/archive/test_V2.jsonl", "w") as json_file:
    json.dump(test_data, json_file, indent=4)
