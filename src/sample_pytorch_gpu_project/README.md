# AML Component Example

This subdirectory contains a configured and tested lightweight Azure Machine Learning (AML) CLI v2 pipeline components example. This example allows you to seemlessly move from working in the the local Dev Container environment to a cloud based environment with the exact same Dockerfile. As an exmaple workflow, you could work with the sample `train.py` and `inference.py` with your local CPU/GPU to get things working and then easily transition to running the same scripts in an AML cloud environment that has a more powerful GPU.

## Using the AML CLI v2

The Dev Container environment comes pre-configured with Azure CLI and the AML CLI v2 extension. See this link for more information: <https://learn.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli?view=azureml-api-2&tabs=public>. 

With your Dev Container launched for `src/sample_pytorch_gpu_project`, verify that the AML CLI v2 extension is installed with:

```
az ml
```

If this runs then log-in to your Azure account with:

```
az login
```

Alternatively, you may need to specify the specific tenant that contains the Subscription and Workspace you will be running AML jobs in:

```
az login --use-device-code --tenant azurelsis.onmicrosoft.com
```

## Setup AML Compute and Docker Environment

After logging into the AML CLI you will need to setup an AML compute clusters and AML custom environment to run the train.py and inference.py scripts in the AML components pipeline example (`aml_example/sample-aml-components-pipeline.yml`).

We will need two types of compute clusters, a GPU one for training and inference and a CPU one for evaluation metrics. Create the compute clusters using the CLI (adjust any setting in the YAML first): `az ml compute create -f aml_setup/create-gpu-compute.yaml -g $RESOURCE_GROUP -w $WORKSPACE_NAME` and `az ml compute create -f aml_setup/create-cpu-compute.yaml -g $RESOURCE_GROUP -w $WORKSPACE_NAME`, we will use these cluster for running AML command components by specifying the 'compute' property in dl-components-pipeline.yml

## Run the AML Component Example


## Explanation of AML Files


## How to delete all AML dependencies and source files

If you don't need to use any of the sample AML integrations follow the steps below to remove all dependencies and related source files.

1. In `.devcontainer/Dockerfile`, remove:

    ```bash
    RUN wget -qO- https://aka.ms/InstallAzureCLIDeb | bash
    ```

    and

    ```bash
    RUN az extension add --name ml
    ```

2. Remove the mlflow dependencies in `.devcontainer/requirements.txt`:

    ```
    mlflow==2.3.0
    azureml-mlflow==1.50.0
    ```

    Note that you could keep the mlflow dependency if you want to keep `train.py` and `inference.py` for local runs with mlflow logging.

3. Delete the entire `aml_example` directory.

    ```bash
    cd /workspace/src/sample_pytorch_gpu_project
    rm -rf aml_example
    ```

4. [Optional] Delete `train.py` and `inference.py` which are included as examples to work with the AML pipeline component. You could also retain these samples for as an example of working with pytorch locally.
