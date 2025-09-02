FROM python:3.12.11-alpine AS builder

WORKDIR /services/conversion

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN export PYTHONPATH=$PYTHONPATH:/services/conversion

COPY . .
EXPOSE ${CONVERSION_SERVICE_PORT}

ENTRYPOINT [ "python", "app.py" ]