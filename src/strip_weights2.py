import torch
import torch, lightning as L
import os

CKPT_PATH   = "/s1_infer/epoch-13-val_f1-0.0000.ckpt"
OUTPUT_DIR  = "/s1_infer"


print("Loading checkpoint")
ckpt = torch.load(CKPT_PATH, map_location="cpu")

print(f'loaded checkpoint keys: {list(ckpt.keys())}')

print("Stripping weights...")

# Accept either {'state_dict': ...} or a raw dict of param->tensor
state = ckpt["state_dict"] if isinstance(ckpt, dict) and "state_dict" in ckpt else ckpt

# If you still have the original big .ckpt, you can also copy its 'hyper_parameters' here.
minimal = {
    "state_dict": state,
    "pytorch-lightning_version": L.__version__,
    "hyper_parameters": ckpt.get("hyper_parameters", {}),  # safe default
}

 


base, ext = os.path.splitext(os.path.basename(CKPT_PATH))
output_path = os.path.join(OUTPUT_DIR, f"{base}_weights{ext}")
torch.save(minimal, output_path)
print(f"Stripped weights saved to: {output_path}")
