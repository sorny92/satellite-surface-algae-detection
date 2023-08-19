from dataset.sample_data import visualize_stack
import reader
import numpy as np

if __name__ == "__main__":
    import sys
    es = reader.EuroSAT(sys.argv[1])
    for e in es:
        print(e[0])
        min_val = np.min(e[0].compute())
        max_val = np.max(e[0].compute())
        visualize_stack(e[0]/max_val)
