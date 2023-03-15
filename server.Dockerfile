FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10.6

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src/server /app/server