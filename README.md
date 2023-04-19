# Dev Containers for ML feasibility study with VS Code

## Overview

This repository provides a VSCode Dev Container based project template that can help accelerate your Machine Learning inner-loop development phase. The template covers the phases from early ML experimentation (local training/testing) till production oriented ML model training (cloud based training/testing with bigger CPUs and GPUs).

During the early phase of Machine Learning project, you may face challenges such as each data scientist creating various different python environments that span across CPU and GPU that tend to have different setup procedures. With the power of Dev Containers, you can automate environment setup process across the team and every data scientist will get the exact same environment automatically. This template provides both CPU and GPU Dev Container setup as examples.

Another challenge you may face is each data scientist creating low quality codebase. That is fine during experimentation stage to keep the team agility high and maximize team’s experimentation throughput. But when you move to model productionization stage, you experience the big burden of bringing the code quality up to production level. With the power of python tools and VSCode extensions configured for this template on top of Dev Containers, you can keep the code quality high automatically without losing team’s agility and experimentation throughput and ease the transition to productionization phase.


### Features

- Multi dev container samples (both CPU and GPU) with many common config steps already configured as following:
  - Automated code quality checks (linter and auto formatter) with black, flake8, isort and bandit on VSCode on save
  - Automated code quality checks (linter and auto formatter) with black, flake8, isort and bandit as precommit hook
  - Zero effort transition from local env to Azure Machine Learning (cloud based env) by leveraging the same Dev Container
  - Pre-configured VSCode extensions installed such as python, jupyter, shellcheck, code-spell-checker, git tools etc
- Github Actions and Azure Devops CI pipelines that run isolated pytest for all Dev Containers under src, including test result reporting and coverage reporting

This template automates all tedious setup process as much as possible and saves time and reduces setup errors for the entire data scientist team.

## Getting Started

This section provides a comprehensive guide on how to set up a development environment using Dev Containers in Visual Studio Code with step-by-step instructions.

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

If you have connected to the origin repository using SSH authentication, you will need to do a bit of setup to reuse your local SSH key inside a Dev Container automatically, which will allow you to interact with the origin repository (git push, git pull etc.) inside the Dev Container.

1. Try the recommendations in the official docs: https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials
1. If the previous step doesn't work, try the below method, that includes a bit of additional code to add keys to the SSH agent.

Add the following to your ~/.bash_profile or ~/.profile or ~/.zprofile (by default most WSL users will have only a ~/.profile) so an ssh-agent will be started when needed and default keys will be added to the agent. The ssh-agent will then automatically forward keys to your Dev Container when its launched.

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

## CI Pipeline

This repository contains various templates for running a CI pipeline on either Azure Devops (under .azuredevops dir) or on Github Actions (under .github dir). Each of the CI pipeline configurations provided have the following features at a high level:
- Run code quality checks including flake8 and bandit over the repository
- Find all subdirectories under src and run all Pytest tests inside the associated Docker containers
- Publish test results and code coverage statistics

We recommend setting up pipeline triggers for PR merging and CI, this will ensure the pipeline runs when a PR is made or updated aswell as when a PR is merged into your main branch. See the sections belows for links on how to do this with Azure Devops and Github Actions.

### Running all unit tests with ci-tests.sh
As multiple independent directories can be added under src, each with its own Dockerfile and requirements, running unit tests for each directory under src needs to be done within the Docker container of each src subdirectory. The ci-tests.sh script automates this task of running all unit tests for the repository with the following steps:
1. Finding all subdirectories under src/ that have at least one test_*.py under a tests folder
2. Building each Docker image for each subdirectory with tests, using the Dockerfile in the associated .devcontainer directory
3. For each subdirectory with tests, running Pytest for all tests inside the matching Docker container built in step 2
4. All test results and coverage reports are combined for each individual src subdirectory that had tests and is made ready for publishing in a CI pipeline

Note that the ci-test.sh can be run locally aswell and it is assumed that all tests are written with Pytest.

### Azure Deveops CI Pipeline
See https://learn.microsoft.com/en-us/azure/devops/pipelines/create-first-pipeline?view=azure-devops for how to setup a pipeline in Azure Devops. Note that to use the provided template in this repository, you will need to specify the path to .azuredevops/ado-ci-pipeline-ms-hosted during the pipeline setup process in Azure Devops.

### Choosing between Azure Devops Microsoft-hosted vs Self-hosted CI Pipeline
There are two templates for running a CI pipeline in Azure Devops, a pipeline configuration that uses a Microsoft hosted agent to run the pipeline (.azuredevops/ado-ci-pipeline-ms-hosted.yml) and a pipeline configuration that uses a self-hosted agent to run the pipeline (.azuredevops/ado-ci-pipeline-self-hosted.yml). 

The Microsoft hosted version is easiest to start with and recommended. Where you may consider switching to the self-hosted version, is when you have added several directories under src/ that have individual containers and the size of all the docker builds in the CI pipeline comes up against the 10GB disk storage limit for Microsoft hosted pipelines (see this link for resource limitations of Microsoft hosted agents: https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/hosted?view=azure-devops&tabs=yaml#capabilities-and-limitations). In this case (or when other resource constraints are met) switching to a self-hosted agent pipeline may be an option and the template at .azuredevops/ado-ci-pipeline-self-hosted.yml includes additional steps to help manage space consumed by CI pipeline runs. The two versions are otherwise identitical in terms of building each docker container under src, running pytest within each of these containers and publishing test results and coverage information.

### Github Actions CI Pipeline

TODO

## Future Roadmap and TODOs

- Add Docker build caching to Azure Devops MS hosted CI pipeline

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
