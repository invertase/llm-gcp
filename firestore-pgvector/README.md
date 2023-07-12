Documenting steps

1. go to cloud console for your project, Cloud SQL, create instance of postgresql, e.g firestore-pgvector-demo

2. use populate_firestore script in scripts.py

3. `gcloud sql connect firestore-pgvector-demo --user=postgres ` in terminal to connect

4. `CREATE EXTENSION IF NOT EXISTS vector;`

5.
```CREATE TABLE embeddings(
    id INTEGER,
    embedding vector(768)
);
```

now we have the required datatypes and table.

Currently in `main.py` there is a script to query using pgvector, but this assumes the environment is all set up etc. WIP to get this down.
______

Development:

Used `poetry` to track dependencies, but not needed. You will have to `python3 -m venv venv` and `source venv/bin/activate`. Currently running scripts from `firestore-pgvector` directory, but this will change.