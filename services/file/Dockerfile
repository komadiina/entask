FROM python:3.12.11-alpine AS builder

WORKDIR /services/file

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN export PYTHONPATH=$PYTHONPATH:/services/file

COPY . .
EXPOSE ${FILE_SERVICE_PORT}

ENTRYPOINT [ "python", "app.py" ]