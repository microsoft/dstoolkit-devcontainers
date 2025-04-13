FROM python:3.11.11
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# install Azure CLI
RUN wget -qO- https://aka.ms/InstallAzureCLIDeb | bash
# create non-root user and set the default user
ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # Add sudo support
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*
# some packages try to create new directories in /usr/local/lib/python3.11/site-packages etc during uv sync so permission needs to be granted
RUN chown -R $USERNAME:$USERNAME /usr/local
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
