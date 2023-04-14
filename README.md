# Dev Containers for ML feasibility study with VS Code

# TODO: this needs better explanation
A comprehensive guide on how to set up a development environment using Dev Containers in Visual Studio Code. This project includes step-by-step instructions on how to install the necessary tools and extensions, how to use SSH keys in Dev Containers, and how to create a new directory under `src` with a new environment.  

Features:

- Easy to follow instructions for setting up a development environment using Dev Containers in Visual Studio Code
- Includes instructions on how to use SSH keys in Dev Containers
- Includes instructions on how to create a new directory under `src` with a new environment
- Saves time and reduces errors by automating the setup process

> This repo has been populated by an initial template to help get you started. Please
> make sure to update the content to build a great experience for community-building.

As the maintainer of this project, please make a few updates:

- Improving this README.MD file to provide a great experience
- Updating SUPPORT.MD with content about this project's support experience
- Understanding the security reporting process in SECURITY.MD
- Remove this section from the README


## Getting Started

### How to setup dev environment?

1. Install [Visual Studio Code](https://code.visualstudio.com/)
1. If your team has a commercial license for Docker Desktop, follow [VS Code Remote Containers | Docker Desktop](https://code.visualstudio.com/docs/remote/containers#_installation). Otherwise, go to [VS Code Remote Containers | Rancher Desktop Docs](https://docs.rancherdesktop.io/how-to-guides/vs-code-remote-containers/) and finish the first step (Install and launch Rancher Desktop. Select dockerd (moby) as the Container Runtime from the Kubernetes Settings menu.)
1. Install [VSCode Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) on vscode
1. Copy `.env.example` and rename it to `.env`. This is where you store your credentials etc. `.env` is automatically loaded into dev container as environment variables. When you add new environment variables `.env`, update `.env.example` as well to share that with others but don't include any credentials there. `.env` is gitignored so your credentials in that file won't be accidentally committed.
1. Run `Dev Containers: Open Folder in Container...` from the Command Palette (F1) and select the `notebooks` directory
1. VS Code will then build and start up a container, connect this window to service `notebooks`, and install VS Code extensions specified in `notebooks/.devcontainer/devcontainer.json`.
1. Run `pre-commit install` in vscode terminal within dev container you just opened. This will setup your git precommit hook. This needs to run only once in the project and you don't need to rerun this every container rebuild.
1. Now set up is done. If you want to develop in another directory for example under `src`, run `Dev Containers: Open Folder in Container...` and go to that directory that has `.devcontainer` and that will setup an dev environment for that directory.
1. When you or others update either `requirements.txt` or `Dockerfile` in your working directory, make sure to rebuild your container to apply those changes to container. Run `Dev Containers: Rebuild and Reopen in Container...` for that.

### Using SSH Keys in Dev Containers

TODO: by Bhavik

If you have connected to the origin repository using SSH authentication, you will need to do a bit of setup to reuse your local SSH key inside a devcontainer automatically, which will allow you to interact with the origin repository (git push, git pull etc.) inside the devcontainer.

1. Try the recommendations in the official docs: https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials
1. If the previous step doesn't work, try the below method, that includes a bit of additional code to add keys to the SSH agent.

Add the following to your ~/.bash_profile or ~/.profile or ~/.zprofile (by default most WSL users will have only a ~/.profile) so an ssh-agent will be started when needed and default keys will be added to the agent. The ssh-agent will then automatically forward keys to your devcontainer when its launched.

```sh
# this part taken from https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials
# check that link for the latest version or updates
if [ -z "$SSH_AUTH_SOCK" ]; then
   # Check for a currently running instance of the agent
   RUNNING_AGENT="`ps -ax | grep 'ssh-agent -s' | grep -v grep | wc -l | tr -d '[:space:]'`"
   if [ "$RUNNING_AGENT" = "0" ]; then
        # Launch a new instance of the agent
        ssh-agent -s &> $HOME/.ssh/ssh-agent
   fi
   eval `cat $HOME/.ssh/ssh-agent`
fi

# ADD SSH Keys to the SSH agent
# if using non-default SSH key, add it to ssh-add command like:
# ssh-add /path/to/your/ssh-key
ssh-add
```

## How to create a new directory under src with a new environment?

1. Copy `src/sample_cpu_project/` under `src` and rename it. If you need gpu environment, base off of `src/sample_pytorch_gpu_project` instead
1. Edit `.devcontainer/devcontainer.json` under the new directory and replace `sample_cpu_project` with the new directory name
1. Edit `.devcontainer/docker-compose.yml` under the new directory and replace `sample_cpu_project` with the new directory name
1. Update `COPY sample_cpu_project/.devcontainer/requirements.txt` in `Dockerfile` with a new path
1. Update other parts of `Dockerfile` if you need
1. Update `requirements.txt` if you need
1. Run `Dev Containers: Open Folder in Container...` from the Command Palette (F1) and select the new directory and make sure you can successfully open the new directory on VS Code running in a container

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
