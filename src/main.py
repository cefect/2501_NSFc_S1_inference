"""endpoint for HTC CLI"""

# ---- Logging / verbosity control
import os, logging

#ARGS retrive

LOGLEVEL = os.environ.get("LOGLEVEL", "DEBUG").upper()
LOGFILE = os.environ.get("LOGFILE", "job.log")


from .logr import get_new_file_logger, get_new_console_logger

#console logger should land in .out
log = get_new_console_logger(
    logger = logging.getLogger(),
    level = getattr(logging, LOGLEVEL, logging.INFO),
)

#file logger should land in the output directory
log = get_new_file_logger(
    logger= log,
    level = logging.DEBUG,
    fp=LOGFILE,
)

# Quiet common third-party noise; raise if you want it
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("rasterio").setLevel(logging.WARNING)
logging.getLogger("albumentations").setLevel(logging.WARNING)

 
#parse args==============
import argparse
 
parser = argparse.ArgumentParser(description="Inference script for Terratorch SemanticSegmentationTask checkpoints")
parser.add_argument("input_dir", help="Directory containing input .tif/.tiff files")
parser.add_argument("ckpt_path", help="Path to the checkpoint file")
parser.add_argument("output_dir", help="Directory to save output masks")
#parser.add_argument("--overwrite", action="store_true", default=True, help="Overwrite existing output files")

args = parser.parse_args()


# Import and run main function===================
from .only_inferences_s1 import main

main(args.input_dir, args.ckpt_path, args.output_dir,log=log)


#WRAP==============
log.info("Inference completed.")