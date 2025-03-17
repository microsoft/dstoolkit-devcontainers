# leverage multi-stage build and copy python binaries to cuda container
FROM python:3.11.11 as python
FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu24.04
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

# create non-root user and set the default user
ARG USERNAME=devuser
# uid=1000 is already used for ubuntu so use 1010 instead
ARG USER_UID=1010
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME 
USER $USERNAME

# make all python tools installed by uv accessible
ENV PATH=$PATH:/home/$USERNAME/.local/bin
# it tends to improve startup time (at the cost of increased installation time)
ENV UV_COMPILE_BYTECODE=1
# This prevents uv from creating venv but instead makes it use the system python in container
ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_PROJECT_FILE=.devcontainer/pyproject.toml
RUN sudo chown -R $USERNAME:$USERNAME /usr/local

# install project dependencies & python dev tools
COPY src/sample_pytorch_gpu_project/.devcontainer/pyproject.toml src/sample_pytorch_gpu_project/.devcontainer/uv.lock ./
RUN uv sync --no-cache --project $UV_PROJECT_FILE --frozen

# install common module related packages
# This part can be potentially improved by https://docs.astral.sh/uv/concepts/projects/workspaces/#when-not-to-use-workspaces to move away from requirements.txt and gets its own lock file
COPY src/common/requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt --system

RUN az extension add --name ml
