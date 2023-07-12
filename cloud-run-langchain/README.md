## Local debugging

## Setup the environment

To debug locally, first you need to install the dependencies and activate the virtual environment.

Run the following commands in the root of the project:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Using uvicorn

To run the application locally in the terminal, you can use uvicorn:

```bash
uvicorn app.main:app --reload
```

### VS Code

To debug the application in VS Code, you can use the provided [launch](.vscode/launch.json) configuration. This will start the application in debug mode and allow you to set breakpoints.

The application will be available at http://0.0.0.0:8080.

## Deployment

### Building the container

### Deploying to Cloud Run