#!/bin/bash
: '
This script will run all unit tests in the repository (for all directories under src/ that
have at least one test_*.py under a tests folder). It will build a Docker image for each directory with tests, 
using the Dockerfile in the .devcontainer directory. It will then run pytest in the Docker container
and save the test results and coverage report to the build artifacts directory. This script can be run
locally or also in an ADO CI pipeline or Github Actions CI pipeline. See the 
.azuredevops/ado-ci-pipeline-ms-hosted.yml file for an example use in an ADO CI pipeline and the
.github/workflows/ci.yaml for an example use in Github Actions pipeline.
'

set -eE

repo_root="$(pwd)"

# Find all the 'src' subdirectories with a 'tests' folder, extract the dir name as test_dir_parent
for test_dir_parent in $(find "${repo_root}/src" -type d -name 'tests' -exec dirname {} \; | sed "s|${repo_root}/src/||"); do
    # Check for at least one Python file in the 'tests' subdirectory of test_dir_parent
    count_test_py_files=$(find "${repo_root}/src/${test_dir_parent}/tests"/*.py 2>/dev/null | wc -l)
    if [ $count_test_py_files != 0 ]; then
        # Use the devcontainer Dockerfile to build a Docker image for the module to run tests
        docker build "${repo_root}" -f "${repo_root}/src/${test_dir_parent}/.devcontainer/Dockerfile" -t "${test_dir_parent}"
        
        echo "Running tests for ${test_dir_parent}, found ${count_test_py_files} test files"
        
        : '
        Run the tests in the built Docker container, saving the test results and coverage report to /tmp/artifact_output.
        Some other key parts of the docker run command are explained here:
           - The local /tmp dir is mounted to docker /tmp so that there are no permission issues with the docker user and the 
             pipeline user that runs this script and the user that accesses the test results and coverage report artifacts.
           - The --cov-append option tells pytest coverage to append the results to the existing coverage data, instead of 
             overwriting it, this builds up coverage for each $test_dir_parent in a single coverage report for publishing.
           - Set the .coverage location to be under /tmp so it is writable, coverage.py uses this file to store intermediate 
             data while measuring code coverage across multiple test runs or when combining data from multiple sources.
           - exit with pytest exit code to ensure script exits with non-zero exit code if pytest fails, this ensure the CI
             pipeline in ADO fails if any tests fail.
        '
        docker run  \
            -v "${repo_root}:/workspace" \
            -v "/tmp:/tmp" \
            --env test_dir_parent="$test_dir_parent" \
            --env COVERAGE_FILE=/tmp/artifact_output/.coverage \
            "${test_dir_parent}" \
            /bin/bash -ec '
                mkdir -p /tmp/artifact_output/$test_dir_parent; \
                env "PATH=$PATH" \
                env "PYTHONPATH=/workspace/src/$test_dir_parent:$PYTHONPATH" \
                pytest \
                    --junitxml=/tmp/artifact_output/$test_dir_parent/test-results-$test_dir_parent.xml \
                    -o junit_suite_name=$test_dir_parent \
                    --doctest-modules \
                    --cov \
                    --cov-config=/workspace/pyproject.toml \
                    --cov-report=xml:/tmp/artifact_output/coverage.xml \
                    --cov-append \
                    /workspace/src/$test_dir_parent; \
                exit $?'
    fi
done

: '
If running CI on ADO with MS-hosted agents, copy the test and coverage results to the build artifacts directory
so that it is preserved for publishing. See the .azuredevops/ado-ci-pipeline-ms-hosted.yml file for how the 
BUILD_ARTIFACTSTAGINGDIRECTORY is set.
'
if [ -n "$BUILD_ARTIFACTSTAGINGDIRECTORY" ]; then
    cp -r /tmp/artifact_output/* "${BUILD_ARTIFACTSTAGINGDIRECTORY}"
fi
