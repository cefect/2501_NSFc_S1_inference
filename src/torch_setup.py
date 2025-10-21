

import os, glob, math, warnings
import numpy as np
import torch
import torch.nn.functional as F
import rasterio
from rasterio.windows import Window
from terratorch.tasks import SemanticSegmentationTask
import tqdm
import sys


print('start')

print(f"Python version: {sys.version}")
print(f"PyTorch version: {torch.__version__}")
print(f"NumPy version: {np.__version__}")
print(f"Rasterio version: {rasterio.__version__}")
print(f"tqdm version: {tqdm.__version__}")

if torch.cuda.is_available():
    print("CUDA is available.")
    print(f"Number of CUDA devices: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"Device {i}: {torch.cuda.get_device_name(i)}")
else:
    print("CUDA is not available.")


print('end')
