import numpy as np

num_items = min(np.random.geometric(p=0.4),10)
for _ in range(10):
    print(num_items)