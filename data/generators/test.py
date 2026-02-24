import numpy as np


for _ in range(10):
    num_items = min(np.random.geometric(p=0.4),20)
    print(num_items)