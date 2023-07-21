import tomllib as toml

def populate_firestore():

    COLLECTION_NAME = "pgvector"

    from firebase_admin import firestore, initialize_app

    initialize_app()

    db = firestore.client()

    import json
    # get the fake data from fake_data.json
    with open("./functions/fake_data.json", "r") as f:
        fake_data = json.load(f)

    for datum in fake_data:
        db.collection(COLLECTION_NAME).document(str(datum["id"])).set(datum)


def prepare_for_deployment():
    #  this function copies dependencies from pyproject.toml to requirements.txt
    
    #  read pyproject.toml
    with open('pyproject.toml', 'rb') as f:
        pyproject = toml.load(f)

    #  get dependencies
    dependencies = pyproject['tool']['poetry']['dependencies']

    #  write dependencies to requirements.txt
    with open('./functions/requirements.txt', 'w') as f:
        for key, value in dependencies.items():
            if key != 'python':
                # remove ^ from start of value if it exists
                if value[0] == '^':
                    value = value[1:]
                f.write(f'{key}=={value}\n')