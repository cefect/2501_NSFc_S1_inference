# small project for replicating Saurabh's S1 inference

for original version and data transfer, see `l:\05_DATA\_jobs\2501_NSFc\2025 10 03 - Sarubah - S1 inference\readme.md`



## Build containers
from wsl:
```bash
#build the container
#docker build -f container/Dockerfile -t cefect/s1_inference:v0 .

docker build -f container/pytorch_prebuilt/Dockerfile -t cefect/s1_inference:torch_v0 .

 


# push
# docker push cefect/usfloods_inference_c1:v0

# #run w/ compose and launch a bash terminal
docker compose -f container/pytorch_prebuilt/docker-compose.yml \
    --project-directory ./ run \
    --rm base /bin/bash

# docker compose -f container/c1_spatial/docker-compose.yml --project-directory ./ \
#     up --detach

# docker compose -f container/c1_spatial/docker-compose.yml down

# #test the head bash script from within the container
# bash 
```

## explore containers
```bash

docker run -it --rm --gpus all cefect/s1_inference:torch_v0 /bin/bash


#vanilla pytorch
docker run -it --rm --gpus all pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime /bin/bash

```

## run (from inside container)
