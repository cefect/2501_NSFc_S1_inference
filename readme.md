# small project for replicating Saurabh's S1 inference

for original version and data transfer, see `l:\05_DATA\_jobs\2501_NSFc\2025 10 03 - Sarubah - S1 inference\readme.md`



## Build containers

using `--target deploy` for base deployment
on top of this, we layer `--target dev` with additional tools useful for development. 

### Deployment

from wsl:
```bash
#build the container (for deployment... `dev` target is only used by Dev Container plugin)
docker build -f container/Dockerfile -t cefect/pytorch-2.6.0-cuda12.4_terratorch:v0 --target deploy .

# push
docker push cefect/pytorch-2.6.0-cuda12.4_terratorch:v0 

#test (locally)
docker run -it --rm --gpus all \
  -v $(pwd)/src:/workspace/src \
  cefect/pytorch-2.6.0-cuda12.4_terratorch:v0 \
  bash -lc "python /workspace/src/torch_setup.py"
 
```
### Dev
use Dev Container plugin w/ `/.devcontainer/devcontainer.json` to build via `docker-compase.yml`


 
