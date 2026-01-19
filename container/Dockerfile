#pytorch base extended with miniconda (rasterio + terratorch)
#USE===================
#need to give access to GPU devices w/ 
#   `docker run -it --rm --gpus all`
# OR
#   compose, deploy,resources, reservationse...



# Base: PyTorch + CUDA 12.4 + cuDNN 9 + Conda
FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime AS base
SHELL ["/bin/bash","-lc"]


# use conda
#NO! this will downgrade pytorch to cpu only
# Apply your environment.yml directly into base
#COPY container/pytorch_prebuilt/environment.yml /tmp/environment.yml

#create a new environment
#NO: can pull lots of packages and occasionally try to replace PyTorch
# RUN conda env create -n conda_env -f /tmp/environment.yml \
#  && conda clean -afy




#simple install of pytorch layered ontop of conda env
# WOrks. MUST SPECIFY terratorch==1.1 (>1.1 has issues with OpenCV)
RUN python -m pip install --no-cache-dir --no-deps terratorch
RUN python -m pip install --no-cache-dir "pip==24.3.1" \
 && python -m pip install --no-cache-dir "terratorch==1.1" "rasterio==1.4.3"

# also doesnt work
# RUN python -m pip install --no-cache-dir --upgrade pip \
#  && python -m pip uninstall -y opencv-python opencv-contrib-python || true \
#  && python -m pip install --no-cache-dir opencv-python-headless \
#  && python -m pip install --no-cache-dir terratorch rasterio


#purge
RUN conda clean -afy



# Interactive shells get the conda hooks
RUN echo '. /opt/conda/etc/profile.d/conda.sh' >> /etc/bash.bashrc

#Ensures logs appear in real time when Docker redirects container output
ENV PYTHONUNBUFFERED=1 

#set CPU cores to 1
#avoids wasting CPU cycles and prevents multiple libraries (MKL, OpenMP, etc.) from all trying to multithread simultaneously.
ENV OMP_NUM_THREADS=2 MKL_NUM_THREADS=1


WORKDIR /workspace


#DEV TOOLS===================================
FROM base AS dev
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*

 # Mark VS Code workspace path as safe to avoid 'dubious ownership' errors
RUN git config --system --add safe.directory /workspace
