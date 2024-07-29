# Guide for Software Composition Analysis (SCA) Tool

This guide provides detailed instructions on how to build, run, and use the Software Composition Analysis (SCA) tool designed to scan for vulnerabilities in container images, file systems, and Git repositories. The tool is designed to generate reports for container images and filesystems using Trivy.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Building the Docker Image](#building-the-docker-image)
4. [Running the Docker Container](#running-the-docker-container)
5. [Tool Usage](#tool-usage)
6. [Troubleshooting](#troubleshooting)
7. [Additional Information](#additional-information)


## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Git (optional, for cloning the repository)

## Project Structure

```
software-composition-analysis/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── GUIDE.md
├── README.md
├── requirements.txt
├── setup.py
└── software_composition_analysis/
    ├── __init__.py
    ├── __version__.py
    ├── main.py
    ├── core/
    |   ├── __init__.py
    |   ├── input.py
    |   ├── logger.py
    |   └── models.py
    |
    ├── service/
    |   ├── __init__.py
    |   └── trivy.py
    |
    └── support/
        ├── __init__.py
        └── enums.py
```

## Building the Docker Image

1. Open a terminal and navigate to the project directory:

   ```bash
   cd path/to/software-composition-analysis
   ```

2. Build the Docker image using the following command:

   ```bash
   sudo docker build --no-cache . -f Dockerfile -t software-composition-analysis:latest
   ```

   This command builds a Docker image named `software-composition-analysis` based on the instructions in the Dockerfile.

## Running the Docker Container

To run the SCA tool inside a Docker container, use the following command structure:

```bash
sudo docker run --rm -it -v $(pwd)/output:/output software-composition-analysis [arguments]
```

Replace `[arguments]` with the actual arguments for the tool.

### Explanation of Docker run options:

- `--rm`: Automatically remove the container when it exits.
- `-it`: Run container in interactive mode.
- `software-composition-analysis`: The name of the Docker image to run.

## Tool Usage

The SCA tool accepts several command-line arguments:

- `-t, --target`: (Required) Target as path/image to scan.
- `-tt, --target-type`: (Required) Type of target to scan
- `-ov, --output-via`: (Required) Specify output method: "file" or "webhook".
- `-w, --webhook`: Webhook URL (required if output_via is "webhook").
- `-o, --output`: File path for output (required if output_via is "file").
- `-l, --log`: Log level (DEBUG or ERROR, default is DEBUG).

### Example Commands:

1. Scan a Docker image and output to a file:
   ```bash
   sudo docker run --rm -it -v $(pwd)/output:/output software-composition-analysis -tt image -t alpine:latest -ov file -o /output/results.json
   ```

2. Scan a local directory and send results to a webhook:
   ```bash
   sudo docker run --rm -it -v $(pwd)/output:/output -v /path/to/scan:/scan software-composition-analysis -tt filesystem -t /scan -ov webhook -w https://webhook.site/your-unique-url
   ```

3. Few ways to Run scan:

    - For image from registry
    ```bash
    sudo docker run --rm -it -v $(pwd)/output:/output software-composition-analysis -tt image
    -t alpine:latest -ov file -o /output/alpine.json
    ```

    - For local docker image
    ```bash
    sudo docker run --rm -it -v $(pwd)/output:/output -v /var/run/docker.sock:/var/run/docker.sock software-composition-analysis -tt image
    -t attack-surface-discovery:latest -ov file -o /output/asm.json
    ```

    - For local repo path
    ```bash
    sudo docker run --rm -it -v $(pwd)/output:/output -v /home/tri/trishiras/attack-surface-discovery:/scan software-composition-analysis -tt filesystem
    -t /scan  -ov file -o /output/local.json
    ```


Note: When using file output or scanning local directories, you need to mount volumes to access the results or scan targets from your host machine.

## Troubleshooting

1. **Permission Issues**: If you encounter permission problems when writing to mounted volumes, you may need to adjust the permissions or use a named volume.

2. **Network Issues**: Ensure your Docker network settings allow the container to access the target network or webhook URL.

3. **Missing Requirements**: If the build fails due to missing requirements, check that your `requirements.txt` file is up to date and includes all necessary dependencies.

## Additional Information

- The tool uses Python 3.12 as specified in the Dockerfile.
- The tool integrates Trivy for generating SCA report. For detailed information about Trivy's capabilities, refer to its documentation or use the `trivy --help` command inside the container.
- The SCA tool supports various output formats.


### Trivy --help output

```
Scanner for vulnerabilities in container images, file systems, and Git repositories, as well as for configuration issues and hard-coded secrets

Usage:
  trivy [global flags] command [flags] target
  trivy [command]

Examples:
  # Scan a container image
  $ trivy image python:3.4-alpine

  # Scan a container image from a tar archive
  $ trivy image --input ruby-3.1.tar

  # Scan local filesystem
  $ trivy fs .

  # Run in server mode
  $ trivy server

Scanning Commands
  config      Scan config files for misconfigurations
  filesystem  Scan local filesystem
  image       Scan a container image
  kubernetes  [EXPERIMENTAL] Scan kubernetes cluster
  repository  Scan a repository
  rootfs      Scan rootfs
  sbom        Scan SBOM for vulnerabilities and licenses
  vm          [EXPERIMENTAL] Scan a virtual machine image

Management Commands
  module      Manage modules
  plugin      Manage plugins
  vex         [EXPERIMENTAL] VEX utilities

Utility Commands
  clean       Remove cached files
  completion  Generate the autocompletion script for the specified shell
  convert     Convert Trivy JSON report into a different format
  help        Help about any command
  server      Server mode
  version     Print the version

Flags:
      --cache-dir string          cache directory (default "/root/.cache/trivy")
  -c, --config string             config path (default "trivy.yaml")
  -d, --debug                     debug mode
  -f, --format string             version format (json)
      --generate-default-config   write the default config to trivy-default.yaml
  -h, --help                      help for trivy
      --insecure                  allow insecure server connections
  -q, --quiet                     suppress progress bar and log output
      --timeout duration          timeout (default 5m0s)
  -v, --version                   show version

Use "trivy [command] --help" for more information about a command.
```

For more information or to report issues, please refer to the project's documentation or repository.