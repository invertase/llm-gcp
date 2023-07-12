FROM python:3.11-slim

WORKDIR /code

ENV PYTHONUNBUFFERED True

COPY ./requirements.txt /code/requirements.txt

# Install production dependencies.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# Run the web service on container startup. Here we use the guvicorn ASGI server.
# It must listen on 0.0.0.0:8080, see Cloud Run container contract: https://cloud.google.com/run/docs/reference/container-contract
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]