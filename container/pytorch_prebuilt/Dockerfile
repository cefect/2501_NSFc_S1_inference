#not tested

# Base: PyTorch + CUDA 12.4 + cuDNN 9 + Conda
FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime
SHELL ["/bin/bash","-lc"]


# Apply your environment.yml directly into base
COPY container/pytorch_prebuilt/environment.yml /tmp/environment.yml

#create a new environment
#NO: can pull lots of packages and occasionally try to replace PyTorch
# RUN conda env create -n conda_env -f /tmp/environment.yml \
#  && conda clean -afy

RUN conda env update -n base -f /tmp/environment.yml && conda clean -afy


# Interactive shells get the conda hooks
RUN echo '. /opt/conda/etc/profile.d/conda.sh' >> /etc/bash.bashrc

ENV PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
WORKDIR /workspace


 
