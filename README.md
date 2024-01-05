# Dev Containers for ML feasibility study with VS Code

A machine learning and data science project template that makes it easy to work with multiple Docker based [VSCode Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) in the same repository. The template also makes it easy to transition projects to the cloud and production by including automated code quality checks, pytest configuration, CI pipeline templates and a sample for running on Azure Machine Learning.

## Contents

- [Dev Containers for ML feasibility study with VS Code](#dev-containers-for-ml-feasibility-study-with-vs-code)
  - [Contents](#contents)
  - [Introduction and Overview](#introduction-and-overview)
    - [Features](#features)
  - [Getting Started](#getting-started)
    - [How to setup dev environment?](#how-to-setup-dev-environment)
  - [How to create a new directory under src with a new environment](#how-to-create-a-new-directory-under-src-with-a-new-environment)
  - [Directory Structure](#directory-structure)
    - [`notebooks` directory vs `src` directory](#notebooks-directory-vs-src-directory)
  - [AML Example](#aml-example)
  - [CI Pipeline](#ci-pipeline)
    - [Running all unit tests with `ci-tests.sh`](#running-all-unit-tests-with-ci-testssh)
    - [How to Configure Azure DevOps CI Pipeline](#how-to-configure-azure-devops-ci-pipeline)
      - [Choosing between Azure DevOps Microsoft-hosted vs Self-hosted CI Pipeline](#choosing-between-azure-devops-microsoft-hosted-vs-self-hosted-ci-pipeline)
    - [How to Configure Github Actions CI Pipeline](#how-to-configure-github-actions-ci-pipeline)
  - [Using SSH Keys in Dev Containers](#using-ssh-keys-in-dev-containers)
  - [Future Roadmap and TODOs](#future-roadmap-and-todos)
  - [Contributing](#contributing)
  - [Trademarks](#trademarks)

## Introduction and Overview

This repository provides a [VSCode Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) based project template that can help accelerate your Machine Learning inner-loop development phase. The template covers the phases from early ML experimentation (local training/testing) until production oriented ML model training (cloud based training/testing with bigger CPUs and GPUs).

During the early phase of Machine Learning project, you may face challenges such as each data scientist creating various different python environments that span across CPU and GPU that tend to have different setup procedures. With the power of Dev Containers, you can automate environment setup process across the team and every data scientist will get the exact same environment automatically. This template provides both CPU and GPU Dev Container setup as examples. To support multiple different ML approaches with different python environments to be experimented in one project, this solution allows multiple different Dev Containers to be used in one repository while having a "common" module that will be installed into all Dev Container to enable code reuse across different Dev Containers.

Another challenge you may face is each data scientist creating a low quality codebase. That is fine during the experimentation stage to keep the team agility high and maximize your team’s experimentation throughput. But when you move to the model productionization stage, you experience the burden of bringing code quality up to production level. With the power of python tools and VSCode extensions configured for this template on top of Dev Containers, you can keep the code quality high automatically without losing your team’s agility and experimentation throughput and ease the transition to the productionization phase.

### Features

- Multiple Dev Container samples (both CPU and GPU) with many common config steps already configured as following:
  - Automated code quality checks (linter and auto formatter) and automated fix when possible with ruff on VSCode on save
  - Automated code quality checks (linter and auto formatter) with ruff as precommit hook
  - Zero effort transition from local env to Azure Machine Learning (cloud based env) by leveraging the same Dockerfile
  - Pre-configured VSCode extensions installed such as python, jupyter, shellcheck, code-spell-checker, git tools etc
- [Github Actions and Azure DevOps CI pipelines](#ci-pipeline) that run linter (ruff) and pytest with test result reporting and coverage reporting
- Pull Request templates that helps you to write a good PR description for both Github and Azure DevOps

This template automates all tedious setup process as much as possible and saves time and reduces setup errors for the entire data scientist team.

## Getting Started

This section provides a comprehensive guide on how to set up a development environment using Dev Containers in Visual Studio Code with step-by-step instructions.

### How to setup dev environment?

1. Install [Visual Studio Code](https://code.visualstudio.com/)
1. If your team has a commercial license for Docker Desktop, follow [VS Code Remote Containers | Docker Desktop](https://code.visualstudio.com/docs/remote/containers#_installation). Otherwise, go to [VS Code Remote Containers | Rancher Desktop Docs](https://docs.rancherdesktop.io/how-to-guides/vs-code-remote-containers/) and finish the first step (Install and launch Rancher Desktop. Select dockerd (moby) as the Container Runtime from the Kubernetes Settings menu.)
1. Install [VSCode Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) on vscode
1. **If you forget this step, you will get an error when you try to build the container so make sure you have `.env` at root of this directory before you move on to the next step.**. Copy `.env.example` and rename it to `.env`. This is where you store your credentials etc. `.env` is automatically loaded into dev container as environment variables. When you add new environment variables `.env`, update `.env.example` as well to share that with others but don't include any credentials there. `.env` is gitignored so your credentials in that file won't be accidentally committed.
1. Run `Dev Containers: Open Folder in Container...` from the Command Palette (F1) and select the `notebooks` directory.
1. VS Code will then build and start up a container, connect this window to Dev Container: `notebooks`, and install VS Code extensions specified in `notebooks/.devcontainer/devcontainer.json`. `pre-commit install --overwrite` runs as part of `postCreateCommand` in `devcontainer.json` and this will setup your git precommit hook automatically.
1. Now set up is done. If you want to develop in another directory for example under `src`, run `Dev Containers: Open Folder in Container...` and go to that directory that has `.devcontainer` and that will setup an dev environment for that directory.
1. When you or others update either `requirements.txt` or `Dockerfile` in your working directory, make sure to rebuild your container to apply those changes to container. Run `Dev Containers: Rebuild and Reopen in Container...` for that.

## How to create a new directory under src with a new environment

1. Copy `src/sample_cpu_project/` under `src` and rename it. If you need gpu environment, base off of `src/sample_pytorch_gpu_project` instead
1. Edit `.devcontainer/devcontainer.json` under the new directory and replace `sample_cpu_project` with the new directory name in `"name"` and `"workspaceFolder"`
1. Update `COPY sample_cpu_project/.devcontainer/requirements.txt` in `Dockerfile` with a new path
1. Update other parts of `Dockerfile` if you need
1. Update `requirements.txt` if you need
1. Run `Dev Containers: Open Folder in Container...` from the Command Palette (F1) and select the new directory and make sure you can successfully open the new directory on VS Code running in a container

## Directory Structure

This section gives you overview of the directory structure of this template. Only essential files are covered in this structure graph for simplicity. The directory structure is as follows:

```bash
.
├── .azuredevops                   # CI pipelines for Azure DevOps. Details at section: How to Configure Azure DevOps CI Pipeline 
├── .github                        # CI pipelines for Github Actions. Details at section: How to Configure Github Actions CI Pipeline 
├── .pre-commit-config.yaml        # pre-commit config file with formatting and linting. Setup is covered in Section: Getting Started
├── .env.example                   # Example of .env file. Setup is covered in Section: Getting Started
├── ci-tests.sh                    # Details at Section: Running all unit tests with ci-tests.sh
├── data                           # Directory to keep your data for local training etc. This directory is gitignored 
├── notebooks                      # Setup process is covered in Section: How to setup dev environment?
│   ├── .devcontainer              # dev container related configuration files goes to here following VSCode convention
│   │   ├── devcontainer.json      # dev container configuration and VS Code settings, extensions etc.
│   │   ├── Dockerfile             # referred in devcontainer.json
│   │   └── requirements.txt       # includes python package list for notebooks. used in Dockerfile
│   └── sample_notebook.py         # example of interactive python script
├── pyproject.toml                 # Setting file for ruff, pytest and pytest-cov
└── src
    ├── common                     # this module is accessible from all modules under src. put functions  you want to import across the projects here
    │   └── requirements.txt       # python package list for common module. installed in all Dockerfile under src. python tools for src goes to here too
    ├── sample_cpu_project         # cpu project example. Setup process is covered in Section: How to setup dev environment?
    │   ├── .devcontainer          # dev container related configuration files goes to here following VSCode convention
    │   │   ├── devcontainer.json  # dev container configuration and VS Code settings, extensions etc.
    │   │   ├── Dockerfile         # referred in devcontainer.json. Supports only CPU
    │   │   └── requirements.txt   # includes python package list for sample_cpu_project. used in Dockerfile
    │   ├── sample_main.py         
    │   └── tests                  # pytest scripts for sample_cpu_project goes here
    │       └── test_dummy.py      # pytest script example
    └── sample_pytorch_gpu_project # gpu project example with pytorch. Setup process is covered in Section: How to setup dev environment?
        ├── README.md              # README for AML example contained in sample_pytorch_gpu_project
        ├── .devcontainer          # dev container related configuration files goes to here following VSCode convention
        │   ├── devcontainer.json  # dev container configuration and VS Code settings, extensions etc.
        │   ├── Dockerfile         # referred in devcontainer.json. Supports GPU
        │   └── requirements.txt   # includes python package list for sample_pytorch_gpu_project. used in Dockerfile
        ├── aml_example/           # Sample AML CLI v2 Components-based pipeline, including setup YAML. See sample_pytorch_gpu_project/README for full details of files in this directory.
        ├── sample_main.py        
        ├── inference.py           # Example pytorch inference/eval script that also works with aml_example
        ├── train.py               # Example pytorch model training script that also works with aml_example
        └── tests                  # pytest scripts for sample_pytorch_gpu_project goes here
            └── test_dummy.py      # pytest script example
```

### `notebooks` directory vs `src` directory

There are two places to put python scripts/modules in this template. The `notebooks` directory is for experimental or throw-away python scripts and jupyter notebooks that you want to run cell by cell interactively. For example, EDA, one-off visualization codes, new model approaches you are not certain yet if you want to maintain over time typically go to this directory. The `src` directory is for python scripts and modules that you want to reuse and maintain over time. The `src` directory is also where you would put unit tests (typically under a `src/your_module/tests` directory).

Given the nature of each directory's responsibility, there is also a different quality governance required. One big difference is that pre-commit hooks and CI pipelines run `ruff check` (linter) over `src` but not over `notebooks` (`ruff format` still run for both). For scripts in `notebooks`, we recommend you use [interactive python scripts](https://code.visualstudio.com/docs/python/jupyter-support-py#_convert-jupyter-notebooks-to-python-code-file) where you can have jupyter-like code cells within `.py` files rather than jupyter notebooks `.ipynb`. Interactive python files gives you the following benefits:

- Comes with full benefits of python extension in VSCode such as code completion, linting, auto formatting, debugging etc
- pre-commit hooks and CI pipelines will work as they run over `.py` files (but not perfectly over `.ipynb` files)
- Python file format is easier to review during a pull request review

Interactive python scripts and jupyter notebooks are interchangeable as described in [Convert Jupyter notebooks to Python code file](https://code.visualstudio.com/docs/python/jupyter-support-py#_convert-jupyter-notebooks-to-python-code-file) so you can switch between them easily too if you want to use both formats during the development.

## AML Example

An Azure Machine Learning (AML) example is provided under `src/sample_pytorch_gpu_example`. The example is a AML Components-based ML pipeline, that runs a pytorch based training step followed by a inference/evaluation step. This example shows the seamless transition of moving from a local run (inside the Dev Container) of pytorch based training/inference and running in the cloud in the exact same Docker environment with flexible compute options. See the [AML Components-based Pipeline Example README](src/sample_pytorch_gpu_project/README.md) for a detailed explanation and instructions of the example code.

## CI Pipeline

This repository contains templates for running a Continuous Integration (CI) pipeline on either Azure DevOps (under `.azuredevops` directory) or on Github Actions (under `.github` directory). Each of the CI pipeline configurations provided have the following features at a high level:

- Run code quality checks (`ruff check`) over the repository
- Find all subdirectories under `src` and run all pytest tests inside the associated Docker containers
- Publish test results and code coverage statistics

We recommend setting up pipeline triggers for PR creation, editing and merging. This will ensure the pipeline runs continuously and will help catch any issues earlier in your development process.

See the sections below for links on how to setup pipelines with [Azure DevOps](#how-to-configure-azure-devops-ci-pipeline) and [Github Actions](#how-to-configure-github-actions-ci-pipeline). Note that if you are only using one of these platforms to host a pipeline (or neither), you can safely delete either (or both) the `.azuredevops` directory or the `.github` directory.

### Running all unit tests with `ci-tests.sh`

As multiple independent directories can be added under `src`, each with its own Dockerfile and requirements, running unit tests for each directory under `src` needs to be done within the Docker container of each `src` subdirectory. The `ci-tests.sh` script automates this task of running all unit tests for the repository with the following steps:

1. Finds all subdirectories under `src` that have at least one `test_*.py` under a `tests` folder
2. Builds each Docker image for each subdirectory with tests, using the Dockerfile in the associated `.devcontainer` directory
3. Runs pytest for each subdirectory with tests, inside the matching Docker container built in step 2
4. Combine all test results and coverage reports from step 3, with reports in a valid format for publishing in either Azure DevOps or Github Actions hosted pipeline

Note that the `ci-test.sh` script can be run locally as well and it is assumed that all tests are written with pytest.

### How to Configure Azure DevOps CI Pipeline

See [create your first pipeline](https://learn.microsoft.com/en-us/azure/devops/pipelines/create-first-pipeline?view=azure-devops) for how to setup a pipeline in Azure DevOps. Note that to use the provided template in this repository, you will need to specify the path to `.azuredevops/ado-ci-pipeline-ms-hosted.yml` during the pipeline setup process in Azure DevOps.

#### Choosing between Azure DevOps Microsoft-hosted vs Self-hosted CI Pipeline

There are two templates for running a CI pipeline in Azure DevOps, a pipeline configuration that uses a Microsoft hosted agent to run the pipeline (`.azuredevops/ado-ci-pipeline-ms-hosted.yml`) and a pipeline configuration that uses a self-hosted agent to run the pipeline (`.azuredevops/ado-ci-pipeline-self-hosted.yml`).

The Microsoft hosted version is easiest to start with and recommended. Where you may consider switching to the self-hosted version, is when you have added several directories under `src` that have individual containers and the size of all the docker builds in the CI pipeline comes up against the 10GB disk storage limit for Microsoft hosted pipelines (see [resource limitations of Microsoft hosted agents](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/hosted?view=azure-devops&tabs=yaml#capabilities-and-limitations)). In this case (or when other resource constraints are met) switching to a self-hosted agent pipeline may be an option and the template at `.azuredevops/ado-ci-pipeline-self-hosted.yml` includes additional steps to help manage space consumed by CI pipeline runs. The two versions are otherwise identitical in terms of building each docker container under `src`, running pytest within each of these containers and publishing test results and coverage information.

### How to Configure Github Actions CI Pipeline

Github Actions CI pipeline is defined in `.github/workflows/ci.yaml`. As long as this repository is hosted in github, the pipeline will be automatically triggered when a PR is made or updated as well as when a PR is merged into your main branch with the setting below, so **no additional setting is required**.

```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
```

## Using SSH Keys in Dev Containers

If you have connected to the origin repository using SSH authentication, you will need to do a bit of setup to reuse your local SSH key inside a Dev Container automatically, which will allow you to interact with the origin repository (git push, git pull etc.) inside the Dev Container.

1. Try the recommendations in the official docs for [sharing git credentials](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials)
1. If the previous step doesn't work, try the below method, that includes a bit of additional code to add keys to the SSH agent.

Add the following to your ~/.bash_profile, ~/.profile, ~/.zprofile or similar (by default most WSL users will have only a ~/.profile) so an ssh-agent will be started when needed and default keys will be added to the agent. The ssh-agent will then automatically forward keys to your Dev Container when its launched.

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

## Future Roadmap and TODOs

- Add Docker build caching to Azure DevOps MS hosted CI pipeline
- Add tensorflow GPU example
- Investigate making `src/common` installed with `pip -e`
- Use a common requirements.txt for code quality dependencies

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow [Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).

Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.

Any use of third-party trademarks or logos are subject to those third-party's policies.
