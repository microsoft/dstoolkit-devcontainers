FROM python:3.11.15
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


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
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

# it tends to improve startup time (at the cost of increased installation time)
ENV UV_COMPILE_BYTECODE=1
# This prevents uv from creating venv but instead makes it use the system python in container
ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_PROJECT_FILE=.devcontainer/pyproject.toml

# Changing the default UV_LINK_MODE silences warnings about not being able to use hard links since the cache and sync target are on separate file systems
ENV UV_LINK_MODE=copy
# Install dependencies (as root for simplicity; devuser can still use installed packages)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=src/sample_cpu_project/.devcontainer/uv.lock,target=/src/sample_cpu_project/.devcontainer/uv.lock \
    --mount=type=bind,source=src/sample_cpu_project/.devcontainer/pyproject.toml,target=/src/sample_cpu_project/.devcontainer/pyproject.toml \
    --mount=type=bind,source=src/common/pyproject.toml,target=/src/common/pyproject.toml \
    uv sync --locked --project /src/sample_cpu_project/.devcontainer

# Allow devuser to manage packages at runtime without sudo (e.g. uv add)
RUN chown -R $USERNAME:$USERNAME /usr/local
USER $USERNAME
ENV PATH=$PATH:/home/$USERNAME/.local/bin


