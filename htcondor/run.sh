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


# ---- Run your program ----
echo "Running inference script with arguments..."
python -u src/only_inferences_s1.py "$INPUT_DIR" "$CKPT_PATH" "$OUTPUT_DIR"


echo "Done"