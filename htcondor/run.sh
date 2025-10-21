#!/bin/bash
# run.sh — launched by HTCondor inside your Docker container
set -Eeuo pipefail

#USE:
# bash ./htcondor/run.sh input_dir ckpt_path output_dir [--overwrite]

# ---- Keep your job arguments safe; do NOT rely on $1/$2/$3 after conda activation ----
INPUT_DIR="$1"
CKPT_PATH="$2"
OUTPUT_DIR="$3"
 
# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "[INFO] Running in: $PWD"
#echo "[INFO] Args: input_dir='$INPUT_DIR' ckpt_path='$CKPT_PATH' output_dir='$OUTPUT_DIR' "
 
# ----   inject and activate conda
source /opt/conda/etc/profile.d/conda.sh
conda activate base
echo "Conda environment activated"




#Set by CONDOR:
#CUBACORES GOMAXPROCS JULIA_NUM_THREADS MKL_NUM_THREADS NUMEXPR_NUM_THREADS OMP_NUM_THREADS OMP_THREAD_LIMIT OPENBLAS_NUM_THREADS PYTHON_CPU_COUNT ROOT_MAX_THREADS TF_LOOP_PARALLEL_ITERATIONS TF_NUM_THREADS
echo "[INFO] Thread/CPU environment variables:"
echo "CUBACORES: ${CUBACORES:-unset}"
echo "GOMAXPROCS: ${GOMAXPROCS:-unset}"
echo "JULIA_NUM_THREADS: ${JULIA_NUM_THREADS:-unset}"
echo "MKL_NUM_THREADS: ${MKL_NUM_THREADS:-unset}"
echo "NUMEXPR_NUM_THREADS: ${NUMEXPR_NUM_THREADS:-unset}"
echo "OMP_NUM_THREADS: ${OMP_NUM_THREADS:-unset}"
echo "OMP_THREAD_LIMIT: ${OMP_THREAD_LIMIT:-unset}"
echo "OPENBLAS_NUM_THREADS: ${OPENBLAS_NUM_THREADS:-unset}"
echo "PYTHON_CPU_COUNT: ${PYTHON_CPU_COUNT:-unset}"
echo "ROOT_MAX_THREADS: ${ROOT_MAX_THREADS:-unset}"
echo "TF_LOOP_PARALLEL_ITERATIONS: ${TF_LOOP_PARALLEL_ITERATIONS:-unset}"
echo "TF_NUM_THREADS: ${TF_NUM_THREADS:-unset}"

#GPU related
echo "CUDA_VISIBLE_DEVICES: ${CUDA_VISIBLE_DEVICES:-unset}"
echo "NVIDIA_VISIBLE_DEVICES: ${NVIDIA_VISIBLE_DEVICES:-unset}"



# Quiet/lean defaults on cluster
export PROGRESS=0           # our script will read this to disable tqdm
export LOGLEVEL=INFO     # our script will read this for logging level
export LOGFILE=$OUTPUT_DIR/main.log  # our script will read this for logging file
export PYTHONWARNINGS=ignore
export PYTHONOPTIMIZE=1

# Optional: small GDAL cache for many concurrent jobs (MB)
export GDAL_CACHEMAX=256


# ---- Run your program ----
echo "Running inference script with arguments..."
python -O src/main.py "$INPUT_DIR" "$CKPT_PATH" "$OUTPUT_DIR"


echo "Done"