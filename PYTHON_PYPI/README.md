# Python PYPI pipeline
This pipeline is for python modules that you want to publish to a pypi repository

## Onboarding
1. Copy the .github directory to your project repository
2. create your project folder and tests folder for unit testing
3. initialize your project with the uv package manager. This will generate your pyproject.toml file
```bash
uv init --name project_name --author "" --license MIT --venv
```
4. To publish to pypi, you will need to login and generate a bearer token and save it as PYPI_TOKEN in your actions secrets in your repository
