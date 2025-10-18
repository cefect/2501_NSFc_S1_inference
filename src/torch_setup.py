

import os, glob, math, warnings
import numpy as np
import torch
import torch.nn.functional as F
import rasterio
from rasterio.windows import Window
from terratorch.tasks import SemanticSegmentationTask
from tqdm import tqdm


print('start')

if torch.cuda.is_available():
    print("CUDA is available.")
    print(f"Number of CUDA devices: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"Device {i}: {torch.cuda.get_device_name(i)}")
else:
    print("CUDA is not available.")


print('end')
