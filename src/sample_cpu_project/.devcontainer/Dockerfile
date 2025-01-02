FROM python:3.11.11
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

# make all python tools installed by pip accesible
ENV PATH=$PATH:/home/devuser/.local/bin

RUN pip install --no-cache-dir pip --upgrade

COPY src/sample_cpu_project/.devcontainer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# install common module related pacakages
COPY src/common/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# install python tools
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt


