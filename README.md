# MATHOS

## Overview
Mathos is a toolset to supercharge your "second brain" workflow. It provides a  customizable, interactive assistant.

## Goals
- Help non-neurotypical users in organizing and planning their projects and tasks
- Help any performance-oriented user in optimizing their knowledge base

## Requirements
- a python 3.11 environment
- Podman (or Docker)
- `podman build -t mathos src/backend/`
- `podman run --name mathos -p 8000:8000 localhost/mathos`

## License
This project is licensed under the GPL3 License. See the [LICENSE](LICENSE) file for details.