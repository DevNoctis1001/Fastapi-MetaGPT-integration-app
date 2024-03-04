import os
from octokit import Octokit

def upload_to_github(repo_name, directory, token):
    octokit = Octokit(token=token)
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
            repo_path = file_path.replace(directory, '').lstrip('/')
            octokit.repos.createOrUpdateFileContents(
                owner='your-github-username',
                repo=repo_name,
                path=repo_path,
                message=f'Add {file}',
                content=content
            )


def simulate_metagpt_output():
    # Define the directory structure and file content
    file_structure = {
        'config/settings.py': "class Settings:\n    SECRET_KEY: str = 'your-secret-key'",
        'app/user.py': "from pydantic import BaseModel\n\nclass User(BaseModel):\n    id: int\n    name: str",
        'app/project/project.py': "class Project:\n    def __init__(self, name):\n        self.name = name",
        'app/project/report.py': "def generate_report(project):\n    return f'Report for {project.name}'",
        'main.py': "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'Hello': 'World'}",
        'utils.py': "def util_function():\n    pass"
    }

    # Create the root directory for the codebase
    codebase_root = 'dummy_codebase'
    os.makedirs(codebase_root, exist_ok=True)

    # Create directories and files with content
    for filepath, content in file_structure.items():
        full_path = os.path.join(codebase_root, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as file:
            file.write(content)

    # Return the path to the created codebase
    return codebase_root

