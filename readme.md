# small project for replicating Saurabh's S1 inference

for original version and data transfer, see `l:\05_DATA\_jobs\2501_NSFc\2025 10 03 - Sarubah - S1 inference\readme.md`



## Build containers --------

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


 
## running on CHTC ------------------------------

### setup
- login via VPN and SSH
- clone repo


### running and managing jobs
- login via VPN and SSH

#### prep data
```bash

#tarball the inputs
cd /mnt/htc-cephfs/fuse/root/staging/sbryant8/2501_NSFc
tar -czf s1_infer.tar.gz -C . s1_infer


```bash
#submit the job
cd /home/sbryant8/LS/09_REPOS/2501_NSFc_S1_inference
condor_submit htcondor/test.sub
 
 
#watch the que
condor_watch_q 

#read about holds
condor_q -hold

#cancel jobs
condor_rm <id>
condor_rm -all

#look at some old jobs
condor_history -constraint 'Owner == "sbryant8"' -limit 5

#TUNE: investigate the resources of an old job
#OPT1: just open the log file
#OPT2
condor_history 4543341.0 \
  -format "JobID: %d.%d  " ClusterId ProcId \
  -format "Memory: %d MB  " MemoryUsage \
  -format "Disk: %.1f MB\n" '(DiskUsage/1024.0)'

```