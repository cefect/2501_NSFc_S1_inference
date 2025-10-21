![Docker Image Version (latest)](https://img.shields.io/docker/v/cefect/pytorch-2.6.0-cuda12.4_terratorch?sort=semver&logo=docker)




# small project for replicating Saurabh's S1 inference on HTC



for original version and data transfer, see `l:\05_DATA\_jobs\2501_NSFc\2025 10 03 - Sarubah - S1 inference\readme.md`

## Input data
Requires the sample S1 tiles and lightning checkpoint file provided [here](https://drive.google.com/drive/folders/1oKlLTJPTMpdsd-lasMQc5-YnOs3c0G-i?usp=sharing):
- Example_img\
- epoch-13-val_f1-0.0000_weights.ckpt


## Structure
favouring a modular strategy for improved clarity, re-usability, and testing (vs. monolithic) 

```css
run.sub → run.sh → src/main.py → src/only_inferences_s1.py

```
- **run.sub** submits the job. HTCondor submit file. 
- **run.sh**: configures the shell (conda, variables) and calls the main.py
- **main.py**: python CLI endpoint. digests arguments and sets up python, configures the logging, calls the function
- **only_inferences_s1.py**: source code containing the actual function we run

 


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
### Development
use Dev Container plugin w/ `/.devcontainer/devcontainer.json` to build via `docker-compase.yml`


 
## running on CHTC ------------------------------

### setup
- login via VPN and SSH
- clone repo


### running and managing jobs
- login via VPN and SSH

#### prep 
- copy over input files (to your staging)
```bash
#check your quota
get_quotas /staging/sbryant8

#tarball the input images
#NOTE: no value in tarballing the large checkpoint file
#NOTE: be sure the tarball unpacks in a predictable way
cd /mnt/htc-cephfs/fuse/root/staging/sbryant8/2501_NSFc/s1_infer
tar -czf Example_img ?
```

- update `htcondor/run.sub` to reflect your paths

#### Submit 

```bash
#submit the job
cd /home/sbryant8/LS/09_REPOS/2501_NSFc_S1_inference
condor_submit htcondor/run.sub && condor_watch_q
```

If successful, this should output flood segmentation masks (.tifs) to `$(STAGING_DIR)/output/`.
Various log files should also be generated:
- $(STAGING_DIR)/output/: python debug logger
- $(LOG_BASE).out: STDOUT (run.sh and python logging >= INFO)
- $(LOG_BASE).err: STDERR (run.sh and python logging >= ERROR)
- $(LOG_BASE).htc-log: HTCondor scheduler out



#### Monitor
```bash
#watch the que
condor_watch_q 

#read about holds
condor_q -hold

#cancel jobs
condor_rm -all

#look at some old jobs
condor_history -constraint 'Owner == "sbryant8"' -limit 5
```

#### Tune
```bash
#TUNE: investigate the resources of an old job
#OPT1: just open the log file
#OPT2: 
condor_history 4543341.0 \
  -format "JobID: %d.%d  " ClusterId ProcId \
  -format "Memory: %d MB  " MemoryUsage \
  -format "Disk: %.1f MB\n" '(DiskUsage/1024.0)'

```
