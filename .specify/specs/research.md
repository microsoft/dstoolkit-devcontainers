# Research: DevContainers CI Action

**Date**: 2025-12-16
**Purpose**: Research `devcontainers/ci` GitHub Action for implementing devcontainer build testing

## Key Findings

### Action: devcontainers/ci@v0.3

**Repository**: https://github.com/devcontainers/ci
**Version**: v0.3 (latest stable)

### Key Parameters

| Parameter | Required | Usage for Our Implementation |
|-----------|----------|------------------------------|
| `subFolder` | No | **CRITICAL** - Use with matrix to specify each devcontainer path |
| `runCmd` | Yes | Use for smoke tests: `python --version && pytest --version && ruff --version` |
| `push` | No | Set to `never` (we only want to validate builds, not push images) |
| `imageName` | No | Optional - not needed if `push: never` |
| `cacheFrom` | No | Optional - can improve build speed but not critical for MVP |

### Matrix Strategy for Multiple DevContainers

```yaml
strategy:
  matrix:
    subfolder:
      - notebooks
      - src/sample_cpu_project
      - src/sample_pytorch_gpu_project
  fail-fast: false  # Continue testing other containers if one fails

steps:
  - uses: devcontainers/ci@v0.3
    with:
      subFolder: ${{ matrix.subfolder }}
      runCmd: python --version && pytest --version && ruff --version
      push: never
```

**Note**: `fail-fast: false` ensures all devcontainers are tested even if one fails.

### Docker Layer Caching

The `devcontainers/ci` action uses Docker BuildKit which has built-in layer caching support.

**Options for caching**:
1. **No explicit caching** (MVP) - BuildKit provides some automatic caching
2. **GitHub Actions cache** - Use `cacheFrom` parameter with registry
3. **Registry caching** - Use `cacheFrom: ghcr.io/...` but requires `imageName` and push setup

**Recommendation for MVP**: Start without explicit caching. If builds are slow, add `cacheFrom` in Phase 5 (US4).

### Environment Setup

The action expects:
- Repository checked out with `actions/checkout@v4`
- `.env` file if devcontainer.json references it with `runArgs: ["--env-file", ...]`

**Solution for .env**:
```yaml
- name: Setup .env file
  run: cp .env.example .env
```

### GPU DevContainer Handling

**Finding**: GPU devcontainers (using CUDA base images) build successfully without GPU runtime. GPU is only needed for running CUDA code, not for building the image.

**No special handling needed** - the action will build GPU devcontainers normally in CI.

### Error Reporting

The action provides clear error messages:
- JSON parse errors → Shows syntax error with line number
- Missing Dockerfile → Shows file not found error
- Build failures → Shows Docker build output with error
- Failed runCmd → Shows command output and exit code

Each matrix job appears separately in GitHub Actions UI with individual pass/fail status.

### Parallel Execution

Matrix jobs in GitHub Actions run in parallel by default (up to 20 concurrent jobs on ubuntu-latest runners).

**Expected behavior**: All 3 devcontainer builds will start simultaneously.

## Implementation Decisions

### Phase 2 (US1): Basic CI Job
- Use `devcontainers/ci@v0.3` with single devcontainer first (notebooks)
- Set `push: never` (no image publishing needed)
- Add `.env` setup step before action

### Phase 3 (US2): Matrix Strategy
- Add matrix with 3 subfolder paths
- Set `fail-fast: false` to test all configurations
- Use `${{ matrix.subfolder }}` in job name for identification

### Phase 4 (US3): Smoke Tests
- Add `runCmd: python --version && pytest --version && ruff --version`
- Post-create commands execute automatically (pre-commit install)
- Features install automatically (common-utils with zsh)

### Phase 5 (US4): Optimization
- Measure baseline build times first
- If >10 minutes total, investigate `cacheFrom` with GitHub Container Registry
- Not needed for MVP

## Sample Workflow Snippet

```yaml
test-devcontainers:
  runs-on: ubuntu-latest
  strategy:
    matrix:
      subfolder:
        - notebooks
        - src/sample_cpu_project
        - src/sample_pytorch_gpu_project
    fail-fast: false
  
  steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Setup .env file
      run: cp .env.example .env
    
    - name: Build and test devcontainer
      uses: devcontainers/ci@v0.3
      with:
        subFolder: ${{ matrix.subfolder }}
        runCmd: python --version && pytest --version && ruff --version
        push: never
```

## Open Questions Resolved

1. **Does the action support matrix builds?** ✅ Yes, use `subFolder` parameter with matrix
2. **How to handle .env file?** ✅ Copy `.env.example` to `.env` before action
3. **Do GPU containers work?** ✅ Yes, build without GPU runtime requirements
4. **Is caching needed?** ⚠️ Optional, not needed for MVP

## References

- [devcontainers/ci GitHub Action](https://github.com/devcontainers/ci)
- [GitHub Action Documentation](https://github.com/devcontainers/ci/blob/main/docs/github-action.md)
- [Dev Container Specification](https://containers.dev/)

---

**Research Complete**: Ready to proceed with implementation
