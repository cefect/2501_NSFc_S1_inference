"""endpoint for CLI"""

# ---- Logging / verbosity control
import os, logging 


LOGLEVEL = os.environ.get("LOGLEVEL", "DEBUG").upper()
LOGFILE = os.environ.get("LOGFILE", "job.log")

from .logr import get_new_file_logger
log = get_new_file_logger(
    logger_name="s1_infer",
    level = getattr(logging, LOGLEVEL, logging.INFO),
    fp=LOGFILE,
)

# Quiet common third-party noise; raise if you want it
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("rasterio").setLevel(logging.INFO)
logging.getLogger("albumentations").setLevel(logging.WARNING)

 
    
import argparse

from .only_inferences_s1 import main

 
parser = argparse.ArgumentParser(description="Inference script for Terratorch SemanticSegmentationTask checkpoints")
parser.add_argument("input_dir", help="Directory containing input .tif/.tiff files")
parser.add_argument("ckpt_path", help="Path to the checkpoint file")
parser.add_argument("output_dir", help="Directory to save output masks")
#parser.add_argument("--overwrite", action="store_true", default=True, help="Overwrite existing output files")

args = parser.parse_args()

main(args.input_dir, args.ckpt_path, args.output_dir,
     log=log)