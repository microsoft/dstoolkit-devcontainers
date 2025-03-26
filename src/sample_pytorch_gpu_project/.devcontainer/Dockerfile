# leverage multi-stage build and copy python binaries to cuda-dl-base container
FROM python:3.11.11 as python
FROM nvcr.io/nvidia/cuda-dl-base:24.12-cuda12.6-devel-ubuntu24.04
COPY --from=python /usr/local/ /usr/local/
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update \
    && apt-get install -y \
    wget \
    git \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# install Azure CLI
RUN wget -qO- https://aka.ms/InstallAzureCLIDeb | bash

# uid=1000 is already used as non-root user `ubuntu` so no need to create a new user
ARG USERNAME=ubuntu
# this is required for uv sync not to get permissions errors
RUN chown -R $USERNAME:$USERNAME /usr/local
# delete password of the user
RUN passwd -d $USERNAME
USER $USERNAME

# make all python tools installed by uv accessible
ENV PATH=$PATH:/home/$USERNAME/.local/bin
# it tends to improve startup time (at the cost of increased installation time)
ENV UV_COMPILE_BYTECODE=1
# This prevents uv from creating venv but instead makes it use the system python in container
ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_PROJECT_FILE=.devcontainer/pyproject.toml

# install project dependencies & python dev tools
COPY src/sample_pytorch_gpu_project/.devcontainer/pyproject.toml src/sample_pytorch_gpu_project/.devcontainer/uv.lock ./
RUN uv sync --no-cache --project $UV_PROJECT_FILE --frozen

# install common module related packages
# This part can be potentially improved by https://docs.astral.sh/uv/concepts/projects/workspaces/#when-not-to-use-workspaces to move away from requirements.txt and gets its own lock file
COPY src/common/requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt --system

RUN az extension add --name ml
