import numpy as np
from tqdm import tqdm
import os

def ks2count(src_folder, bin_width = 400):
    times_file = os.path.join(src_folder, 'spike_times.npy')
    clusters_file = os.path.join(src_folder, 'spike_clusters.npy')
    bin_width = 400 # 32000 / 80
    
    times = np.load(times_file).squeeze()
    clusters = np.load(clusters_file).squeeze()
    
    print('times shape:', times.shape)
    print('clusters shape:', clusters.shape)
    assert times.ndim == 1 and clusters.ndim == 1, f'input dim should be 1, but got times {times.ndim} and clusters {clusters.ndim}'
    
    assert times.size == clusters.size, f'dim of times and clusters should be same, but got times {times.shape} and clusters {clusters.shape}'
    
    tgt_dim = (int(np.max(times) // bin_width) + 1, int(np.max(clusters) + 1))
    tgt = np.zeros(tgt_dim)

    for i in tqdm(range(len(times))):
        t, c = times[i], clusters[i]
        tgt[int(t // bin_width), c] += 1
    print('target shape:', tgt.shape)
    return tgt
    
    
    
    
    