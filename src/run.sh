#!/bin/bash
# run.sh — launched by HTCondor inside your Docker container
set -Eeuo pipefail

#USE:
# bash ./src/run.sh data/array.txt output.txt

# ---- Keep your job arguments safe; do NOT rely on $1/$2 after conda activation ----
# INPUT="$1"
# OUTPUT="$2"

echo "[INFO] Running in: $PWD"
#ls -R
#echo "[INFO] Args: input='$INPUT'  output='$OUTPUT'"
 
# ----   injects conda to shell
 
#doing this in container
#eval "$(/opt/conda/etc/profile.d/conda.sh shell.bash hook)"
source /opt/conda/etc/profile.d/conda.sh


conda activate base

echo "Conda environment activated"
conda info --envs

# output CUDA capabilities
# Check CUDA capabilities with error handling
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi || echo "[WARNING] nvidia-smi failed"
else
    echo "[WARNING] nvidia-smi not found"
fi

if command -v nvcc &> /dev/null; then
    nvcc --version || echo "[WARNING] nvcc failed"
else
    echo "[WARNING] nvcc not found"
fi

# ---- Run your program ----
echo "Running "

#requires preserve_relative_paths = True
#-u force the stdout and stderr streams to be unbuffered
python -u src/torch_setup.py

echo "Done"