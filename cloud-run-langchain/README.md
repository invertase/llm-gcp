# Deploying a LangChain application to Cloud Run

## Overview
This repository contains a sample application that can be deployed to Cloud Run. 

The application is built using FastAPI and uses the [LangChain Python SDK](https://python.langchain.com/docs/get_started/introduction.html), and exposes two routes:
1. `/chat`: This route is used to send a message to the chatbot and get a response.
2. `/new_session`: This route is used to set a new active session with the chatbot.



The sample also demonstrates how to persist the user's session in Firestore, and restore it back to give the LLM a long-lasting memory.

## Pre-requisites

- Python >= 3.9
- [gcloud CLI](https://cloud.google.com/sdk/docs/install)

You will also need to create a Google Cloud project with billing enabled, and enable the following APIs:

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

## Local debugging

### Setup the environment

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

To debug the application in VS Code, you can use the provided [launch](../.vscode/launch.json) configuration. This will start the application in debug mode and allow you to set breakpoints.

The application will be available at http://0.0.0.0:8080.

## Deployment

The application can be deployed to Cloud Run using the following command:

```bash
gcloud run deploy SERVICE_NAME --source . --project PROJECT_ID --allow-unauthenticated
```

Where `SERVICE_NAME` is the name of the service you want to deploy, can be any of your choice.

Read more about [deploying to Cloud Run](https://cloud.google.com/run/docs/deploying).

## Usage

To add new messages to the chatbot, you can use the `/chat` route. The route expects a JSON body with the following structure:

```json
{
    "message": "Hello, how are you?"
}
```

The response will be a JSON with the following structure:

```json
{
    "message": "I'm fine, thank you!"
}
```

To start delete all messages in the session, you can use the `/clear_session` route. The route expects no body, and will return a JSON with the following structure:

```json
{
    "message": "Session cleared!"
}
```

### Authentication

The application uses [Firebase Authentication](https://firebase.google.com/docs/auth) to authenticate the user. The authentication token is passed in the `Authorization` header of the request. 

The token is sent by default from any of the client Firebase SDKs, but you can also obtain it manually.

To obtain the token manually for testing, call the identity toolkit API:

```bash
curl https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=API_KEY \
-H 'Content-Type: application/json' \
--data-binary '{"email":"EMAIL","password":"PASSWORD","returnSecureToken":true}'
```

Where `API_KEY` is the API key of your Firebase project, and `EMAIL` and `PASSWORD` are the credentials of the user you want to authenticate.

The response will be a JSON with the following structure:

```json
{
    "kind": "identitytoolkit#VerifyPasswordResponse",
    "localId": "LOCAL_ID",
    "email": "EMAIL",
    "displayName": "",
    "idToken": "ID_TOKEN",
    "registered": true,
    "refreshToken": "REFRESH_TOKEN",
    "expiresIn": "EXPIRES_IN"
}
```

Where `ID_TOKEN` is the token you need to pass in the `Authorization` header of the request, like this:

```bash
curl http://0.0.0.0:8080/chat \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer ID_TOKEN' \
--data-binary '{"message":"Hello, how are you?"}'
```
