# Bundling OpenAPI Specifications with Swagger in FastAPI

## Introduction

This guide shows you how to combine several OpenAPI specification files into one using Swagger-CLI in your FastAPI backend. This way, your OpenAPI specifications stay organized and easy to manage in one place.

## Prerequisites

- Your project's OpenAPI specification files are located in the `/specifications` folder.
- Node.js installed on your machine.
- Swagger-CLI installed globally via npm:

```bash
npm install -g swagger-cli
```

## Merging Multiple OpenAPI Specification Files

1. **Create a Script for Merging Specifications**:

   - Create a directory named `scripts` in your project root.
   - Inside the `scripts` directory, create a file named `merge_specifications.sh` with the following content:

```bash
#!/bin/bash

# Navigate to specifications directory
cd specifications

# Merge OpenAPI specifications
swagger-cli bundle -o ../openapi.yaml --type yaml
```

2. **Run the Script**:

```bash
bash scripts/merge_specifications.sh
```

- This command executes the script, which merges all OpenAPI specification files in the `specifications` folder into a single file named `openapi.yaml` at the root of your project.

## Integrating Compiled OpenAPI Specification in FastAPI

1. **Load the Compiled OpenAPI Specification in FastAPI**:

```python
from fastapi import FastAPI
import yaml

# Load compiled OpenAPI specification
with open("openapi.yaml", "r") as file:
    openapi_schema = yaml.load(file, Loader=yaml.FullLoader)

app = FastAPI(openapi_schema=openapi_schema)

# ... rest of your code ...
```

## Automation (Optional)

If you have a CI/CD pipeline, consider automating the running of `merge_specifications.sh` script whenever there are changes to the `specifications/` directory to ensure that the OpenAPI spec is always up-to-date.

With this setup, you have a streamlined process for managing and merging your OpenAPI specifications within your FastAPI backend, ensuring a centralized source of truth for your API specifications.