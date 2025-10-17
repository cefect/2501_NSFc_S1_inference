# CHTC + pytorch + Docker usage

Currently we recommend using “nvidia/cuda” containers with a tag beginning with “12.1.1-devel” for best integration with our system.

## resources/info
- CHTC templates-GPU from [2025-03](https://github.com/CHTC/templates-GPUs/tree/master/ml_workflow) w/ `nvidia/cuda:12.4.1-runtime-ubuntu22.04` and using pip

- CHTC [conda-pytorch recipe from 2024](https://github.com/CHTC/recipes/tree/main/software/Conda/conda-pytorch)

- wiki [Use GPUs](https://chtc.cs.wisc.edu/uw-research-computing/gpu-jobs#a-available-chtc-gpus) says: "Currently we recommend using “nvidia/cuda” containers with a tag beginning with “12.1.1-devel” for best integration with our system."

- wik [Run Machine Learning Jobs](https://chtc.cs.wisc.edu/uw-research-computing/machine-learning-htc.html) says: "we recommend choosing the most recently published image that ends in -runtime."

- image [pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime](https://hub.docker.com/layers/pytorch/pytorch/2.6.0-cuda12.4-cudnn9-runtime/images/sha256-77f17f843507062875ce8be2a6f76aa6aa3df7f9ef1e31d9d7432f4b0f563dee) probably a nice example

## CHTC architecture
looks like ~129 nodes w/ >=12.4

# alternate 