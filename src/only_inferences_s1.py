#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

working.. but no GPU

2 band. trained w/ Priv3 on flood planet
normalized inputs


Inference-only script for Terratorch SemanticSegmentationTask checkpoints.
- Reads all .tif/.tiff under INPUT_DIR (non-recursive by default).
- Optionally selects specific band indices (0-based).
- Runs on GPU if available.
- Saves single-band uint8 GeoTIFF masks (0/1) aligned to source CRS/transform.

 
"""

# =========================
# CONFIG (edit these only)
# =========================
INPUT_DIR   = "/s1_infer/Example_img"
#CKPT_PATH   = "/s1_infer/epoch-13-val_f1-0.0000.ckpt"
CKPT_PATH   = "/s1_infer/epoch-13-val_f1-0.0000_weights.ckpt"
OUTPUT_DIR  = "/s1_infer/out"

BAND_INDICES   = [0, 1]   # set to None to use all bands; 0-based (e.g., [0,1,2,3,4,5])
BATCH_SIZE     = 4        # images per batch
FLOAT_SCALE    = None     # e.g., 10000.0 if you need to divide inputs by a scale; or None
TILE_DIVISIBLE = 1        # pad H,W to nearest multiple (e.g., 32) for some decoders; 1 = no pad
OUTPUT_COMPRESS = "LZW"   # GeoTIFF compression: "LZW", "DEFLATE", etc.

# Force specific GPU before importing torch/lightning
import os

#silence albumentations logging. 
import logging
logging.getLogger("albumentations").setLevel(logging.WARNING)

#move onto container
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "3"  # change if needed

# =========================
# Imports
# =========================
import glob
import time
from typing import List, Optional

import numpy as np
import torch
import rasterio
from terratorch.tasks import SemanticSegmentationTask
from tqdm import tqdm


# =========================
# Helpers
# =========================
def list_tifs(folder: str) -> List[str]:
    files = sorted(glob.glob(os.path.join(folder, "*.tif")))
    files += sorted(glob.glob(os.path.join(folder, "*.tiff")))
    return files

def read_image_select_bands(path: str, band_indices: Optional[List[int]]):
    """Return np.float32 array of shape (C, H, W)."""
    with rasterio.open(path) as src:
        if band_indices is None:
            arr = src.read()  # (C,H,W), all bands
        else:
            arr = src.read(indexes=[i + 1 for i in band_indices])  # rasterio is 1-based
    return arr.astype(np.float32)

def maybe_pad_to_multiple(t: torch.Tensor, multiple: int):
    """Pad CHW tensor to next multiple of H,W if needed. Returns padded tensor and (origH, origW)."""
    if multiple <= 1:
        return t, t.shape[-2], t.shape[-1]
    _, H, W = t.shape
    padH = (multiple - (H % multiple)) % multiple
    padW = (multiple - (W % multiple)) % multiple
    if padH == 0 and padW == 0:
        return t, H, W
    # Pad (left, right, top, bottom) = (0, padW, 0, padH)
    t = torch.nn.functional.pad(t, (0, padW, 0, padH), mode="reflect")
    return t, H, W

def unpad_to_size(t: torch.Tensor, H: int, W: int):
    """Crop back to original H,W."""
    return t[..., :H, :W]

def save_mask_like(ref_path: str, mask: np.ndarray, out_path: str, compress: str = "LZW"):
    """Save 2D uint8 mask with same geotransform/CRS as ref."""
    mask = mask.astype("uint8")
    with rasterio.open(ref_path) as src:
        profile = src.profile.copy()
        profile.update({
            "count": 1,
            "dtype": "uint8",
            "compress": compress,
        })
        # Ensure dims match our (possibly unpadded) prediction
        profile["width"] = mask.shape[1]
        profile["height"] = mask.shape[0]

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with rasterio.open(out_path, "w", **profile) as dst:
            dst.write(mask, 1)


# =========================
# Main
# =========================
def main(overwrite=True):
    start_time = time.time()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] Device: {device}")

    print(f"[INFO] Loading checkpoint: {CKPT_PATH}")
    # If your ckpt doesn't contain hparams, you can pass model_args=... and model_factory=...
    #model = SemanticSegmentationTask.load_from_checkpoint(CKPT_PATH)
    model = SemanticSegmentationTask.load_from_checkpoint(
            CKPT_PATH,
            map_location="cpu",   # see “hand to GPU?” below
            strict=False           # or False if you changed model keys
        )
    model.eval().to(device)

    img_paths = list_tifs(INPUT_DIR)
    if not img_paths:
        raise FileNotFoundError(f"No .tif/.tiff files found under {INPUT_DIR}")

    print(f"[INFO] Found {len(img_paths)} images.")
    bs = max(1, int(BATCH_SIZE))

    for start in range(0, len(img_paths), bs):
        batch_paths = img_paths[start:start + bs]

        imgs = []
        shapes = []
        for p in batch_paths:
            arr = read_image_select_bands(p, BAND_INDICES)  # (C,H,W) float32
            if FLOAT_SCALE and FLOAT_SCALE > 0:
                arr = arr / float(FLOAT_SCALE)
            t = torch.from_numpy(arr)  # (C,H,W)
            t, origH, origW = maybe_pad_to_multiple(t, TILE_DIVISIBLE)
            shapes.append((origH, origW))
            imgs.append(t)

        batch = torch.stack(imgs, dim=0).to(device)  # (B,C,H,W)

        with torch.inference_mode():
            out = model(batch)
            # Handle different return types
            if hasattr(out, "output"):
                logits = out.output
            elif isinstance(out, dict) and "output" in out:
                logits = out["output"]
            else:
                logits = out  # assume tensor

            preds = torch.argmax(logits, dim=1)  # (B,H,W)

        preds = preds.detach().cpu()
        for i, p in enumerate(tqdm(batch_paths, desc="Saving masks")):
            pred_i = preds[i]
            H, W = shapes[i]
            if (pred_i.shape[-2], pred_i.shape[-1]) != (H, W):
                pred_i = unpad_to_size(pred_i, H, W)

            base = os.path.basename(p)
            out_path = os.path.join(OUTPUT_DIR, base)  # same name, different folder

            if overwrite and os.path.exists(out_path):
                os.remove(out_path)



            save_mask_like(p, pred_i.numpy(), out_path, compress=OUTPUT_COMPRESS)
            print(f"[OK] Saved: {out_path}")

    print(f"[DONE] Predictions saved to: {OUTPUT_DIR}")
    
    end_time = time.time()
    total_runtime = end_time - start_time
    print(f"[RUNTIME] Total execution time: {total_runtime:.2f} seconds")


if __name__ == "__main__":
    main()
