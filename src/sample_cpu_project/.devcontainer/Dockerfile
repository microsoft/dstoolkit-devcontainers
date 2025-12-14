FROM python:3.11.14
# create non-root user and set the default user
ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Add sudo support (using BuildKit cache mounts to speed up rebuilds)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME

# Make pip-installed tools accessible
ENV PATH=$PATH:/home/$USERNAME/.local/bin

# Install Python packages (using BuildKit cache mounts for faster rebuilds)
RUN --mount=type=cache,target=/pip-cache \
    pip install --cache-dir=/pip-cache pip --upgrade

COPY src/sample_cpu_project/.devcontainer/requirements.txt .
RUN --mount=type=cache,target=/pip-cache \
    pip install --cache-dir=/pip-cache -r requirements.txt

# Install common module related packages
COPY src/common/requirements.txt common-requirements.txt
RUN --mount=type=cache,target=/pip-cache \
    pip install --cache-dir=/pip-cache -r common-requirements.txt

# Install development tools (linters, formatters, test runners, etc.)
COPY requirements-dev.txt .
RUN --mount=type=cache,target=/pip-cache \
    pip install --cache-dir=/pip-cache -r requirements-dev.txt


