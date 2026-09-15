FROM python:3.11.16
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

# Changing the default UV_LINK_MODE silences warnings about not being able to use hard links since the cache and sync target are on separate file systems
ENV UV_LINK_MODE=copy
# Install dependencies using bind mounts instead of COPY to avoid extra layers
# This is the recommended approach by uv: https://docs.astral.sh/uv/guides/integration/docker/#installing-a-project
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked

# Allow devuser to manage packages at runtime without sudo (e.g. uv add)
RUN chown -R $USERNAME:$USERNAME /usr/local
USER $USERNAME
ENV PATH=$PATH:/home/$USERNAME/.local/bin


