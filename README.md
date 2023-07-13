# LLM & data applications on the Cloud ☁️

## What is in this repo?

In this repo, you can find several LLM & data applications written to run on the cloud.

### 1. [LangChain on Cloud Run](./cloud-run-langchain/) 🦜️🔗

![Python](https://img.shields.io/badge/python-3670A0?flat&logo=Python&logoColor=white) ![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=flat&logo=google-cloud&logoColor=white)

This application is a simple imeplementation serverless application that runs on Cloud Run.

Cloud Run is a servelerss powerful platform that allows you to run containers that are invocable via HTTP requests or EventArc on GCP.

### 2. [Firestore indexing using pgvector and Cloud SQL](./firestore-pgvector)
![Python](https://img.shields.io/badge/python-3670A0?flat&logo=Python&logoColor=white) ![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=flat&logo=google-cloud&logoColor=white)

This application is a simple implementation of a Firestore indexing using pgvector and Cloud SQL.

It creates an index of the documents in Firestore and stores them in a Cloud SQL database using pgvector extension. Additionally, it exposes a Cloud Function that allows to query the index.