#USE: see readme.md
FROM continuumio/miniconda3:main



# Use bash as default shell so conda is available in RUN steps if you need it later.
SHELL ["/bin/bash", "-lc"]

COPY ./environment.yml /tmp/environment.yml

# Prefer strict channels for reproducibility; create a named env
RUN conda env create -n conda_env -f /tmp/environment.yml \
 && conda clean -afy

# set project environment variables
# set these here so they persist across all tools that touch the environment
ENV PYTHONPATH=/workspace  


#copy over the source code
#COPY ./src /workspace/src


# Do NOT set an ENTRYPOINT. HTCondor will run your job's executable
# inside the container; leaving ENTRYPOINT unset avoids surprises.