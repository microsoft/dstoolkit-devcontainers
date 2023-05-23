# AML Components-based Pipeline Example

## Introduction

This subdirectory contains a configured and tested lightweight Azure Machine Learning (AML) CLI v2 compopnents-based ML pipeline example. Read more about [AML components-based pipelines](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-component-pipelines-cli?view=azureml-api-2). This example allows you to seemlessly move from working in the local Dev Container environment to a cloud based environment with the exact same Dockerfile.

Two example files are provided, `train.py` and `inference.py` which contains a pytorch example (taken from [this pytorch tutorial](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html?highlight=cifar10)) for training a small conv-net on CIFAR10 and performing inference and evaluation with the trained model. These files are also wrapped in AML components (`aml_example/aml_components/train-component.yaml` and `aml_example/aml_components/inference-component.yaml`) which is then composed in a AML components-based pipeline in `aml_example/sample-aml-components-pipeline.yml`. The example can thus be run locally inside the Dev Container or in the cloud in AML, with the exact same environment. See the sections below for [how to setup](#setting-up-aml-for-running-a-pipeline) and [run the example in AML](#run-the-aml-component-example).

As an exmaple workflow, you could work with the sample `train.py` and `inference.py` with your local CPU/GPU to get things working and then easily transition to running the same scripts in an AML cloud environment that has could have a more powerful GPU.

## Setting up AML for running a pipeline

The sections below go through the setup required for running the AML pipeline-components example.

### 1. Dev Container Setup

Ensure you have run through the [project setup steps outlined](../../README.md#getting-started) in the top-level README. When going through these steps you could also add the AML environment variables to the `.env` file to avoid refering to them in each CLI command. The `.env` file contains commented out names of the the required variables.

### 2. Azure prerequisites

Before you try out the AML example, you will need setup an Azure account with the following:

- If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/free/).

- An Azure Machine Learning workspace. [Create workspace resources](https://learn.microsoft.com/en-us/azure/machine-learning/quickstart-create-resources?view=azureml-api-2).

### 3. Using the AML CLI v2

The Dev Container environment comes configured with Azure CLI and the AML CLI v2 extension. See  [how to configure AML CLI](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli?view=azureml-api-2&tabs=public) for background information.

With your Dev Container launched for `src/sample_pytorch_gpu_project`, verify that the AML CLI v2 extension is installed with:

```bash
az ml
```

If this runs then log-in to your Azure account with:

```bash
az login
```

Alternatively, you may need to specify the specific tenant that contains the Subscription and Workspace you will be running AML jobs in:

```bash
az login --use-device-code --tenant <YOUR_AZURE_TENANT_DOMAIN>
```

Note to avoid manually specifying `-g <YOU_AML_RESOURCE_GROUP> -w <YOU_AML_WORKSPACE>` in the `az` commands below you can place these secrets in your `.env` file in the root of the repository (not tracked by git). You will need to relaunch the Dev Container after adding these.

### 4. Setup AML Compute and Docker Environment

After logging into the AML CLI you will need to setup a AML compute cluster and AML custom environment to run the train.py and inference.py scripts in the AML components pipeline example (`aml_example/sample-aml-components-pipeline.yml`).

### 4a. Setup the AML compute cluster

There are two options provided to setup compute clusters, a GPU cluster (using `aml_example/aml_setup/create-gpu-compute.yaml`) and a CPU cluster (using `aml_example/aml_setup/create-cpu-compute.yaml`). To run the example we will just create the GPU cluster, but in the future you may create both GPU and CPU clusters and then use a mix of compute across different types of scripts (eg. GPU for training and CPU for an evaluation script).

1. First update the `location` and `size` parameters in the  `aml_example/aml_setup/create-gpu-compute.yaml` to match the requirements for your subscription and AML workspace:

    ```yaml
    size: Standard_NC6
    location: centralus
    ```

2. Create the compute cluster from the command line inside the Dev Container:

    ```bash
    az ml compute create -f aml_example/aml_setup/create-gpu-compute.yaml -g <YOU_AML_RESOURCE_GROUP> -w <YOU_AML_WORKSPACE>
    ```

### 4b. Setup the AML custom environment

We will use the exact same Dockerfile that specifies the Dev Container and local running environment for running jobs in AML so that there is a seemless transition to the cloud.

Create the custom AML environment from the command line inside the Dev Container:

```bash
az ml environment create --file aml_example/aml_setup/create-env.yaml -g <YOU_AML_RESOURCE_GROUP> -w <YOU_AML_WORKSPACE>
```

#### **Updating the AML Custom Environment**

Note the AML environment will need to be updated manually anytime new dependencies are added to `.devcontainer/requirements.txt` or `.devcontainer/Dockerfile` is updated. Also if you add new dependencies in `src/common/requirements.txt` that are needed in `src/sample_pytorch_gpu_project` then this will also require a environment rebuild. The environment can be rebuilt by running the exact same command used above to create the environment.

## Run the AML Component Example

After going through the [setup steps](#setting-up-aml-for-running-a-pipeline), you can run the AML component example `aml_example/aml_setup/create-gpu-compute.yaml` which will run `train.py` and `inference.py` in sequence, with the trained model passed between the steps by the pipeline.

Start the pipeline experiment from the command line inside the Dev Container:

```bash
az ml job create -f aml_example/sample-aml-components-pipeline.yml --web --g <YOU_AML_RESOURCE_GROUP> -w <YOU_AML_WORKSPACE>
```

## Explanation of AML Files

```bash
src/sample_pytorch_gpu_project/
├── README.md
├── aml_example                                 # Contains all AML related files
│   ├── aml_components                          # AML component files that are used in sample-aml-components-pipeline.yml
│   │   ├── inference-component.yaml            # AML CLI v2 inference component that wraps inference.py
│   │   └── train-component.yaml                # AML CLI v2 training component that wraps train.py
│   ├── aml_setup                               # AML workspace setup files
│   │   ├── create-cpu-compute.yaml             # Create AML CPU cluster
│   │   ├── create-env.yaml                     # Create AML custom Docker environment
│   │   └── create-gpu-compute.yaml             # Create AML GPU cluster
│   └── sample-aml-components-pipeline.yml      # Sample AML CLI v2 components pipeline that refers to aml_components/inference-component.yaml and aml_components/train-component.yaml
├── inference.py                                # Example of pytorch model inference (from a trained model from train.py)
├── sample_main.py                              # Sample function used by unit tests
├── tests
│   └── test_dummy.py                           # Sample pytest that calls function from sample_main.py
└── train.py                                    # Example of pytorch model training, can be run locally or in AML job

```

## How to delete all AML dependencies and source files

If you don't need to use any of the sample AML integrations follow the steps below to remove all dependencies and related source files.

1. In `.devcontainer/Dockerfile`, remove the following lines :

    ```bash
    RUN wget -qO- https://aka.ms/InstallAzureCLIDeb | bash
    ```

    and

    ```bash
    RUN az extension add --name ml
    ```

2. Remove the `mlflow` dependencies in `.devcontainer/requirements.txt`:

    ```txt
    mlflow==2.3.1
    azureml-mlflow==1.50.0
    ```

    Note that you could keep the `mlflow` dependency if you want to keep `train.py` and `inference.py` for local runs with `mlflow` logging.

3. Delete the entire `aml_example` directory.

    ```bash
    cd /workspace/src/sample_pytorch_gpu_project
    rm -rf aml_example
    ```

4. [Optional] Delete `train.py` and `inference.py` which are included as examples to work with the AML pipeline component. You could also retain these samples for as an example of working with pytorch locally.
