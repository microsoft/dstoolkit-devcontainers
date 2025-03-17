FROM python:3.11.11
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# create non-root user and set the default user
ARG USERNAME=devuser
ARG USER_UID=1010
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # Add sudo support
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*
USER $USERNAME

# make all python tools installed by uv accessible
ENV PATH=$PATH:/home/$USERNAME/.local/bin
# it tends to improve startup time (at the cost of increased installation time)
ENV UV_COMPILE_BYTECODE=1
# This prevents uv from creating venv but instead makes it use the system python in container
ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_PROJECT_FILE=.devcontainer/pyproject.toml
RUN sudo chown -R $USERNAME:$USERNAME /usr/local

# install notebooks related dependencies & python dev tools
COPY notebooks/.devcontainer/pyproject.toml notebooks/.devcontainer/uv.lock ./
RUN uv sync --no-cache --project $UV_PROJECT_FILE --frozen
